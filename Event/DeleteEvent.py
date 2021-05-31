from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event,getUser
DeleteEvent=Blueprint("DeleteEvent", __name__)
@DeleteEvent.route("/deleteEvent",methods=['DELETE'])
def delete():
    event=request.form
    eventDb=get_event()
    userDb=getUser()
    try:
        askEvent=eventDb.currentEvent.find_one({"eventId":event["eventId"]})
        host=askEvent["hosts"]
        print(host)
        for i in range(len(host)):
            userDb.auth.update({ "userId":host[i]},{ "$pull": { "currentEvents": event["eventId"] } })
        eventDb.currentEvent.find_one_and_delete({"eventId":event["eventId"]})
    except:
        return jsonify({"code":404,"msg":"Database failed to delete event."})
    return jsonify({"code":200,"msg":"Database delete event successful."})