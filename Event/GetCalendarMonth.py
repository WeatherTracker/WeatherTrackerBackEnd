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
    # print("這是token",token)
    x=decode_token(token)
    # print("這是x",x)
    if x=="False":
        abort(401)
    else:
        userId=x
    # print("這是我的userID",userId)
    user=userDb.auth.find_one({"userId":userId})
    start=datetime.strptime(month, "%Y-%m")
    end=datetime.strptime(month, "%Y-%m")
    end=end + relativedelta(months=1)
    # print(start)
    # print(end)
    date=set()
    user.pop("_id")
    print(user)
    if user["pastEvents"]!=None:
        pastEvents=user["pastEvents"]
        for i in range(len(pastEvents)):
            pastEventObj=eventDb.pastEvent.find_one({"eventId":pastEvents[i]})
            startTemp=pastEventObj["startTime"]
            endTemp=pastEventObj["endTime"]
            while startTemp<=endTemp:
                if startTemp>=start and startTemp<=end:
                    date.add(startTemp.strftime("%Y-%m-%d"))
                startTemp=startTemp+timedelta(days=1)
    if user["currentEvents"]!=None:
        currentEvents=user["currentEvents"]
        for i in range(len(currentEvents)):
            currentEventObj=eventDb.currentEvent.find_one({"eventId":currentEvents[i]})
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