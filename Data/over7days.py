from pymongo import MongoClient
def chartOver7Days(now_lat,now_lon,date):
    startDate=str(date.month).zfill(2)+'/'+str(date.day).zfill(2)
    client = MongoClient("localhost", 27017)
    calculatedDb = client.calculated
    station_list=calculatedDb.Station_list.find_one({"year":2021}).get("datas")
    near=10000
    nearId=""
    for i in station_list:
        if(pow(i.get('經度')-float(now_lon),2)+pow(i.get('緯度')-float(now_lat),2))<near:
            near=pow(i.get('經度')-float(now_lon),2)+pow(i.get('緯度')-float(now_lat),2)
            nearId=i.get("站號")
    target_data=calculatedDb.calculated.find_one({"id":nearId}).get("datas")
    myCity = calculatedDb.calculated.find_one({"id":nearId}).get("city")
    myName = calculatedDb.calculated.find_one({"id":nearId}).get("name")
    read=0
    resultObj={}
    avgTemp=[]
    rain=[]
    humidity=[]
    wind=[]
    UV=[]
    leftDay=0

    for i in target_data:
        if(i==startDate):
            leftDay=7
        if(leftDay>=1):
            leftDay-=1
            avgTemp.append({"time":i ,"value":target_data.get(i).get("氣溫(C)").get("avg")})
            rain.append({"time":i ,"value":target_data.get(i).get("降水量(mm)").get("avg")})
            humidity.append({"time":i ,"value":target_data.get(i).get("相對溼度(%)").get("avg")})
            wind.append({"time":i ,"value":target_data.get(i).get("風速(m/s)").get("avg")})
            UV.append({"time":i ,"value":target_data.get(i).get("日最高紫外線指數").get("avg")})
    resultObj["temperature"]=avgTemp
    resultObj["POP"]=rain
    resultObj["humidity"]=humidity
    resultObj["windSpeed"]=wind
    resultObj["UV"]=UV
    resultObj["city"]=myCity
    resultObj["area"]=myName
    resultObj["siteName"]=""

    return resultObj


    


    