from flask import request,Blueprint,jsonify,abort
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
from Recommendation.scheduleV3 import getTime
from Verification.TokenGenerator import decode_token
GetRecommendTime=Blueprint("GetRecommendTime", __name__)
@GetRecommendTime.route('/getRecommendTime')
def getData():
    token=request.args["userId"]
    eventId=request.args["eventId"]
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    # result=getTime()
    return "1"
    # return jsonify(result)