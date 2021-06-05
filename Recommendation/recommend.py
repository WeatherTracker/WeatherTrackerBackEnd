import json
from flask_pymongo import pymongo
from flask import jsonify,request,Blueprint
from Recommendation.recommendPoint import nearest_ViewPoint
recommend = Blueprint('recommend',__name__)
@recommend.route('/recommendScene')
def recommandScene():
    y=request.args["longitude"]
    x=request.args["latitude"]
    return jsonify(nearest_ViewPoint(x,y))