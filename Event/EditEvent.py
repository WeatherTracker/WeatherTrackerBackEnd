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
    event["startTime"]=datetime.strptime(event["startTime"], "%Y-%m-%d %H:%M")
    event["endTime"]=datetime.strptime(event["endTime"], "%Y-%m-%d %H:%M")
    # host=event["hosts"]
    # try:
    #     for i in range(len(host)):
    #         db.user.update_one({"userId":host[i]},{"$set":{"currentEvents":event}})
    # except:
    #     return jsonify({"code":404,"msg":"Database failed to edit event."})
    try:
        db.currentEvent.update_one({"eventId":eventId},{"$set":event})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit event."})
    return jsonify({"code":200,"msg":"Database edit event successful."})
