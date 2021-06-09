from pymongo import MongoClient#讀取MongoDB資料庫中的文件
from setup import get_event
from Event.eventTag import timeSegment
from Event.suggest import suggest
from datetime import datetime
from notification.Inform import informAll
def updateTag():
    eventDb=get_event()
    now = datetime.now()
    allEventObj=eventDb.currentEvent.find({"endTime":{"$gte":now}})
    for event in allEventObj:
        # timeSegment("2021-06-05 12:30:00","2021-06-06 21:00:00",25.1505447,121.7735869)
        event["startTime"]=datetime.strftime(event["startTime"],"%Y-%m-%d %H:%M")
        event["endTime"]=datetime.strftime(event["endTime"],"%Y-%m-%d %H:%M")
        oldDynamicTag=event["dynamicTags"]
        event["dynamicTags"]=timeSegment(event["startTime"],event["endTime"],event["latitude"],event["longitude"])
        if event["isOutDoor"]==True:
            staticTag="戶外"
        else:
            staticTag="室內"
        event["suggestions"]=suggest(staticTag,event["dynamicTags"])
        eventDb.currentEvent.update_one({"eventId":event["eventId"]},{"$set":{"dynamicTags":event["dynamicTags"],"suggestions":event["suggestions"]}})
        if len(event["dynamicTags"])>len(oldDynamicTag):
            informAll(event["eventId"],event["eventName"],"這個活動天氣變壞了")
    print("更新所有活動的 eventTags 成功!!!")