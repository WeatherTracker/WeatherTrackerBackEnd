from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime
import uuid
AddEvent=Blueprint("AddEvent", __name__)
@AddEvent.route("/newEvent",methods=['Post'])
def create():
    event=request.json
    print(event)
    try:
        event["eventId"]=str(uuid.uuid4())
    except Exception as e:
        return jsonify({"msg":str(uuid.uuid4())})
    event["startTime"]=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    event["endTime"]=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    event["participants"]=[]
    db=get_event()
    # try:
    #     db.user.insert_one({
    #         "userId":"a",
    #         "FCMToken":"123",
    #         "userName":"王小名",
    #         "currentEvents":[],
    #         "pastEvents":[],
    #         "AHPPreference":[],
    #         "freeTime":[],
    #         "hobbies":[]
    #     })
    # except:
    #     return jsonify({"msg":"database user insert fail"})
    print(event["hosts"][0])
    userId= event["hosts"][0]
    
    user=db.user.find_one({"userId":userId})
    if user is not None:
        description=user["currentEvents"]
        description.append({"eventName":event["eventName"],"startTime":event["startTime"],"endTime":event["endTime"]})
        db.user.update_one({"userId":"a"},{"$set":{"currentEvents":description}})
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
    return jsonify({"code":200,"msg":"Database add event successful."})