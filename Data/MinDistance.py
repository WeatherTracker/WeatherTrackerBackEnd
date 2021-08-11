from setup import get_station
import math
import json
db = get_station()
def CwsMinDistance(now_lat,now_lon):
    all_data=db.CWB_Station_Location.find()
    inf = float('Inf')
    min_d=inf
    SiteName=""
    city=""
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
def EpaMinDistance(now_lat,now_lon):
    all_data=db.EPA_Station_Location.find()
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
def Write_3Days(now_lat,now_lon):
    result=CwsMinDistance(now_lat,now_lon)#傳回測站的地區和縣市
    SiteName=EpaMinDistance(now_lat,now_lon)#傳回測站的名稱
    city=result[0]
    district=result[1]
    print(city+" "+district+" "+SiteName)

    target_SiteName=db.PM2_5.find({"SiteName": SiteName})
    AQI_data=[]
    for i in target_SiteName:
        i.pop("_id")
        for j in range(len(i["forecast"])):
            timeString = i["forecast"][j]["ForecastDate"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
            tag=i["forecast"][j]["tag"]
            AQI_data.append({"time":timeString,"value":i["forecast"][j]["AQI"],"tag":tag})
    target_city=db.CWB_7Days.find({"city": city})
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    UV_dict=i["locations"][j]["times"][k]["data"]
                    timeString = i["locations"][j]["times"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    for s in range(len(i["locations"][j]["times"][k]["data"])):
                        if "紫外線指數" in i["locations"][j]["times"][k]["data"][s]:
                            UV.append({"time":timeString,"value":UV_dict[s]["紫外線指數"],"tag":UV_dict[s]["tag"]})
    target_city=db.CWB_3Days.find({"city": city})
    rain_6hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times_6HR"])):
                    timeString = i["locations"][j]["times_6HR"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串

                    rain_6hr.append({"time":timeString,"value":i["locations"][j]["times_6HR"][k]["data"][0]["6小時降雨機率"],"tag":i["locations"][j]["times_6HR"][k]["data"][0]["tag"]})
                for k in range(len(i["locations"][j]["times_3HR_point"])):
                    timeString = i["locations"][j]["times_3HR_point"][k]["dataTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    for s in range(len(i["locations"][j]["times_3HR_point"][k]["data"])):
                        if "溫度" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                            temperature.append({"time":timeString,"value":i["locations"][j]["times_3HR_point"][k]["data"][s]["溫度"],"tag":i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"]})
                        if "相對濕度" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                            humidity.append({"time":timeString,"value":i["locations"][j]["times_3HR_point"][k]["data"][s]["相對濕度"],"tag":i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"]})
                        if "風速" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                            wind.append({"time":timeString,"value":i["locations"][j]["times_3HR_point"][k]["data"][s]["風速"],"tag":i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"]})
    data_3Days={}
    data_3Days.update({"city":city,"area":district,"siteName":SiteName,"POP":rain_6hr,"temperature":temperature,"humidity":humidity,"windSpeed":wind,"AQI":AQI_data,"UV":UV})
    return data_3Days
def Write_3_To_7Days(now_lat,now_lon):
    result=CwsMinDistance(now_lat,now_lon)#傳回測站的地區和縣市
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
                    timeString = i["locations"][j]["times"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    for s in range(len(i["locations"][j]["times"][k]["data"])):
                        if "12小時降雨機率" in i["locations"][j]["times"][k]["data"][s]:
                            rain_12hr.append({"time":timeString,"value":i["locations"][j]["times"][k]["data"][s]["12小時降雨機率"],"tag":i["locations"][j]["times"][k]["data"][s]["tag"]})
                        if "平均溫度" in i["locations"][j]["times"][k]["data"][s]:
                            temperature.append({"time":timeString,"value":i["locations"][j]["times"][k]["data"][s]["平均溫度"],"tag":i["locations"][j]["times"][k]["data"][s]["tag"]})
                        if "平均相對濕度" in i["locations"][j]["times"][k]["data"][s]:
                            humidity.append({"time":timeString,"value":i["locations"][j]["times"][k]["data"][s]["平均相對濕度"],"tag":i["locations"][j]["times"][k]["data"][s]["tag"]})
                        if "最大風速" in i["locations"][j]["times"][k]["data"][s]:
                            wind.append({"time":timeString,"value":i["locations"][j]["times"][k]["data"][s]["最大風速"],"tag":i["locations"][j]["times"][k]["data"][s]["tag"]})
                        if "紫外線指數" in i["locations"][j]["times"][k]["data"][s]:
                            UV.append({"time":timeString,"value":i["locations"][j]["times"][k]["data"][s]["紫外線指數"],"tag":i["locations"][j]["times"][k]["data"][s]["tag"]})
    data_7Days={}
    data_7Days.update({"city":city,"area":district,"POP":rain_12hr,"temperature":temperature,"humidity":humidity,"windSpeed":wind,"UV":UV})
    return data_7Days
def weatherIcon(now_lat,now_lon):
    result=CwsMinDistance(now_lat,now_lon)#傳回測站的地區和縣市
    print(result)
    city=result[0]
    district=result[1]
    print(city+" "+district)
    target_city=db.CWB_7Days.find({"city": city})
    weather=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                for k in range(len(i["locations"][j]["times"])):
                    timeString = i["locations"][j]["times"][k]["startTime"].strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
                    str1=timeString.split(" ")
                    for s in range(len(i["locations"][j]["times"][k]["data"])):
                        if "天氣現象" in i["locations"][j]["times"][k]["data"][s] and k%2==0 and str1[1]!="00:00:00":
                            with open('data.json',"r",encoding="utf-8") as obj:
                                ans=json.load(obj)
                                for item in range(len(ans)):
                                    if ans[item]["天氣描述"]==i["locations"][j]["times"][k]["data"][s]["天氣現象"]:
                                        if str1[1]=="06:00:00" or str1[1]=="12:00:00":
                                            description=ans[item]["白天"]
                                        elif str1[1]=="18:00:00":
                                            description=ans[item]["夜晚"]
                                        break
                            weather.append(description[:-4])
    return weather