from flask import jsonify,request,Blueprint,abort
from setup import get_event,getUser
from Verification.TokenGenerator import decode_token
InOrOutEvent=Blueprint("InOrOutEvent", __name__)
@InOrOutEvent.route("/inOrOutEvent",methods=['PUT'])
#讓使用者可以知道他是參加者或不是參加者
def participate():
    ask=request.form
    eventDb=get_event()
    userDb=getUser()
    eventId=ask["eventId"]
    token=ask["userId"]
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    action=ask["action"]
    if action=="True":
        try:
            event=eventDb.currentEvent.find_one({"eventId":eventId})
            eventDb.currentEvent.update_one({"eventId":eventId},{"$push":{"participants":userId}})
            user=userDb.auth.find_one({"userId":userId})
            currentEvents=user["currentEvents"]
            userDb.auth.update_one({"userId":userId},{"$push":{"currentEvents":eventId}})
            return jsonify({"code":200,"msg":"Participate in activities successful."})
        except:
            return jsonify({"code":404,"msg":"Participate in activities Flase!!!"})
    else:
        try:
            event=eventDb.currentEvent.find_one({"eventId":eventId})
            participants=event["participants"]
            participants.remove(userId)
            eventDb.currentEvent.update_one({"eventId":eventId},{"$set":{"participants":participants}})
            userDb.auth.update({ "userId":userId},{ "$pull": { "currentEvents":eventId } })
            return jsonify({"code":200,"msg":"Exit event successful."})
        except:
            return jsonify({"code":404,"msg":"Exit event Flase!!!"})