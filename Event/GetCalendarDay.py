from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
# from datetime import datetime,timedelta
import datetime
GetCalendarDay=Blueprint("GetCalendarDay", __name__)
@GetCalendarDay.route("/getCalendarDay")
def getDay():
    day=request.args["day"]
    userId=request.args["userId"]
    db=get_event()
    user=db.user.find_one({"userId":userId})
    ask=datetime.datetime.strptime(day,"%Y-%m-%d").date()
    today = datetime.date.today()
    if ask>=today:
        event=user["currentEvents"]
        start=datetime.datetime.strptime(day, "%Y-%m-%d")
        # print(type(start))
        end=start+datetime.timedelta(days=1)
        result=[]
        for i in range(len(event)):
            eventobj=db.currentEvent.find_one({"eventId":event[i]})
            startTime=eventobj["startTime"]
            endTime=eventobj["endTime"]
            if (endTime>=start and endTime<=end) or (startTime>=start and startTime<=end) or (startTime<=start and endTime>=end):
                startTime=datetime.datetime.strftime(eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["startTime"]=startTime[:-3]
                endTime=datetime.datetime.strftime(eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["endTime"]=endTime[:-3]
                eventobj.pop("_id")
                result.append(eventobj)
    else:
        event=user["pastEvents"]
        start=datetime.datetime.strptime(day, "%Y-%m-%d")
        # print(type(start))
        end=start+datetime.timedelta(days=1)
        result=[]
        for i in range(len(event)):
            eventobj=db.pastEvent.find_one({"eventId":event[i]})
            startTime=eventobj["startTime"]
            endTime=eventobj["endTime"]
            if (endTime>=start and endTime<=end) or (startTime>=start and startTime<=end) or (startTime<=start and endTime>=end):
                startTime=datetime.datetime.strftime(eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["startTime"]=startTime[:-3]
                endTime=datetime.datetime.strftime(eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["endTime"]=endTime[:-3]
                eventobj.pop("_id")
                result.append(eventobj)
    return jsonify(result)