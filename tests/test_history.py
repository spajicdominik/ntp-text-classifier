# Testovi za povijest klasifikacija.

from __future__ import annotations

import unittest

from text_classifier.history import ClassificationHistory, HistoryEntry
from text_classifier.model.classifier import ClassificationResult


def _rez(label: str) -> ClassificationResult:
    return ClassificationResult(text="t", label=label, confidence=0.5)


class TestHistory(unittest.TestCase):
    def test_add_vraca_entry(self) -> None:
        h = ClassificationHistory()
        entry = h.add(_rez("Sports"), "ručni unos")
        self.assertIsInstance(entry, HistoryEntry)
        self.assertEqual(entry.result.label, "Sports")
        self.assertEqual(entry.source_name, "ručni unos")

    def test_limit_izbacuje_najstarije(self) -> None:
        h = ClassificationHistory(limit=2)
        h.add(_rez("A"), "s")
        h.add(_rez("B"), "s")
        h.add(_rez("C"), "s")
        self.assertEqual(len(h), 2)
        self.assertEqual([e.result.label for e in h], ["B", "C"])

    def test_latest_od_najnovijeg(self) -> None:
        h = ClassificationHistory()
        h.add(_rez("A"), "s")
        h.add(_rez("B"), "s")
        self.assertEqual([e.result.label for e in h.latest()], ["B", "A"])
        self.assertEqual([e.result.label for e in h.latest(1)], ["B"])

    def test_clear(self) -> None:
        h = ClassificationHistory()
        h.add(_rez("A"), "s")
        h.clear()
        self.assertEqual(len(h), 0)


if __name__ == "__main__":
    unittest.main()
