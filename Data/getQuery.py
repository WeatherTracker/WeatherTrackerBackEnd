from flask import Flask,request,render_template,Blueprint
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import os
from flask import jsonify
import datetime
from datetime import datetime,timedelta
import time
import json
# from Event.min_distance import CWS_min_distance
# from Event.min_distance import EPA_min_distance
# from Event.min_distance import write_3Days
# from Event.min_distance import write_3_to_7Days

from min_distance import CWS_min_distance,EPA_min_distance,write_3Days,write_3_to_7Days
from history_min_distance import history_min_distance,write_history
getQuery = Blueprint('getquery',__name__)
# client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
# db = client.station
@getQuery.route('/456')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"
@app.route('/getChart/<string:TimeData>/<float:now_lat>/<float:now_lon>')
def getData(TimeData,now_lat,now_lon):
    now=datetime.now()
    print(now)
    ask=datetime.strptime(TimeData,"%Y-%m-%d %H:%M:%S.%f")
    print(ask)
    after_3days = now +timedelta(days = 3)
    after_7days = now +timedelta(days = 7)
    if ask<now:
        print("history")
        history=write_history(TimeData,now_lat,now_lon)
        return jsonify(history)
    elif ask<after_3days:
        print("in 3 Days")
        data_3Days=write_3Days(now_lat,now_lon)
        return jsonify(data_3Days)
    elif ask<after_7days:
        print("3-7 Days")
        data_7Days=write_3_to_7Days(now_lat,now_lon)
        return jsonify(data_7Days)
    else:
        print("  >7 Days use ACCU")
        return "ACCU + history"