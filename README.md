# NLP klasifikator teksta

Seminarski rad iz kolegija **Napredne tehnike programiranja** i
**Operativni sustavi**.

Desktop (Tkinter) aplikacija koja klasificira uneseni tekst u jednu od
četiri klase (**World/politika, Sports, Business, Sci/Tech**) koristeći
prethodno istreniran BERT model (AG News, PyTorch / HuggingFace).

Unos teksta: ručno, iz `.txt` datoteke ili parsiranje web stranice.

Za Operativne sustave aplikacija je zapakirana na dva načina:
**Docker image** i **snap paket**.

## Tehnologije i verzije

- **Python 3.9+** — lokalno testirano na 3.9.7 (Anaconda), u Dockeru i snapu
  se koristi 3.12
- PyTorch, transformers (HuggingFace), Tkinter, aiohttp, BeautifulSoup
- model: [`mrm8488/bert-mini-finetuned-age_news-classification`](https://huggingface.co/mrm8488/bert-mini-finetuned-age_news-classification) (~43 MB)
- Docker Desktop 29 (Docker Compose v5)
- snapcraft 9, base `core24` (Ubuntu 24.04)

Model radi samo na **engleskom** tekstu, jer je treniran na engleskim vijestima.

## Struktura projekta

```
src/text_classifier/
  config.py            konstante i postavke (PEP 526 anotacije)
  decorators.py        @log_calls, @timed (dekoratori + closure)
  logging_config.py    postavljanje logiranja (konzola + logs/app.log)
  sources/             izvori teksta (ABC TextSource + implementacije)
  model/               Classifier (Protocol) + BERT implementacija (PyTorch)
  history.py           povijest klasifikacija (deque)
  service.py           ThreadPoolExecutor + Future (concurrency sloj)
  gui/app.py           Tkinter grafičko sučelje
tests/                 unittest + doctest
scripts/
  download_model.py    skine model u mapu (koristi se kod Docker/snap builda)
Dockerfile             Docker image
compose.yaml           Docker Compose
snap/
  snapcraft.yaml       opis snap paketa
  local/launcher.sh    skripta koja pokreće aplikaciju unutar snapa
```

## Lokalno pokretanje

```bash
pip install -r requirements.txt
cd src
python -m text_classifier
```

Prvi put se model skine s HuggingFacea (~43 MB), poslije je u cacheu.

Testovi (iz korijena projekta) — pokreće i unittest i doctest:

```bash
python -m unittest discover -s tests -t .
```

---

## Docker

Aplikacija ima GUI, a Docker container nema ekran, pa se prozor iz
containera šalje na X server računala na kojem se pokreće (X11 forwarding).
Model se skida već kod builda, tako da container radi i bez interneta.

### Build

```bash
docker build -t text-classifier:1.0 .
```

Prvi build traje par minuta (torch je velik). Slojevi u `Dockerfile`-u su
poredani tako da se ovisnosti i model instaliraju prije nego se kopira kod,
pa promjena u kodu ne pokreće ponovnu instalaciju torcha (layer caching).

### Pokretanje na Linuxu

```bash
xhost +local:
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix text-classifier:1.0
```

`xhost +local:` dopusti containeru da crta prozore na tvom X serveru.

### Pokretanje na macOS (XQuartz)

1. Instaliraj [XQuartz](https://www.xquartz.org/).
2. U XQuartzu: *Settings → Security* → uključi **Allow connections from
   network clients**, pa XQuartz ugasi (Cmd+Q) i ponovno upali.
3. Dok XQuartz radi, u terminalu:
   ```bash
   /opt/X11/bin/xhost +localhost
   docker run --rm -e DISPLAY=host.docker.internal:0 text-classifier:1.0
   ```

`xhost` dopuštenje nestaje kad se XQuartz ugasi, pa ga treba ponoviti.

### Pokretanje na Windowsu

Nisam testirao (nemam Windows PC) - Instalirati
[VcXsrv](https://sourceforge.net/projects/vcxsrv/), pokrenuti ga s opcijom
*Disable access control* i onda:

```powershell
docker run --rm -e DISPLAY=host.docker.internal:0 text-classifier:1.0
```

### Docker Compose

```bash
docker compose up --build
```

Default je `DISPLAY=host.docker.internal:0` (Mac/Windows). Na Linuxu:

```bash
DOCKER_DISPLAY=:0 docker compose up --build
```

---

## Snap

Snap se builda i pokreće na Linuxu (Ubuntu 24.04).

### Build i instalacija (Ubuntu 24.04)

```bash
sudo snap install snapcraft --classic
snapcraft pack
sudo snap install text-classifier_1.0_*.snap --devmode --dangerous
text-classifier
```

`snapcraft pack` treba LXD. Ako se builda u virtualci koja služi samo za
to, može i bez njega:

```bash
sudo snapcraft pack --destructive-mode
```

### Build i pokretanje na macOS-u (Multipass)

Snapcraft ne radi na macOS-u, pa se koristi Ubuntu virtualka preko
[Multipassa](https://multipass.run/). Prozor se opet prikazuje kroz XQuartz.

```bash
brew install --cask multipass
multipass launch 24.04 --name snap-builder --cpus 4 --memory 4G --disk 30G
multipass shell snap-builder
```

Unutar virtualke:

```bash
sudo snap install snapcraft --classic
git clone <URL ovog repozitorija> text-classifier
cd text-classifier
sudo snapcraft pack --destructive-mode
sudo snap install text-classifier_1.0_arm64.snap --devmode --dangerous
```

Za prikaz prozora treba IP adresa Maca gledano iz virtualke. To je obično
prva adresa u mreži virtualke (kod mene VM ima `192.168.252.2`, a Mac
`192.168.252.1`; provjeri s `multipass list`). Na Macu dopusti VM-u
pristup XQuartzu, pa u virtualki pokreni aplikaciju:

```bash
# na Macu
/opt/X11/bin/xhost +192.168.252.2
# u virtualki
DISPLAY=192.168.252.1:0 text-classifier
```

---
