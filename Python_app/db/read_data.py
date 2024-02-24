import sqlite3
from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, TEXT, MetaData
from sqlalchemy.orm import sessionmaker

main = create_engine('sqlite:///main.sqlite', echo=False)
data = create_engine('sqlite:///data.sqlite', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=main)
SessionData = sessionmaker(bind=data)
metadata = MetaData()
metadata.reflect(bind=data)


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


# 读取一个cut的信息以供导出
def read_total_cut(cut_id):
    session = Session()
    session_data = SessionData()
    in_out = session.execute(text("select in_point,out_point from CUT where cut_id=" + str(cut_id))).fetchone()
    in_out = [in_out[0], in_out[1]]
    segments = session.execute(
        text("select  time_offset, start_offset, end_offset,time_start,time_end,F.file_id,segment_id"
             " from Segment join main.FILE F on Segment.file_id = F.file_id"
             " where cut_id = " + str(cut_id))).fetchall()
    now_pos = datetime.strptime(in_out[0], "%Y-%m-%dT%H:%M:%SZ")
    ret = []

    # data_cache = {}
    # data_cache_keys = {}
    # for segment in segments:
    #     if segment[5] not in data_cache:
    #         da = data.execute("select * from " + str(segment[5]))
    #         data_cache[segment[5]] = da.fetchall()
    #         data_cache_keys[segment[5]] = [items[0] for items in da.description]

    data_bind = session.execute(text("select segment_id, data_id, heading_name from Data_Bind where segment_id in "
                                     " (select segment_id from Segment where cut_id= " + str(cut_id) + ")")).fetchall()

    while now_pos < datetime.strptime(in_out[1], "%Y-%m-%dT%H:%M:%SZ"):
        data_frame = {"timestamp": now_pos.strftime("%Y-%m-%dT%H:%M:%SZ")}
        for segment in segments:
            if now_pos > datetime.strptime(segment[3], "%Y-%m-%dT%H:%M:%SZ") + timedelta(
                    microseconds=segment[0]) + timedelta(microseconds=segment[1]) and now_pos < datetime.strptime(
                segment[4], "%Y-%m-%dT%H:%M:%SZ") + timedelta(microseconds=segment[0]) - timedelta(
                microseconds=segment[2]):
                for bind in data_bind:
                    if bind[0] == segment[6]:
                        res = session_data.execute(text("select " + str(bind[2]) + " from " + str(segment[5]) +
                                                        " where timestamp > '" + (now_pos - timedelta(
                            microseconds=segment[0])).strftime("%Y-%m-%dT%H:%M:%SZ") + "'")).fetchone()
                        add_info(data_frame, bind[1], res[0])
        finish_frame(data_frame)
        ret.append(data_frame)

        now_pos += timedelta(seconds=1)
    return ret


def add_info(data_frame, data_bind, data_values):
    # print(data_frame, data_bind, data_values)
    match data_bind:
        case 1:
            data_frame["heart_rate"] = data_values
        case 2:
            data_frame["speed"] = data_values
            data_frame["enhanced_speed"] = data_values
        case 3:
            data_frame["cadence"] = data_values
        case 4:
            data_frame["power"] = data_values
        case 5:
            data_frame["grade"] = data_values
        case 6:
            data_frame["temperature"] = data_values
        case 7:
            data_frame["absolute_pressure"] = data_values
        case 8:
            data_frame["altitude"] = data_values
            data_frame["enhanced_altitude"] = data_values
        case 9:
            data_frame["position_lat"] = data_values
        case 10:
            data_frame["position_long"] = data_values
        case 11:
            data_frame["distance"] = data_values


def finish_frame(data_frame):
    if "heart_rate" not in data_frame:
        data_frame["heart_rate"] = 0
    if "speed" not in data_frame:
        data_frame["speed"] = 0
    if "cadence" not in data_frame:
        data_frame["cadence"] = 0
    if "power" not in data_frame:
        data_frame["power"] = 0
    if "grade" not in data_frame:
        data_frame["grade"] = 0
    if "temperature" not in data_frame:
        data_frame["temperature"] = 0
    if "absolute_pressure" not in data_frame:
        data_frame["absolute_pressure"] = 0
    if "altitude" not in data_frame:
        data_frame["altitude"] = 0
    if "position_lat" not in data_frame:
        data_frame["position_lat"] = 0
    if "position_long" not in data_frame:
        data_frame["position_long"] = 0
    if "distance" not in data_frame:
        data_frame["distance"] = 0
    if "enhanced_speed" not in data_frame:
        data_frame["enhanced_speed"] = 0
    if "enhanced_altitude" not in data_frame:
        data_frame["enhanced_altitude"] = 0
    if "gps_accuracy" not in data_frame:
        data_frame["gps_accuracy"] = 1
