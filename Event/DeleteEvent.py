from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import get_event,getUser
from notification.Inform import informAll
DeleteEvent=Blueprint("DeleteEvent", __name__)
@DeleteEvent.route("/deleteEvent/<string:eventId>",methods=['DELETE'])
def delete(eventId):
    # event=request.form
    eventDb=get_event()
    userDb=getUser()
    try:
        askEvent=eventDb.currentEvent.find_one({"eventId":eventId})
        informAll(eventId,askEvent["eventName"],"這個活動被刪除了!!!!")
        host=askEvent["hosts"]
        print(host)
        for i in range(len(host)):
            userDb.auth.update({ "userId":host[i]},{ "$pull": { "currentEvents": eventId } })
        eventDb.currentEvent.find_one_and_delete({"eventId":eventId})
    except:
        return jsonify({"code":404,"msg":"刪除活動失敗"})
    return jsonify({"code":200,"msg":"刪除活動成功"})