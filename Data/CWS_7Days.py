import requests
import json
from pymongo import MongoClient
import time
import datetime
from Data.Tag7DaysCreater import districtTagCreater,globalTagCreater,mergeTag,add7DaysTagToDB
def Get_7Days_Data():
    time_start=time.time()
    count=0
    url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-063?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
    Data2 = requests.get(url)
    globalAll=json.loads(Data2.text)#把json變成dictionary
    for i in range(len(globalAll["records"]["locations"][0]["location"])):
        if globalAll["records"]["locations"][0]["location"][i]["locationName"]=="中正區":
            weather_info=globalAll["records"]["locations"][0]["location"][i]["weatherElement"]
            for j in range(len(weather_info)):
                if weather_info[j]["description"]=="平均溫度":
                    globalTime=weather_info[j]["time"]
                    data=["temperature"]
                    for k in range(len(globalTime)):
                        try:
                            transfer=int(globalTime[k]["elementValue"][0]["value"])
                        except:
                            transfer=None
                        data.append(transfer)
            globalTag=globalTagCreater(data)
            break
    while count<=21:
        location={}
        time_list=[]
        if count<=1:#003,007
            url1 = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-00"+str((4*count+3))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        else:#011-087
            url1="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-0"+str((4*count+3))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        count=count+1
        Data1 = requests.get(url1)
        all=json.loads(Data1.text)#把json變成dictionary
        
        for i in range(len(all["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"])):
            time_list.append({"startTime":all["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["startTime"],"endTime":all["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][i]["endTime"]})
        
        all_district_info=all["records"]["locations"][0]["location"]
        for i in range(len(all_district_info)):
            times=[]
            times_dict={}
            POP=["POP"]
            temperature=["temperature"]
            humidity=["humidity"]
            windSpeed=["windSpeed"]
            UV=["UV"]
            for j in range(len(time_list)):
            
                weather_info=all["records"]["locations"][0]["location"][i]["weatherElement"]
                data=[]
                
                for k in range(len(weather_info)):
                    time_info=weather_info[k]["time"]
                    for s in range(len(time_info)):
                        if time_info[s]["startTime"]==time_list[j]["startTime"] and time_info[s]["endTime"]==time_list[j]["endTime"]:
                            if weather_info[k]["description"]=="天氣現象" or weather_info[k]["description"]=="天氣預報綜合描述" or weather_info[k]["description"]=="風向":
                                data.append({weather_info[k]["description"]:time_info[s]["elementValue"][0]["value"]})
                            else:
                                try:
                                    transfer=int(time_info[s]["elementValue"][0]["value"])
                                except:
                                    transfer=None
                                data.append({weather_info[k]["description"]:transfer})
                                if weather_info[k]["description"]=="平均溫度":
                                    temperature.append(transfer)
                                elif weather_info[k]["description"]=="平均相對濕度":
                                    humidity.append(transfer)
                                elif weather_info[k]["description"]=="最大風速":
                                    windSpeed.append(transfer)
                                elif weather_info[k]["description"]=="12小時降雨機率":
                                    POP.append(transfer)
                                elif weather_info[k]["description"]=="紫外線指數":
                                    UV.append(transfer)
                # times.append({"startTime":time_list[j]["startTime"],"endTime":time_list[j]["endTime"],"data":data})
                times.append({"startTime":datetime.datetime.strptime(time_list[j]["startTime"], "%Y-%m-%d %H:%M:%S"),"endTime":datetime.datetime.strptime(time_list[j]["endTime"], "%Y-%m-%d %H:%M:%S"),"data":data})
                times_dict.update({"times":times})
            times=add7DaysTagToDB(times,districtTagCreater(POP))
            times=add7DaysTagToDB(times,mergeTag(globalTag,districtTagCreater(temperature)))
            times=add7DaysTagToDB(times,districtTagCreater(humidity))
            times=add7DaysTagToDB(times,districtTagCreater(windSpeed))
            times=add7DaysTagToDB(times,districtTagCreater(UV))
            times_dict.update({"times":times})
            location.update({all_district_info[i]["locationName"]:times_dict})
            
        result={"city":all["records"]["locations"][0]["locationsName"],"location":location}
        WriteData(result)
        # file = 'CWS_7Days.json'
        # with open(file, 'w',encoding='utf8') as obj:
        #     json.dump(result, obj, ensure_ascii=False)#把結果寫入CWS.json檔
    time_end=time.time()
    print("寫入7天資料要花",time_end-time_start,"s")
def WriteData(result):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.CWB_7Days.update_one(
            {"city": result["city"]},
            {"$set": {
                "locations": result["location"]
            }}, upsert=True
        )
    except Exception as e:
        print(e)
if __name__ =='__main__':
    Get_7Days_Data()