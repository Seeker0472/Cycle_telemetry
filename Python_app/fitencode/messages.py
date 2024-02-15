from struct import pack
from typing import Tuple

from sqlalchemy import null

from fitencode import fields

MESSAGE_DATA = 0
MESSAGE_DEFINITION = 0x40


class Message:
    mesg_num = 0
    local_mesg_num = 0

    # filter 函数会遍历类的所有属性和方法，但只返回那些值是 fields.Field 类实例的属性。
    @property
    def fields(self) -> Tuple[fields.Field]:
        return tuple(
            filter(lambda t: isinstance(t[1], fields.Field),
                   self.__class__.__dict__.items()))

    @property
    def definition(self) -> bytes:
        fields_ = tuple(map(lambda kv: kv[1].definition, self.fields))
        reserved = 0
        is_big_endian = 1
        header = pack('>BBBHB',
                      MESSAGE_DEFINITION | self.local_mesg_num,
                      reserved, is_big_endian, self.mesg_num, len(fields_))
        return header + b''.join(fields_)

    def pack(self, **kwargs) -> bytes:
        contents = list()
        for name, field in self.fields:
            if name not in kwargs.keys():
                # contents.append(field.pack(null))
                raise Exception(f'unknown data field: {name}')
            # print(name)
            contents.append(field.pack(kwargs[name]))
        header = pack('>B', MESSAGE_DATA | self.local_mesg_num)
        return header + b''.join(contents)


class FileId(Message):
    mesg_num = 0

    type = fields.FileField(field_def=0)
    manufacturer = fields.Uint16Field(field_def=1)
    product = fields.Uint16Field(field_def=2)
    serial_number = fields.Uint32zField(field_def=3)
    time_created = fields.DateTimeField(field_def=4)
    number = fields.Uint16Field(field_def=5)
    product_name = fields.StringField(field_def=8, size=20)


class Lap(Message):
    mesg_num = 19

    timestamp = fields.DateTimeField(field_def=253)
    event = fields.EventField(field_def=0)
    event_type = fields.EventTypeField(field_def=1)
    start_time = fields.DateTimeField(field_def=2)
    start_position_lat = fields.Sint32Field(field_def=3)
    start_position_long = fields.Sint32Field(field_def=4)
    total_elapsed_time = fields.Uint32Field(field_def=7)
    total_timer_time = fields.Uint32Field(field_def=8)
    total_distance = fields.Uint32Field(field_def=9)
    total_calories = fields.Uint16Field(field_def=11)
    avg_speed = fields.Uint16Field(field_def=13)
    max_speed = fields.Uint16Field(field_def=14)
    avg_heart_rate = fields.Uint8Field(field_def=15)
    max_heart_rate = fields.Uint8Field(field_def=16)
    avg_cadence = fields.Uint8Field(field_def=17)
    max_cadence = fields.Uint8Field(field_def=18)
    avg_power = fields.Uint16Field(field_def=19)
    max_power = fields.Uint16Field(field_def=20)
    total_ascent = fields.Uint16Field(field_def=21)
    total_descent = fields.Uint16Field(field_def=22)
    sport = fields.SportField(field_def=25)
    normalized_power = fields.Uint16Field(field_def=33)
    left_right_balance = fields.LeftRightBalanceField(field_def=34)
    sub_sport = fields.SubSportField(field_def=39)
    avg_altitude = fields.Uint16Field(field_def=42)
    max_altitude = fields.Uint16Field(field_def=43)
    avg_grade = fields.Sint16Field(field_def=45)
    avg_pos_grade = fields.Sint16Field(field_def=46)
    avg_neg_grade = fields.Sint16Field(field_def=47)
    max_pos_grade = fields.Sint16Field(field_def=48)
    max_neg_grade = fields.Sint16Field(field_def=49)
    avg_temperature = fields.Sint8Field(field_def=50)
    max_temperature = fields.Sint8Field(field_def=51)
    total_moving_time = fields.Uint32Field(field_def=52)
    min_altitude = fields.Uint16Field(field_def=62)
    min_heart_rate = fields.Uint8Field(field_def=63)
    enhanced_avg_speed = fields.Uint32Field(field_def=110)
    enhanced_max_speed = fields.Uint32Field(field_def=111)
    enhanced_avg_altitude = fields.Uint32Field(field_def=112)
    enhanced_min_altitude = fields.Uint32Field(field_def=113)
    enhanced_max_altitude = fields.Uint32Field(field_def=114)


class Record(Message):
    mesg_num = 20

    timestamp = fields.DateTimeField(field_def=253)
    position_lat = fields.Sint32Field(field_def=0)
    position_long = fields.Sint32Field(field_def=1)
    altitude = fields.Uint16Field(field_def=2)
    enhanced_altitude = fields.Uint16Field(field_def=78)
    heart_rate = fields.Uint8Field(field_def=3)
    cadence = fields.Uint8Field(field_def=4)
    distance = fields.Uint32Field(field_def=5)
    speed = fields.Uint16Field(field_def=6)
    enhanced_speed = fields.Uint16Field(field_def=73)
    power = fields.Uint16Field(field_def=7)
    # compressed_speed_distance = fields.ByteField(field_def=8, size=3)
    grade = fields.Sint16Field(field_def=9)
    temperature = fields.Sint8Field(field_def=13)
    gps_accuracy = fields.Uint8Field(field_def=31)
    # calories = fields.Uint16Field(field_def=33)
    absolute_pressure = fields.Uint32Field(field_def=91)
    # The remaining 10 to 120 fields can be added by those who need them.


# class SegmentLap(Message):
#     mesg_num = 142
#
#     message_index = fields.MessageIndexField(field_def=254)
#     timestamp = fields.DateTimeField(field_def=253)
#     event = fields.EventField(field_def=0)
#     event_type = fields.EventTypeField(field_def=1)
#     start_time = fields.DateTimeField(field_def=2)
#     start_position_lat = fields.Sint32Field(field_def=3)
#     start_position_long = fields.Sint32Field(field_def=4)
#     end_position_lat = fields.Sint32Field(field_def=5)
#     end_position_long = fields.Sint32Field(field_def=6)
#     total_elapsed_time = fields.Uint32Field(field_def=7)
#     total_timer_time = fields.Uint32Field(field_def=8)
#     total_distance = fields.Uint32Field(field_def=9)
#     # The remaining 10 to 90 fields can be added by those who need them.
#     name = fields.StringField(field_def=29, size=16)
#

# class TimestampCorrelation(Message):
#     mesg_num = 162
#
#     timestamp = fields.DateTimeField(field_def=253)
#     fractional_timestamp = fields.Uint16Field(field_def=0)
#     system_timestamp = fields.DateTimeField(field_def=1)
#     fractional_system_timestamp = fields.Uint16Field(field_def=2)
#     local_timestamp = fields.LocalDateTimeField(field_def=3)
#     timestamp_ms = fields.Uint16Field(field_def=4)
#     system_timestamp_ms = fields.Uint16Field(field_def=5)


class Session(Message):
    mesg_num = 18

    timestamp = fields.DateTimeField(field_def=253)
    event = fields.EventField(field_def=0)
    event_type = fields.EventTypeField(field_def=1)
    start_time = fields.DateTimeField(field_def=2)
    start_position_lat = fields.Sint32Field(field_def=3)
    start_position_long = fields.Sint32Field(field_def=4)
    sport = fields.SportField(field_def=5)
    sub_sport = fields.SubSportField(field_def=6)
    total_elapsed_time = fields.Uint32Field(field_def=7)
    total_timer_time = fields.Uint32Field(field_def=8)
    total_distance = fields.Uint32Field(field_def=9)
    total_calories = fields.Uint16Field(field_def=11)
    avg_speed = fields.Uint16Field(field_def=14)
    max_speed = fields.Uint16Field(field_def=15)
    avg_heart_rate = fields.Uint8Field(field_def=16)
    max_heart_rate = fields.Uint8Field(field_def=17)
    avg_cadence = fields.Uint8Field(field_def=18)
    max_cadence = fields.Uint8Field(field_def=19)
    avg_power = fields.Uint16Field(field_def=20)
    max_power = fields.Uint16Field(field_def=21)
    total_ascent = fields.Uint16Field(field_def=22)
    total_descent = fields.Uint16Field(field_def=23)
    num_laps = fields.Uint16Field(field_def=26)
    normalized_power = fields.Uint16Field(field_def=34)
    training_stress_score = fields.Uint16Field(field_def=35)
    intensity_factor = fields.Uint16Field(field_def=36)
    left_right_balance = fields.LeftRightBalanceField(field_def=37)
    avg_altitude = fields.Uint16Field(field_def=49)
    max_altitude = fields.Uint16Field(field_def=50)
    avg_grade = fields.Sint16Field(field_def=52)
    avg_pos_grade = fields.Sint16Field(field_def=53)
    avg_neg_grade = fields.Sint16Field(field_def=54)
    max_pos_grade = fields.Sint16Field(field_def=55)
    max_neg_grade = fields.Sint16Field(field_def=56)
    avg_temperature = fields.Sint8Field(field_def=57)
    max_temperature = fields.Sint8Field(field_def=58)
    total_moving_time = fields.Uint32Field(field_def=59)
    min_heart_rate = fields.Uint8Field(field_def=64)
    min_altitude = fields.Uint16Field(field_def=71)
    enhanced_avg_speed = fields.Uint32Field(field_def=124)
    enhanced_max_speed = fields.Uint32Field(field_def=125)
    enhanced_avg_altitude = fields.Uint32Field(field_def=126)
    enhanced_min_altitude = fields.Uint32Field(field_def=127)
    enhanced_max_altitude = fields.Uint32Field(field_def=128)


class Activity(Message):
    mesg_num = 34
    timestamp = fields.DateTimeField(field_def=253)  ## True?
    total_timer_time = fields.Uint32Field(field_def=0)
    num_sessions = fields.Uint16Field(field_def=1)
    type = fields.EnumField(field_def=2)
    event = fields.EnumField(field_def=3)
    event_type = fields.EnumField(field_def=4)
    local_timestamp = fields.LocalDateTimeField(field_def=5)
    event_group = fields.Uint8Field(field_def=6)
