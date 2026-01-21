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

    def hinzu(self, film: Film) -> Film:
        if any(
            f.titel.lower() == film.titel.lower() and f.jahr == film.jahr
            for f in self._filme
        ):
            raise ValueError(f"Der Film {film.titel} ({film.jahr}) existiert bereits.")

        film.id = self._next_id
        self._next_id += 1

        film.titel = film.titel.strip()
        film.jahr = int(film.jahr)
        film.genres = [g.strip() for g in film.genres if g.strip()]

        self._filme.append(film)
        return film
    
    def film_loeschen(self, film: Film) -> None:
        for i, f in enumerate(self._filme):
            if f.id == film.id:
                del self._filme[i]
                return
            
        raise ValueError(f"Der Film mit ID {film.id} kann nicht gefunden werden.")
    
    def set_status(self, film_id: int, status: FilmeStatus):
        film = self.get_by_id(film_id)
        if film is None:
            raise ValueError(f"Der Film mit ID {film_id} kann nicht gefunden werden.")
        film.status = status
    
    def hinzufuegen_kommentar(self, film_id: int, text: str) -> Film:
        text = text.strip()
        if not text:
            raise ValueError("Der Kommentar kann nicht leer sein.")

        film = self.get_by_id(film_id)
        if film is None:
            raise ValueError(f"Der Film mit ID {film_id} kann nicht gefunden werden.")

        film.kommentare.append(text)
        return film

    def set_alle(self, filme: List[Film]) -> None:
        self._filme = list(filme)
        self._next_id = max((f.id for f in self._filme), default=0) + 1

    def _index_von(self, film_id: int) -> int:
        for i, f in enumerate(self._filme):
            if f.id == film_id: 
                return i
        raise ValueError(f"Der Film mit ID {film_id} kann nicht gefunden werden.")  

