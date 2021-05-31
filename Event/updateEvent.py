from datetime import datetime
from setup import get_event,getUser
def updateEvent():
    eventDb=get_event()
    uesrDb=getUser()
    now=datetime.now()
    result=eventDb.currentEvent.find({'endTime': {'$lt': now}})
    for i in result:
        try:
            for j in uesrDb.auth.find({}):
                if i["eventId"] in j["currentEvents"]:
                    uesrDb.auth.update_one(j,{ "$push": { "pastEvents": i["eventId"] },"$pull": { "currentEvents": i["eventId"]} })
            eventDb.pastEvent.insert_one(i)
            eventDb.currentEvent.delete_one(i)
            print("EveryDay Database updateEvent Success!!!")
        except:
            print("EveryDay Database updateEvent Flase!!!")