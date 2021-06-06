import json
from Event.eventTag import timeSegment
def transfer(dynamicTag):
    with open("transferTag.json","r",encoding="utf-8") as obj:
        all=json.load(obj)
        type=all[dynamicTag]
        return type
def suggest(staticTag,dynamic):
    with open("suggest.json","r",encoding="utf-8") as obj:
        test=json.load(obj)
        resultObj={}
        allPeople=[]
        participant=[]
        host=[]
        add=","
        for i in range(len(dynamic)):
            dynamicTag=dynamic[i]
            typeTag=transfer(dynamicTag)
            result=test[staticTag]["dynamicTags"][typeTag]
            allPeople.append(result["all"])
            participant.append(result["participant"])
            host.append(result["host"])
        allRemain=add.join(allPeople)
        participantRemain=add.join(participant)
        hostRemain=add.join(host)
        resultObj.update({"all":allRemain,"participant":participantRemain,"host":hostRemain})
        print(resultObj)
        return resultObj
# tag=timeSegment("2021-06-05 12:30:00","2021-06-12 21:00:00",25.1505447,121.7735869)
# suggest("戶外",tag)