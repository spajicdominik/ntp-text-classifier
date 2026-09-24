# Dohvat teksta s web stranice.
#
# Samo skidanje je asinkrono (asyncio + aiohttp), a `read` je obicni omotac
# oko toga, da se klasa i dalje uklapa u TextSource kao i ostali izvori.

from __future__ import annotations

import asyncio

import aiohttp
from bs4 import BeautifulSoup

from ..config import REQUEST_TIMEOUT_S
from ..decorators import timed
from .base import TextSource


class WebTextSource(TextSource):
    """Skine stranicu sa zadanog URL-a i izvuce tekst iz nje."""

    name = "web"

    def __init__(self, url: str) -> None:
        self._url = url

    async def read_async(self) -> str:
        """Asinkrono skine stranicu i vrati ocisceni tekst."""
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_S)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self._url) as response:
                response.raise_for_status()
                html = await response.text()
        return self._extract_text(html)

    @timed("web.read")
    def read(self) -> str:
        # asyncio.run otvara svoju petlju dogadaja, pa ovo ne smije ici iz
        # koda koji vec vrti petlju. U GUI-u se zove iz radne dretve, tu je ok.
        return asyncio.run(self.read_async())

    @staticmethod
    def _extract_text(html: str) -> str:
        """Izvuce samo vidljivi tekst, skripte i stilove baca van.

        >>> WebTextSource._extract_text(
        ...     "<html><body><p>Bok</p><script>x=1</script></body></html>")
        'Bok'
        """
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return " ".join(soup.get_text(separator=" ").split())
