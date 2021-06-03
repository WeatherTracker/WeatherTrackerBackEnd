from flask import request,jsonify,Blueprint,abort
from pymongo import MongoClient
from setup import getUser
from Verification.TokenGenerator import decode_token
ViewProfile=Blueprint("ViewProfile", __name__)
@ViewProfile.route("/getProfile")
def view():
    token=request.args["userId"]
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    userDb=getUser()
    userObj=userDb.auth.find_one({"userId":userId})
    userObj.pop("_id")
    userObj.pop("email")
    userObj.pop("password")
    userObj.pop("userId")
    print(userObj)
    return jsonify(userObj)