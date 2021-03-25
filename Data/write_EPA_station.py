from pymongo import MongoClient
import json
import time
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
db = client.station
def getdata():
    time_start=time.time()
    with open('Station_location.json', 'r', encoding="utf-8") as f:
        # 把json檔为dict
        station_data={}
        json_data = json.load(f)
        for i in range(len(json_data["result"]["records"])):
            SiteName=json_data["result"]["records"][i]["SiteName"]
            try:
                lon=float(json_data["result"]["records"][i]["TWD97Lon"])
            except:
                lon=None
            try:
                lat=float(json_data["result"]["records"][i]["TWD97Lat"])
            except:
                lat=None
            station_data.update({SiteName:{"lat":lat,"lon":lon}})
        # print(station_data)
        write_database(station_data)
    time_end=time.time()
    print("寫入環保署測站資料要花",time_end-time_start,"s")
def write_database(station_data):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.EPA_station_location.insert_one(
            {
                "data":station_data
            }
        )
    except Exception as e:
        print(e)

getdata()

