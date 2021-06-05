from setup import get_event,get_station
from Data.MinDistance import CwsMinDistance,EpaMinDistance
import datetime
import json
eventDb=get_event()
stationDb=get_station()

def tag7Days(startTime,endTime,latitude,longitude,Days3):
    result=CwsMinDistance(latitude,longitude)#傳回測站的地區和縣市
    city=result[0]
    district=result[1]
    target_city=stationDb.CWB_7Days.find({"city": city})
    rain_12hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                flag=False
                flagUV=False
                for k in range(len(i["locations"][j]["times"])):
                    judgeTime=i["locations"][j]["times"][k]["startTime"]
                    if startTime<=judgeTime and judgeTime<=endTime and judgeTime>=Days3:
                        if flag==False and k>0:# 抓取7天內的第1筆資料
                            for s in range(len(i["locations"][j]["times"][k-1]["data"])):
                                if "12小時降雨機率" in i["locations"][j]["times"][k-1]["data"][s]:
                                    rain_12hr.append(i["locations"][j]["times"][k-1]["data"][s]["tag"])
                                if "平均溫度" in i["locations"][j]["times"][k-1]["data"][s]:
                                    temperature.append(i["locations"][j]["times"][k-1]["data"][s]["tag"])
                                if "平均相對濕度" in i["locations"][j]["times"][k-1]["data"][s]:
                                    humidity.append(i["locations"][j]["times"][k-1]["data"][s]["tag"])
                                if "最大風速" in i["locations"][j]["times"][k-1]["data"][s]:
                                    wind.append(i["locations"][j]["times"][k-1]["data"][s]["tag"])
                                if "紫外線指數" in i["locations"][j]["times"][k-1]["data"][s]:
                                    UV.append(i["locations"][j]["times"][k-1]["data"][s]["tag"])
                                    flagUV=True
                            if flagUV==False and k>1:
                                UV.append(i["locations"][j]["times"][k-2]["data"][9]["tag"])
                            flag=True
                        for s in range(len(i["locations"][j]["times"][k]["data"])):# 抓取7天內的資料
                            if "12小時降雨機率" in i["locations"][j]["times"][k]["data"][s]:
                                rain_12hr.append(i["locations"][j]["times"][k]["data"][s]["tag"])
                            if "平均溫度" in i["locations"][j]["times"][k]["data"][s]:
                                temperature.append(i["locations"][j]["times"][k]["data"][s]["tag"])
                            if "平均相對濕度" in i["locations"][j]["times"][k]["data"][s]:
                                humidity.append(i["locations"][j]["times"][k]["data"][s]["tag"])
                            if "最大風速" in i["locations"][j]["times"][k]["data"][s]:
                                wind.append(i["locations"][j]["times"][k]["data"][s]["tag"])
                            if "紫外線指數" in i["locations"][j]["times"][k]["data"][s]:
                                UV.append(i["locations"][j]["times"][k]["data"][s]["tag"])
    data_7Days={}
    data_7Days.update({"POP":rain_12hr,"temperature":temperature,"humidity":humidity,"windSpeed":wind,"UV":UV})
    return data_7Days
def tag3Days(startTime,endTime,latitude,longitude):
    result=CwsMinDistance(latitude,longitude)#傳回測站的地區和縣市
    SiteName=EpaMinDistance(latitude,longitude)#傳回測站的名稱
    city=result[0]
    district=result[1]
    target_SiteName=stationDb.PM2_5.find({"SiteName": SiteName})
    AQI_data=[]
    for i in target_SiteName:
        i.pop("_id")
        for j in range(len(i["forecast"])):
            judgeTime = i["forecast"][j]["ForecastDate"]
            if startTime+datetime.timedelta(days=-1)<=judgeTime and startTime>=judgeTime:
                tag=i["forecast"][j]["tag"]
                AQI_data.append(tag)
                break
        for j in range(len(i["forecast"])):
            judgeTime = i["forecast"][j]["ForecastDate"]
            if startTime<=judgeTime and judgeTime<=endTime:
                tag=i["forecast"][j]["tag"]
                AQI_data.append(tag)
    target_city=stationDb.CWB_7Days.find({"city": city})
    UV=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                flag=False
                flagUV=False
                for k in range(0,6):
                    judgeTime = i["locations"][j]["times"][k]["startTime"]
                    if startTime<=judgeTime and judgeTime<=endTime:
                        if flag==False:
                            if "紫外線指數" in i["locations"][j]["times"][k-1]["data"][9]:
                                UV_dict=i["locations"][j]["times"][k-1]["data"]
                                UV.append(UV_dict[9]["tag"])
                            if "紫外線指數" not in i["locations"][j]["times"][k-1]["data"][9] and k>1:
                                UV_dict=i["locations"][j]["times"][k-2]["data"]
                                UV.append(UV_dict[9]["tag"])
                            flag=True
                        if "紫外線指數" in i["locations"][j]["times"][k]["data"][9]:
                            UV_dict=i["locations"][j]["times"][k]["data"]
                            UV.append(UV_dict[9]["tag"])
    target_city=stationDb.CWB_3Days.find({"city": city})
    rain_6hr=[]
    temperature=[]
    humidity=[]
    wind=[]
    for i in target_city:
        i.pop("_id")
        for j in i["locations"]:
            if j==district:
                flag=False
                for k in range(len(i["locations"][j]["times_6HR"])):
                    judgeTime = i["locations"][j]["times_6HR"][k]["startTime"]
                    if startTime<=judgeTime and judgeTime<=endTime:
                        if flag==False and k>0:
                            rain_6hr.append(i["locations"][j]["times_6HR"][k-1]["data"][0]["tag"])
                            flag=True
                        rain_6hr.append(i["locations"][j]["times_6HR"][k]["data"][0]["tag"])
                flag=False
                for k in range(len(i["locations"][j]["times_3HR_point"])):
                    judgeTime=i["locations"][j]["times_3HR_point"][k]["dataTime"]
                    if startTime<=judgeTime and judgeTime<=endTime:
                        if flag==False and k>0:
                            for s in range(len(i["locations"][j]["times_3HR_point"][k-1]["data"])):
                                if "溫度" in i["locations"][j]["times_3HR_point"][k-1]["data"][s]:
                                    temperature.append(i["locations"][j]["times_3HR_point"][k-1]["data"][s]["tag"])
                                if "相對濕度" in i["locations"][j]["times_3HR_point"][k-1]["data"][s]:
                                    humidity.append(i["locations"][j]["times_3HR_point"][k-1]["data"][s]["tag"])
                                if "風速" in i["locations"][j]["times_3HR_point"][k-1]["data"][s]:
                                    wind.append(i["locations"][j]["times_3HR_point"][k-1]["data"][s]["tag"])
                            flag=True
                        for s in range(len(i["locations"][j]["times_3HR_point"][k]["data"])):
                            if "溫度" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                                temperature.append(i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"])
                            if "相對濕度" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                                humidity.append(i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"])
                            if "風速" in i["locations"][j]["times_3HR_point"][k]["data"][s]:
                                wind.append(i["locations"][j]["times_3HR_point"][k]["data"][s]["tag"])
    data_3Days={}
    data_3Days.update({"POP":rain_6hr,"temperature":temperature,"humidity":humidity,"windSpeed":wind,"AQI":AQI_data,"UV":UV})
    return data_3Days
def mergeSet(Day3,Day7):
    result={}
    if Day3!={} and Day7!={}:
        resultPOP=set(Day3["POP"]+Day7["POP"])
        resultTemperature=set(Day3["temperature"]+Day7["temperature"])
        resultHumidity=set(Day3["humidity"]+Day7["humidity"])
        resultWindSpeed=set(Day3["windSpeed"]+Day7["windSpeed"])
        resultAQI=set(Day3["AQI"])
        resultUV=set(Day3["UV"]+Day7["UV"])
    elif Day3!={}:
        resultPOP=set(Day3["POP"])
        resultTemperature=set(Day3["temperature"])
        resultHumidity=set(Day3["humidity"])
        resultWindSpeed=set(Day3["windSpeed"])
        resultAQI=set(Day3["AQI"])
        resultUV=set(Day3["UV"])
    elif Day7!={}:
        resultPOP=set(Day7["POP"])
        resultTemperature=set(Day7["temperature"])
        resultHumidity=set(Day7["humidity"])
        resultWindSpeed=set(Day7["windSpeed"])
        resultUV=set(Day7["UV"])
    else:
        resultPOP={}
        resultTemperature={}
        resultHumidity={}
        resultWindSpeed={}
        # resultAQI={}
        resultUV={}
    if Day3!={}:
        result.update({"POP":resultPOP,"temperature":resultTemperature,"humidity":resultHumidity,"windSpeed":resultWindSpeed,"AQI":resultAQI,"UV":resultUV})
    else:
        result.update({"POP":resultPOP,"temperature":resultTemperature,"humidity":resultHumidity,"windSpeed":resultWindSpeed,"UV":resultUV})
    return result
def mergeTag(data):#這邊還有 大陸冷氣團/寒冷(橘燈) 的問題
    tag=[]
    if "下雨" in data["POP"]:
        tag.append("下雨")
    hot=["炎熱(黃燈)","炎熱(橘燈)","炎熱(紅燈)"]
    cold=["大陸冷氣團","強烈大陸冷氣團","寒冷(黃燈)","寒冷(橘燈)","寒冷(紅燈)"]
    UV_tag=["中量級(黃燈)","高量級(橘燈)","過量級(紅燈)","危險級(紫燈)"]
    AQI_tag=["對敏感族群不健康(橘燈)","對所有族群不健康(紅燈)","非常不健康(紫燈)","危害(黑燈)"]
    hotIndex=0
    coldIndex=0
    UVIndex=0
    AQIIndex=0
    if "炎熱(黃燈)" in data["temperature"]:
        hotIndex=1
    if "炎熱(橘燈)" in data["temperature"]:
        hotIndex=2
    if "炎熱(紅燈)" in data["temperature"]:
        hotIndex=3
    if hotIndex!=0:
        tag.append(hot[hotIndex-1])
    if "大陸冷氣團" in data["temperature"]:
        coldIndex=1
    if "強烈大陸冷氣團" in data["temperature"]:
        coldIndex=2
    if "寒冷(黃燈)" in data["temperature"]:
        coldIndex=3
    if "寒冷(橘燈)" in data["temperature"]:
        coldIndex=4
    if "寒冷(紅燈)" in data["temperature"]:
        coldIndex=5
    if coldIndex!=0:
        tag.append(cold[coldIndex-1])
    if "乾燥" in data["humidity"]:
        tag.append("乾燥")
    if "潮濕" in data["humidity"]:
        tag.append("潮濕")
    if "中量級(黃燈)" in data["UV"]:
        UVIndex=1
    if "高量級(橘燈)" in data["UV"]:
        UVIndex=2
    if "過量級(紅燈)" in data["UV"]:
        UVIndex=3
    if "危險級(紫燈)" in data["UV"]:
        UVIndex=4
    if UVIndex!=0:
        tag.append(UV_tag[UVIndex-1])
    if "AQI" in data:
        if "對敏感族群不健康(橘燈)" in data["AQI"]:
            AQIIndex=1
        if "對所有族群不健康(紅燈)" in data["AQI"]:
            AQIIndex=2
        if "非常不健康(紫燈)" in data["AQI"]:
            AQIIndex=3
        if "危害(黑燈)" in data["AQI"]:
            AQIIndex=4
        if AQIIndex!=0:
            tag.append(AQI_tag[AQIIndex-1])
    if "強風" in data["windSpeed"]:
        tag.append("強風")
    return tag
def timeSegment(startTime,endTime,latitude,longitude):
    startTime=datetime.datetime.strptime(startTime,"%Y-%m-%d %H:%M")
    endTime=datetime.datetime.strptime(endTime,"%Y-%m-%d %H:%M")
    now=datetime.datetime.now()
    Days3=now+datetime.timedelta(days=3)
    Days7=now+datetime.timedelta(days=7)
    print(Days3,Days7)
    tag3={}
    tag7={}
    if endTime>=now and startTime<Days3:
        tag3=tag3Days(startTime,endTime,latitude,longitude)
        # print(tag3)
    if startTime<=Days7 and endTime>=Days3:
        tag7=tag7Days(startTime,endTime,latitude,longitude,Days3)
        # print(tag7)
    result=mergeSet(tag3,tag7)
    judge=mergeTag(result)
    # print(result)
    # print(judge)
    return judge
# timeSegment("2021-06-05 12:30:00","2021-06-06 21:00:00",25.1505447,121.7735869)