from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from setup import get_station
from datetime import datetime
GetAlerts = Blueprint("GetAlerts", __name__)

@GetAlerts.route("/getAlerts")
def getAlert():
    stationDb=get_station()
    result=stationDb.Alerts.find_one({})
    # for i in result[0]:
    #     i["effective"]=datetime.strftime(i["effective"], "%Y-%m-%d %H:%M:%S")
    #     i["expires"]=datetime.strftime(i["expires"], "%Y-%m-%d %H:%M:%S")
    return jsonify(result["alerts"])

