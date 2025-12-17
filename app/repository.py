from __future__ import annotations
from dataclasses import replace
from typing import List, Optional

from app.models import Film, FilmeStatus

class FilmeRepository:

    def __init__(self) -> None:
        self.filme: List[Film] = []
        self._next_id: int = 1

    def list_alle(self) -> List[Film]:
        return list(self.filme)

    def get_by_id(self, film_id: int) -> Optional[Film]:
        for f in self.filme:
            if(film_id == f.id):
                return f
            return None

    def hinzu(self, titel: str, jahr: int, genres: List[str]) -> Optional[Film]:
        if any(f.titel.lower() == titel.lower() and f.jahr == jahr for f in self.filme):
            raise ValueError(f"Das Film {titel} {jahr} exestriert schon.")

        film = Film(
            id = self._next_id,
            titel = titel.strip(),
            jahr = int(jahr),
            status= FilmeStatus.GEPLANNT,
            genres=[g.strip() for g in genres if g.strip()],
        )
        self.filme.append(film)
        self._next_id += 1
        return film
    

