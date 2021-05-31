from flask import request,jsonify,Blueprint
from pymongo import MongoClient
from setup import getUser
from Verification.TokenGenerator import decode_token
ViewProfile=Blueprint("ViewProfile", __name__)
@ViewProfile.route("/viewProfile")
def view():
    token=request.args["userId"]
    if decode_token(token)==False:
        return None
    else:
        userId=decode_token(token)
    userDb=getUser()
    userObj=userDb.auth.find_one({"userId":userId})
    userObj.pop("_id")
    print(userObj)
    return jsonify(userObj)