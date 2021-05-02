from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
DeleteEvent=Blueprint("DeleteEvent", __name__)
@DeleteEvent.route("/deleteEvent",methods=['DELETE'])
def delete():
    event=request.json
    db=get_event()
    # try:
    #     askEvent=db.currentEvent.find_one_and_delete({"eventId":event["eventId"]})
    # except:
    #     return jsonify({"code":404,"msg":"Database failed to delete event."})
    try:
        askEvent=db.currentEvent.find_one_and_delete({"eventId":event["eventId"]})
    except:
        return jsonify({"code":404,"msg":"Database failed to delete event."})
    return jsonify({"code":200,"msg":"Database delete event successful."})