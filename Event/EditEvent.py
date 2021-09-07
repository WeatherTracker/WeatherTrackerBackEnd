from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import get_event
from datetime import datetime
from Event.eventTag import timeSegment
from Event.suggest import suggest
from notification.Inform import informAll
EditEvent=Blueprint("EditEvent", __name__)
@EditEvent.route("/editEvent",methods=['PUT'])
def edit():
    event=request.json
    print(event)
    eventDb=get_event()
    eventId=event["eventId"]
    eventObj=eventDb.currentEvent.find_one({"eventId":eventId})
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
        informAll(eventId,eventName,"主辦者修改活動了")
        if len(dynamicTags)>len(eventObj["dynamicTags"]):
            informAll(eventId,eventName,"這個活動天氣變壞了")
    except:
        return jsonify({"code":404,"msg":"修改活動失敗"})
    return jsonify({"code":200,"msg":"修改活動成功"})