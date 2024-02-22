import json

from Service import mp4_gpx_extractor, fitphaser, fit, xingzhe
from db import read_data

# fitphaser.phase_fit("C:\\Users\\gmx47\\OneDrive\\桌面\\test\\te.fit", "TestFit")
#
# mp4_gpx_extractor.extract_mp4("C:\\Data\\100GOPRO\\GH030107.MP4", "testMp4")
#
# mp4_gpx_extractor.read_gpx('C:\\Data\\AAExample\\route1.gpx', "TestGpx")
#
# print(mp4_gpx_extractor.get_mp4_start_end("C:\\Data\\100GOPRO\\GH030107.MP4"))

# da = fit.create_fit("TABLE_0")
# print(da)

# import sqlite3
#
# conn = sqlite3.connect('data.sqlite')
# cur = conn.cursor()
# data=cur.execute("select * from TABLE_3").fetchall()
# print(data)

# xingzhe.get_activity_list()
#
import db.Project_page_db as ppdb

result=ppdb.get_all_info(2)
print(json.dumps(result))
print("done")
