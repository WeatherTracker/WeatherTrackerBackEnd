from pymongo import MongoClient
from datetime import datetime
import json
from setup import get_calculated
db=get_calculated()
targetEvent=db.event.find_one({"eventID":"event01"})
locate=targetEvent.get("locate")
stationList=db.Station_list.find_one({"year":2020}).get("datas")
totalFar=1000
nearestStationID=""
for i in stationList:
    far=pow(locate.get("x")-i.get("經度"),2)+pow(locate.get("y")-i.get("緯度"),2)
    if far<totalFar:
       totalFar=far
       nearestStationID=i.get("站名")
print(nearestStationID)
time=targetEvent.get("start_time")
timeString=datetime.strftime(time,"%Y %m/%d %H:%M:%S")
timeArray=timeString.split(" ")
station=db.Station_history_data.find_one({"name":nearestStationID,'year':int(timeArray[0])}).get('datas')
print(timeArray[1])
print (station[timeArray[1]])
dynamicTags= (station[timeArray[1]].get('dynamicTags'))
eventTags=targetEvent.get('tags')
print(eventTags[1])
comment=db.comment.find_one({"tags":"tags"}).get(eventTags[0]).get('staticTags').get(eventTags[1]).get(dynamicTags[0]).get(eventTags[2])
print(comment)




