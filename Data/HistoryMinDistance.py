from setup import get_station
import math
db = get_station()
def HistoryMinDistance(TimeData,now_lat,now_lon):
    TimeData=TimeData[0:4]
    # print(TimeData)
    year=int(TimeData)
    latestYear=int(TimeData)-6
    if(year<=latestYear):
        all_data=db.Station_list.find({"year":year-1})
    else:
        all_data=db.Station_list.find({"year":2015})
    inf = float('Inf')
    min_d=inf
    city=""
    SiteName=""
    for item in all_data:
        for location in item["datas"]:
            station_lat=location["緯度"]
            station_lon=location["經度"]
            x=float(now_lat)-station_lat
            y=float(now_lon)-station_lon
            distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
            if distance<min_d:
                min_d=distance
                city=location["城市"]
                SiteName=location["站名"]
            # print(item["datas"][location]["緯度"]+" "+item["datas"][location]["經度"])
    
    result=[]
    result.append(city)
    result.append(SiteName)
    
    print(result)
    return result
def WriteHistory(TimeData,now_lat,now_lon):
    result=HistoryMinDistance(TimeData,now_lat,now_lon)#傳回最近的測站的地區和縣市
    city=result[0]
    SiteName=result[1]
    year=int(TimeData[0:4])
    
    TimeData=TimeData[5:10].replace("-","/")
    print(TimeData)
    target_data=db.Station_history_data.find({"city": city,"name":SiteName,"year":year})
    result=HistoryMinDistance(TimeData,now_lat,now_lon)#傳回最近的測站的地區和縣市
    for i in target_data:
        temperature=i["datas"][TimeData]["氣溫(C)"]
        humidity=i["datas"][TimeData]["相對溼度(%)"]
        wind=i["datas"][TimeData]["風速(m/s)"]
        UV=i["datas"][TimeData]["日最高紫外線指數"]
    history={}
    history.update({"參考測站年分":year,"測站所在縣市":city,"測站名稱":SiteName,"氣溫":temperature,"相對溼度":humidity,"風速":wind,"日最高紫外線指數":UV})
    print(history)
    return history    