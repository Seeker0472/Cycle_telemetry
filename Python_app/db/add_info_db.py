import sqlite3


def add_cut(name="新的剪辑", comments=""):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    cur.execute("insert into CUT (name, comments) values (?,?)", (name, comments))
    row_id = cur.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return row_id


def add_account(platform, name, account, password, cookie, others, info, comments):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    cur.execute("insert into Accounts (platform, name, account, password, cookie, others, info, comments)values (?,?,"
                "?,?,?,?,?,?)", (platform, name, account, password, cookie, others, info, comments))
    row_id = cur.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return row_id


def add_segments(cut_id, time_line_id, file_ids):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    for file_id in file_ids:
        cur.execute("insert into Segment (time_offset, start_offset, end_offset, file_id, CUT_id, row_id) values "
                    "(0,0,0,?,?,?);", (file_id,cut_id, time_line_id ))
    conn.commit()
    conn.close()
