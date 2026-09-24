# Pamti zadnjih par klasifikacija da ih GUI moze izlistati.

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from .config import HISTORY_LIMIT
from .model.classifier import ClassificationResult


@dataclass(frozen=True)
class HistoryEntry:
    """Jedan red u povijesti: sto je ispalo, odakle je tekst i kad."""

    result: ClassificationResult
    source_name: str
    timestamp: datetime


class ClassificationHistory:
    """Povijest ogranicene velicine. Kad se napuni, najstariji ispadne sam.

    >>> from text_classifier.model.classifier import ClassificationResult
    >>> h = ClassificationHistory(limit=2)
    >>> _ = h.add(ClassificationResult("a", "Sports", 0.9), "ručni unos")
    >>> _ = h.add(ClassificationResult("b", "World", 0.8), "datoteka")
    >>> _ = h.add(ClassificationResult("c", "Business", 0.7), "web")
    >>> len(h)
    2
    >>> [e.result.label for e in h]
    ['World', 'Business']
    """

    def __init__(self, limit: int = HISTORY_LIMIT) -> None:
        # deque s maxlen sam izbacuje najstarije, ne moram to rucno paziti
        self._entries: deque[HistoryEntry] = deque(maxlen=limit)

    def add(self, result: ClassificationResult, source_name: str) -> HistoryEntry:
        """Ubaci novi rezultat u povijest i vrati zapis koji je nastao."""
        entry = HistoryEntry(
            result=result,
            source_name=source_name,
            timestamp=datetime.now(),
        )
        self._entries.append(entry)
        return entry

    def latest(self, count: int | None = None) -> list[HistoryEntry]:
        """Zapisi od najnovijeg prema starijem."""
        items = list(reversed(self._entries))
        return items if count is None else items[:count]

    def clear(self) -> None:
        self._entries.clear()

    def __iter__(self) -> Iterator[HistoryEntry]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
