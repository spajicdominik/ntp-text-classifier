# Tkinter sucelje. Lijevo je unos teksta, desno rezultat i povijest.
#
# Dvije stvari koje bi inace zamrznule prozor idu u pozadinsku dretvu:
# ucitavanje modela i sama klasifikacija. Rezultat se natrag u GUI vraca
# preko root.after, jer se Tkinter widgeti smiju dirati samo iz glavne dretve.

from __future__ import annotations

import logging
import threading
import tkinter as tk
from concurrent.futures import Future
from tkinter import filedialog, messagebox, ttk

from ..config import APP_TITLE, CLASS_DESCRIPTIONS, CLASS_LABELS
from ..history import HistoryEntry
from ..service import ClassificationService
from ..sources.file import FileTextSource
from ..sources.manual import ManualTextSource
from ..sources.web import WebTextSource

logger = logging.getLogger("text_classifier")


class App:
    """Glavni prozor aplikacije."""

    def __init__(self, root: tk.Tk, service: ClassificationService | None = None) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x560")

        # Servis se moze predati izvana (tako ga testovi ubace gotovog),
        # inace ga slozimo sami tek kad se model ucita.
        self._service: ClassificationService | None = service
        # Odakle je trenutni tekst, to ide u povijest.
        self._origin: str = "ručni unos"

        self._build_layout()

        if self._service is None:
            self._set_status("Učitavam model…")
            self._classify_btn.config(state=tk.DISABLED)
            threading.Thread(target=self._load_model, daemon=True).start()
        else:
            self._set_status("Spreman.")

    # Slaganje sucelja

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self._build_left(container)
        self._build_right(container)

        self._status = ttk.Label(self.root, relief=tk.SUNKEN, anchor=tk.W, padding=4)
        self._status.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_left(self, parent: ttk.Frame) -> None:
        left = ttk.LabelFrame(parent, text="Unos teksta", padding=8)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)

        self._text_input = tk.Text(left, wrap=tk.WORD, height=12)
        self._text_input.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # red s URL-om
        ttk.Label(left, text="URL:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self._url_entry = ttk.Entry(left)
        self._url_entry.grid(row=1, column=1, sticky="ew", pady=(8, 0))
        ttk.Button(left, text="Dohvati", command=self._on_fetch_web).grid(
            row=1, column=2, sticky="e", pady=(8, 0), padx=(6, 0)
        )

        # red s gumbima
        controls = ttk.Frame(left)
        controls.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        ttk.Button(controls, text="Učitaj .txt", command=self._on_load_file).pack(
            side=tk.LEFT
        )
        ttk.Button(controls, text="Očisti", command=self._on_clear).pack(
            side=tk.LEFT, padx=6
        )
        self._classify_btn = ttk.Button(
            controls, text="Klasificiraj", command=self._on_classify
        )
        self._classify_btn.pack(side=tk.RIGHT)

    def _build_right(self, parent: ttk.Frame) -> None:
        right = ttk.Frame(parent)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        result_box = ttk.LabelFrame(right, text="Rezultat", padding=8)
        result_box.grid(row=0, column=0, sticky="ew")
        result_box.columnconfigure(1, weight=1)

        self._result_var = tk.StringVar(value="—")
        ttk.Label(result_box, textvariable=self._result_var,
                  font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        # po jedna traka za svaku klasu, da se vidi i koliko su ostale dobile
        self._bars: dict[str, tuple[ttk.Progressbar, tk.StringVar]] = {}
        for i, label in enumerate(CLASS_LABELS, start=1):
            ttk.Label(result_box, text=CLASS_DESCRIPTIONS.get(label, label)).grid(
                row=i, column=0, sticky="w", pady=2
            )
            bar = ttk.Progressbar(result_box, maximum=100.0, length=180)
            bar.grid(row=i, column=1, sticky="ew", padx=6)
            pct = tk.StringVar(value="0%")
            ttk.Label(result_box, textvariable=pct, width=6).grid(row=i, column=2)
            self._bars[label] = (bar, pct)

        hist_box = ttk.LabelFrame(right, text="Povijest klasifikacija", padding=8)
        hist_box.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        hist_box.rowconfigure(0, weight=1)
        hist_box.columnconfigure(0, weight=1)

        self._history_list = tk.Listbox(hist_box)
        self._history_list.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(hist_box, command=self._history_list.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self._history_list.config(yscrollcommand=scroll.set)

    # Ucitavanje modela

    def _load_model(self) -> None:
        """Ucita model u pozadini pa javi glavnoj dretvi da je gotovo."""
        try:
            from ..model.transformer_classifier import TransformerClassifier

            classifier = TransformerClassifier()
        except Exception as exc:  # noqa: BLE001 - sto god pukne, zelim to vidjeti
            logger.exception("Neuspjelo učitavanje modela")
            self.root.after(0, self._on_model_error, exc)
            return
        self.root.after(0, self._on_model_ready, classifier)

    def _on_model_ready(self, classifier: object) -> None:
        self._service = ClassificationService(classifier)  # type: ignore[arg-type]
        self._classify_btn.config(state=tk.NORMAL)
        self._set_status("Spreman.")

    def _on_model_error(self, exc: Exception) -> None:
        self._set_status(f"Greška pri učitavanju modela: {exc}")
        messagebox.showerror("Greška", f"Model se nije mogao učitati:\n{exc}")

    # Gumbi

    def _on_load_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Odaberi .txt datoteku",
            filetypes=[("Tekstualne datoteke", "*.txt"), ("Sve datoteke", "*.*")],
        )
        if not path:
            return
        try:
            text = FileTextSource(path).read()
        except OSError as exc:
            messagebox.showerror("Greška", str(exc))
            return
        self._set_text(text)
        self._origin = f"datoteka: {path.split('/')[-1]}"
        self._set_status(f"Učitano iz {self._origin}.")

    def _on_fetch_web(self) -> None:
        url = self._url_entry.get().strip()
        if not url:
            messagebox.showinfo("Web", "Upiši URL za dohvat.")
            return
        self._set_status(f"Dohvaćam {url} …")
        # skidanje stranice zna potrajati, pa ne ide u glavnoj dretvi
        thread = threading.Thread(
            target=self._fetch_web_worker, args=(url,), daemon=True
        )
        thread.start()

    def _fetch_web_worker(self, url: str) -> None:
        try:
            text = WebTextSource(url).read()
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, self._set_status, f"Greška pri dohvatu: {exc}")
            return
        self.root.after(0, self._on_web_fetched, url, text)

    def _on_web_fetched(self, url: str, text: str) -> None:
        self._set_text(text)
        self._origin = f"web: {url}"
        self._set_status(f"Dohvaćeno s {url} ({len(text)} znakova).")

    def _on_clear(self) -> None:
        self._text_input.delete("1.0", tk.END)
        self._origin = "ručni unos"
        self._set_status("Očišćeno.")

    def _on_classify(self) -> None:
        if self._service is None:
            return
        text = self._text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Klasifikacija", "Nema teksta za klasifikaciju.")
            return
        source = ManualTextSource(text, name=self._origin)
        self._set_status("Klasificiram…")
        self._classify_btn.config(state=tk.DISABLED)
        future = self._service.submit(source)
        # Kad radna dretva zavrsi, vrati se u GUI dretvu preko after().
        future.add_done_callback(
            lambda f: self.root.after(0, self._on_classified, f)
        )

    def _on_classified(self, future: "Future[HistoryEntry]") -> None:
        self._classify_btn.config(state=tk.NORMAL)
        try:
            # ako je u radnoj dretvi puklo, greska iskoci tu
            entry = future.result()
        except Exception as exc:  # noqa: BLE001
            logger.exception("Greška u klasifikaciji")
            self._set_status(f"Greška: {exc}")
            messagebox.showerror("Greška", str(exc))
            return
        self._render_result(entry)
        self._set_status("Gotovo.")

    # Prikaz

    def _render_result(self, entry: HistoryEntry) -> None:
        result = entry.result
        opis = CLASS_DESCRIPTIONS.get(result.label, result.label)
        self._result_var.set(f"{opis}  ({result.confidence:.0%})")
        for label, (bar, pct) in self._bars.items():
            value = result.scores.get(label, 0.0) * 100.0
            bar["value"] = value
            pct.set(f"{value:.0f}%")
        line = (
            f"{entry.timestamp:%H:%M:%S}  {result.label} "
            f"({result.confidence:.0%})  [{entry.source_name}]"
        )
        self._history_list.insert(0, line)  # najnovije na vrh

    def _set_text(self, text: str) -> None:
        self._text_input.delete("1.0", tk.END)
        self._text_input.insert("1.0", text)

    def _set_status(self, message: str) -> None:
        self._status.config(text=message)

    def on_close(self) -> None:
        if self._service is not None:
            self._service.shutdown()
        self.root.destroy()


def run() -> None:
    """Slozi logiranje, otvori prozor i pusti Tkinter da vrti svoje."""
    from ..logging_config import setup_logging

    setup_logging()
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
