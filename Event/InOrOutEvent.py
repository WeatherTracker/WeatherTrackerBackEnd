from flask import jsonify,request,Blueprint,abort
from setup import get_event,getUser
from Verification.TokenGenerator import decode_token
InOrOutEvent=Blueprint("InOrOutEvent", __name__)
@InOrOutEvent.route("/inOrOutEvent",methods=['POST'])
#讓使用者可以知道他是參加者或不是參加者
def participate():
    eventDb=get_event()
    userDb=getUser()
    eventId=request.form["eventId"]
    token=request.form["userId"]
    print("eventId is "+eventId)
    print("userId is "+token)
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    action=request.form["action"]
    eventObj=eventDb.currentEvent.find_one({"eventId":eventId})
    identity="somePeople"
    for i in range(len(eventObj["hosts"])):
        if userId==eventObj["hosts"][i]:
            identity="host"
            break
    if identity!="host":
        for i in range(len(eventObj["participants"])):
            if userId==eventObj["participants"][i]:
                identity="participant"
                break
    print("要參加嗎",action)
    print("身分是",identity)
    if action=="true" and identity=="somePeople":
        try:
            event=eventDb.currentEvent.find_one({"eventId":eventId})
            eventDb.currentEvent.update_one({"eventId":eventId},{"$push":{"participants":userId}})
            user=userDb.auth.find_one({"userId":userId})
            currentEvents=user["currentEvents"]
            userDb.auth.update_one({"userId":userId},{"$push":{"currentEvents":eventId}})
            return jsonify({"code":200,"msg":"參加活動成功"})
        except:
            return jsonify({"code":404,"msg":"參加活動成功"})
    if action=="true" and (identity=="participant" or identity=="host"):
        return jsonify({"code":404,"msg":"你已經參加過這個活動了"})
    if action=="false":
        try:
            event=eventDb.currentEvent.find_one({"eventId":eventId})
            participants=event["participants"]
            participants.remove(userId)
            eventDb.currentEvent.update_one({"eventId":eventId},{"$set":{"participants":participants}})
            userDb.auth.update({ "userId":userId},{ "$pull": { "currentEvents":eventId } })
            return jsonify({"code":200,"msg":"離開活動成功"})
        except:
            return jsonify({"code":404,"msg":"離開活動失敗"})