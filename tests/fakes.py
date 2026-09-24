# Lazni klasifikator, da testovi ne moraju ucitavati pravi model.

from __future__ import annotations

from text_classifier.model.classifier import ClassificationResult


class FakeClassifier:
    """Uvijek vrati istu klasu, a usput pamti s cime je pozvan.

    Nista ne nasljeduje, samo ima metodu `classify` i to je dovoljno da
    prode kao Classifier.
    """

    def __init__(self, label: str = "Sports", confidence: float = 0.99) -> None:
        self._label = label
        self._confidence = confidence
        self.calls: list[str] = []

    def classify(self, text: str) -> ClassificationResult:
        self.calls.append(text)
        return ClassificationResult(
            text=text,
            label=self._label,
            confidence=self._confidence,
            scores={self._label: self._confidence},
        )
