import tkinter as tk
from tkinter import ttk, messagebox

from app.models import Film, FilmeStatus
from app.repository import FilmeRepository

# если OMDb модуль у тебя есть:
from app.providers.omdb import film_von_omdb_holen

import app.converter

class FilmTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Film Tracker")
        self.geometry("900x520")
        self.resizable(False, False)

        self.repo = FilmeRepository()
        self.aktueller_film: Film | None = None

        self._build_ui()

    def _build_ui(self):
        left = ttk.Frame(self, padding=10)
        left.pack(side="left", fill="y")

        right = ttk.Frame(self, padding=10)
        right.pack(side="right", fill="both", expand=True)

        PAD_Y = 6
        ENTRY_WIDTH = 36

        # --- Titel ---
        ttk.Label(left, text="Titel:").grid(row=0, column=0, sticky="w", pady=PAD_Y)
        self.titel_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.titel_var, width=ENTRY_WIDTH)\
        .grid(row=0, column=1, pady=PAD_Y, sticky="ew")

        # --- Jahr ---
        ttk.Label(left, text="Jahr:").grid(row=1, column=0, sticky="w", pady=PAD_Y)
        self.jahr_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.jahr_var, width=ENTRY_WIDTH)\
        .grid(row=1, column=1, pady=PAD_Y, sticky="ew")

        # --- Suchen ---
        ttk.Button(left, text="Suchen (OMDb)", command=self.suchen_omdb, width=ENTRY_WIDTH)\
        .grid(row=2, column=0, columnspan=2, pady=PAD_Y, sticky="ew")

        # --- Status ---
        ttk.Label(left, text="Status:").grid(row=3, column=0, sticky="w", pady=PAD_Y)
        self.status_var = tk.StringVar(value=FilmeStatus.GEPLANT.value)
        ttk.Combobox(
        left,
        textvariable=self.status_var,
        values=[s.value for s in FilmeStatus],
        state="readonly",
        width=ENTRY_WIDTH - 2
        ).grid(row=3, column=1, pady=PAD_Y, sticky="ew")

        # --- Kommentar ---
        ttk.Label(left, text="Kommentar:").grid(row=4, column=0, sticky="w", pady=PAD_Y)
        self.kommentar_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.kommentar_var, width=ENTRY_WIDTH)\
        .grid(row=4, column=1, pady=PAD_Y, sticky="ew")

        # --- Kommentar Button ---
        ttk.Button(left, text="Kommentar hinzufügen", command=self.kommentar_hinzufuegen, width=ENTRY_WIDTH)\
        .grid(row=5, column=0, columnspan=2, pady=PAD_Y, sticky="ew")

        # --- Hinzufügen ---
        ttk.Button(left, text="In Liste hinzufügen", command=self.in_liste_hinzufuegen, width=ENTRY_WIDTH)\
        .grid(row=6, column=0, columnspan=2, pady=PAD_Y, sticky="ew")

        # Info Bereich
        self.info = tk.Text(left, width=40, height=12)
        self.info.grid(row=7, column=0, columnspan=2, pady=8)
        self.info.configure(state="disabled")

        # --- Rechte Seite: Liste ---
        ttk.Label(right, text="Meine Filme").pack(anchor="w")

        self.listbox = tk.Listbox(right, height=20)
        self.listbox.pack(fill="both", expand=True, pady=8)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        btns = ttk.Frame(right)
        btns.pack(fill="x")

        ttk.Button(btns, text="Status: GESEHEN", command=lambda: self.status_setzen(FilmeStatus.GESEHEN)).pack(side="left", padx=4)
        ttk.Button(btns, text="Status: GEPLANT", command=lambda: self.status_setzen(FilmeStatus.GEPLANT)).pack(side="left", padx=4)

        ttk.Button(btns, text="Refresh", command=self.refresh_liste).pack(side="right", padx=4)

        self.refresh_liste()

    # -------- Aktionen --------
    def suchen_omdb(self):
        titel = self.titel_var.get().strip()
        jahr_txt = self.jahr_var.get().strip()

        if not titel:
            messagebox.showwarning("Fehlt", "Bitte Titel eingeben.")
            return

        jahr = None
        if jahr_txt:
            if not jahr_txt.isdigit():
                messagebox.showwarning("Fehler", "Jahr muss eine Zahl sein.")
                return
            jahr = int(jahr_txt)

        try:
            daten = film_von_omdb_holen(titel, jahr)
            self.aktueller_film = Film(
                id=0,
                titel=daten.titel,
                jahr=daten.jahr,
                genres=daten.genres,
                kommentare=[],
                bewertungen=None,
                status=FilmeStatus(self.status_var.get()),
            )
            self._show_info(self.aktueller_film, daten.schauspieler, daten.imdb_rating)
        except Exception as e:
            messagebox.showerror("OMDb Fehler", str(e))

    def kommentar_hinzufuegen(self):
        if self.aktueller_film is None:
            messagebox.showinfo("Info", "Bitte zuerst einen Film suchen.")
            return
        text = self.kommentar_var.get().strip()
        if not text:
            return
        self.aktueller_film.kommentare.append(text)
        self.kommentar_var.set("")
        self._show_info(self.aktueller_film, None, None)

    def in_liste_hinzufuegen(self):
        if self.aktueller_film is None:
            messagebox.showinfo("Info", "Bitte zuerst einen Film suchen.")
            return
        try:
            gespeichert = self.repo.hinzu(self.aktueller_film)
            self.aktueller_film = None
            self._clear_info()
            self.refresh_liste()
            messagebox.showinfo("OK", f"Hinzugefügt: {gespeichert.titel} ({gespeichert.jahr})")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def refresh_liste(self):
        self.listbox.delete(0, tk.END)
        for film in self.repo.list_alle():
            self.listbox.insert(tk.END, f"{film.id}. {film.titel} ({film.jahr}) [{film.status.value}]")

    def on_select(self, _event):
        sel = self.listbox.curselection()
        if not sel:
            return
        text = self.listbox.get(sel[0])
        film_id = int(text.split(".")[0])
        film = self.repo.get_by_id(film_id)
        if film:
            self._show_info(film, None, None)

    def status_setzen(self, status: FilmeStatus):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Bitte Film in der Liste auswählen.")
            return
        text = self.listbox.get(sel[0])
        film_id = int(text.split(".")[0])
        try:
            self.repo.set_status(film_id, status)
            self.refresh_liste()
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    # -------- UI Helpers --------
    def _show_info(self, film: Film, schauspieler, imdb_rating):
        self.info.configure(state="normal")
        self.info.delete("1.0", tk.END)
        self.info.insert(tk.END, f"Titel: {film.titel}\n")
        self.info.insert(tk.END, f"Jahr: {film.jahr}\n")
        self.info.insert(tk.END, f"Status: {film.status.value}\n")
        self.info.insert(tk.END, f"Genres: {', '.join(film.genres)}\n")
        if imdb_rating is not None:
            self.info.insert(tk.END, f"IMDb Rating: {imdb_rating}\n")
        if schauspieler:
            self.info.insert(tk.END, f"Schauspieler: {', '.join(schauspieler)}\n")
        if film.kommentare:
            self.info.insert(tk.END, "\nKommentare:\n")
            for k in film.kommentare:
                self.info.insert(tk.END, f" - {k}\n")
        self.info.configure(state="disabled")

    def _clear_info(self):
        self.info.configure(state="normal")
        self.info.delete("1.0", tk.END)
        self.info.configure(state="disabled")


def main():
    app = FilmTrackerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()