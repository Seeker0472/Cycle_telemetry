from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, TEXT, MetaData
from contextlib import ExitStack
from sqlalchemy.orm import sessionmaker
import datetime

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

    def __repr__(self):
        return ("<Segment(segment_id='%s', time_offset='%s', start_offset='%s', end_offset='%s', file_id='%s', "
                "CUT_id='%s', row_id='%s')>") % (
            self.segment_id, self.time_offset, self.start_offset, self.end_offset, self.file_id, self.CUT_id,
            self.row_id)

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
    with (ExitStack() as stack):
        # main_conn = stack.enter_context(main.connect())
        # data_conn = stack.enter_context(data.connect())
        # print(cutid)

        # 先查询这个cut有哪些Segments
        segments = session.query(Segment).from_statement(
            text("SELECT * FROM Segment  WHERE CUT_id = " + str(cutid))).all()
        # 获取cut的基本信息,和Segments一样来初始化TimeLine
        cutinfo = session.execute(
            text("SELECT Cur_pos,in_point,out_point FROM CUT WHERE cut_id = " + str(cutid))).fetchone()
        print(cutid)
        if cutinfo is None:
            raise Exception("No such cut id")
        if segments is None:
            raise Exception("No such cut id")
        # 封装
        result['TimeLine'] = {}
        result['TimeLine']['Cur_pos'] = current_pos = datetime.datetime.strptime(cutinfo[0], '%Y-%m-%dT%H:%M:%SZ')
        result['TimeLine']['in_point'] = cutinfo[1]
        result['TimeLine']['out_point'] = cutinfo[2]
        result['TimeLine']['segments'] = segments
        print(result)
        # bi = main_conn.execute(text("SELECT * FROM Data_Bind WHERE CUT_id = " + str(cutid))).fetchall()

        # 获取所有数据绑定的信息,并缓存在全局变量里面
        # TODO: 有关Python如何格式化TimeStamp,在导入的时候需要把信息格式化为一样的格式!!!!!
        bind_info = bind = session.execute(
            text(
                "SELECT id,data_id,heading_name,S.file_id,name,time_start,time_end,S.start_offset,S.end_offset,time_offset, S.segment_id ,F.file_id "
                " FROM Data_Bind join main.Segment S on Data_Bind.segment_id = S.segment_id and cut_id = " + str(
                    cutid) +
                " join FILE F on S.file_id = F.file_id")).fetchall()

        # 遍历所有数据,寻找需要在data.sqlite中查找哪张表
        result['DataBind'] = {}
        all_data = set()
        for items in bind:
            if datetime.datetime.strptime(items[5], '%Y-%m-%dT%H:%M:%SZ') + items[7] < current_pos - items[9] < datetime.datetime.strptime(items[6], '%Y-%m-%dT%H:%M:%SZ') - items[8]:
                all_data.add(items[1])
                result['DataBind'][items[1]] = {
                    'id': items[0],
                    'segment_id': items[10],
                    'heading_name': items[2],
                    'file_name': items[4],
                    # 'time_start': items[5],
                    # 'time_end': items[6],
                    # 'start_offset': items[7],
                    # 'end_offset': items[8],
                    # 'time_offset': items[9],
                    'data': None,
                }
        # 查找表,并封装数据
        for items in all_data:
            target_time = current_pos - items[9]
            obj = session_data.execute(
                text("SELECT * FROM " + str(items[4]) + " WHERE timestamp >" + str(
                    target_time) + 'order by timestamp asc'))
            column_names = obj.keys()
            data_now = obj.fetchone()
            # 将每一行转换为字典，其中键是列名
            datas = dict(zip(column_names, data_now))

            result['DataBind'][items]['data'] = data

        print(bind)
