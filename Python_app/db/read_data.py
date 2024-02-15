import sqlite3


def read_fit(table_name):
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute("select * from " + table_name)
    headers = cur.description
    headers = [items[0] for items in headers]
    # data = cur.fetchall()
    # print(cur.description)
    data = [dict(zip(headers, row)) for row in cur.fetchall()]
    conn.close()
    return data
