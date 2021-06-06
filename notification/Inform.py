from flask import request,Blueprint,jsonify
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import time
import json
from setup import get_event, get_station,getUser
from notification.FCMTest import getFCMtoken
Inform=Blueprint("Inform", __name__)
@Inform.route('/inform/<string:eventId>')
def informAll(eventId):
    userDb=getUser()
    eventDb=get_event()
    eventObj=eventDb.currentEvent.find_one({"eventId":eventId})
    hosts=eventObj["hosts"]
    participants=eventObj["participants"]
    eventAlluser=[]
    for i in range(len(hosts)):
        hostObject=userDb.auth.find_one({"userId":hosts[i]})
        hostFCM=hostObject["FCMToken"]
        eventAlluser.append(hostFCM)
    for i in range(len(participants)):
        participantsObject=userDb.auth.find_one({"userId":participants[i]})
        participantFCM=participantsObject["FCMToken"]
        eventAlluser.append(participantFCM)
    try:
        getFCMtoken(eventAlluser)
        return jsonify({"code":200,"msg":"Send notifications successful."})
    except:
        return jsonify({"code":404,"msg":"Send notifications fail."})
    # return jsonify(eventAlluser)