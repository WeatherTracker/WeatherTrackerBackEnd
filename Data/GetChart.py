from flask import request,Blueprint,jsonify
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import datetime
import time
import json
from setup import get_station
from Data.MinDistance import CwsMinDistance,EpaMinDistance,Write_3Days,Write_3_To_7Days
from Data.HistoryMinDistance import HistoryMinDistance,WriteHistory

import schedule
import threading
GetChart=Blueprint("GetChart", __name__)
@GetChart.route('/getChart')
def getData():
    time_start=time.time()
    TimeData=request.args["day"]
    now_lat=request.args["latitude"]
    now_lon=request.args["longitude"]
    today = datetime.date.today()
    ask=datetime.datetime.strptime(TimeData,"%Y-%m-%d").date()
    print(ask)
    after_3days = today +datetime.timedelta(days = 3)
    after_7days = today +datetime.timedelta(days = 7)
    if ask<today:
        print("history")
        history=WriteHistory(TimeData,now_lat,now_lon)
        return jsonify(history)
    elif ask<after_3days:
        print("in 3 Days")
        data_3Days=Write_3Days(now_lat,now_lon)
        time_end=time.time()
        print("爬3天要花",time_end-time_start,"s")
        return jsonify(data_3Days)
    elif ask<after_7days:
        print("3-7 Days")
        data_7Days=Write_3_To_7Days(now_lat,now_lon)
        time_end=time.time()
        print("爬7天要花",time_end-time_start,"s")
        return jsonify(data_7Days)
    else:
        print("  >7 Days use ACCU")
        return "ACCU + history"

# getData("2021-03-26 23:59:59.628556","22.7254758","120.2628547")