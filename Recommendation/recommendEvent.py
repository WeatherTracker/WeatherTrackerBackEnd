from pymongo import MongoClient
import math
def nearest_ViewPoint(lat,lon,resultNumber=5):
    calculated = MongoClient("localhost", 27017)
    db = calculated.client.viewPoint
    viewPointArray=db.find_one({"Listname":"1"}).get("Infos").get("info")
    result=[]
    sample={}
    for viewPoint in viewPointArray:
        x=lat-viewPoint.get("latitude")
        y=lon-viewPoint.get("longitude")
        distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
        viewPoint["distance"]=distance
        target=0
        if(len(result)<resultNumber):
            result.append(viewPoint)
            for i in result:
                if i.get("distance")<result[target].get("distance"):
                    target=result.index(i)
        else:
            if(distance<=result[target].get("distance")):
                del result[target]
                result.append(viewPoint)
                for i in result:
                    if result[target].get("distance")>i.get("distance"):
                        target=result.index(i)
    print(result)
    return(result)
nearest_ViewPoint(121.7735869,25.1505495)
        


    