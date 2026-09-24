# Tekst ucitan iz .txt datoteke s diska.

from __future__ import annotations

from pathlib import Path

from .base import TextSource


class FileTextSource(TextSource):
    """Procita datoteku kao UTF-8.

    >>> import os, tempfile
    >>> p = os.path.join(tempfile.mkdtemp(), "primjer.txt")
    >>> with open(p, "w", encoding="utf-8") as f:
    ...     _ = f.write("bok iz datoteke")
    >>> FileTextSource(p).read()
    'bok iz datoteke'
    """

    name = "datoteka"

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def read(self) -> str:
        if not self._path.is_file():
            raise FileNotFoundError(f"Datoteka ne postoji: {self._path}")
        # encoding navodim izricito da se isto ponasa na svim racunalima
        return self._path.read_text(encoding="utf-8")
