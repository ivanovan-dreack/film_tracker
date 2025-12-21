from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

import requests
from dotenv import load_dotenv


@dataclass
class OmdbFilmDaten:
    titel: str
    jahr: int
    genres: List[str]
    schauspieler: List[str]
    imdb_rating: Optional[float]

def _parse_jahr(jahr_text: str) -> int:
    jahr_text = (jahr_text or "").strip()
    if not jahr_text:
        return 0
    
    jahr_text = jahr_text.replace("–", "-").replace("—", "-")

    first_part = jahr_text.split("-")[0].strip()
    try:
        return int(first_part)
    except ValueError:
        return 0
    
def film_von_omdb_holen(titel: str, jahr: Optional[int] = None) -> OmdbFilmDaten:
    load_dotenv()  # lädt .env Datei
    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise ValueError("OMDB_API_KEY fehlt.")
    
    params = {
        "t": titel,
        "apikey": api_key,
        "type": "movie",
        "plot": "short",
    }
    if jahr is not None:
        params["y"] = str(jahr)

    r = requests.get("https://www.omdbapi.com/", params=params,
                     timeout=15)
    r.raise_for_status()
    data = r.json()

    if data.get("Response") != "True":
        raise ValueError(f"OMDb: {data.get('Error', 'Film nicht gefunden')}")
    
    genres = [g.strip() for g in (data.get("Genre") or "").split(",") if g.strip()]
    schauspieler = [a.strip() for a in (data.get("Actors") or "").split(",") if a.strip()]

    imdb_rating: Optional[float] = None
    raw_rating = data.get("imdbRating")
    if raw_rating and raw_rating != "N/A":
        try:
            imdb_rating = float(raw_rating)
        except ValueError:
            imdb_rating = None
    
    return OmdbFilmDaten(
        titel=(data.get("Title") or titel).strip(),
        jahr=_parse_jahr(data.get("Year") or ""),
        genres=genres,
        schauspieler=schauspieler,
        imdb_rating=imdb_rating,
    )