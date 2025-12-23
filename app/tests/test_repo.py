from app.repository import FilmeRepository
from app.models import FilmeStatus, Film

def test_repo_add_comment_and_status():
    repo = FilmeRepository()

    film = Film(
            id = 1,
            titel = "Dune",
            jahr = 2021,
            status= FilmeStatus.GEPLANT,
            genres=["Sci-Fi"],
        )
    film = repo.hinzu(film)
    repo.hinzufuegen_kommentar(film.id, "Sehr gut")
    repo.set_status(film.id, FilmeStatus.GESEHEN)

    alle = repo.list_alle()
    assert len(alle) == 1
    assert alle[0].titel == "Dune"
    assert alle[0].status == FilmeStatus.GESEHEN
    assert alle[0].kommentare == ["Sehr gut"]