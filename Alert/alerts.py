import requests
import json
from pymongo import MongoClient
import datetime
import time

def GetData():
    time_start=time.time()
    url3 = 'https://alerts.ncdr.nat.gov.tw/api/datastore?apikey=76Xg3iaxYgKSw5LXZ54m4%2BxO6KXYq74GjsMMkCriTGO03j3hOxf0WJUM%2BtsXnb0s&format=json'
    #民生示警API
    Data3 = requests.get(url3)
    ask3=json.loads(Data3.text)
    for i in range(len(ask3["result"])):
        alerts.append({"effective":datetime.datetime.strptime(ask3["result"][i]["effective"].replace("T"," "), "%Y-%m-%d %H:%M:%S"),"expires":datetime.datetime.strptime(ask3["result"][i]["expires"].replace("T"," "), "%Y-%m-%d %H:%M:%S"),"description":ask3["result"][i]["description"]})
        
        # alerts.append({"effective":ask3["result"][i]["effective"].replace("T"," "),"expires":ask3["result"][i]["expires"].replace("T"," "),"description":ask3["result"][i]["description"]})
    city={"alerts":alerts}
    # print(city)
    WriteData(city)
    # file="alerts.json"
    # with open(file,'w',encoding='utf8') as obj:
    #     json.dump(city,obj,ensure_ascii=False)
    time_end=time.time()
    print("爬取警告要花",time_end-time_start,"s")
def WriteData(city):
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.station
    try:
        db.Alerts.update(
            {"alerts": ""},
            {"$set": {
                "alerts": city["alerts"]
            }}, upsert=True
        )
        # print('寫入成功')
    except Exception as e:
        print(e)
if __name__ =='__main__':
    alerts=[]
    GetData()