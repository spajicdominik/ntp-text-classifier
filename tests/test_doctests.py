# Pokupi doctestove iz izvornog koda i ubaci ih u unittest.
#
# Zahvaljujuci load_tests protokolu jedan `python -m unittest` pokrene i
# obicne testove i sve >>> primjere iz docstringova.

from __future__ import annotations

import doctest
import unittest

from text_classifier import decorators, history
from text_classifier.sources import base
from text_classifier.sources import file as file_source
from text_classifier.sources import manual, web

_MODULI = [decorators, history, base, manual, file_source, web]


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite,
               ignore: object) -> unittest.TestSuite:
    for modul in _MODULI:
        tests.addTests(doctest.DocTestSuite(modul))
    return tests


if __name__ == "__main__":
    unittest.main()
