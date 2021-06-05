from pymongo import MongoClient
import math
from flask import request,jsonify,Blueprint
#from setup import get_event
client = MongoClient("localhost", 27017)
def hobby_event(staticTag,lon,lat):
    print(staticTag)
    eventDb=client.event
    recommendEventList=[]
    recommendEvent=eventDb.currentEvent.find({"staticHobbyTag":staticTag,"isPublic":True})
    for i in recommendEvent:
        i.pop("_id")
        print(i)
        recommendEventList.append(i)
    recommendEventList.sort(key=lambda s: pow((s.get("longitude")-float(lon)),2)+pow((s.get("latitude")-float(lat)),2))
    return recommendEventList