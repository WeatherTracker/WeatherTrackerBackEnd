import requests
import json
from pymongo import MongoClient
from datetime import datetime
import time
from Data.Tag3DaysCreater import districtTagCreater,addAQITagToDB
def Get_PM2_5Data():
    #現在AQI data
    time_start = time.time()
    url3 = "https://data.epa.gov.tw/api/v1/aqx_p_432?api_key=a8d65da5-df91-47dc-8981-fee0315fecd9"
    Data3 = requests.get(url3)
    now_all = json.loads(Data3.text)

    # 區域PM2.5 forecast data
    url1 = "https://data.epa.gov.tw/api/v1/aqf_p_01?api_key=a8d65da5-df91-47dc-8981-fee0315fecd9"
    Data1 = requests.get(url1)
    forecast_all = json.loads(Data1.text)
    County = ""
    SiteName = ""
    for i in range(len(now_all["records"])):
        forecast = []
        now = []
        try:
            now_value = int(now_all["records"][i]["AQI"])
        except:
            now_value = None
        now.append({"AQI": now_value, "Status": now_all["records"][i]["Status"], "PublishTime": datetime.strptime(now_all["records"][i]["PublishTime"].replace(
            "/", "-"), "%Y-%m-%d %H:%M:%S"), "Longitude": now_all["records"][i]["Longitude"], "Latitude": now_all["records"][i]["Latitude"]})

        
        County = now_all["records"][i]["County"]
        latest=forecast_all["records"][0]["PublishTime"]
        if County == "基隆市" or County == "臺北市" or County == "新北市" or County == "桃園市":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "北部":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "臺中市" or County == "彰化縣" or County == "南投縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "中部":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "雲林縣" or County == "嘉義縣" or County == "臺南市" or County == "嘉義市":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "雲嘉南":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "高雄市" or County == "屏東縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "高屏":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "花蓮縣" or County == "臺東縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "花東":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "新竹市" or County == "新竹縣" or County == "苗栗縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "竹苗":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "宜蘭縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "宜蘭":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "澎湖縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "澎湖":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "金門縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "金門":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        if County == "連江縣":
            AQI=["AQI"]
            for j in range(len(forecast_all["records"])):
                if forecast_all["records"][j]["PublishTime"]==latest:
                    forecast_date = datetime.strptime(
                        forecast_all["records"][j]["ForecastDate"], "%Y-%m-%d")
                    try:
                        forecast_value = int(forecast_all["records"][j]["AQI"])
                    except:
                        forecast_value = None
                    if forecast_all["records"][j]["Area"] == "馬祖":
                        forecast.append(
                            {"Area": forecast_all["records"][j]["Area"], "AQI": forecast_value, "ForecastDate": forecast_date})
                        AQI.append(forecast_value)
                else:
                    break
        forecast=addAQITagToDB(forecast,districtTagCreater(AQI))
        forecast=sorted(forecast, key = lambda i: i["ForecastDate"])
        city = {"SiteName": now_all["records"][i]["SiteName"],
                "County": now_all["records"][i]["County"], "now": now, "forecast": forecast}
        # print(city)
        SiteName = now_all["records"][i]["SiteName"]
        County = now_all["records"][i]["County"]
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
    except Exception as e:
        print(e)