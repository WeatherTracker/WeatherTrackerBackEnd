from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import time
GetCalendarMonth=Blueprint("GetCalendarMonth", __name__)
@GetCalendarMonth.route("/getCalendarMonth")
def getDate():
    begin=time.time()
    month=request.args["month"]
    userId=request.args["userId"]
    db=get_event()
    user=db.user.find_one({"userId":userId})
    
    start=datetime.strptime(month, "%Y-%m")
    end=datetime.strptime(month, "%Y-%m")
    end=end + relativedelta(months=1)
    print(start)
    print(end)
    date=set()
    pastEvents=user["pastEvents"]
    currentEvents=user["currentEvents"]
    for i in range(len(pastEvents)):
        pastEventObj=db.pastEvent.find_one({"eventId":pastEvents[i]})
        startTemp=pastEventObj["startTime"]
        endTemp=pastEventObj["endTime"]
        while startTemp<=endTemp:
            if startTemp>=start and startTemp<=end:
                date.add(startTemp.strftime("%Y-%m-%d"))
            startTemp=startTemp+timedelta(days=1)
    for i in range(len(currentEvents)):
        currentEventObj=db.currentEvent.find_one({"eventId":currentEvents[i]})
        startTemp=currentEventObj["startTime"]
        endTemp=currentEventObj["endTime"]
        while startTemp<=endTemp:
            if startTemp>=start and startTemp<=end:
                date.add(startTemp.strftime("%Y-%m-%d"))
            startTemp=startTemp+timedelta(days=1)
    end2=time.time()
    print("回傳當月活動總共花 ",str(end2-begin)," 秒")
    return jsonify(sorted(date))
 
# datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
# dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
 
# data_list = []
# while datestart<=dateend:
#     data_list.append(datestart.strftime('%Y-%m-%d')) 
#     datestart+=datetime.timedelta(days=1)
# print(data_list)