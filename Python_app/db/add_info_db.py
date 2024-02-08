import sqlite3


def add_cut(name="新的剪辑", comments=""):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    cur.execute("insert into CUT (name, comments) values (?,?)", (name, comments))
    row_id = cur.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return row_id
