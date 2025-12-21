from app.repository import FilmeRepository
from app.models import FilmeStatus

def test_repo_add_comment_and_status():
    repo = FilmeRepository()

    film = repo.hinzu("Dune", 2021, ["Sci-Fi"])
    repo.hinzufuegen_kommentar(film.id, "Sehr gut")
    repo.set_status(film.id, FilmeStatus.GESEHEN)

    alle = repo.list_alle()
    assert len(alle) == 1
    assert alle[0].titel == "Dune"
    assert alle[0].status == FilmeStatus.GESEHEN
    assert alle[0].kommentare == ["Sehr gut"]