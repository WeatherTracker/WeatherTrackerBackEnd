from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import getUser
from Verification.TokenGenerator import decode_token
EditProfile=Blueprint("EditProfile", __name__)
@EditProfile.route("/editProfile",methods=['PUT'])
def edit():
    profile=request.json
    print(profile)
    userName=profile["userName"]
    AHPPreference=profile["AHPPreference"]
    freeTime=profile["freeTime"]
    hobbies=profile["hobbies"]
    barValue=profile["barValue"]
    token=profile["userId"]
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    userDb=getUser()
    try:
        userDb.auth.update_one({"userId":userId},{"$set":{"userName":userName,"AHPPreference":AHPPreference,"freeTime":freeTime,"hobbies":hobbies,"barValue":barValue}})
    except:
        return jsonify({"code":404,"msg":"個人資料修改失敗"})
    return jsonify({"code":200,"msg":"個人資料修改成功"})