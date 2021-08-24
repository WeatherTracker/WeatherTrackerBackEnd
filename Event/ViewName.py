from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from setup import get_event, getUser
from Verification.TokenGenerator import decode_token
ViewName = Blueprint("ViewName", __name__)

@ViewName.route("/viewName")
def getName():
    eventId = request.args["eventId"]
    eventDb = get_event()
    userDb = getUser()
    eventobj = eventDb.currentEvent.find_one({"eventId": eventId})
    participants=eventobj["participants"]
    result=[]
    for i in participants:
        userobj = userDb.auth.find_one({"userId": i})
        result.append(userobj["userName"])
    return jsonify(result)
@ViewName.route("/levelUp",methods=['POST'])
def levelup():
    eventId = request.form["eventId"]
    eventDb = get_event()
    userDb = getUser()
    eventobj = eventDb.currentEvent.find_one({"eventId": eventId})
    participants=eventobj["participants"]
    try:
        for i in participants:
            print(i)
            eventDb.currentEvent.update_one({"eventId": eventId},{ "$push": { "hosts": i },"$pull": { "participants": i} })
        return jsonify("成功 levelUp")    
    except:
        return jsonify("levelUp 失敗")