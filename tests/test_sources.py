# Testovi za izvore teksta i apstraktnu klasu koju dijele.

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from text_classifier.sources.base import TextSource
from text_classifier.sources.file import FileTextSource
from text_classifier.sources.manual import ManualTextSource
from text_classifier.sources.web import WebTextSource


class TestManualSource(unittest.TestCase):
    def test_read_vraca_tekst(self) -> None:
        self.assertEqual(ManualTextSource("bok").read(), "bok")

    def test_read_cleaned_normalizira_praznine(self) -> None:
        self.assertEqual(ManualTextSource("  a   b  ").read_cleaned(), "a b")

    def test_ime_se_moze_nadjacati(self) -> None:
        self.assertEqual(ManualTextSource("x", name="web: url").name, "web: url")

    def test_je_textsource(self) -> None:
        self.assertIsInstance(ManualTextSource("x"), TextSource)


class TestFileSource(unittest.TestCase):
    def test_cita_datoteku(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.txt"
            p.write_text("sadržaj", encoding="utf-8")
            self.assertEqual(FileTextSource(p).read(), "sadržaj")

    def test_nepostojeca_datoteka_baca(self) -> None:
        with self.assertRaises(FileNotFoundError):
            FileTextSource("/ne/postoji/nikako.txt").read()


class TestWebSource(unittest.TestCase):
    def test_extract_text_mice_skripte(self) -> None:
        html = "<html><body><p>Bok</p><script>var x=1;</script></body></html>"
        self.assertEqual(WebTextSource._extract_text(html), "Bok")


class TestABCNasljedivanje(unittest.TestCase):
    def test_nepotpuna_podklasa_se_ne_moze_instancirati(self) -> None:
        class Nepotpuna(TextSource):
            pass  # ne implementira read()

        with self.assertRaises(TypeError):
            Nepotpuna()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
