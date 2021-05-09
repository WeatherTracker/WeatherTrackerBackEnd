from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime,timedelta
GetCalendarDay=Blueprint("GetCalendarDay", __name__)
@GetCalendarDay.route("/getCalendarDay")
def getDay():
    day=request.args["day"]
    userId=request.args["userId"]
    db=get_event()
    user=db.user.find_one({"userId":userId})
    event=user["currentEvents"]
    start=datetime.strptime(day, "%Y-%m-%d")
    end=start+timedelta(days=1)
    result=[]
    for i in range(len(event)):
        startTime=event[i]["startTime"]
        endTime=event[i]["endTime"]
        if (endTime>=start and endTime<=end) or (startTime>=start and startTime<=end) or (startTime<=start and endTime>=end):
            event[i]["startTime"]=datetime.strftime(event[i]["startTime"], "%Y-%m-%d %H:%M:%S")
            event[i]["endTime"]=datetime.strftime(event[i]["endTime"], "%Y-%m-%d %H:%M:%S")
            result.append(event[i])
    return jsonify(result)