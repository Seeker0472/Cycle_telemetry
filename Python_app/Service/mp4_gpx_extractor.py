import gpmf
import numpy as np
from db import read_data_db
import gpxpy
import gpxpy.gpx
from dateutil import tz
from pymediainfo import MediaInfo


def extract_mp4(file_path, name, comments=""):
    # Read the binary stream from the file
    stream = gpmf.io.extract_gpmf_stream(file_path)
    # Extract GPS low level data from the stream
    gps_blocks = gpmf.gps.extract_gps_blocks(stream)
    # Parse low level data into more usable format
    gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
    data = []
    for row in gps_data:
        data.append((row.timestamp, round(np.mean(row.latitude), 7), round(np.mean(row.longitude), 7),
                     round(np.mean(row.altitude), 2),
                     round(np.mean(row.speed_2d), 2), round(np.mean(row.speed_3d), 2)))

    return read_data_db.store_mp4_data(data, file_path, name, comments)


def get_mp4_start_end(file_path, enforce=0):
    media_info = MediaInfo.parse(file_path)
    data = media_info.to_json()
    if media_info.video_tracks[0].title == 'GoPro AVC  ' or enforce != 0:
        startend = [media_info.other_tracks[0].time_code_of_first_frame,
                    media_info.other_tracks[0].time_code_of_last_frame]
    else:
        raise RuntimeError("MayBe Not GoPro RAW!")
    # print(data)
    return startend


def read_gpx(file_path, name,comments):
    gpx_file = open(file_path, 'r', encoding='utf-8')

    gpx = gpxpy.parse(gpx_file)

    tracks = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # 转化时间格式
                tracks.append((point.time.astimezone(tz.tzutc()).strftime('%Y-%m-%dT%H:%M:%SZ'), point.latitude,
                               point.longitude, point.elevation))
                # tracks.append((point.time, point.latitude, point.longitude, point.elevation))
                # print(f'Point at ({point.latitude},{point.longitude}) -> {point.elevation}')
    # 不存进数据库
    for waypoint in gpx.waypoints:
        print(f'waypoint {waypoint.name} -> ({waypoint.latitude},{waypoint.longitude})')

    for route in gpx.routes:
        print('Route:')
        for point in route.points:
            print(f'Point at ({point.latitude},{point.longitude}) -> {point.elevtion}')

    read_data_db.store_gpx_data(tracks, file_path, name,comments)
