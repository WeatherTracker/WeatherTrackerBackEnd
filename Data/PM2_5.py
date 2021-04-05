import requests
import json
from pymongo import MongoClient
from datetime import datetime
import time
count=0
def getdata(count):
    time_start=time.time()
    while count<=76:
        if count==76:
            url2 = 'https://data.epa.gov.tw/api/v1/aqx_p_461?api_key=a8d65da5-df91-47dc-8981-fee0315fecd9'#基隆的PM2.5 history
        else:
            url2 = 'https://data.epa.gov.tw/api/v1/aqx_p_'+str(count+189)+'?api_key=a8d65da5-df91-47dc-8981-fee0315fecd9'#基隆的PM2.5 history
        count=count+1
        Data2 = requests.get(url2)
        history_all=json.loads(Data2.text)
        forecast=[]
        history={}
        now=[]
        all_time=[]
        time_list=[]
        
        for i in range(len(history_all["records"])):
            if history_all["records"][i]["MonitorDate"] not in time_list:
                time_list.append(history_all["records"][i]["MonitorDate"])
        for i in range(len(time_list)):
            data={}
            for j in range(len(history_all["records"])):
                if history_all["records"][j]["MonitorDate"]==time_list[i]:
                    if history_all["records"][j]["ItemEngName"]=="PM2.5" or history_all["records"][j]["ItemEngName"]=="PM10":
                        try:
                            data.update({history_all["records"][j]["ItemEngName"]+"("+history_all["records"][j]["ItemUnit"]+")":int(history_all["records"][j]["Concentration"])})
                        except:
                            data.update({history_all["records"][j]["ItemEngName"]+"("+history_all["records"][j]["ItemUnit"]+")":None})
                    else:
                        try:
                            data.update({history_all["records"][j]["ItemEngName"]+"("+history_all["records"][j]["ItemUnit"]+")":float(history_all["records"][j]["Concentration"])})
                        except:
                            data.update({history_all["records"][j]["ItemEngName"]+"("+history_all["records"][j]["ItemUnit"]+")":None})
            all_time.append({"MonitorDate":datetime.strptime(time_list[i],"%Y-%m-%d %H:%M:%S"),"data":data})
        history.update({"time":all_time})

        url1="https://opendata.epa.gov.tw/api/v1/AQFN?%24skip=0&%24top=1000&%24format=json"#區域PM2.5 forecast data
        Data1 = requests.get(url1)
        forecast_all=json.loads(Data1.text)

        County=history_all["records"][0]["County"]
        
        if County=="基隆市" or County=="台北市" or County=="新北市" or County=="桃園市":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="北部":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="台中市" or County=="彰化縣" or County=="南投縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="中部":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="雲林縣" or County=="嘉義縣" or County=="台南市":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="雲嘉南":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="高雄市" or County=="屏東縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="高屏":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="花蓮縣" or County=="台東縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="花東":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="新竹市" or County=="新竹縣"  or County=="苗栗縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="竹苗":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="宜蘭縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="宜蘭":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="澎湖縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="澎湖":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="金門縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="金門":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        if County=="馬祖縣":
            for i in range(len(forecast_all)):
                forecast_date=datetime.strptime(forecast_all[i]["ForecastDate"],"%Y-%m-%d")
                try:
                    forecast_value=int(forecast_all[i]["AQI"])
                except:
                    forecast_value=None
                if forecast_all[i]["Area"]=="馬祖":
                    forecast.append({"Area":forecast_all[i]["Area"],"AQI":forecast_value,"ForecastDate":forecast_date})
        
        url3="https://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?sort=SiteName&offset=0&limit=1000"#政府資料開放平台的AQI
        Data3 = requests.get(url3)
        now_all=json.loads(Data3.text)

        for i in range(len(now_all["result"]["records"])):
            if now_all["result"]["records"][i]["SiteName"]==history_all["records"][0]["SiteName"]:
                try:
                    now_value=int(now_all["result"]["records"][i]["AQI"])
                except:
                    now_value=None
                now.append({"AQI":now_value,"Status":now_all["result"]["records"][i]["Status"],"PublishTime":datetime.strptime(now_all["result"]["records"][i]["PublishTime"].replace("/","-"),"%Y-%m-%d %H:%M:%S"),"Longitude":now_all["result"]["records"][i]["Longitude"],"Latitude":now_all["result"]["records"][i]["Latitude"]})

        city={"SiteName":history_all["records"][0]["SiteName"],"County":history_all["records"][0]["County"],"now":now,"forecast":forecast,"history":history}
        SiteName=history_all["records"][0]["SiteName"]
        County=history_all["records"][0]["County"]
        writedata(city,SiteName,County)
        # file = 'PM2_5.json'
        # with open(file, 'w',encoding='utf8') as obj:
        #     json.dump(city, obj,ensure_ascii=False)#把結果寫入CWS.json檔
    time_end=time.time()
    print("爬取PM2_5要花",time_end-time_start,"s")
def writedata(city,SiteName,County):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.PM2_5.update_one(
            {"SiteName": SiteName,"County": County},
            {"$set": {
                "update_Time":datetime.now(),
                "now": city["now"],
                "forecast":city["forecast"],
                "history":city["history"]
            }}, upsert=True
        )
    except Exception as e:
        print(e)
getdata(count)