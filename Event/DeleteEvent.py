from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
DeleteEvent=Blueprint("DeleteEvent", __name__)
@DeleteEvent.route("/deleteEvent",methods=['DELETE'])
def delete():
    event=request.form
    db=get_event()
    try:
        askEvent=db.currentEvent.find_one({"eventId":event["eventId"]})
        host=askEvent["hosts"]
        print(host)
        for i in range(len(host)):
            db.user.update({ "userId":host[i]},{ "$pull": { "currentEvents": { "eventId":event["eventId"] } } })
        db.currentEvent.find_one_and_delete({"eventId":event["eventId"]})
    except:
        return jsonify({"code":404,"msg":"Database failed to delete event."})
    return jsonify({"code":200,"msg":"Database delete event successful."})