# Sve konstante na jednom mjestu, da ih ne moram traziti po kodu.

from __future__ import annotations

from pathlib import Path

# Redoslijed je bitan, mora pratiti izlaze modela (LABEL_0 do LABEL_3).
CLASS_LABELS: tuple[str, ...] = ("World", "Sports", "Business", "Sci/Tech")

# Ovo se vidi u sucelju pa je na hrvatskom.
CLASS_DESCRIPTIONS: dict[str, str] = {
    "World": "Svijet / politika",
    "Sports": "Sport",
    "Business": "Ekonomija / biznis",
    "Sci/Tech": "Znanost i tehnologija",
}

# Mali BERT istreniran na AG News vijestima. Uzeo sam bas njega jer ima
# safetensors format, stari .bin ne prolazi s torchom 2.2.2.
MODEL_NAME: str = "mrm8488/bert-mini-finetuned-age_news-classification"
MAX_TOKENS: int = 256

APP_TITLE: str = "NLP klasifikator teksta"
HISTORY_LIMIT: int = 50          # koliko zadnjih klasifikacija pamtimo
REQUEST_TIMEOUT_S: float = 10.0  # koliko cekamo da se web stranica javi

PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]
LOG_DIR: Path = PROJECT_ROOT / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"
