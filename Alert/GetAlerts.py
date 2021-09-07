from flask import request, jsonify, Blueprint
from pymongo import MongoClient
from setup import get_station
from datetime import datetime
from Alert.alert import getAlert
import time
GetAlerts = Blueprint("GetAlerts", __name__)

@GetAlerts.route("/getAlerts")
def getAllAlert():
    
    time_start=time.time()
    lat=float(request.args["latitude"])
    lon=float(request.args["longitude"])
    result=getAlert(lat,lon)
    # for i in result[0]:
    #     i["effective"]=datetime.strftime(i["effective"], "%Y-%m-%d %H:%M:%S")
    #     i["expires"]=datetime.strftime(i["expires"], "%Y-%m-%d %H:%M:%S")
    return result