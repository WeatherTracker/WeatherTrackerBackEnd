from pymongo import MongoClient
client = MongoClient("localhost", 27017)
pastDb=client.event.pastEvent
for i in range(50):
    sampleEvent={"endTime":{"date":"2021-06-09T16:00:00.000Z"},
        "eventName":"冬季盃",
        "hostRemark":"海大康樂館",
        "hosts":["dbe3ffed-da60-4a6a-8365-2885ed4e3d4a"],
        "isOutDoor":False,
        "isPublic":True,
        "latitude":25.1505447,
        "longitude":121.7757756,
        "startTime":{"date":"2021-06-09T13:00:00.000Z"},
        "staticHobbyClass":"視聽類",
        "staticHobbyTag":"KTV",
        "eventId":"ad26b7b6-6066-498c-a1d9-3fc5c4bc48d9",
        "participants":[],
        "dynamicTags":["寒冷(黃燈)","潮濕"],}
    pastDb.insert_one(sampleEvent)
