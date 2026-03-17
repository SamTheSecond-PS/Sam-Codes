import sqlite3 as sl

con = sl.connect("data.db")
cr = con.cursor()
for row in cr.execute("SELECT * FROM logs WHERE PROCESSED = 0"):
    with open("forreader.txt", 'w') as f:
        ide, msg, proc, date = row
        proc = 1
        cr.execute("UPDATE logs SET processed = 1 WHERE id = ?", (ide))
        f.write(f"{ide} | {msg} | {proc} | {date}\n")
    row = (ide, msg, proc, date)
con.commit()



        