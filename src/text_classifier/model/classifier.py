# Kako klasifikator mora izgledati i sto vraca.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class ClassificationResult:
    """Rezultat jedne klasifikacije. Frozen jer se nakon toga vise ne mijenja."""

    text: str
    label: str
    confidence: float
    # vjerojatnosti svih klasa, ne samo pobjednicke, da GUI moze nacrtati trake
    scores: dict[str, float] = field(default_factory=dict)


@runtime_checkable
class Classifier(Protocol):
    """Sve sto ima metodu `classify` prolazi kao klasifikator.

    Nema nasljedivanja, dovoljno je da se metoda poklapa. Zbog toga u
    testovima mogu ubaciti lazni klasifikator, a ostatak koda ne zna razliku.
    """

    def classify(self, text: str) -> ClassificationResult:
        ...
