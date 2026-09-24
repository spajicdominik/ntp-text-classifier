# Zajednicka osnova za sve odakle mozemo dobiti tekst.
#
# Napravljeno kao apstraktna klasa, a ne protokol, jer izvori dijele i nesto
# koda (`read_cleaned`), pa ga ovako naslijede umjesto da ga svi prepisuju.

from __future__ import annotations

from abc import ABC, abstractmethod


class TextSource(ABC):
    """Svaki izvor teksta mora znati vratiti svoj tekst."""

    # Pise se u povijest, da se vidi odakle je tekst dosao.
    name: str = "nepoznato"

    @abstractmethod
    def read(self) -> str:
        """Vrati sirovi tekst. Podklase ovo moraju napisati same."""
        raise NotImplementedError

    def read_cleaned(self) -> str:
        """Isto kao read(), samo pobaca visak praznina i prijelaza u novi red.

        >>> class Dummy(TextSource):
        ...     name = "dummy"
        ...     def read(self) -> str:
        ...         return "  puno   \\n praznina  "
        >>> Dummy().read_cleaned()
        'puno praznina'
        """
        return " ".join(self.read().split())
