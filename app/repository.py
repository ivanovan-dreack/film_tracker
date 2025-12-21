from __future__ import annotations
from dataclasses import replace
from typing import List, Optional

from app.models import Film, FilmeStatus

class FilmeRepository:

    def __init__(self) -> None:
        self._filme: List[Film] = []
        self._next_id: int = 1

    def list_alle(self) -> List[Film]:
        return list(self._filme)

    def get_by_id(self, film_id: int) -> Optional[Film]:
        for f in self._filme:
            if(film_id == f.id):
                return f
            return None

    def hinzu(self, titel: str, jahr: int, genres: List[str]) -> Optional[Film]:
        if any(f.titel.lower() == titel.lower() and f.jahr == jahr for f in self._filme):
            raise ValueError(f"Das Film {titel} {jahr} exestriert schon.")

        film = Film(
            id = self._next_id,
            titel = titel.strip(),
            jahr = int(jahr),
            status= FilmeStatus.GEPLANT,
            genres=[g.strip() for g in genres if g.strip()],
        )
        self._filme.append(film)
        self._next_id += 1
        return film
    
    def set_status(self, film_id: int, status: FilmeStatus) -> Film:
        id = self._index_von(film_id)
        updated = replace(self._filme[id], status=status)
        self._filme[id] = updated
        return updated
    
    def hinzufuegen_kommentar(self, film_id: int, text: str) -> Film:
        text = text.strip()
        if not text:
            raise ValueError(f"Der Kommentar kann nicht leer sein.")
        id = self._index_von(film_id)
        film = self._filme[id]
        updated_kommentare = list(film.kommentare)
        updated_kommentare.append(text)

        updated = replace(self._filme[id], kommentare = updated_kommentare)
        self._filme[id] = updated
        return updated


    def _index_von(self, film_id: int) -> int:
        for i, f in enumerate(self._filme):
            if f.id == film_id: 
                return i
            raise ValueError(f"Der Film mit ID {film_id} kann nicht gefunden werden.")  

