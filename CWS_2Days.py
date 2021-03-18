import requests
import json
import datetime
import time
from pymongo import MongoClient
count=0
# url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-001?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
def getdata(count):
    time_start=time.time()
    while count<=21:
        all_times_12HR=[]
        all_times_6HR=[]
        all_times_3HR_range=[]
        all_times_3HR_point=[]
        times_dict={}
        location={}
        if count<=2:#001-009
            url1 = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-00"+str((4*count+1))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        else:#013-085
            url1="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-0"+str((4*count+1))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        count=count+1
        Data1 = requests.get(url1)
        all=json.loads(Data1.text)#把json變成dictionary
        weather_info=all["records"]["locations"][0]["location"][0]["weatherElement"]
        for i in range(len(weather_info)):
            if weather_info[i]["description"]=="12小時降雨機率":
                time_info=weather_info[i]["time"]
                for j in range(len(time_info)):
                    all_times_12HR.append({"startTime":weather_info[i]["time"][j]["startTime"],"endTime":weather_info[i]["time"][j]["endTime"]})
            if weather_info[i]["description"]=="6小時降雨機率":
                time_info=weather_info[i]["time"]
                for j in range(len(time_info)):
                    all_times_6HR.append({"startTime":weather_info[i]["time"][j]["startTime"],"endTime":weather_info[i]["time"][j]["endTime"]})
            if weather_info[i]["description"]=="天氣現象":
                time_info=weather_info[i]["time"]
                for j in range(len(time_info)):
                    all_times_3HR_range.append({"startTime":weather_info[i]["time"][j]["startTime"],"endTime":weather_info[i]["time"][j]["endTime"]})
            if weather_info[i]["description"]=="體感溫度":
                time_info=weather_info[i]["time"]
                for j in range(len(time_info)):
                    all_times_3HR_point.append({"dataTime":weather_info[i]["time"][j]["dataTime"]})

        all_district_info=all["records"]["locations"][0]["location"]

        for i in range(len(all_district_info)):
            times_12HR=[]
            for j in range(len(all_times_12HR)):
                
                weather_info=all["records"]["locations"][0]["location"][i]["weatherElement"]
                data={}
                for k in range(len(weather_info)):
                    if weather_info[k]["description"]=="12小時降雨機率":
                        time_info=weather_info[k]["time"]
                        for s in range(len(time_info)):
                            if time_info[s]["startTime"]==all_times_12HR[j]["startTime"] and time_info[s]["endTime"]==all_times_12HR[j]["endTime"]:
                                data.update({weather_info[k]["description"]:time_info[s]["elementValue"][0]["value"]})

                times_12HR.append({"startTime":datetime.datetime.strptime(all_times_12HR[j]["startTime"], "%Y-%m-%d %H:%M:%S"),"endTime":datetime.datetime.strptime(all_times_12HR[j]["endTime"], "%Y-%m-%d %H:%M:%S"),"data":data})
                # times_12HR.append({"startTime":all_times_12HR[j]["startTime"],"endTime":all_times_12HR[j]["endTime"],"data":data})
                times_dict.update({"times_12HR":times_12HR})
            location.update({all_district_info[i]["locationName"]:times_dict})

        for i in range(len(all_district_info)):
            times_6HR=[]
            for j in range(len(all_times_6HR)):
                weather_info=all["records"]["locations"][0]["location"][i]["weatherElement"]
                data={}
                for k in range(len(weather_info)):
                    if weather_info[k]["description"]=="6小時降雨機率":
                        time_info=weather_info[k]["time"]
                        for s in range(len(time_info)):
                            if time_info[s]["startTime"]==all_times_6HR[j]["startTime"] and time_info[s]["endTime"]==all_times_6HR[j]["endTime"]:
                                data.update({weather_info[k]["description"]:time_info[s]["elementValue"][0]["value"]})
                times_6HR.append({"startTime":datetime.datetime.strptime(all_times_6HR[j]["startTime"], "%Y-%m-%d %H:%M:%S"),"endTime":datetime.datetime.strptime(all_times_6HR[j]["endTime"], "%Y-%m-%d %H:%M:%S"),"data":data})
                # times_6HR.append({"startTime":all_times_6HR[j]["startTime"],"endTime":all_times_6HR[j]["endTime"],"data":data})
                times_dict.update({"times_6HR":times_6HR})
            location.update({all_district_info[i]["locationName"]:times_dict})

        for i in range(len(all_district_info)):
            times_3HR_range=[]
            for j in range(len(all_times_3HR_range)):
                weather_info=all["records"]["locations"][0]["location"][i]["weatherElement"]
                data={}
                for k in range(len(weather_info)):
                    if weather_info[k]["description"]=="天氣現象" or weather_info[k]["description"]=="天氣預報綜合描述":
                        time_info=weather_info[k]["time"]
                        for s in range(len(time_info)):
                            if time_info[s]["startTime"]==all_times_3HR_range[j]["startTime"] and time_info[s]["endTime"]==all_times_3HR_range[j]["endTime"]:
                                data.update({weather_info[k]["description"]:time_info[s]["elementValue"][0]["value"]})
                times_3HR_range.append({"startTime":datetime.datetime.strptime(all_times_3HR_range[j]["startTime"], "%Y-%m-%d %H:%M:%S"),"endTime":datetime.datetime.strptime(all_times_3HR_range[j]["endTime"], "%Y-%m-%d %H:%M:%S"),"data":data})
                # times_3HR_range.append({"startTime":all_times_3HR_range[j]["startTime"],"endTime":all_times_3HR_range[j]["endTime"],"data":data})
                times_dict.update({"times_3HR_range":times_3HR_range})
            location.update({all_district_info[i]["locationName"]:times_dict})
        
        for i in range(len(all_district_info)):
            times_3HR_point=[]
            for j in range(len(all_times_3HR_point)):
                
                weather_info=all["records"]["locations"][0]["location"][i]["weatherElement"]
                data={}
                
                for k in range(len(weather_info)):
                    if weather_info[k]["description"]=="體感溫度" or weather_info[k]["description"]=="溫度" or weather_info[k]["description"]=="相對濕度" or weather_info[k]["description"]=="舒適度指數" or weather_info[k]["description"]=="風速" or weather_info[k]["description"]=="風向" or weather_info[k]["description"]=="露點溫度":
                        time_info=weather_info[k]["time"]
                        for s in range(len(time_info)):
                            if time_info[s]["dataTime"]==all_times_3HR_point[j]["dataTime"]:
                                data.update({weather_info[k]["description"]:time_info[s]["elementValue"][0]["value"]})
                times_3HR_point.append({"dataTime":datetime.datetime.strptime(all_times_3HR_point[j]["dataTime"], "%Y-%m-%d %H:%M:%S"),"data":data})
                # times_3HR_point.append({"dataTime":all_times_3HR_point[j]["dataTime"],"data":data})
                times_dict.update({"times_3HR_point":times_3HR_point})

            location.update({all_district_info[i]["locationName"]:times_dict})
        
        result={"city":all["records"]["locations"][0]["locationsName"],"location":location}
        writedata(result)
    time_end=time.time()
    print("爬2天要花",time_end-time_start,"s")

def writedata(result):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.CWS_2Days.update_one(
            {"city": result["city"]},
            {"$set": {
                "locations": result["location"]
            }}, upsert=True
        )
        # print('寫入成功')
    except Exception as e:
        print(e)
    # file = 'CWS_2Days.json'
    # with open(file, 'w',encoding='utf8') as obj:
    #     json.dump(result, obj, ensure_ascii=False)#把結果寫入CWS.json檔
getdata(count)