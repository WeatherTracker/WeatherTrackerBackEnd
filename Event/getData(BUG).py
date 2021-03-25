from flask import Flask,request,render_template
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import os
from flask import jsonify
import datetime
from datetime import datetime,timedelta
import math
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
db = client.station
def CWS_min_distance(now_lat,now_lon):
    all_data=db.CWB_station_location.find()
    inf = float('Inf')
    min_d=inf
    SiteName=""
    for item in all_data:
        for location in item["data"]:
            for district in item["data"][location]:
                station_lat=item["data"][location][district]["lat"]
                station_lon=item["data"][location][district]["lon"]
                x=float(now_lat)-station_lat
                y=float(now_lon)-station_lon
                distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
                if distance<min_d:
                    min_d=distance
                    city=location
                    SiteName=district
    result=[]
    result.append(city)
    result.append(SiteName)
    return result
def EPA_min_distance(now_lat,now_lon):
    all_data=db.EPA_station_location.find()
    inf = float('Inf')
    min_d=inf
    SiteName=""
    for item in all_data:
        for location in item["data"]:
            station_lat=item["data"][location]["lat"]
            station_lon=item["data"][location]["lon"]
            x=float(now_lat)-station_lat
            y=float(now_lon)-station_lon
            distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
            if distance<min_d:
                min_d=distance
                SiteName=location
    return SiteName
def write_3Days(now_lat,now_lon):
    result=CWS_min_distance(now_lat,now_lon)#傳回測站的地區和縣市
    SiteName=EPA_min_distance(now_lat,now_lon)#傳回測站的名稱
    city=result[0]
    district=result[1]
    print(city+" "+district+" "+SiteName)

    target_SiteName=db.PM2_5.find({"SiteName": SiteName})
    AQI_data=[]
    for i in target_SiteName:
        i.pop("_id")
        for j in range(len(i["forecast"])):
            AQI_data.append({i["forecast"][j]["ForecastDate"]:i["forecast"][j]["AQI"]})
    target_city=db.CWB_7Days.find({"city": city})
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    UV_dict=i["locations"][j]["times"][k]["data"]
                    if "紫外線指數" in UV_dict.keys():
                        UV.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["紫外線指數"]})
    
    target_city=db.CWB_3Days.find({"city": city})
    rain_12hr=[]
    rain_6hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times_12HR"])):
                    rain_12hr.append({i["locations"][j]["times_12HR"][k]["startTime"]:i["locations"][j]["times_12HR"][k]["data"]["12小時降雨機率"]})
                for k in range(len(i["locations"][j]["times_6HR"])):
                    rain_6hr.append({i["locations"][j]["times_6HR"][k]["startTime"]:i["locations"][j]["times_6HR"][k]["data"]["6小時降雨機率"]})
                for k in range(len(i["locations"][j]["times_3HR_point"])):
                    temperature.append({i["locations"][j]["times_3HR_point"][k]["dataTime"]:i["locations"][j]["times_3HR_point"][k]["data"]["溫度"]})
                    humidity.append({i["locations"][j]["times_3HR_point"][k]["dataTime"]:i["locations"][j]["times_3HR_point"][k]["data"]["相對濕度"]})
                    wind.append({i["locations"][j]["times_3HR_point"][k]["dataTime"]:i["locations"][j]["times_3HR_point"][k]["data"]["風速"]})
    data_3Days={}
    data_3Days.update({"12小時降雨機率":rain_12hr,"6小時降雨機率":rain_6hr,"溫度":temperature,"相對濕度":humidity,"風速":wind,"AQI":AQI_data,"紫外線":UV})
    print(data_3Days)
def write_3_to_7Days(now_lat,now_lon):
    result=CWS_min_distance(now_lat,now_lon)#傳回測站的地區和縣市
    city=result[0]
    district=result[1]
    print(city+" "+district)

    target_city=db.CWB_7Days.find({"city": city})
    rain_12hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    rain_12hr.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["12小時降雨機率"]})
                    temperature.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["平均溫度"]})
                    humidity.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["平均相對濕度"]})
                    wind.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["最大風速"]})
                    UV_dict=i["locations"][j]["times"][k]["data"]
                    if "紫外線指數" in UV_dict.keys():
                        UV.append({i["locations"][j]["times"][k]["startTime"]:i["locations"][j]["times"][k]["data"]["紫外線指數"]})
    data_7Days={}
    data_7Days.update({"12小時降雨機率":rain_12hr,"平均溫度":temperature,"平均相對濕度":humidity,"最大風速":wind,"紫外線指數":UV})
    print(data_7Days)
def getData(TimeData,now_lat,now_lon):
    now=datetime.now()
    print(now)
    ask=datetime.strptime(TimeData,"%Y-%m-%d %H:%M:%S.%f")
    print(ask)
    after_3days = now +timedelta(days = 3)
    after_7days = now +timedelta(days = 7)
    if ask<now:
        print("history")
    elif ask<after_3days:
        print("in 3 Days")
        write_3Days(now_lat,now_lon)
    elif ask<after_7days:
        print("3-7 Days")
        write_3_to_7Days(now_lat,now_lon)
    else:
        print("  >7 Days use ACCU")

getData("2021-03-26 23:59:59.628556","22.7254758","120.2628547")