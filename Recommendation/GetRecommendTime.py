from flask import request,Blueprint,jsonify,abort
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
from Recommendation.scheduleV3 import getTime
from Verification.TokenGenerator import decode_token
GetRecommendTime=Blueprint("GetRecommendTime", __name__)
@GetRecommendTime.route('/getRecommendTime',methods=['POST'])
def getData():
    token=request.form["userId"]
    eventId=request.form["eventId"]
    whiteList=request.form.getlist("whiteList")
    blackList=request.form.getlist("blackList")
    x=decode_token(token)
    if x=="False":
        abort(401)
    else:
        userId=x
    result=getTime(userId,eventId,whiteList,blackList)
    return jsonify(result)