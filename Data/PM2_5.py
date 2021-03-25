import requests
import json
from pymongo import MongoClient
import datetime
import time
forecast=[]
history={}
now=[]
all_time=[]
def getdata():
    time_start=time.time()
    url2 = 'https://opendata.epa.gov.tw/api/v1/ATM00548?%24skip=0&%24top=1000&%24format=json'#基隆的PM2.5 history
    Data2 = requests.get(url2)
    history_all=json.loads(Data2.text)
    time_list=[]
    
    for i in range(len(history_all)):
        if history_all[i]["MonitorDate"] not in time_list:
            time_list.append(history_all[i]["MonitorDate"])
    # time_list=set(time_list)
    for i in range(len(time_list)):
        data={}
        for j in range(len(history_all)):
            if history_all[j]["MonitorDate"]==time_list[i]:
                data.update({history_all[j]["ItemEngName"]:history_all[j]["Concentration"]+" "+history_all[j]["ItemUnit"]})
        temp_time=time_list[i].replace("/","-")
        temp_time=temp_time.replace("上午 ","")
        temp_time=temp_time.replace("下午 ","")
        all_time.append({"MonitorDate":datetime.datetime.strptime(temp_time,"%Y-%m-%d %H:%M:%S"),"data":data})

        # alerts.append({"effective":datetime.datetime.strptime(ask3["result"][i]["effective"].replace("T"," "), "%Y-%m-%d %H:%M:%S"),"expires":datetime.datetime.strptime(ask3["result"][i]["expires"].replace("T"," "), "%Y-%m-%d %H:%M:%S"),"description":ask3["result"][i]["description"]})
    history.update({"time":all_time})

    url1="https://opendata.epa.gov.tw/api/v1/AQFN?%24skip=0&%24top=1000&%24format=json"#區域PM2.5 forecast data
    Data1 = requests.get(url1)
    forecast_all=json.loads(Data1.text)

    County=history_all[0]["County"]
    
    if County=="基隆市" or County=="台北市" or County=="新北市" or County=="桃園市":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="北部":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="台中市" or County=="彰化縣" or County=="南投縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="中部":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="雲林縣" or County=="嘉義縣" or County=="台南市":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="雲嘉南":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="高雄市" or County=="屏東縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="高屏":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="花蓮縣" or County=="台東縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="花東":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="新竹市" or County=="新竹縣"  or County=="苗栗縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="竹苗":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="宜蘭縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="宜蘭":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="澎湖縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="澎湖":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="金門縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="金門":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    if County=="馬祖縣":
        for i in range(len(forecast_all)):
            if forecast_all[i]["Area"]=="馬祖":
                forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_all[i]["AQI"],"ForecastDate":datetime.datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")})
    
    url3="https://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?sort=SiteName&offset=0&limit=1000"#政府資料開放平台的AQI
    Data3 = requests.get(url3)
    now_all=json.loads(Data3.text)

    for i in range(len(now_all["result"]["records"])):
        if now_all["result"]["records"][i]["SiteName"]==history_all[0]["SiteName"]:
            now.append({"AQI":now_all["result"]["records"][i]["AQI"],"Status":now_all["result"]["records"][i]["Status"],"PublishTime":datetime.datetime.strptime(now_all["result"]["records"][i]["PublishTime"].replace("/","-"),"%Y-%m-%d %H:%M:%S"),"Longitude":now_all["result"]["records"][i]["Longitude"],"Latitude":now_all["result"]["records"][i]["Latitude"]})

    city={"station":history_all[0]["SiteName"],"County":history_all[0]["County"],"now":now,"forecast":forecast,"history":history}
    writedata(city)
    # file = 'PM2_5.json'
    # with open(file, 'w',encoding='utf8') as obj:
    #     json.dump(city, obj,ensure_ascii=False)#把結果寫入CWS.json檔
    time_end=time.time()
    print("爬取PM2_5要花",time_end-time_start,"s")
def writedata(city):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.PM2_5.update(
            {"station": "基隆","County": "基隆市"},
            {"$set": {
                "now": city["now"],
                "forecast":city["forecast"],
                "history":city["history"]
            }}, upsert=True
        )
        # self.collection.insert(data)
        print('寫入成功')
    except Exception as e:
        print(e)
getdata()