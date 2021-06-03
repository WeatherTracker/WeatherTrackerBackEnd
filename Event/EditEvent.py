from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from flask import abort
EditEvent=Blueprint("EditEvent", __name__)
@EditEvent.route("/editEvent",methods=['PUT'])
def edit():
    event=request.json
    eventDb=get_event()
    eventId=event["eventId"]
    eventName=event["eventName"]
    hostRemark=event["hostRemark"]
    staticHobbyClass=event["staticHobbyClass"]
    staticHobbyTag=event["staticHobbyTag"]
    longitude=event["longitude"]
    latitude=event["latitude"]
    isOutDoor=event["isOutDoor"]
    isPublic=event["isPublic"]
    startTime=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    endTime=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    print(event)
    try:
        eventDb.currentEvent.update_one({"eventId":eventId},{"$set":{"eventId":eventId,"eventName":eventName,"hostRemark":hostRemark,"staticHobbyClass":staticHobbyClass,"staticHobbyTag":staticHobbyTag,"longitude":longitude,"latitude":latitude,"isOutDoor":isOutDoor,"isPublic":isPublic,"startTime":startTime,"endTime":endTime}})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit event."})
    return jsonify({"code":200,"msg":"Database edit event successful."})