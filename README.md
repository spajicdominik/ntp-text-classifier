# NLP klasifikator teksta

Seminarski rad iz kolegija **Napredne tehnike programiranja**.

Desktop (Tkinter) aplikacija koja klasificira uneseni tekst u jednu od
četiri klase (**World/politika, Sports, Business, Sci/Tech**) koristeći
prethodno istreniran DistilBERT model (AG News, PyTorch / HuggingFace).

Unos teksta: ručno, iz `.txt` datoteke ili
parsiranje web stranice.

## Pokretanje

```bash
cd src
python -m text_classifier
```

Testovi (path projekta) — pokreće i unittest i doctest:

```bash
python -m unittest discover -s tests -t .
```

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
```