import requests
import tkinter
import json
import re

'''
一开始想要使用的免费API：
http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=
然后这个就似了，接下来改为使用高德的免费API：
https://restapi.amap.com/v3/weather/weatherInfo?
'''


def require_weather_data(city):
    file = open("key.cfg", "r")
    key = file.read()
    file.close()
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}"
    r = requests.get(url)
    r.encoding = "utf-8"
    data = r.json()
    # 也可以写作：（但需要import json）
    # dic=json.loads(r.text)
    try:
        if data["status"] == "0":
            raise Exception["发生错误：天气数据返回失败！"]
        else:
            lives = dict(data["lives"][0])  # 将获得的json数据按规则转化为字典类型
    except Exception as e:
        print(e)
    else:
        return lives


if __name__ == "__main__":
    city_name=input("请输入你需要查询天气的城市名称：")
    weather_data = require_weather_data(city_name)
    print("当前{0}（省）{1}实时天气：{2}，气温{3}摄氏度，{4}风{5}级，空气湿度{6}%。更新时间：{7}。"
          .format(weather_data["province"], weather_data["city"], weather_data["weather"],
                  weather_data["temperature_float"], weather_data["winddirection"], weather_data["windpower"],
                  weather_data["humidity_float"], weather_data["reporttime"]))
