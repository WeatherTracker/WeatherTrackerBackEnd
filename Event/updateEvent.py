from datetime import datetime
from setup import get_event
def updateEvent():
    db=get_event()
    now=datetime.now()
    result=db.currentEvent.find({'endTime': {'$lt': now}})
    for i in result:
        try:
            for j in db.user.find({}):
                if i["eventId"] in j["currentEvents"]:
                    db.user.update_one(j,{ "$push": { "pastEvents": i["eventId"] },"$pull": { "currentEvents": i["eventId"]} })
            db.pastEvent.insert_one(i)
            db.currentEvent.delete_one(i)
            print("EveryDay Database updateEvent Success!!!")
        except:
            print("EveryDay Database updateEvent Flase!!!")