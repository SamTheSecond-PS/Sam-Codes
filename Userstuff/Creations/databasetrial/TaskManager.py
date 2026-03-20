import sqlite3 as sq, shlex as sh

conn = sq.connect("data.db")
cr = conn.cursor()
cr.execute("DROP TABLE IF EXISTS log")
cr.execute("CREATE TABLE log (id INTEGER, task TEXT, done INTEGER, priority INTEGER)")
conn.commit()

def add_task(id, name, priority=0, finish=0):
    cr.execute("INSERT INTO log VALUES (?, ?, ?, ?)", (id, name, finish, priority))
    conn.commit()


def finish_task(id):
    for line in cr.execute("SELECT * FROM log WHERE done = 0"):
        cr.execute("UPDATE log SET done = 1 WHERE id = ?", (id))
        conn.commit()


def list_task():
    fx = cr.execute("SELECT id, task, done, priority FROM log").fetchall()  # list of rows

    
    tasks = [{"id": r[0], "task": r[1], "done": r[2], "priority": r[3]} for r in fx]

    
    tasks_sorted = sorted(tasks, key=lambda x: x["priority"], reverse=True)

   
    for i, task in enumerate(tasks_sorted, start=1):
        print(i, task["task"], task["priority"])

    conn.commit()


def delete_task(id):
    cr.execute("DELETE FROM log WHERE id = ?", (id))
    conn.commit()


while True:
    c = input(">>")
    spl =  sh.split(c)
    if not spl:
        continue
    elif spl[0] == "list":
        list_task()
    elif spl[0] == "add":
        if not spl[4] and spl[3]:
            add_task(spl[1], spl[2])
        elif spl[3]:
            if spl[4]:
                add_task(spl[1], spl[2], int(spl[3]), int(spl[4]))
            else:
                add_task(spl[1], spl[2], int(spl[3]))
        else:
            add_task(spl[1], spl[2])

    elif spl[0] == "finish":
        if spl[1]:
            finish_task(spl[1])
        else:
            print("Enter a id")
    
    elif spl[0] == "del":
        if isinstance(spl[1], int):
            delete_task(spl[1])
    
    else:
        print("!(known)")

    


    

    
                
