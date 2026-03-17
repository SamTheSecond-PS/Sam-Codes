import sqlite3 as sl
import random as rd
from datetime import datetime as dt


con = sl.connect("data.db")
cr = con.cursor() 

Texts = ["SAM HERE", "sam not here", "sam.is.alive", "fud tasty fr", "OVEN EXPLODED"]
br = [1, 0]

cr.execute("CREATE TABLE IF NOT EXISTS logs  (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, processed INTEGER, timestamp TEXT)")
x = 0
while x < 10:   
    cr.execute("INSERT INTO logs (message, processed, timestamp) VALUES (?, ?, ? )", (rd.choice(Texts), rd.choice(br), dt.now().isoformat()))
    con.commit()
    x += 1




