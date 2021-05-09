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
    event=user["currentEvents"]
    start=datetime.strptime(month, "%Y-%m")
    end=datetime.strptime(month, "%Y-%m")
    end=end + relativedelta(months=1)
    print(start)
    print(end)
    date=set()
    for i in range(len(event)):
        startTemp=event[i]["startTime"]
        endTemp=event[i]["endTime"]
        while startTemp<=endTemp:
            if startTemp>=start and startTemp<=end:
                date.add(startTemp.strftime("%Y-%m-%d"))
            startTemp=startTemp+timedelta(days=1)
    end2=time.time()
    print(end2-begin)
    return jsonify(sorted(date))
 
# datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
# dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
 
# data_list = []
# while datestart<=dateend:
#     data_list.append(datestart.strftime('%Y-%m-%d')) 
#     datestart+=datetime.timedelta(days=1)
# print(data_list)