import sqlite3 as sql, json
from pathlib import Path


movies = json.loads(Path(Path("../JSONFiles/movies.json")).read_text())

with sql.connect("db.sqlite3") as conn:
    command = "SELECT * FROM Movies"
    CURSOR = conn.execute(command)
    for row in CURSOR:
        print(row)
    movies = CURSOR.fetchall()
    print(movies)