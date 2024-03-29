import requests
import tkinter as tk
from tkinter import messagebox

'''
一开始想要使用的免费API：
http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=43656176&appsecret=I42og6Lm&ext=&cityid=&city=
然后这个就似了，接下来改为使用高德的免费API：
https://restapi.amap.com/v3/weather/weatherInfo?
'''


def require_weather_data(city):
    with open("key.cfg", "r") as file:
        key = file.read().strip()  # 去除可能的换行符
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}"
    r = requests.get(url)
    r.encoding = "utf-8"
    data = r.json()
    # 也可以写作：（但需要import json）
    # dic=json.loads(r.text)
    try:
        # 检查HTTP响应状态码
        if r.status_code != 200:
            raise Exception(f"发生错误：请求天气数据失败，HTTP状态码 {r.status_code}")
        # 检查返回的数据中是否包含错误
        elif ("status" in data and data["status"] != "1") or data["count"]=="0":
            raise Exception("发生错误：天气数据返回失败！请检查输入城市名是否合法。")
    except Exception as e:
        return str(e)
    else:
        lives = dict(data["lives"][0])  # 将获得的json数据按规则转化为字典类型
        return lives


def main():
    root = tk.Tk()  # 创建一个主窗口
    root.title("WeatherReporter")  # 设置窗口标题
    root.geometry("640x480")  # 设置窗口大小

    label = tk.Label(root, text="请输入你需要查询天气的城市名称：\n（暂只支持中国大陆的城市及港澳）",font=('黑体',16))
    label.pack()

    entry = tk.Entry(root,font=('黑体',16))
    entry.pack()

    def on_button_click():
        city_name = entry.get()
        try:
            weather_data = require_weather_data(city_name)
            if isinstance(weather_data, str):
                raise Exception(weather_data)
            elif not weather_data:
                raise Exception("发生错误：天气数据返回失败！请不要输入数字。")
            else:
                message.config(text="{0}（省）{1}\n实时天气：{2}\n气温：{3}摄氏度\n{4}风{5}级\n相对湿度：{6}%\n更新时间：{7}"
                               .format(weather_data["province"], weather_data["city"], weather_data["weather"],
                                       weather_data["temperature"], weather_data["winddirection"],
                                       weather_data["windpower"],
                                       weather_data["humidity"], weather_data["reporttime"]))
        except Exception as e:
            messagebox.showerror("未知错误：", str(e))  # 使用messagebox显示错误

    button = tk.Button(root, text="确认", command=on_button_click,font=('黑体',12))
    button.pack()

    message = tk.Message(root,font=('黑体',24))
    message.pack()

    root.mainloop()  # 进入主循环


if __name__ == "__main__":
    main()