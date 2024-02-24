from sqlalchemy import null

from fitencode import FitEncode, messages
from datetime import datetime
from math import floor
from db import read_data


def create_fit(data, path="./cache/activity.fit"):
    # data = read_data.read_fit(table_name)
    with open(path, 'bw') as f:
        fit = FitEncode(buffer=f)
        file_id = messages.FileId()
        fit.add_definition(file_id)
        ts0 = floor(datetime.strptime(data[0]["timestamp"], '%Y-%m-%dT%H:%M:%SZ').timestamp() - 631065600)
        # 确定好number是什么!
        fit.add_record(
            file_id.pack(manufacturer=292, type=0x04, product=20,
                         serial_number=1001, time_created=ts0, number=6084, product_name="NAV 1"))

        # Add the definition of the local message to be used
        # timestamp = LocalTimestampCorrelation()
        record = messages.Record()
        lap = messages.Lap()
        session = messages.Session()
        activity = messages.Activity()
        # fit.add_definition(timestamp)
        fit.add_definition(record)

        statistics = {"heart_rate": {"max": 0, "min": 0, "avg": 0}, "altitude": {"max": 0, "min": 0, "avg": 0},
                      "enhanced_altitude": {"max": 0, "min": 0, "avg": 0}, "cadence": {"max": 0, "avg": 0},
                      "speed": {"max": 0, "avg": 0}, "enhanced_speed": {"max": 0, "avg": 0},
                      "power": {"max": 0, "avg": 0}, "temperature": {"max": 0, "avg": 0},
                      "pos_grade": {"max": 0, "avg": 0, "count": 0}, "neg_grade": {"max": 0, "avg": 0, "count": 0},
                      "grade": {"avg": 0}, "total_distance": 0, "total_ascent": 0, "total_descent": 0}
        statistics["altitude"]["max"] = statistics["altitude"]["min"] = statistics["altitude"]["avg"] = data[0][
            "altitude"]
        statistics["enhanced_altitude"]["max"] = statistics["enhanced_altitude"]["min"] = \
            statistics["enhanced_altitude"]["avg"] = data[0]["enhanced_altitude"]
        statistics["cadence"]["max"] = statistics["cadence"]["avg"] = data[0]["cadence"]
        statistics["speed"]["max"] = statistics["speed"]["avg"] = data[0]["speed"]
        statistics["enhanced_speed"]["max"] = statistics["enhanced_speed"]["avg"] = data[0]["enhanced_speed"]
        statistics["power"]["max"] = statistics["power"]["avg"] = data[0]["power"]
        statistics["temperature"]["max"] = statistics["temperature"]["avg"] = data[0]["temperature"]
        statistics["pos_grade"]["max"] = statistics["pos_grade"]["avg"] = statistics["pos_grade"]["count"] = 0
        statistics["neg_grade"]["max"] = statistics["neg_grade"]["avg"] = statistics["neg_grade"]["count"] = 0
        statistics["grade"]["avg"] = data[0]["grade"]
        statistics["total_distance"] = 0
        statistics["total_ascent"] = 0
        statistics["total_descent"] = 0

        # Adding a 'Lap 1' data records
        for records, prev in zip(data, data[1:]):
            fit.add_record(
                record.pack(timestamp=floor(datetime.strptime(records["timestamp"],
                                                              '%Y-%m-%dT%H:%M:%SZ').timestamp() - 631065600),
                            position_lat=records['position_lat'],
                            position_long=records['position_long'], altitude=(records['altitude'] * 5 + 500),
                            enhanced_altitude=(records['enhanced_altitude'] * 5 + 500),
                            heart_rate=records['heart_rate'],
                            cadence=records['cadence'], distance=int(records['distance'] * 100),
                            speed=int(records['speed'] * 1000), enhanced_speed=int(records['enhanced_speed'] * 1000),
                            power=records['power'], grade=int(records['grade'] * 100),
                            temperature=records['temperature'], gps_accuracy=records['gps_accuracy'],
                            absolute_pressure=records['absolute_pressure'])
            )
            if records['altitude'] > statistics["altitude"]["max"]:
                statistics["altitude"]["max"] = records['altitude']
            if records['altitude'] < statistics["altitude"]["min"]:
                statistics["altitude"]["min"] = records['altitude']
            statistics["altitude"]["avg"] += records['altitude']
            if records['enhanced_altitude'] > statistics["enhanced_altitude"]["max"]:
                statistics["enhanced_altitude"]["max"] = records['enhanced_altitude']
            if records['enhanced_altitude'] < statistics["enhanced_altitude"]["min"]:
                statistics["enhanced_altitude"]["min"] = records['enhanced_altitude']
            statistics["enhanced_altitude"]["avg"] += records['enhanced_altitude']
            if records['cadence'] > statistics["cadence"]["max"]:
                statistics["cadence"]["max"] = records['cadence']
            statistics["cadence"]["avg"] += records['cadence']
            if records['speed'] > statistics["speed"]["max"]:
                statistics["speed"]["max"] = records['speed']
            statistics["speed"]["avg"] += records['speed']
            if records['enhanced_speed'] > statistics["enhanced_speed"]["max"]:
                statistics["enhanced_speed"]["max"] = records['enhanced_speed']
            statistics["enhanced_speed"]["avg"] += records['enhanced_speed']
            if records['power'] > statistics["power"]["max"]:
                statistics["power"]["max"] = records['power']
            statistics["power"]["avg"] += records['power']
            if records['temperature'] > statistics["temperature"]["max"]:
                statistics["temperature"]["max"] = records['temperature']
            statistics["temperature"]["avg"] += records['temperature']
            statistics["grade"]["avg"] += records['grade']
            statistics["total_distance"] += records['distance']
            if records['grade'] > 0:
                statistics["pos_grade"]["avg"] += records['grade']
                statistics["pos_grade"]["max"] = records['grade'] if records['grade'] > statistics["pos_grade"][
                    "max"] else statistics["pos_grade"]["max"]
                statistics["pos_grade"]["count"] += 1
            if records['grade'] < 0:
                statistics["neg_grade"]["avg"] += records['grade']
                statistics["neg_grade"]["max"] = records['grade'] if records['grade'] < statistics["neg_grade"][
                    "max"] else statistics["neg_grade"]["max"]
                statistics["neg_grade"]["count"] += 1
            statistics["total_ascent"] += records['altitude'] - prev['altitude'] if records['altitude'] - prev[
                'altitude'] > 0 else 0
            statistics["total_descent"] += prev['altitude'] - records['altitude'] if prev['altitude'] - records[
                'altitude'] > 0 else 0

        statistics["altitude"]["avg"] = statistics["altitude"]["avg"] / len(data)
        statistics["enhanced_altitude"]["avg"] = statistics["enhanced_altitude"]["avg"] / len(data)
        statistics["cadence"]["avg"] = statistics["cadence"]["avg"] / len(data)
        statistics["speed"]["avg"] = statistics["speed"]["avg"] / len(data)
        statistics["enhanced_speed"]["avg"] = statistics["enhanced_speed"]["avg"] / len(data)
        statistics["power"]["avg"] = statistics["power"]["avg"] / len(data)
        statistics["temperature"]["avg"] = statistics["temperature"]["avg"] / len(data)
        statistics["grade"]["avg"] = statistics["grade"]["avg"] / len(data)
        statistics["pos_grade"]["avg"] = statistics["pos_grade"]["avg"] / statistics["pos_grade"]["count"]
        statistics["neg_grade"]["avg"] = statistics["neg_grade"]["avg"] / statistics["neg_grade"]["count"]

        fit.add_definition(lap)

        ts1 = floor(datetime.strptime(data[len(data) - 1]["timestamp"], '%Y-%m-%dT%H:%M:%SZ').timestamp() - 631065600)
        fit.add_record(
            lap.pack(
                timestamp=ts1,
                event=9,
                event_type=1,
                start_time=ts0,
                start_position_lat=data[0]['position_lat'],
                start_position_long=data[0]['position_long'],
                total_elapsed_time=ts1 - ts0,
                total_timer_time=ts1 - ts0,
                total_distance=int(data[len(data) - 1]['distance'] * 100),
                total_calories=len(data),
                avg_speed=int(statistics["speed"]["avg"] * 1000),
                max_speed=int(statistics["speed"]["max"] * 1000),
                avg_heart_rate=statistics["heart_rate"]["avg"],
                max_heart_rate=statistics["heart_rate"]["max"],
                avg_cadence=int(statistics["cadence"]["avg"]),
                max_cadence=int(statistics["cadence"]["max"]),
                avg_power=int(statistics["power"]["avg"]),
                max_power=statistics["power"]["max"],
                total_ascent=statistics["total_ascent"],
                total_descent=statistics["total_descent"],
                sport=2,
                normalized_power=0,
                left_right_balance=0,
                sub_sport=7,
                avg_altitude=int(statistics["altitude"]["avg"] * 5 + 500),
                max_altitude=int(statistics["altitude"]["max"] * 5 + 500),
                avg_grade=int(statistics["grade"]["avg"] * 100),
                avg_pos_grade=int(statistics["pos_grade"]["avg"] * 100),
                avg_neg_grade=int(statistics["neg_grade"]["avg"] * 100),
                max_pos_grade=int(statistics["pos_grade"]["max"] * 100),
                max_neg_grade=int(statistics["neg_grade"]["max"] * 100),
                avg_temperature=int(statistics["temperature"]["avg"]),
                max_temperature=statistics["temperature"]["max"],
                total_moving_time=ts1 - ts0,
                min_altitude=int(statistics["altitude"]["min"] * 5 + 500),
                min_heart_rate=statistics["heart_rate"]["min"],
                enhanced_avg_speed=int(statistics["enhanced_speed"]["avg"] * 1000),
                enhanced_max_speed=int(statistics["enhanced_speed"]["max"] * 1000),
                enhanced_avg_altitude=int(statistics["enhanced_altitude"]["avg"] * 5 + 500),
                enhanced_min_altitude=int(statistics["enhanced_altitude"]["min"] * 5 + 500),
                enhanced_max_altitude=int(statistics["enhanced_altitude"]["max"] * 5 + 500)

            )
        )
        fit.add_definition(session)

        fit.add_record(
            session.pack(
                timestamp=ts1,
                event=8,
                event_type=1,
                start_time=ts0,
                start_position_lat=data[0]['position_lat'],
                start_position_long=data[0]['position_long'],
                sport=2,
                sub_sport=7,
                total_elapsed_time=ts1 - ts0,
                total_timer_time=ts1 - ts0,
                total_distance=int(data[len(data) - 1]['distance'] * 100),
                total_calories=len(data),
                avg_speed=int(statistics["speed"]["avg"] * 1000),
                max_speed=int(statistics["speed"]["max"] * 1000),
                avg_heart_rate=statistics["heart_rate"]["avg"],
                max_heart_rate=statistics["heart_rate"]["max"],
                avg_cadence=int(statistics["cadence"]["avg"]),
                max_cadence=int(statistics["cadence"]["max"]),
                avg_power=int(statistics["power"]["avg"]),
                max_power=statistics["power"]["max"],
                total_ascent=statistics["total_ascent"],
                total_descent=statistics["total_descent"],
                num_laps=1,
                normalized_power=0,
                training_stress_score=0,
                intensity_factor=0,
                left_right_balance=0,
                avg_altitude=int(statistics["altitude"]["avg"] * 5 + 500),
                max_altitude=int(statistics["altitude"]["max"] * 5 + 500),
                avg_grade=int(statistics["grade"]["avg"] * 100),
                avg_pos_grade=int(statistics["pos_grade"]["avg"] * 100),
                avg_neg_grade=int(statistics["neg_grade"]["avg"] * 100),
                max_pos_grade=int(statistics["pos_grade"]["max"] * 100),
                max_neg_grade=int(statistics["neg_grade"]["max"] * 100),
                avg_temperature=int(statistics["temperature"]["avg"]),
                max_temperature=statistics["temperature"]["max"],
                total_moving_time=ts1 - ts0,
                min_heart_rate=statistics["heart_rate"]["min"],
                min_altitude=int(statistics["altitude"]["min"] * 5 + 500),
                enhanced_avg_speed=int(statistics["enhanced_speed"]["avg"] * 1000),
                enhanced_max_speed=int(statistics["enhanced_speed"]["max"] * 1000),
                enhanced_avg_altitude=int(statistics["enhanced_altitude"]["avg"] * 5 + 500),
                enhanced_min_altitude=int(statistics["enhanced_altitude"]["min"] * 5 + 500),
                enhanced_max_altitude=int(statistics["enhanced_altitude"]["max"] * 5 + 500),

            ))
        fit.add_definition(activity)
        fit.add_record(activity.pack(
            timestamp=ts1,
            total_timer_time=ts1 - ts0,
            num_sessions=1,
            type=0,
            event=26,
            event_type=9,
            local_timestamp=ts1,
            event_group=0,
        ))

        fit.finish()
