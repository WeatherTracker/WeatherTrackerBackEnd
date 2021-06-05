from pymongo import MongoClient
import datetime
import json

titles = ["測站氣壓(hPa)", "海平面氣壓(hPa)", "測站最高氣壓(hPa)", "測站最低氣壓(hPa)", "氣溫(C)", "最高氣溫(C)",	"最低氣溫(C)", "露點溫度(℃)", "相對溼度(%)", "最小相對溼度(%)",  "風速(m/s)", "風向(360degree)", "最大陣風(m/s)",
          "最大陣風風向(360degree)", "降水量(mm)", "降水時數(hour)", "最大十分鐘降水量(mm)", "最大六十分鐘降水量(mm)", "日照時數(hour)", "日照率(%)", "全天空日射量(MJ/M^2)", "能見度(km)", "A型蒸發量(mm)", "日最高紫外線指數", "總雲量(0~10)"]
############################################ 記得修改 ##########################################
client = MongoClient('localhost', 27017)
db = client['station']
collect = db['stationListTest']
# collect2 = db['Station_history_data']
collect2 = db['hisTest']
# collect3 = db['Station_caculated_data']
collect3 = db['calTest']
############################################ 記得修改 ##########################################


def newDoc(dic_datas, target_date):
    foo = {}
    for json_data in titles:
        foo[json_data] = {"avg": dic_datas["datas"][json_data], "std": None, "count": 0}
    collect3.insert_one({"city": dic_datas["城市"],
                         "id": dic_datas["站號"],
                         "name": dic_datas["站名"],
                         "info": {"startDate": target_date},
                         "datas": {target_date.strftime("%m/%d"): foo}})


def newInnerDoc(dic_datas, target_date):
    foo = {}
    for json_data in titles:
        foo[json_data] = {"avg": dic_datas["datas"][json_data], "std": None, "count": 0}
    collect3.update_one({"id": dic_datas["站號"]},
                        {"$set": {"datas."+target_date.strftime("%m/%d"): foo}}, True)
    return foo
