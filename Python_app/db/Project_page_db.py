from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, TEXT, MetaData
from sqlalchemy.orm import sessionmaker
import datetime, json
from gps_phaser import coordTransform_utils as ctu

main = create_engine('sqlite:///main.sqlite', echo=True)
data = create_engine('sqlite:///data.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=main)
SessionData = sessionmaker(bind=data)
metadata = MetaData()
metadata.reflect(bind=data)

bind_info = None
segments = None


# Segment的类
class Segment(Base):
    __tablename__ = 'Segment'
    segment_id = Column(Integer, primary_key=True)
    time_offset = Column(Integer)
    start_offset = Column(Integer)
    end_offset = Column(Integer)
    file_id = Column(String)
    CUT_id = Column(Integer)
    row_id = Column(Integer)
    name = Column(String)
    time_start = Column(String)
    time_end = Column(String)

    # def __repr__(self):
    #     return (
    #         "<Segment(segment_id='%s', time_offset='%s', start_offset='%s', end_offset='%s', file_id='%s', "
    #         "CUT_id='%s', row_id='%s', name='%s', time_start='%s', time_end='%s')>") % (
    #         self.segment_id, self.time_offset, self.start_offset, self.end_offset, self.file_id, self.CUT_id,
    #         self.row_id, self.name, self.time_start, self.time_end)
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "segment_id": self.segment_id,
            "time_offset": self.time_offset,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
            "file_id": self.file_id,
            "CUT_id": self.CUT_id,
            "row_id": self.row_id,
            "name": self.name,
            "time_start": self.time_start,
            "time_end": self.time_end
        }


# Data_Bind的类
class DataBind(Base):
    __tablename__ = 'Data_Bind'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer)
    data_id = Column(Integer)
    heading_name = Column(String)
    CUT_id = Column(Integer)

    def __repr__(self):
        return (
            "<Data_Bind(id='%s', segment_id='%s', data_id='%s', head='%s', file_id='%s', CUT_id='%s', row_id='%s')>") % (
            self.id, self.segment_id, self.data_id, self.head, self.file_id, self.CUT_id, self.row_id)


# 用于初始化Project页面
def get_all_info(cutid):
    global bind_info, segments, data
    result = {}
    session = Session()
    session_data = SessionData()

    # 先查询这个cut有哪些Segments
    segments = session.query(Segment).from_statement(
        text(
            "select  segment_id, time_offset, start_offset, end_offset, FILE.file_id, CUT_id, row_id,name,time_start,time_end "
            " from Segment   join FILE on Segment.file_id = FILE.file_id and CUT_id= " + str(cutid))).all()
    # 获取cut的基本信息,和Segments一样来初始化TimeLine
    cutinfo = session.execute(
        text("SELECT Cur_pos,in_point,out_point FROM CUT WHERE cut_id = " + str(cutid))).fetchone()
    if cutinfo is None:
        raise Exception("No such cut id")
    if segments is None:
        raise Exception("No such cut id")
    # 封装
    result['TimeLine'] = {}
    result['TimeLine']['Cur_pos'] = cutinfo[0]  # datetime.datetime.strptime(cutinfo[0], '%Y-%m-%dT%H:%M:%SZ')
    current_pos = datetime.datetime.strptime(cutinfo[0], '%Y-%m-%dT%H:%M:%SZ')
    result['TimeLine']['in_point'] = cutinfo[1]  # in_point
    result['TimeLine']['out_point'] = cutinfo[2]  # out_point
    result['TimeLine']['segments'] = [item.to_dict() for item in segments]

    # 获取所有数据绑定的信息,并缓存在全局变量里面
    bind_info = bind = session.execute(
        text(
            "SELECT id,data_id,heading_name,S.file_id,name,time_start,time_end,S.start_offset,S.end_offset,time_offset, S.segment_id ,F.file_id "
            " FROM Data_Bind join main.Segment S on Data_Bind.segment_id = S.segment_id and cut_id = " + str(
                cutid) +
            " join FILE F on S.file_id = F.file_id")).fetchall()

    # 遍历所有数据,寻找需要在data.sqlite中查找哪张表
    result['DataBind'] = {}
    data_cache = {}
    for items in bind:  # dataid是绑定数据的类型(心率等)
        # 如果指定数据的时间范围包含当前时间,则查找数据
        if datetime.datetime.strptime(items[5], '%Y-%m-%dT%H:%M:%SZ').timestamp() + items[
            7] < current_pos.timestamp() - items[9] < datetime.datetime.strptime(items[6],
                                                                                 '%Y-%m-%dT%H:%M:%SZ').timestamp() - \
                items[8]:
            # 如果数据表不在缓存中,则查找数据并加入缓存
            if items[3] not in data_cache:
                data_cache[items[3]] = {}
                target_time = (current_pos - datetime.timedelta(seconds=items[9])).strftime('%Y-%m-%dT%H:%M:%SZ')
                obj = session_data.execute(text(
                    "SELECT * FROM " + items[
                        3] + " WHERE timestamp > '" + target_time + "' order by timestamp asc"))
                data_cache[items[3]]['data'] = obj.fetchone()
                data_cache[items[3]]['column_names'] = obj.keys()

            result['DataBind'][items[1]] = {
                'id': items[0],
                'segment_id': items[10],
                'heading_name': items[2],
                'file_name': items[4],
                # 'table_name': items[3],
                # 'time_start': items[5],
                # 'time_end': items[6],
                # 'start_offset': items[7],
                # 'end_offset': items[8],
                # 'time_offset': items[9],
                'data': data_cache[items[3]]['data'][list(data_cache[items[3]]['column_names']).index(items[2])],
            }
    result['Map'] = {}
    result['Map']['PointsList'] = {}

    # 获取所有的文件id
    files = set()
    for items in segments:
        files.add(items.file_id)
    for items in files:
        res = session_data.execute(
            text(
                "WITH NumberedRows AS (SELECT position_long,position_lat,ROW_NUMBER() OVER (ORDER BY timestamp ) AS rn FROM " + items + ")SELECT * FROM NumberedRows "
                                                                                                                                        "WHERE rn % 5 = 1")).fetchall()  # 这里跳过了一些数据,减轻前端的压力
        result['Map']['PointsList'][items] = [
            ctu.wgs84_to_bd09((180.0 / (2.0 ** 31.0)) * item[0], (180.0 / (2.0 ** 31.0)) * item[1]) for item in res]

    # 获取所有时间轴的当前位置信息
    result['Map']['Pos'] = []
    for items in segments:
        if datetime.datetime.strptime(items.time_start,
                                      '%Y-%m-%dT%H:%M:%SZ').timestamp() + items.start_offset < current_pos.timestamp() - items.time_offset < datetime.datetime.strptime(
            items.time_end,
            '%Y-%m-%dT%H:%M:%SZ').timestamp() - items.end_offset:
            target_time = (current_pos - datetime.timedelta(seconds=items.time_offset)).strftime('%Y-%m-%dT%H:%M:%SZ')
            info = session_data.execute(
                text("SELECT position_lat,position_long FROM " + items.file_id + " WHERE timestamp > '" + str(
                    target_time) + "' order by timestamp asc")).fetchone()
            result['Map']['Pos'].append({
                'segment_id': items.segment_id,
                'name': items.name,
                'position': [info[0], info[1]]
            })
    session.close()
    session_data.close()
    return result


def get_datasource(cut_id, time):
    session = Session()
    res = session.execute(text('select segment_id,name,record_data_name,F.file_id from Segment join main.FILE F'
                               ' on Segment.file_id = F.file_id and CUT_id= ' + str(cut_id) +
                               " where time_start < '" + time + "' and time_end > '" + time + "'")).fetchall()
    data = []
    for items in res:
        child_nodes = []
        child = items[2].split("&*&"),
        for item in child[0]:
            child_nodes.append({
                "name": item,
                "leaf": True,
                "value": str(items[0]) + '/' + item,
                "file_id": str(items[0]) + '/' + item,
            })
        data.append({
            # "segment_id": items[0],
            "name": items[1],
            "file_id": items[3],
            "children": child_nodes,
            "leaf": False,
        })
    session.close()
    print(data)
    return data


def update_cur_pos_time(cut_id, time):
    print(time)
    # time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    print(time)
    global bind_info
    session = Session()
    session.execute(text("update CUT set Cur_pos = '" + str(time) + "' where cut_id = '" + str(cut_id) + "'"))
    session.commit()
    result = {'DataBind': {}}
    data_cache = {}
    session_data = SessionData()
    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    for items in bind_info:  # dataid是绑定数据的类型(心率等)
        print(time.timestamp())

        # 如果指定数据的时间范围包含当前时间,则查找数据
        if datetime.datetime.strptime(items[5], '%Y-%m-%dT%H:%M:%SZ').timestamp() + items[
            7] < time.timestamp() - items[9] < datetime.datetime.strptime(items[6],
                                                                          '%Y-%m-%dT%H:%M:%SZ').timestamp() - \
                items[8]:
            # 如果数据表不在缓存中,则查找数据并加入缓存
            if items[3] not in data_cache:
                data_cache[items[3]] = {}
                target_time = (time - datetime.timedelta(seconds=items[9])).strftime('%Y-%m-%dT%H:%M:%SZ')
                obj = session_data.execute(text(
                    "SELECT * FROM " + items[
                        3] + " WHERE timestamp > '" + target_time + "' order by timestamp asc"))
                data_cache[items[3]]['data'] = obj.fetchone()
                data_cache[items[3]]['column_names'] = obj.keys()

            result['DataBind'][items[1]] = {
                'id': items[0],
                'segment_id': items[10],
                'heading_name': items[2],
                'file_name': items[4],
                'data': data_cache[items[3]]['data'][list(data_cache[items[3]]['column_names']).index(items[2])],
            }
    session.close()
    session_data.close()
    return result


def bind_data(segment_id, data_id, heading_name, time):
    # print(segment_id, data_id, heading_name, time)
    global bind_info
    session = Session()
    session.execute(text(
        "insert into Data_Bind(segment_id,data_id,heading_name) values('" + str(segment_id) + "','" + str(
            data_id) + "','" + heading_name + "')"))
    session.commit()
    cutid = session.execute(text("select CUT_id from Segment where segment_id = " + str(segment_id))).fetchone()[0]
    # 获取所有数据绑定的信息,并缓存在全局变量里面
    bind_info = session.execute(
        text(
            "SELECT id,data_id,heading_name,S.file_id,name,time_start,time_end,S.start_offset,S.end_offset,time_offset, S.segment_id ,F.file_id "
            " FROM Data_Bind join main.Segment S on Data_Bind.segment_id = S.segment_id and cut_id = " + str(
                cutid) +
            " join FILE F on S.file_id = F.file_id")).fetchall()
    session.close()
    return update_cur_pos_time(cutid, time)
