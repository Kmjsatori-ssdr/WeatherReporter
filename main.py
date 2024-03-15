import requests
import tkinter
import json
import re

'''
一开始想要使用的免费API：
http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=
然后这个就寄了，接下来改为使用高德的免费API：
'''


def require_weather_data(city_name):
    url = "http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=" + city_name
    r = requests.get(url)
    r.encoding = "utf-8"
    dic = r.json()
    # 也可以写作：（但需要import json）
    # dic=json.loads(r.text)
    try:
        city = dic["city"]
        if city != city_name:
            raise Exception("CityNameError")
    except KeyError:
        print(f"发生了错误：{dic['errmsg']}")
        return None
    except Exception as e:
        print(f"出现了意料之外的错误：{e}呢")
        return None
    else:
        return dic


if __name__ == "__main__":
    # city_name=input("请输入你需要查询天气的城市名称：")
    city_name = "北京"
    dic=require_weather_data(city_name)
    print(dic)