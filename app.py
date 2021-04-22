from flask import Flask,request,render_template
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import os
from flask import jsonify
import datetime
from datetime import datetime,timedelta

import time
import json
from setup import create_app
from setup import get_station
from Data.MinDistance import CwsMinDistance,EpaMinDistance,Write_3Days,Write_3_To_7Days
from Data.HistoryMinDistance import HistoryMinDistance,WriteHistory
# client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
# db = client.station
app = create_app()
db = get_station()
app.config["JSON_AS_ASCII"] = False
@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"
@app.route('/getChart')
def getData():
    time_start=time.time()
    TimeData=request.args["day"]
    now_lat=request.args["latitude"]
    now_lon=request.args["longitude"]
    now=datetime.now()
    print(now)
    ask=datetime.strptime(TimeData,"%Y-%m-%d %H:%M:%S.%f")
    print(ask)
    after_3days = now +timedelta(days = 3)
    after_7days = now +timedelta(days = 7)
    if ask<now:
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
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5603))
    app.run(host='0.0.0.0', port=port)