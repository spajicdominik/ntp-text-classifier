# Testovi za ClassificationService.
#
# Koristi lazni klasifikator, tako da testovi lete i ne moraju skidati model.

from __future__ import annotations

import unittest

from text_classifier.service import ClassificationService
from text_classifier.sources.manual import ManualTextSource

from .fakes import FakeClassifier


class TestClassificationService(unittest.TestCase):
    def setUp(self) -> None:
        self.classifier = FakeClassifier(label="Sports", confidence=0.9)
        self.service = ClassificationService(self.classifier)

    def tearDown(self) -> None:
        self.service.shutdown()

    def test_submit_vraca_future_s_rezultatom(self) -> None:
        source = ManualTextSource("neki tekst")
        entry = self.service.submit(source).result(timeout=5)
        self.assertEqual(entry.result.label, "Sports")
        self.assertEqual(entry.source_name, "ručni unos")

    def test_klasifikator_dobiva_ocisceni_tekst(self) -> None:
        self.service.submit(ManualTextSource("  puno   praznina ")).result(timeout=5)
        self.assertEqual(self.classifier.calls, ["puno praznina"])

    def test_povijest_se_puni(self) -> None:
        for _ in range(3):
            self.service.submit(ManualTextSource("x")).result(timeout=5)
        self.assertEqual(len(self.service.history), 3)

    def test_koristi_protocol_ne_konkretnu_klasu(self) -> None:
        from text_classifier.model.classifier import Classifier

        self.assertIsInstance(self.classifier, Classifier)


if __name__ == "__main__":
    unittest.main()
