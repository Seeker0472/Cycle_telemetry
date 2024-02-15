import fitdecode
import datetime
from db import insert_data_db


def phase_fit(path,name,comments):
    print("开始处理FIT文件:" + path + "...")
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    fit_data = []
    # 读取FIT文件
    # 使用 with 语句来确保文件正确关闭
    with fitdecode.FitReader(path) as fit:
        # fit 是一个生成器，它会产生 FIT 文件中的记录
        for frame in fit:
            # 只处理数据记录（跳过文件头等）
            if isinstance(frame, fitdecode.records.FitDataMessage):
                recordData = {
                    "name": frame.name,
                    "fields": {}
                }
                # print(f"记录名: {frame.name}")
                for field in frame.fields:
                    if isinstance(field.value, datetime.datetime):
                        field.value = field.value.strftime(date_format)
                    recordData["fields"][field.name] = {
                        "value": field.value,
                        "units": field.units
                    }
                    # print(
                    #     f" - 字段名: {field.name},值类型: {type(field.value)}, 值: {field.value}, 单位: {field.units}")
                # print()
                fit_data.append(recordData)

    return insert_data_db.store_fit_data(fit_data, path, name,comments)

# for data in fit_data[1]["fields"]:
#     print(data)
#     print(data["value"])
#     print(data["units"])

# 将数据写入 JSON 文件
# fit_json = json.dumps(fit_data, indent=4)
# with open("C:/Users/gmx47/OneDrive/桌面/te.json", "w") as f:
#     f.write(fit_json)
