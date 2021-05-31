from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import getUser
from Verification.TokenGenerator import decode_token
EditProfile=Blueprint("EditProfile", __name__)
@EditProfile.route("/editProfile",methods=['PUT'])
def edit():
    profile=request.form
    userName=profile["userName"]
    AHPPreference=profile["AHPPreference"]
    freeTime=profile["freeTime"]
    hobbies=profile["hobbies"]
    token=profile["userId"]
    if decode_token(token)==False:
        return None
    else:
        userId=decode_token(token)
    userDb=getUser()
    userObj=userDb.auth.find_one({"userId":userId})
    profile["email"]=userObj["email"]
    profile["FCMToken"]=userObj["FCMToken"]
    profile["currentEvent"]=userObj["currentEvent"]
    profile["pastEvent"]=userObj["pastEvent"]
    profile["password"]=userObj["password"]
    try:
        userDb.auth.update_one({"userId":userId},{"$set":profile})
    except:
        return jsonify({"code":404,"msg":"Database failed to edit profile."})
    return jsonify({"code":200,"msg":"Database edit profile successful."})
    # profile["past"]