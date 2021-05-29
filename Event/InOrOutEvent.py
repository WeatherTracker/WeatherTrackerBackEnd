from flask import jsonify,request,Blueprint
from setup import get_event
InOrOutEvent=Blueprint("InOrOutEvent", __name__)
@InOrOutEvent.route("/inOrOutEvent",methods=['PUT'])

def participate():
    ask=request.form
    db=get_event()
    eventId=ask["eventId"]
    userId=ask["userId"]
    action=ask["action"]
    if action=="True":
        try:
            event=db.currentEvent.find_one({"eventId":eventId})
            db.currentEvent.update_one({"eventId":eventId},{"$push":{"participants":userId}})
            user=db.user.find_one({"userId":userId})
            currentEvents=user["currentEvents"]
            db.user.update_one({"userId":userId},{"$push":{"currentEvents":eventId}})
            return jsonify({"code":200,"msg":"Participate in activities successful."})
        except:
            return jsonify({"code":404,"msg":"Participate in activities Flase!!!"})
    else:
        try:
            event=db.currentEvent.find_one({"eventId":eventId})
            participants=event["participants"]
            participants.remove(userId)
            db.currentEvent.update_one({"eventId":eventId},{"$set":{"participants":participants}})
            db.user.update({ "userId":userId},{ "$pull": { "currentEvents":eventId } })
            return jsonify({"code":200,"msg":"Exit event successful."})
        except:
            return jsonify({"code":404,"msg":"Exit event Flase!!!"})