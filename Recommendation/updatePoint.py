import requests
from pymongo import MongoClient
import json
import codecs
def updatePoint():
    # url="https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json"
    # allSpot = requests.get(url)
    client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
    db = client.event
    # allSpot=json.loads(allSpot.text)
    allSpotTest=json.load(codecs.open('https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json', 'r', 'utf-8-sig'))
    try:
        db.viewPoint.update_one(
            {"Listname": "1"},
            {"$set": allSpotTest}, upsert=True
        )
        print("成功")
    except Exception as e:
        print(e)