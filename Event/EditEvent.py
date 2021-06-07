from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import get_event
from datetime import datetime
from Event.eventTag import timeSegment
from Event.suggest import suggest
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
    dynamicTags=timeSegment(event["startTime"],event["endTime"],event["latitude"],event["longitude"])
    if event["isOutDoor"]==True:
        staticTag="戶外"
    else:
        staticTag="室內"
    suggestions=suggest(staticTag,dynamicTags)

    startTime=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    endTime=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    try:
        eventDb.currentEvent.update_one({"eventId":eventId},{"$set":{"eventId":eventId,"eventName":eventName,"hostRemark":hostRemark,"staticHobbyClass":staticHobbyClass,"staticHobbyTag":staticHobbyTag,"longitude":longitude,"latitude":latitude,"isOutDoor":isOutDoor,"isPublic":isPublic,"startTime":startTime,"endTime":endTime,"dynamicTags":dynamicTags,"suggestions":suggestions}})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit event."})
    return jsonify({"code":200,"msg":"Database edit event successful."})