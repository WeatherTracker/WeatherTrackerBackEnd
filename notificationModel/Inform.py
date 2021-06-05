from flask import request,Blueprint,jsonify
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import time
import json
from setup import get_event, get_station,getUser
from notificationModel.FCMTest import getFCMtoken
Inform=Blueprint("Inform", __name__)
@Inform.route('/inform/<string:eventId>')
def informAll(eventId):
    time_start=time.time()
    userDb=getUser()
    eventDb=get_event()
    eventObj=eventDb.currentEvent.find_one({"eventId":eventId})
    hosts=eventObj["hosts"]
    participants=eventObj["participants"]
    userObject=userDb.auth.find_one({"eventId":eventId})

    return "1"