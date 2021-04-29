import requests
import json
from pymongo import MongoClient
from datetime import datetime
import time
def GetData():
    time_start = time.time()
    url3 = "https://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?sort=SiteName&offset=0&limit=1000"  # 政府資料開放平台的AQI
    Data3 = requests.get(url3)
    now_all = json.loads(Data3.text)

    # 區域PM2.5 forecast data
    url1 = "https://opendata.epa.gov.tw/api/v1/AQFN?%24skip=0&%24top=1000&%24format=json"
    Data1 = requests.get(url1)
    forecast_all = json.loads(Data1.text)
    County = ""
    SiteName = ""
    for i in range(len(now_all["result"]["records"])):

        forecast = []
        now = []
        try:
            now_value = int(now_all["result"]["records"][i]["AQI"])
        except:
            now_value = None
        now.append({"AQI": now_value, "Status": now_all["result"]["records"][i]["Status"], "PublishTime": datetime.strptime(now_all["result"]["records"][i]["PublishTime"].replace(
            "/", "-"), "%Y-%m-%d %H:%M:%S"), "Longitude": now_all["result"]["records"][i]["Longitude"], "Latitude": now_all["result"]["records"][i]["Latitude"]})

        County = now_all["result"]["records"][i]["County"]
        if County == "基隆市" or County == "臺北市" or County == "新北市" or County == "桃園市":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "北部":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "臺中市" or County == "彰化縣" or County == "南投縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "中部":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "雲林縣" or County == "嘉義縣" or County == "臺南市" or County == "嘉義市":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "雲嘉南":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "高雄市" or County == "屏東縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "高屏":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "花蓮縣" or County == "臺東縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "花東":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "新竹市" or County == "新竹縣" or County == "苗栗縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "竹苗":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "宜蘭縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "宜蘭":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "澎湖縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "澎湖":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "金門縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "金門":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        if County == "連江縣":
            for j in range(len(forecast_all)):
                forecast_date = datetime.strptime(
                    forecast_all[j]["ForecastDate"], "%Y-%m-%d")
                try:
                    forecast_value = int(forecast_all[j]["AQI"])
                except:
                    forecast_value = None
                if forecast_all[j]["Area"] == "馬祖":
                    forecast.append(
                        {"Area": forecast_all[j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
        city = {"SiteName": now_all["result"]["records"][i]["SiteName"],
                "County": now_all["result"]["records"][i]["County"], "now": now, "forecast": forecast}
        print(city)
        SiteName = now_all["result"]["records"][i]["SiteName"]
        County = now_all["result"]["records"][i]["County"]
        WriteData(city, SiteName, County)
        # file = 'PM2_5.json'
        # with open(file, 'w',encoding='utf8') as obj:
        #     json.dump(city, obj,ensure_ascii=False)#把結果寫入CWS.json檔
    time_end = time.time()
    print("爬取PM2_5要花", time_end-time_start, "s")

def WriteData(city, SiteName, County):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.PM2_5.update_one(
            {"SiteName": SiteName,"County":County},
            {"$set": {
                "update_Time": datetime.now(),
                "now": city["now"],
                "forecast": city["forecast"]
            }}, upsert=True

        )
        print("寫入成功")
    except Exception as e:
        print(e)
# if __name__=='__main__':
#     GetData()