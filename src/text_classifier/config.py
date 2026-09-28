# Sve konstante na jednom mjestu, da ih ne moram traziti po kodu.

from __future__ import annotations

import os
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
# U Dockeru i snapu je model vec skinut pri buildu, pa tamo preko
# TEXT_CLASSIFIER_MODEL dobijemo putanju do mape umjesto imena s HuggingFacea.
MODEL_NAME: str = os.environ.get(
    "TEXT_CLASSIFIER_MODEL",
    "mrm8488/bert-mini-finetuned-age_news-classification",
)
MAX_TOKENS: int = 256

APP_TITLE: str = "NLP klasifikator teksta"
HISTORY_LIMIT: int = 50          # koliko zadnjih klasifikacija pamtimo
REQUEST_TIMEOUT_S: float = 10.0  # koliko cekamo da se web stranica javi

# config.py -> text_classifier/ -> src/ -> korijen projekta
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# U snapu je mapa aplikacije samo za citanje, pa logovi moraju u SNAP_USER_COMMON.
_SNAP_DATA = os.environ.get("SNAP_USER_COMMON")
LOG_DIR: Path = Path(_SNAP_DATA) / "logs" if _SNAP_DATA else PROJECT_ROOT / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"
