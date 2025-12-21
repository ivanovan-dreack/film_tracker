from app.providers.omdb import film_von_omdb_holen, _parse_jahr

film = film_von_omdb_holen("Dune", 2021)
print(film)

def test_parse_jahr():
    assert _parse_jahr("2021") == 2021
    assert _parse_jahr("2014–2019") == 2014
    assert _parse_jahr("") == 0