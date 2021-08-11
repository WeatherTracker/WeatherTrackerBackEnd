import requests
from pymongo import MongoClient
import json
import codecs
from setup import get_event
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
eventDb = get_event()
def updatePoint():
    url="https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json"
    allSpot = requests.get(url)
    allSpot.encoding = 'utf-8-sig'
    allSpotTest = json.loads(allSpot.text)
    try:
        eventDb.viewPoint.update_one({"Listname": "1"},{"$set": allSpotTest["XML_Head"]})
        print("成功")
    except Exception as e:
        print(e)