from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import get_event,getUser
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from Verification.TokenGenerator import decode_token
import time
GetCalendarMonth=Blueprint("GetCalendarMonth", __name__)
@GetCalendarMonth.route("/getCalendarMonth")
def getDate():
    begin=time.time()
    month=request.args["month"]
    token=request.args["userId"]
    eventDb=get_event()
    userDb=getUser()
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    user=userDb.auth.find_one({"userId":userId})
    start=datetime.strptime(month, "%Y-%m")
    end=datetime.strptime(month, "%Y-%m")
    end=end + relativedelta(months=1)
    date=set()
    user.pop("_id")
    print(user)
    if len(user["pastEvents"])!=0:
        pastEvents=user["pastEvents"]
        pastEventObjs = eventDb.pastEvent.find({"eventId":{"$in":pastEvents}})
        for event in pastEventObjs:
            startTemp=event["startTime"]
            endTemp=event["endTime"]
            while startTemp<=endTemp:
                if startTemp>=start and startTemp<=end:
                    date.add(startTemp.strftime("%Y-%m-%d"))
                startTemp=startTemp+timedelta(days=1)
    if len(user["currentEvents"])!=0:
        currentEvents=user["currentEvents"]
        currentEventObjs = eventDb.currentEvent.find({"eventId":{"$in":currentEvents}})
        for event in currentEventObjs:
            startTemp=event["startTime"]
            endTemp=event["endTime"]
            while startTemp<=endTemp:
                if startTemp>=start and startTemp<=end:
                    date.add(startTemp.strftime("%Y-%m-%d"))
                startTemp=startTemp+timedelta(days=1)
    end2=time.time()
    print("回傳當月活動總共花 ",str(end2-begin)," 秒")
    print(sorted(date))
    return jsonify(sorted(date))