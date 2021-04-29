from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event
from datetime import datetime,timedelta
# import datetime
from dateutil.relativedelta import relativedelta
GetCalendarMonth=Blueprint("GetCalendarMonth", __name__)
@GetCalendarMonth.route("/getCalendarMonth")
def getDate():
    month=request.args["month"]
    userId=request.args["userId"]
    print(userId)
    db=get_event()
    user=db.user.find_one({"userId":userId})
    event=user["currentEvents"]
    start=datetime.strptime(month, "%Y-%m")
    end=datetime.strptime(month, "%Y-%m")
    end=end + relativedelta(months=1)
    print(start)
    print(end)
    date=[]
    # print(start)
    # print(end)
    for i in range(len(event)):
        startTemp=event[i]["startTime"]
        endTemp=event[i]["endTime"]
        
        while startTemp<=endTemp:
            # print(bool(startTemp<=endTemp))
            if startTemp>=start and startTemp<=end:
                date.append(startTemp.strftime("%Y-%m-%d"))
                startTemp=startTemp+timedelta(days=1)
    print(date)
            
    return jsonify({"eventsOnlyTime":list(set(date))})
# start='2019-01-01'
# end='2019-03-7'
 
# datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
# dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
 
# data_list = []
# while datestart<=dateend:
#     data_list.append(datestart.strftime('%Y-%m-%d')) 
#     datestart+=datetime.timedelta(days=1)
# print(data_list)