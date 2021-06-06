from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import get_event,getUser
from datetime import datetime
import uuid
from Verification.TokenGenerator import decode_token
from Event.eventTag import timeSegment
from Event.suggest import suggest
AddEvent=Blueprint("AddEvent", __name__)
@AddEvent.route("/newEvent",methods=['Post'])
def create():
    event=request.json
    try:
        event["eventId"]=str(uuid.uuid4())
    except Exception as e:
        return jsonify({"msg":str(uuid.uuid4())})
    
    event["participants"]=[]
    dynamicTags=timeSegment(event["startTime"],event["endTime"],float(event["latitude"]),float(event["longitude"]))
    event["dynamicTags"]=dynamicTags
    if event["isOutDoor"]==True:
        staticTag="戶外"
    else:
        staticTag="室內"
    event["suggestions"]=suggest(staticTag,dynamicTags)
    event["startTime"]=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    event["endTime"]=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    eventDb=get_event()
    userDb=getUser()
    hosts=[]
    token=event["hosts"]
    for i in range(len(token)):
        x=decode_token(token[i])
        if x=="False":
            abort(401)
        else:
            hosts.append(x)
    event["hosts"]=hosts
    try:
        eventDb.currentEvent.insert_one(event)
    except:
        return jsonify({"code":404,"msg":"Database failed to add event."})
    eventId=event["eventId"]
    for i in range(len(hosts)):
        userId= hosts[i]
        user=userDb.auth.find_one({"userId":userId})
        if user is not None:
            currentEvents=user["currentEvents"]
            currentEvents.append(eventId)
            userDb.auth.update_one({"userId":userId},{"$set":{"currentEvents":currentEvents}})
    return jsonify({"code":200,"msg":"Database add event successful."})