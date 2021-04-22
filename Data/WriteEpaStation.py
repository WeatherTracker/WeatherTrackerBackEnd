from pymongo import MongoClient
import json
import time
import requests
def GetData():
    time_start=time.time()
    url = "https://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?sort=SiteName&offset=0&limit=1000"  # 政府資料開放平台的AQI
    Data = requests.get(url)
    dict_data = json.loads(Data.text)
    station_data={}
    for i in range(len(dict_data["result"]["records"])):
        SiteName=dict_data["result"]["records"][i]["SiteName"]
        try:
            lon=float(dict_data["result"]["records"][i]["Longitude"])
        except:
            lon=None
        try:
            lat=float(dict_data["result"]["records"][i]["Latitude"])
        except:
            lat=None
        station_data.update({SiteName:{"lat":lat,"lon":lon}})
    WriteDatabase(station_data)
    time_end=time.time()
    print("寫入環保署測站資料要花",time_end-time_start,"s")
def WriteDatabase(station_data):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.EPA_Station_Location.insert_one(
            {
                "data":station_data
            }
        )
    except Exception as e:
        print(e)
if __name__ =='__main__':
    GetData()