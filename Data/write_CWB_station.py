import requests
import json
import datetime
import time
from pymongo import MongoClient
count=0
# url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-001?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
def getdata(count):
    time_start=time.time()
    
    city={}
    while count<=21:
        if count<=2:#001-009
            url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-00"+str((4*count+1))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        else:#013-085
            url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-0"+str((4*count+1))+"?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        count=count+1
        # url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-005?Authorization=CWB-D55ED7A7-56DD-4C73-964D-E61FACF6E5FE"
        
        Data = requests.get(url)
        station_info=json.loads(Data.text)
        station_data={}
        for i in range(len(station_info["records"]["locations"][0]["location"])):
            district=station_info["records"]["locations"][0]["location"][i]["locationName"]
            try:
                longitude=float(station_info["records"]["locations"][0]["location"][i]["lon"])
            except:
                longitude=None
            try:
                latitude=float(station_info["records"]["locations"][0]["location"][i]["lat"])
            except:
                latitude=None
            station_data.update({district:{"lat":latitude,"lon":longitude}})
        city.update({station_info["records"]["locations"][0]["locationsName"]:station_data})
        # locationsName=station_info["records"]["locations"][0]["locationsName"]
    writedata(city)
    # print(station_data)
    time_end=time.time()
    print("寫入中央氣象局測站資料要花",time_end-time_start,"s")

def writedata(city):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.CWB_station_location.insert_one(
            {
                "data":city
            }
        )
        # print('寫入成功')
    except Exception as e:
        print(e)
    # file = 'CWS_2Days.json'
    # with open(file, 'w',encoding='utf8') as obj:
    #     json.dump(result, obj, ensure_ascii=False)#把結果寫入CWS.json檔
getdata(count)