import json
from pathlib import Path

prt = print
ask = input


data = Path("movies.json").read_text()
movies = json.loads(data)
prt(movies[0]["title"])

