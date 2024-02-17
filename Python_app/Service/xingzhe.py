from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import requests
import json
from db import add_info_db


def login(user_account, user_password):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    # 发送GET请求
    response = requests.get("https://www.imxingzhe.com/user/login", headers=headers)

    # 获取服务器返回的Cookie
    cookies = response.cookies

    rd = cookies.get("rd")
    session_id = cookies.get("sessionid")
    coo = {
        "rd": rd,
        "sessionid": session_id,
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'rd': rd,
    }
    print(rd)
    result = response.content.decode("utf-8")
    s = BeautifulSoup(result, 'html.parser')
    public_key = str(s.find(id="pubkey").contents[0])
    print(public_key)

    safe_password_encrypted = encode_password(public_key, rd, user_password)

    # 创建登录数据字典
    login_data = {
        "account": user_account,
        "password": safe_password_encrypted,
        "source": "web"
    }

    # 发送登录请求
    # response = requests.post('https://www.imxingzhe.com/user/login', data=json.dumps(login_data), headers=headers,cookies=coo)

    response = requests.post('https://www.imxingzhe.com/api/v4/account/login', data=json.dumps(login_data),
                             headers=headers, cookies=coo)
    if response.status_code != 200:
        raise Exception("登录失败" + response.text)
    res_json = response.json()
    if res_json['res'] != 1:
        raise Exception("登录失败" + str(res_json))

    # for cookie in response.cookies:
    #     print(f"Name: {cookie.name}, Value: {cookie.value}")
    #
    stored_cookie = {
        "csrftoken": response.cookies.get("csrftoken"),
        "sessionid": response.cookies.get("sessionid"),
    }

    stored_others = {
        "enuid": res_json["data"]["enuid"],
        "userid": res_json["data"]["userid"],
    }

    add_info_db.add_account(platform=1, name=res_json["data"]["username"], account=user_account, password=user_password,
                            cookie=str(stored_cookie), others=str(stored_others), info="", comments="")

    # 打印响应体（或其他处理）
    print(response.text)
    return 'OK'


def encode_password(public_key, rd, user_password):
    # 拼接密码和随机数
    safe_password = user_password + ";" + rd

    # 创建RSA对象
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(safe_password.encode(encoding="utf-8")))  # 对密码字符串加密
    safe_password_encrypted = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return safe_password_encrypted


def get_activity_list(csrftoken, sessionid):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    cookies = {
        "csrftoken": csrftoken,
        "sessionid": sessionid,
    }
    response = requests.get("https://www.imxingzhe.com/api/v4/user_month_info/?user_id=6565670&year=2023&month=11",
                            headers=headers, cookies=cookies)
    print(response.text)
