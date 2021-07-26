from pymongo import MongoClient
import json
client = MongoClient("localhost", 27017)
pastEvent=client.event.pastEvent.find()
pastEvent2={}
for i in pastEvent:
    tags=i.get('dynamicTags')
    for j in tags:
        if(j=="強紫外線"):
            tags.pop(tags.index(j))
            tags.append("過量級(紅燈)")
    i['dynamicTags']=tags
    client.event.pastEvent2.insert_one(i)

    
    