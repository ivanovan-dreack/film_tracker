from app.repository import FilmeRepository
from app.models import FilmeStatus

repo = FilmeRepository()
film = repo.hinzu("Dune", 2021, ["Sci-Fi"])
repo.hinzufuegen_kommentar(film.id, "Sehr gut")
repo.set_status(film.id, FilmeStatus.GESEHEN)

print(repo.list_alle())