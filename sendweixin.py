import random
from time import localtime
from requests import get, post
from datetime import datetime, date
import sys
import os
import json
 
 
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
 
 
def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
 

def send_message(to_user, access_token, pafd):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "login_state": {
                "value": "{}".format(pafd["login_state"]),
                "color": get_color()
            },
            "last_date": {
                "value": "{}".format(pafd["last_date"]),
                "color": get_color()
            },
            "last_area": {
                "value": "{}".format(pafd["last_area"]),
                "color": get_color()
            },
            "last_address": {
                "value": "{}".format(pafd["last_address"]),
                "color": get_color()
            },
            "today_date": {
                "value": "{}".format(pafd["today_date"]),
                "color": get_color()
            },
            "submit_state": {
                "value": "{}".format(pafd["submit_state"]),
                "color": get_color()
            },
            "operate_state": {
                "value": "{}".format(pafd["operate_state"]),
                "color": get_color()
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)

 
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    try:
        with open("pafd.json",) as f:
            pafd = json.load(f)
    except FileNotFoundError:
        print("推送消息失败，请检查pafd.json文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, pafd)
    os.system("pause")