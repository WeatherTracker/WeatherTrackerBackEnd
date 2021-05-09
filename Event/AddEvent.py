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
    try:
        db.user.insert_one({
            "userId":"a",
            "FCMToken":"123",
            "userName":"王小名",
            "currentEvents":[],
            "pastEvents":[],
            "AHPPreference":[],
            "freeTime":[],
            "hobbies":[]
        })
        db.user.insert_one({
            "userId":"b",
            "FCMToken":"123",
            "userName":"王中名",
            "currentEvents":[],
            "pastEvents":[],
            "AHPPreference":[],
            "freeTime":[],
            "hobbies":[]
        })
        db.user.insert_one({
            "userId":"c",
            "FCMToken":"123",
            "userName":"王大名",
            "currentEvents":[],
            "pastEvents":[],
            "AHPPreference":[],
            "freeTime":[],
            "hobbies":[]
        })
    except:
        return jsonify({"msg":"database user insert fail"})
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
    event.pop("_id")
    for i in range(len(host)):
        userId= event["hosts"][i]
        user=db.user.find_one({"userId":userId})
        if user is not None:
            description=user["currentEvents"]
            # description.append({"eventId":event["eventId"],"eventName":event["eventName"],"startTime":event["startTime"],"endTime":event["endTime"]})
            description.append(event)
            db.user.update_one({"userId":userId},{"$set":{"currentEvents":description}})
    return jsonify({"code":200,"msg":"Database add event successful."})