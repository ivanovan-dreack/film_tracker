from app.models import Film, FilmeStatus

def speichern_json(filme, dateiname="filme.json"):
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write("[\n")

        for i, film in enumerate(filme):
            f.write("  {\n")
            f.write(f'    "id": {film.id},\n')
            f.write(f'    "titel": "{film.titel}",\n')
            f.write(f'    "jahr": {film.jahr},\n')

            # Genres
            f.write('    "genres": [')
            for j, genre in enumerate(film.genres):
                f.write(f'"{genre}"')
                if j < len(film.genres) - 1:
                    f.write(", ")
            f.write("],\n")

            # Kommentare
            f.write('    "kommentare": [')
            for j, kommentar in enumerate(film.kommentare):
                f.write(f'"{kommentar}"')
                if j < len(film.kommentare) - 1:
                    f.write(", ")
            f.write("],\n")

            # Bewertung
            if film.bewertungen is None:
                f.write('    "bewertungen": null,\n')
            else:
                f.write(f'    "bewertungen": {film.bewertungen},\n')

            # Status (Enum → String)
            f.write(f'    "status": "{film.status.value}"\n')

            f.write("  }")
            if i < len(filme) - 1:
                f.write(",")
            f.write("\n")

        f.write("]\n")


def lesen_json(dateiname="filme.json"):
    filme = []

    with open(dateiname, "r", encoding="utf-8") as f:
        inhalt = f.read()

    # äußere [ ] entfernen
    inhalt = inhalt.strip()
    inhalt = inhalt[1:-1].strip()

    if not inhalt:
        return filme

    # einzelne Film-Objekte trennen
    objekte = inhalt.split("},")
    
    for obj in objekte:
        obj = obj.strip()
        if not obj.endswith("}"):
            obj += "}"

        zeilen = obj.replace("{", "").replace("}", "").split("\n")

        daten = {}
        for zeile in zeilen:
            zeile = zeile.strip().rstrip(",")
            if not zeile:
                continue

            key, value = zeile.split(":", 1)
            key = key.strip().replace('"', '')
            value = value.strip()

            daten[key] = value

        # Werte umwandeln
        film_id = int(daten["id"])
        titel = daten["titel"].strip('"')
        jahr = int(daten["jahr"])

        genres = daten["genres"].strip("[]")
        genres = [] if not genres else [g.strip().strip('"') for g in genres.split(",")]

        kommentare = daten["kommentare"].strip("[]")
        kommentare = [] if not kommentare else [k.strip().strip('"') for k in kommentare.split(",")]

        bewertungen = None
        if daten["bewertungen"] != "null":
            bewertungen = int(daten["bewertungen"])

        status = FilmeStatus(daten["status"].strip('"'))

        filme.append(
            Film(
                id=film_id,
                titel=titel,
                jahr=jahr,
                genres=genres,
                kommentare=kommentare,
                bewertungen=bewertungen,
                status=status,
            )
        )

    return filme

def speichern_xml(filme, dateiname="filme.xml"):
    with open(dateiname, "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<Filme>\n')
        
        for i, film in enumerate(filme):
            f.write('   <Film>\n')
            f.write(f'      <Id>{film.id}</Id>\n')
            f.write(f'      <Titel>{film.titel}</Titel>\n')
            f.write(f'      <Jahr>{film.jahr}</Jahr>\n')

            # Genres
            f.write('       <Genres>\n')
            for j, genre in enumerate(film.genres):
                f.write(f'          <Genre>{genre}</Genre>\n')
            f.write("       </Genres>\n")

            # Kommentare
            f.write('       <Kommentare>')
            for j, kommentar in enumerate(film.kommentare):
                f.write(f'         <Kommentar>{kommentar}</Kommentar>')
            f.write('       </Kommentare>\n')

            # Bewertung
            if film.bewertungen is None:
                f.write('       <Bewertungen>null</Bewertungen>\n')
            else:
                f.write(f'       <Bewertungen>{film.bewertungen}</Bewertungen>\n')

            # Status
            f.write(f'      <Status>{film.status.value}</Status>\n')

            f.write('   </Film>\n')
        f.write('</Filme>\n')

from app.models import Film, FilmeStatus


def lesen_xml(dateiname="filme.xml"):
    filme = []

    with open(dateiname, "r", encoding="utf-8") as f:
        text = f.read()
    bloecke = text.split("<Film>")
    
    for block in bloecke[1:]:  # erstes Element ist vor dem ersten Film
        block = block.split("</Film>")[0]

        def wert(tag):
            if f"<{tag}>" not in block:
                return ""
            return block.split(f"<{tag}>")[1].split(f"</{tag}>")[0].strip()

        film_id = int(wert("Id"))
        titel = wert("Titel")
        jahr = int(wert("Jahr"))

        # Genres lesen
        genres_block = wert("Genres")
        genres = []
        if genres_block:
            for g in genres_block.split("<Genre>")[1:]:
                genres.append(g.split("</Genre>")[0].strip())

        # Kommentare lesen
        kommentare_block = wert("Kommentare")
        kommentare = []
        if kommentare_block:
            for k in kommentare_block.split("<Kommentar>")[1:]:
                kommentare.append(k.split("</Kommentar>")[0].strip())

        # Bewertungen
        bewertungen_text = wert("Bewertungen")
        if bewertungen_text == "null" or bewertungen_text == "":
            bewertungen = None
        else:
            bewertungen = int(bewertungen_text)

        # Status
        status = FilmeStatus(wert("Status"))

        filme.append(
            Film(
                id=film_id,
                titel=titel,
                jahr=jahr,
                genres=genres,
                kommentare=kommentare,
                bewertungen=bewertungen,
                status=status,
            )
        )

    return filme
    

