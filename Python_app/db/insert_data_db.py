import sqlite3
import re


# def ins_data(data):
# tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(tables.fetchall())


def store_fit_data(data, path, name,comments):
    # con = sqlite3.connect("../data.sqlite")
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()

    # 调用create_table创建数据库并返回数据库的名字
    db_name = ""
    date_name = ""

    start_time = ""
    end_time = ""

    dict_names = []
    for row in data:
        if row['name'] == 'record':
            result = create_table(row)
            db_name = result[0]
            date_name = result[1]
            dict_names = row["fields"].keys()
            break
    # others是除了records的数据,record部分被{"name": "record"}替换
    others = []
    records = []
    units = ""
    for row in data:
        if row['name'] != 'record':
            others.append(row)
        else:
            if {"name": "record"} not in others:
                others.append({"name": "record"})
                # 第一次遇到record,把单位存进units里面
                for dict_name in dict_names:
                    units += (row["fields"][dict_name]["units"] if (row["fields"][dict_name]["units"]) else "") + "&*&"
                # 第一次(第一条)设置start
                print(row["fields"][date_name]["value"])
                start_time = row["fields"][date_name]["value"]
            # 每条设置end
            end_time = row["fields"][date_name]["value"]
            tup = ()
            for dict_name in dict_names:
                tup = tup + (row["fields"][dict_name]["value"],)

            records.append(tup)
    units = units[:-3]
    # 生成执行插入的语句,和部分插入信息
    # record_data_name指的是在该表每个字段对应的名字,用&*&分割
    # data_bind指的是字段的绑定信息,用&*&分割
    sql = "INSERT INTO " + db_name + " VALUES ("
    record_data_name = ""
    data_bind = ""
    for i in dict_names:
        sql += "?,"
        record_data_name += i + '&*&'
        # TODO: 这里要改!!!!把时间绑定数据!!!!
        data_bind += '0&*&'
    sql = sql[:-1]
    sql += ')'
    record_data_name = record_data_name[:-3]
    data_bind = data_bind[:-3]

    # print(others)
    cur.executemany(sql, records)
    con.commit()
    con.close()

    # con1 = sqlite3.connect("../main.sqlite")
    con1 = sqlite3.connect("main.sqlite")
    cur1 = con1.cursor()
    # 在当前表格中,record_name--数据库名称, record_data_name--数据项名, data_bind--数据绑定信息, other_messages--其他信息(备注等),
    # unit_transformed--是否变换单位(alpha), units--单位,type--类型, description--描述
    cur1.execute(
        "insert into FILE(file_id, record_data_name, data_bind, comments, units" +
        ", type,other_msg, time_start, time_end,file_path,name) " + " values(?,?,?,?,?,?,?,?,?,?,?)",
        (db_name, record_data_name, data_bind, comments, units, 1, str(others), start_time, end_time, path, name))
    con1.commit()
    con1.close()

    return db_name


def create_table(data):
    # con = sqlite3.connect("../data.sqlite")
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    max_id = find_max_id()
    date_name = ""
    # 生成建表语句
    dict_name = data["fields"].keys()
    db_type = {}
    # 确定对象的数据类型,存储于db_type中
    for name in dict_name:
        if isinstance(data["fields"][name]['value'], int):
            db_type[name] = 'INTEGER'
        if isinstance(data["fields"][name]['value'], float):
            db_type[name] = 'DECIMAL(36,2)'
        if isinstance(data["fields"][name]['value'], str):
            if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", data["fields"][name]['value']):
                # print("TIMR::" + name)
                db_type[name] = 'DATETIME'
                date_name = name
            else:
                db_type[name] = 'NVARCHAR(255)'
    sql = "CREATE TABLE TABLE_" + str(max_id + 1) + "("
    for key in dict_name:
        sql += key + ' ' + db_type[key]
        if db_type[key] == 'DATETIME':
            sql += " constraint" + " TABLE_" + str(max_id + 1) + "_pk primary key"
            sql += " NOT NULL"
        sql += ','
    sql = sql[:-1]
    sql += ')'
    # 建立存储数据表
    cur.execute(sql)
    con.commit()
    con.close()
    # 返回表名
    return ["TABLE_" + str(max_id + 1), date_name]


def find_max_id():
    # con = sqlite3.connect("../data.sqlite")
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    max_id = -1
    # 遍历数据库的所有表,寻找最大的ID
    for table_name in tables:
        table_name = table_name[0]
        if re.match("TABLE_[0-9]*", table_name):
            this_id = table_name.split("_", 1)
            if max_id < int(this_id[1]):
                max_id = int(this_id[1])
    return max_id


def store_mp4_data(data, path, name,comments, units="unitsUndefined"):
    # con = sqlite3.connect("../data.sqlite")
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    max_id = find_max_id()
    sql = "CREATE TABLE TABLE_" + str(max_id + 1) + "(" + \
          "timestamp DATETIME constraint TABLE_" + str(max_id + 1) + "_pk primary key NOT NULL," + \
          "latitude DECIMAL(36,30)," + \
          "longitude DECIMAL(36,30)," + \
          "altitude DECIMAL(10,2)," + \
          "TwoD_Speed DECIMAL(10,2)," + \
          "ThreeD_Speed DECIMAL(10,2))"
    cur.execute(sql)
    start_time = data[0][0]
    end_time = data[len(data) - 1][0]
    cur.executemany("INSERT INTO TABLE_" + str(max_id + 1) + " VALUES(?,?,?,?,?,?)", data)
    con.commit()
    con.close()

    # con1 = sqlite3.connect("../main.sqlite")
    con1 = sqlite3.connect("main.sqlite")
    cur1 = con1.cursor()
    # 在当前表格中,record_name--数据库名称, record_data_name--数据项名, data_bind--数据绑定信息, other_messages--其他信息(备注等),
    # unit_transformed--是否变换单位(alpha), units--单位,type--类型, description--描述
    cur1.execute(
        "insert into FILE (file_id, record_data_name, data_bind, comments, units" +
        ", type,other_msg, time_start, time_end,file_path,name) " + " values(?,?,?,?,?,?,?,?,?,?,?)",
        ("TABLE_" + str(max_id + 1), "timestamp&*&latitude&*&longitude&*&altitude&*&TwoD_Speed&*&ThreeD_Speed",
         "0&*&0&*&0&*&0&*&0&*&0", comments, units, 2, "", start_time, end_time, path, name))
    con1.commit()
    con1.close()
    return "TABLE_" + str(max_id + 1)


def store_gpx_data(data, path, name,comments, units="unitsUndefined"):
    # con = sqlite3.connect("../data.sqlite")
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    max_id = find_max_id()
    sql = "create TABLE TABLE_" + str(max_id + 1) + "(" + \
          "timestamp DATETIME constraint TABLE_X_pk primary key NOT NULL," + \
          "latitude DECIMAL(10,2)," + \
          "longitude DECIMAL(10,2)," + \
          "altitude DECIMAL(10,2))"
    cur.execute(sql)
    cur.executemany("INSERT INTO TABLE_" + str(max_id + 1) + " VALUES(?,?,?,?)", data)
    con.commit()
    con.close()

    start_time = data[0][0]
    end_time = data[len(data) - 1][0]

    # con1 = sqlite3.connect("../main.sqlite")
    con1 = sqlite3.connect("main.sqlite")
    cur1 = con1.cursor()
    # 在当前表格中,record_name--数据库名称, record_data_name--数据项名, data_bind--数据绑定信息, other_messages--其他信息(备注等),
    # unit_transformed--是否变换单位(alpha), units--单位,type--类型, description--描述
    cur1.execute(
        "insert into FILE (file_id, record_data_name, data_bind, comments, units" +
        ", type,other_msg, time_start, time_end,file_path,name) " + " values(?,?,?,?,?,?,?,?,?,?,?)",
        ("TABLE_" + str(max_id + 1), "timestamp&*&latitude&*&longitude&*&altitude",
         "0&*&0&*&0&*&0", comments, units, 3, "", start_time, end_time, path, name))
    con1.commit()
    con1.close()

    return "TABLE_" + str(max_id + 1)
