from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class FilmeStatus(Enum):
    GEPLANT="geplant"
    GESEHEN="gesehen"

@dataclass
class Film:
    id: int
    title: str
    jahr: int
    genres: List[str]
    kommentare: List[str] = field(default_factory=list)
    bewertungen: Optional[int] = None
    status: FilmeStatus= FilmeStatus.GEPLANT
    
