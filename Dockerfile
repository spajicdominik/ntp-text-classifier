# Docker image za NLP klasifikator teksta (Tkinter GUI).
#
# GUI se prikazuje preko X11. Na Macu to radi XQuartz, na Linuxu X server
# koji vec imas. Upute za pokretanje su u README.md.

FROM python:3.12-slim

# tk su biblioteke koje tkinter treba da uopce nacrta prozor. Slim image
# ih nema, pa bi vec `import tkinter` pukao.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tk fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Prvo samo ovisnosti, pa tek onda kod. Tako Docker cachea ovaj spori sloj
# i ne instalira torch ispocetka svaki put kad nesto promijenim u kodu.
COPY requirements.txt .
# torch uzimam s CPU indeksa, inace na amd64 povuce CUDA verziju od par GB
# koja nam ne treba.
RUN pip install --no-cache-dir torch \
        --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Model se skida vec pri buildu, da container radi i bez interneta.
COPY scripts/download_model.py scripts/
RUN python scripts/download_model.py /app/model

COPY src/ src/

ENV TEXT_CLASSIFIER_MODEL=/app/model \
    HF_HUB_OFFLINE=1 \
    PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1

CMD ["python", "-m", "text_classifier"]
