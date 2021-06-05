from setup import get_calculated
import math
import datetime
calculatedDb = get_calculated()
def HistoryMinDistance(TimeData,now_lat,now_lon):
    TimeData=TimeData[0:4]
    year=int(TimeData)
    all_data=calculatedDb.Station_list.find({"year":year})
    inf = float('Inf')
    min_d=inf
    for item in all_data:
        for location in item["datas"]:
            station_lat=location["緯度"]
            station_lon=location["經度"]
            x=float(now_lat)-station_lat
            y=float(now_lon)-station_lon
            distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
            if distance<min_d:
                min_d=distance
                stationId=location["站號"]
    print(stationId)
    return stationId
def WriteHistory(TimeData,now_lat,now_lon):
    stationId=HistoryMinDistance(TimeData,now_lat,now_lon)#傳回最近的測站ID
    # yesterday2=datetime.datetime.strptime(TimeData, "%Y-%m-%d")+datetime.timedelta(days=-2)
    # yesterday=datetime.datetime.strptime(TimeData, "%Y-%m-%d")+datetime.timedelta(days=-1)
    # # today=datetime.strptime(TimeData, "%Y-%m-%d")
    # tomorrow=datetime.datetime.strptime(TimeData, "%Y-%m-%d")+datetime.timedelta(days=1)
    # tomorrow2=datetime.datetime.strptime(TimeData, "%Y-%m-%d")+datetime.timedelta(days=2)
    resultObj={}
    
    queryDate = datetime.datetime.strptime(TimeData, "%Y-%m-%d")#datetime
    targetDate=queryDate+datetime.timedelta(days=0)
    print(targetDate)
    TimeData = datetime.datetime.strftime(targetDate,"%Y-%m-%d")#string
    # todayTimeData=TimeData
    # y=" 00:00:00"
    # todayTimeData=todayTimeData+y
    year=targetDate.year
    timeKey=str(targetDate.month).zfill(2)+"/"+str(targetDate.day).zfill(2)
    target_data=calculatedDb.Station_history_data.find_one({"id":stationId,"year":year})

    temperature=[{"time":TimeData,"value":target_data["datas"][timeKey]["氣溫(C)"]}]
    humidity=[{"time":TimeData,"value":target_data["datas"][timeKey]["相對溼度(%)"]}]
    windSpeed=[{"time":TimeData,"value":target_data["datas"][timeKey]["風速(m/s)"]}]
    UV=[{"time":TimeData,"value":target_data["datas"][timeKey]["日最高紫外線指數"]}]
    
    history={"city":target_data["city"],"siteName":target_data["name"],"area":"","temperature":temperature,"humidity":humidity,"windSpeed":windSpeed,"UV":UV}
    
    return history