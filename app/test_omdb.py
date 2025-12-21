from .providers.omdb import film_von_omdb_holen

film = film_von_omdb_holen("Dune", 2021)
print(film)