# Tekst koji je korisnik sam utipkao u sucelje.

from __future__ import annotations

from .base import TextSource


class ManualTextSource(TextSource):
    """Najjednostavniji izvor, samo vrati ono sto je dobio.

    >>> ManualTextSource("Pozdrav svijete").read()
    'Pozdrav svijete'
    >>> ManualTextSource("  puno   praznina  ").read_cleaned()
    'puno praznina'
    """

    name = "ručni unos"

    def __init__(self, text: str, name: str | None = None) -> None:
        self._text = text
        # GUI promijeni ime kad tekst zapravo nije utipkan nego je dosao
        # iz datoteke ili s weba, da povijest pokaze pravi izvor.
        if name is not None:
            self.name = name

    def read(self) -> str:
        return self._text
