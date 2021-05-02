import urllib.parse
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
titles = ["觀測時間(day)", "測站氣壓(hPa)", "海平面氣壓(hPa)", "測站最高氣壓(hPa)", "測站最高氣壓時間(LST)", "測站最低氣壓(hPa)", "測站最低氣壓時間(LST)", "氣溫(C)", "最高氣溫(C)", "最高氣溫時間(LST)",	"最低氣溫(C)", "最低氣溫時間(LST)", "露點溫度(℃)", "相對溼度(%)", "最小相對溼度(%)", "最小相對溼度時間(LST)", "風速(m/s)", "風向(360degree)",
          "最大陣風(m/s)", "最大陣風風向(360degree)", "最大陣風風速時間(LST)", "降水量(mm)", "降水時數(hour)", "最大十分鐘降水量(mm)", "最大十分鐘降水量起始時間(LST)", "最大六十分鐘降水量(mm)", "最大六十分鐘降水量起始時間(LST)", "日照時數(hour)", "日照率(%)", "全天空日射量(MJ/M^2)", "能見度(km)", "A型蒸發量(mm)", "日最高紫外線指數", "日最高紫外線指數時間(LST)", "總雲量(0~10)"]


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def crawler(targetURL, targetDay, city,  station_name, station_id):
    response = None
    while response is None:
        try:
            response = requests.get(targetURL)
        except Exception as e:
            print("連線錯誤", e)
            pass
    soup = BeautifulSoup(response.text, "html.parser")
    tr = soup.find('td', text=str(targetDay.day).zfill(2)).find_parent('tr')  # 找到目標日
    weather_features = {}
    tds = tr.findAll('td')
    # 目標日的所有天氣因子
    for i in range(len(tds)):
        if i == 0:
            weather_features[titles[i]] = int(tds[i].string)
        else:
            data = tds[i].string[:-1]
            # 日期
            if titles[i][-5:] == "(LST)" and is_number(data[:4]):
                data = datetime.strptime(data, "%Y-%m-%d %H:%M")
            # 數字
            elif is_number(data):
                data = float(data)
            # 空值
            else:
                data = None
            weather_features[titles[i]] = data
    return {"datas": weather_features, "城市": city, "站名": station_name, "站號": station_id}


def URL_Combiner(station_id, station_name, date):
    url = "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=replace1&stname=replace2&datepicker=replace3"
    url = url.replace("replace1", station_id)  # id
    encoded_text = urllib.parse.quote((urllib.parse.quote(station_name)))  # encode 2次
    url = url.replace("replace2", encoded_text)  # name
    target_month = date.strftime("%Y-%m")
    url = url.replace("replace3", target_month)  # date(ex: 2020-09)
    return url


if __name__ == "__main__":
    print("連線mongo")
    # '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
