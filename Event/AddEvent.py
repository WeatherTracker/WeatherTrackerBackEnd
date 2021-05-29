from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime
import uuid
AddEvent=Blueprint("AddEvent", __name__)
@AddEvent.route("/newEvent",methods=['Post'])
def create():
    event=request.json
    try:
        event["eventId"]=str(uuid.uuid4())
    except Exception as e:
        return jsonify({"msg":str(uuid.uuid4())})
    event["startTime"]=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    event["endTime"]=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    event["participants"]=[]
    db=get_event()
    host=event["hosts"]
    print(host)
    try:
        
        db.currentEvent.insert_one(event)
            # db.CurrentEvent.insert_one({
            #     "eventId":123,
            #     "eventName":eventName,
            #     "isPublic":isPublic,
            #     "latitude":latitude,
            #     "longitude":longitude,
            #     "startTime":startTime,
            #     "endTime":endTime,
            #     "participants":participants,
            #     "hosts":hosts,
            #     "isOutDoor":isOutDoor,
            #     "staticHobbyClass":staticHobbyClass,
            #     "staticHobbyTag":staticHobbyTag,
            #     "hostRemark":hostRemark,
            # })
    except:
        return jsonify({"code":404,"msg":"Database failed to add event."})
    # event.pop("_id")
    eventId=event["eventId"]
    for i in range(len(host)):
        userId= event["hosts"][i]
        user=db.user.find_one({"userId":userId})
        if user is not None:
            currentEvents=user["currentEvents"]
            # description.append({"eventId":event["eventId"],"eventName":event["eventName"],"startTime":event["startTime"],"endTime":event["endTime"]})
            currentEvents.append(eventId)
            db.user.update_one({"userId":userId},{"$set":{"currentEvents":currentEvents}})
    return jsonify({"code":200,"msg":"Database add event successful."})