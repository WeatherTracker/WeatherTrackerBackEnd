from flask import request,Blueprint,jsonify
from pymongo import MongoClient#讀取MongoDB資料庫中的文件
import datetime
# from datetime import datetime,timedelta
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

    
# def updater():
#     schedule.every().day.at('00:37').do(Get_3Days_Data,0)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# if __name__ == '__main__':
    # schedule.every().day.at('15:08').do(Get_3Days_Data,0)
    # schedule.every().day.at('15:08').do(Get_7Days_Data,0)
    # schedule.every().day.at('15:08').do(Get_PM2_5Data)
    # while True:
    #     app.debug = True
    #     time.sleep(1)
        
    # t = threading.Thread(target=updater)
    # t.start()
    # app.debug = True
    # port = int(os.environ.get('PORT', 5603))
    # app.run(host='0.0.0.0', port=port)
    # t.join()
    # update3Days()