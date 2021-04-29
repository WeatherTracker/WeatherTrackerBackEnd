import sys
import time
import datetime
import concurrent.futures
from pymongo import MongoClient
import AccuCrawler_V3
# constant
baseURL = "https://www.accuweather.com"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


def distance(long, lati, doc):
    return (doc["經度"]-long)**2+(doc["緯度"]-lati)**2


def findStation(long, lati):
    client = MongoClient('localhost', 27017)
    db = client['test']
    collect = db["Accu_URLs"]
    min = sys.float_info.max
    for doc in collect.find({}):
        d = distance(long, lati, doc)
        if min > d:
            min = d
            area_name = doc["area"]
            area_link = doc["url"]
    return [area_name, area_link]


def getAccu(long, lati, target_date):
    return_list = []
    client = MongoClient('localhost', 27017)
    db = client['test']
    collect = db["Accu_data"]
    nearest_area = findStation(long, lati)
    today = datetime.datetime.today()
    day = (target_date-today).days
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(-3, 4):  # day
            if day+i < 7:
                continue
            temp_target_date = target_date+datetime.timedelta(days=i)
            doc = collect.find_one({"area": nearest_area[0], "date": {"$gte": temp_target_date, "$lt": temp_target_date+datetime.timedelta(days=1)}})
            if doc == None:
                future = executor.submit(AccuCrawler_V3.crawler, nearest_area[0], nearest_area[1], temp_target_date, day)
                futures.append(future)
            else:
                return_list.append(doc)
        for future in concurrent.futures.as_completed(futures):
            return_list.append(future.result())
            collect.insert_one(future.result())
    return return_list


if __name__ == "__main__":
    t1 = time.time()
    results = getAccu(121, 20, datetime.datetime(2021, 4, 15))
    t2 = time.time()
    print("耗時: "+str(t2-t1))
