import json
from pymongo import MongoClient
from flask_pymongo import pymongo
from flask import jsonify,request,Blueprint
from itsdangerous import TimedJSONWebSignatureSerializer
from Recommendation.recommendPoint import nearest_ViewPoint
from Recommendation.recommendEvent import hobby_event
from Recommendation.SearchEvent import search_event
recommend = Blueprint('recommend',__name__)
@recommend.route('/recommendScene')
def recommandScene():
    y=request.args["longitude"]
    x=request.args["latitude"]
    return jsonify(nearest_ViewPoint(x,y))
@recommend.route('/searchEvent')
def searchEvent():
    keyword=request.args["input"]
    result=search_event(keyword)
    print(result)
    return jsonify(result)
@recommend.route('/recommendEvent',methods=['POST'])
def recommandEvent():
    targetUserToken=request.form.get("token")
    s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=36400)
    token=targetUserToken.split('\'')[1] 
    data = s.loads(token)
    targetUser=data.get('userId')
    client = MongoClient("localhost", 27017)
    hobbylist=client.user.auth.find_one({"userId":targetUser}).get("hobbies")
    y=request.form.get("latitude")
    x=request.form.get("longitude")
    result=[]
    for i in hobbylist:
        result=result+hobby_event(i,x,y)
    return jsonify(result)