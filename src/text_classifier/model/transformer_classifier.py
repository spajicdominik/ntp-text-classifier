# Pravi klasifikator: mali BERT istreniran na AG News, vrti se na PyTorchu.

from __future__ import annotations

import os

# transformers inace pokusa povuci i TensorFlow i Flax, a oni su na ovom
# racunalu instalirani ali neispravni pa sve pukne. Ovo mora stajati prije
# nego se transformers uopce uveze.
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_FLAX", "0")

from ..config import CLASS_LABELS, MAX_TOKENS, MODEL_NAME
from ..decorators import timed
from .classifier import ClassificationResult


class TransformerClassifier:
    """Klasificira tekst u jednu od AG News klasa."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        # Uvozim tu, a ne na vrhu, da se modul moze uvesti i bez torcha
        # (npr. kad testiram GUI s laznim klasifikatorom).
        import torch
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
        )

        # Model se ucitava samo jednom, pri stvaranju objekta. Sporo je,
        # pa bi bilo glupo raditi to kod svake klasifikacije.
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # samo predvidamo, ne treniramo
        self.torch = torch

    @timed("classify")
    def classify(self, text: str) -> ClassificationResult:
        # Predugi tekst se odreze na MAX_TOKENS, model ionako ne gleda dalje.
        inputs = self.tokenizer(
            text,
            truncation=True,
            max_length=MAX_TOKENS,
            return_tensors="pt",
        )
        with self.torch.no_grad():  # bez gradijenata je brze i trosi manje
            logits = self.model(**inputs).logits

        # Model vrati sirove brojeve, softmax ih pretvori u vjerojatnosti.
        # [0] je zato sto smo poslali samo jedan tekst.
        probs = logits.softmax(dim=-1)[0]
        idx = int(probs.argmax())
        scores = {CLASS_LABELS[i]: float(probs[i]) for i in range(len(CLASS_LABELS))}
        return ClassificationResult(
            text=text,
            label=CLASS_LABELS[idx],
            confidence=float(probs[idx]),
            scores=scores,
        )
