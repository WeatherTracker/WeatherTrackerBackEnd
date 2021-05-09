from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
EditEvent=Blueprint("EditEvent", __name__)
@EditEvent.route("/editEvent",methods=['PUT'])
def edit():
    event=request.json
    db=get_event()
    eventId=event["eventId"]
    host=event["hosts"]
    # event.pop("eventId")
    try:
        for i in range(len(host)):
            db.user.update_one({"userId":host[i]},{"$set":{"currentEvents":event}})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit event."})
    try:
        db.currentEvent.update_one({"eventId":eventId},{"$set":event})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit event."})
    return jsonify({"code":200,"msg":"Database edit event successful."})
