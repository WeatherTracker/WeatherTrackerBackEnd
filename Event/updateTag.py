from pymongo import MongoClient#讀取MongoDB資料庫中的文件
from setup import get_event
from Event.eventTag import timeSegment
def updateTag():
    eventDb=get_event()
    allEventObj=eventDb.currentEvent.find({})
    for i in range(len(allEventObj)):
        # timeSegment("2021-06-05 12:30:00","2021-06-06 21:00:00",25.1505447,121.7735869)
        allEventObj[i]["dynamicTags"]=timeSegment(allEventObj[i]["startTime"],allEventObj[i]["endTime"],allEventObj[i]["latitude"],allEventObj[i]["longitude"])
        eventDb.currentEvent.update_one({"eventId":allEventObj[i]["eventId"]},{"$set":allEventObj[i]["dynamicTags"]})
    print("更新所有活動的 eventTags 成功!!!")