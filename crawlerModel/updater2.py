import datetime
import time
import statistics
import concurrent.futures
from pymongo import MongoClient
from crawlerModel.StationDownloader_V6 import *
from crawlerModel.newStation import *
from crawlerModel.StationCrawler import *
titles = ["測站氣壓(hPa)", "海平面氣壓(hPa)", "測站最高氣壓(hPa)", "測站最低氣壓(hPa)", "氣溫(C)", "最高氣溫(C)",	"最低氣溫(C)", "露點溫度(℃)", "相對溼度(%)", "最小相對溼度(%)",  "風速(m/s)", "風向(360degree)", "最大陣風(m/s)",
          "最大陣風風向(360degree)", "降水量(mm)", "降水時數(hour)", "最大十分鐘降水量(mm)", "最大六十分鐘降水量(mm)", "日照時數(hour)", "日照率(%)", "全天空日射量(MJ/M^2)", "能見度(km)", "A型蒸發量(mm)", "日最高紫外線指數", "總雲量(0~10)"]


def new_calculator(dic, x):  # 計算新的標準差平均值
    avg = dic["avg"]
    std = dic["std"]
    count = dic["count"]
    n_count = count+1
    if n_count == 1:
        n_avg = round(x, 2)
        n_std = None
    elif n_count == 2:
        n_avg = round((avg*count+x)/(count+1), 2)
        n_std = round(statistics.sqrt((1/n_count)*(x-avg)**2), 2)
    else:
        n_avg = round((avg*count+x)/(count+1), 2)
        n_std = round(statistics.sqrt(((n_count-2)/(n_count-1))*(std**2)+(1/n_count)*(x-avg)**2), 2)
    return {"avg": n_avg, "std": n_std, "count": n_count}


def data_updater(today):
    t1 = time.time()
    # updateStationList(today.year)
    ############################################ 記得修改 ##########################################
    client = MongoClient('localhost', 27017)
    db = client['calculated']
    # collect = db['Station_list']
    collect = db['Station_list']
    # collect2 = db['Station_history_data']
    collect2 = db['Station_history_data']
    # collect3 = db['Station_caculated_data']
    collect3 = db['calculated']
    ############################################ 記得修改 ##########################################

    # 更新歷史資料
    count = 0
    yesterday = today+datetime.timedelta(days=-1)
    json_data = collect.find_one({"year": yesterday.year})
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:  # 可調整Thread數量，100大約330秒
        futures = []
        for station in json_data["datas"]:
            # call 爬蟲模組
            if station["資料起始日期"] <= yesterday and station["撤站日期"] == None:
                count = count+1
                url = URL_Combiner(station["站號"], station["站名"], yesterday)
                future = executor.submit(crawler, url, yesterday, station["城市"], station["站名"], station["站號"])
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            dic_datas = future.result()
            oneDay_data = dic_datas["datas"]
            collect2.update_one({"city": dic_datas["城市"], "id": dic_datas["站號"], "name": dic_datas["站名"], "year": yesterday.year},
                                {'$set': {'datas.' + yesterday.strftime("%m/%d"): oneDay_data}}, True)
            # 更新統計結果
            target_doc = collect3.find_one({"id": dic_datas["站號"]})
            if target_doc == None:  # 新測站
                newDoc(dic_datas, yesterday)
            for i in range(-3, 4):  # 前後+3天
                target_date = yesterday+datetime.timedelta(days=i)
                try:  # 舊日期
                    target_data = target_doc["datas"][target_date.strftime("%m/%d")]
                except Exception as e:  # 新日期
                    target_data = newInnerDoc(dic_datas, target_date)
                # print(target_date)
                # print(target_data)
                for title in titles:  # 每一個因素
                    # print(data[title])
                    # print(target_data[title])
                    if oneDay_data[title] == None:
                        continue
                    # 算數學
                    temp = new_calculator(target_data[title], oneDay_data[title])
                    # 更新
                    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)  # ex :2021/10/16 04:87:63 => 2021/10/16 00:00:00
                    collect3.update_one({"id": dic_datas["站號"]}, {"$set": {"info.endDate": yesterday, "info.updateTime": today}})
                    collect3.update_one({"id": dic_datas["站號"]}, {"$set": {"datas."+target_date.strftime("%m/%d")+"."+title: temp}})
                    # break  # 只找一項
                # print(today, i)
                # break  # 只找一天(前後+3的一天)
            print(dic_datas["站名"], "completed")
            # break  # 只跑一個測站
    t2 = time.time()
    print(count, "個測站已更新，花費"+str(t2-t1)+"秒\n")
# 每天9:30執行任務
# schedule.every().day.at('09:30').do(data_updater, datetime.datetime.today())


def weatherDataUpdater():
    print("開始爬蟲")
    data_updater(datetime.datetime.today())
    
if __name__=="__main__":
    start = datetime.datetime(2021, 6, 4)
    end = datetime.datetime(2021, 6, 7)
    t1 = time.time()
    while start <= end:
        print(start)
        data_updater(start)  # DB只吃datetime不吃date
        start += datetime.timedelta(days=1)
    t2 = time.time()
    print("")
    print("總花費"+str(t2-t1)+"秒")
    print(datetime.datetime.today())