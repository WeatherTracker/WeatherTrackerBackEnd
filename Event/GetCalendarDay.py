from flask import request, jsonify, Blueprint, abort
from pymongo import MongoClient
from setup import get_event, getUser
from Verification.TokenGenerator import decode_token
import datetime
GetCalendarDay = Blueprint("GetCalendarDay", __name__)


@GetCalendarDay.route("/getCalendarDay")
def getDay():
    day = request.args["day"]
    token = request.args["userId"]
    x = decode_token(token)
    if x == "False":
        abort(401)
    else:
        userId = x
    eventDb = get_event()
    userDb = getUser()
    user = userDb.auth.find_one({"userId": userId})
    ask = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    today = datetime.date.today()
    result = []
    if ask < today:
        if len(user["pastEvents"]) != 0:
            event = user["pastEvents"]
            start = datetime.datetime.strptime(day, "%Y-%m-%d")
            end = start+datetime.timedelta(days=1)
            result = []
            # for i in range(len(event)):
            #     eventobj = eventDb.pastEvent.find_one({"eventId": event[i]})
            #     startTime = eventobj["startTime"]
            #     endTime = eventobj["endTime"]
            #     if (endTime >= start and endTime <= end) or (startTime >= start and startTime <= end) or (startTime <= start and endTime >= end):
            #         startTime = datetime.datetime.strftime(
            #             eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
            #         eventobj["startTime"] = startTime[:-3]
            #         endTime = datetime.datetime.strftime(
            #             eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
            #         eventobj["endTime"] = endTime[:-3]
            #         eventobj.pop("_id")
            #         eventobj["isAuth"] = False
            #         result.append(eventobj)
            for i in range(len(event)):
                eventobj = eventDb.pastEvent.find_one({"eventId": event[i]})
                startTime = eventobj["startTime"]
                endTime = eventobj["endTime"]
                if (endTime >= start and endTime < end) or (startTime >= start and startTime < end) or (startTime <= start and endTime > end):
                    startTime = datetime.datetime.strftime(
                        eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
                    eventobj["startTime"] = startTime[:-3]
                    endTime = datetime.datetime.strftime(
                        eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
                    eventobj["endTime"] = endTime[:-3]
                    eventobj.pop("_id")
                    eventobj["isAuth"] = False
                    result.append(eventobj)
    if len(user["currentEvents"]) != 0:
        event = user["currentEvents"]
        start = datetime.datetime.strptime(day, "%Y-%m-%d")
        end = start+datetime.timedelta(days=1)
        result = []
        # for i in range(len(event)):
        #     eventobj = eventDb.currentEvent.find_one({"eventId": event[i]})
        #     startTime = eventobj["startTime"]
        #     endTime = eventobj["endTime"]
        #     if (endTime >= start and endTime <= end) or (startTime >= start and startTime <= end) or (startTime <= start and endTime >= end):
        #         startTime = datetime.datetime.strftime(
        #         eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
        #         eventobj["startTime"] = startTime[:-3]
        #         endTime = datetime.datetime.strftime(eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
        #         eventobj["endTime"] = endTime[:-3]
        #         if userId == eventobj["hosts"][0]:
        #             eventobj["isAuth"] = True
        #         else:
        #             eventobj["isAuth"] = False
        #         eventobj.pop("_id")
        #         result.append(eventobj)
        for i in range(len(event)):
            eventobj = eventDb.currentEvent.find_one({"eventId": event[i]})
            startTime = eventobj["startTime"]
            endTime = eventobj["endTime"]
            if (endTime >= start and endTime < end) or (startTime >= start and startTime < end) or (startTime <= start and endTime > end):
                startTime = datetime.datetime.strftime(
                eventobj["startTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["startTime"] = startTime[:-3]
                endTime = datetime.datetime.strftime(eventobj["endTime"], "%Y-%m-%d %H:%M:%S")
                eventobj["endTime"] = endTime[:-3]
                if userId == eventobj["hosts"][0]:
                    eventobj["isAuth"] = True
                else:
                    eventobj["isAuth"] = False
                eventobj.pop("_id")
                result.append(eventobj)
    return jsonify(result)