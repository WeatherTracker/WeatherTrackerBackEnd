import requests
import json
import math
import re
from pymongo import MongoClient

myKey = "76Xg3iaxYgKSw5LXZ54m4+xO6KXYq74GjsMMkCriTGO03j3hOxf0WJUM+tsXnb0s"
client = MongoClient('localhost', 27017)
db = client['station']
collect = db['Location']


def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d


def deg2rad(deg):
    return deg * (math.pi/180)


def findArea(lat, lon):
    poses = collect.find({})
    minDis = 999
    for pos in poses:
        dis = getDistanceFromLatLonInKm(lat, lon, pos.get("緯度"), pos.get("經度"))
        if minDis > dis:
            minDis = dis
            area = pos.get("area")
    return area


def getAlert(lat, lon):
    result=""
    areaName = findArea(lat, lon)  # 用ACCU查表所在位置名稱
    print("===========================================================")
    print("你在", areaName, "附近")
    response = requests.get("https://alerts.ncdr.nat.gov.tw/api/datastore?apikey="+myKey+"&format=json")
    idData = json.loads(response.text)
    for ids in idData.get("result"):
        detailResponse = requests.get("https://alerts.ncdr.nat.gov.tw/api/dump/datastore?apikey="+myKey+"&capid="+ids.get("capid")+"&format=json")
        detailData = json.loads(detailResponse.text)
        if detailData==None:
            return {"code":200,"msg":""}
        for infoObj in detailData.get("info"):
            for area in infoObj.get("area"):
                if area.get("circle") == None:  # 沒經緯度用地區
                    targetName = area.get("areaDesc")
                    if targetName[0] == "台":
                        targetName = "臺"+targetName[1:]
                    if areaName == targetName:
                        result+=str.strip(infoObj.get("headline"))
                        result+="\n"+str.strip(infoObj.get("description"))
                    elif areaName[:3] == targetName and (areaName[2] == "縣" or areaName[2] == "市"):
                        result+=str.strip(infoObj.get("headline"))
                        result+="\n"+str.strip(infoObj.get("description"))
                else:  # 有經緯度用經緯度
                    latlon = re.split(",| ", area.get("circle"))
                    if getDistanceFromLatLonInKm(lat, lon, float(latlon[0]), float(latlon[1])) < float(latlon[2]):  # 1KM以內
                        result+=str.strip(infoObj.get("headline"))
                        result+="\n"+str.strip(infoObj.get("description"))
                        # print(str.strip(infoObj.get("headline")))
                        # print(str.strip(infoObj.get("description")))
    return {"code":200,"msg":result}

# if __name__ == "__main__":
#     # getAlert(24.412933, 120.770286)  # 苗栗三義(無經緯度)
#     # getAlert(24.140446086774446, 120.67704418427662)  # 台中民權(有經緯度)
#     getAlert(23.7099538,120.5149186)
