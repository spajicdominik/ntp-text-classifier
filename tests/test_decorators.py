# Testovi za dekoratore.

from __future__ import annotations

import unittest

from text_classifier.decorators import log_calls, timed


class TestDecorators(unittest.TestCase):
    def test_log_calls_ne_mijenja_rezultat(self) -> None:
        @log_calls
        def zbroji(a: int, b: int) -> int:
            return a + b

        self.assertEqual(zbroji(2, 3), 5)

    def test_log_calls_cuva_ime_i_docstring(self) -> None:
        @log_calls
        def funkcija() -> None:
            """Opis."""

        self.assertEqual(funkcija.__name__, "funkcija")
        self.assertEqual(funkcija.__doc__, "Opis.")

    def test_timed_vraca_rezultat(self) -> None:
        @timed("test")
        def puta_dva(x: int) -> int:
            return x * 2

        self.assertEqual(puta_dva(21), 42)

    def test_timed_bez_labela_koristi_ime_funkcije(self) -> None:
        @timed()
        def nesto() -> str:
            return "ok"

        self.assertEqual(nesto(), "ok")
        self.assertEqual(nesto.__name__, "nesto")


if __name__ == "__main__":
    unittest.main()
