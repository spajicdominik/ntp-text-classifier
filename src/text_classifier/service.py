# Ovdje se spajaju izvor teksta, klasifikator i povijest.
#
# Klasifikacija zna potrajati (pogotovo ako tekst tek treba dohvatiti s weba),
# pa se ne izvodi u GUI dretvi nego u ThreadPoolExecutoru. Zato `submit` ne
# vraca gotov rezultat nego Future, a sucelje u meduvremenu ostaje zivo.

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor

from .decorators import timed
from .history import ClassificationHistory, HistoryEntry
from .model.classifier import Classifier
from .sources.base import TextSource


class ClassificationService:
    """Vrti klasifikaciju u pozadini i pamti sto je bilo."""

    def __init__(
        self,
        classifier: Classifier,
        history: ClassificationHistory | None = None,
        max_workers: int = 2,
    ) -> None:
        # Tip je Classifier (Protocol), ne konkretna klasa, pa mu u testovima
        # mogu podmetnuti lazni klasifikator bez ikakvog nasljedivanja.
        self._classifier = classifier
        self.history = history if history is not None else ClassificationHistory()
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="classify",
        )

    def submit(self, source: TextSource) -> "Future[HistoryEntry]":
        """Posalji izvor na klasifikaciju i odmah vrati Future.

        Na Future se moze zakaciti `add_done_callback` ili pozvati `.result()`
        ako se ipak zeli pricekati rezultat.
        """
        return self._executor.submit(self._run, source)

    @timed("service.run")
    def _run(self, source: TextSource) -> HistoryEntry:
        # Ovo se izvodi u radnoj dretvi. Ne zna niti ga briga koji je tocno
        # izvor u pitanju, samo trazi tekst od njega.
        text = source.read_cleaned()
        result = self._classifier.classify(text)
        return self.history.add(result, source.name)

    def shutdown(self) -> None:
        """Zatvori bazen dretvi kad se aplikacija gasi."""
        self._executor.shutdown(wait=False)
