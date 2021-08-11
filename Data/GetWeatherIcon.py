from flask import request,Blueprint,jsonify
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import json
from Data.MinDistance import CwsMinDistance,EpaMinDistance,weatherIcon
GetWeatherIcon=Blueprint("GetWeatherIcon", __name__)

@GetWeatherIcon.route('/getWeatherIcon')
def getIcon():
    now_lat=request.args["latitude"]
    now_lon=request.args["longitude"]
    result=weatherIcon(now_lat,now_lon)
    print(result)
    return jsonify(result)

# getData("2021-03-26 23:59:59.628556","22.7254758","120.2628547")