import sqlite3

import math


def all_cut_info(options):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    info = cur.execute("select cut_id, created_time, name, comments from CUT").fetchall()
    conn.close()
    data = []
    for row in info:
        data.append({
            'cut_id': row[0],
            'created_time': row[1],
            'name': row[2],
            'comments': row[3],
        })
    return data


def get_all_file(options):
    conn = sqlite3.connect('main.sqlite')
    cur = conn.cursor()
    sql = "select file_id, name, time_start, time_end, file_path, comments, type, edit_time, imported_time from FILE"
    sql1 = "select count(*) from FILE "
    print(options)
    if options["fliter"]:
        sql += " where type in("
        sql1 += " where type in("
        for item in options["fliter"]:
            match item:
                case 'FIT':
                    sql += '1,'
                    sql1 += '1,'
                case 'MP4':
                    sql += '2,'
                    sql1 += '2,'
                case 'GPX':
                    sql += '3,'
                    sql1 += '3,'
                case _:
                    pass
        sql = sql[:-1]
        sql += ')'
        sql1 = sql1[:-1]
        sql1 += ')'
    if options['order']:
        sql += " order by "
        match options["orderBy"]:
            case 'name':
                sql += 'name' + (' asc' if options['order'] == 'ascending' else ' desc')
            case 'ImportTime':
                sql += 'imported_time' + (' asc' if options['order'] == 'ascending' else ' desc')
            case 'EditTime':
                sql += 'edit_time' + (' asc' if options['order'] == 'ascending' else ' desc')
            case 'TimeStart':
                sql += 'time_start' + (' asc' if options['order'] == 'ascending' else ' desc')
            case 'TimeEnd':
                sql += 'time_end' + (' asc' if options['order'] == 'ascending' else ' desc')
    sql += ' limit ' + str((options['page'] - 1) * options["itemPerPage"]) + ',' + str(
        (options['page']) * options["itemPerPage"])
    info = cur.execute(sql).fetchall()
    # try:
    items_num = cur.execute(sql1).fetchall()[0][0]
    # except ValueError:
    #     items_num = 0
    # 莫名其妙的Bug
    pages = math.ceil(items_num / options["itemPerPage"])*10
    print(pages)
    conn.close()
    result = []
    for row in info:
        match row[6]:
            case 1:
                file_type = "FIT"
            case 2:
                file_type = "MP4"
            case 3:
                file_type = "GPX"
            case _:
                file_type = "Unknown"
        result.append({
            'file_id': row[0],
            'name': row[1],
            'TimeStart': row[2],
            'TimeEnd': row[3],
            'Path': row[4],
            'Comments': row[5],
            'Type': file_type,
            'EditTime': row[7],
            'ImportTime': row[8]
        })
    return {"pages": pages, "items": result}
