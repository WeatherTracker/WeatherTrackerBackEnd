from pymongo import MongoClient
import math
from flask import request,jsonify,Blueprint
from setup import get_event
RecommendEvent=Blueprint("RecommendEvent", __name__)
@RecommendEvent.route("/recommendEvent")
def nearest_ViewPoint():
    eventDb=get_event()
    latitude=request.args["latitude"]
    longitude=request.args["longitude"]
    resultNumber=5
    viewPointArray=eventDb.viewPoint.find_one({"listName":"1"})
    result=[]
    sample={}
    for viewPoint in range(len(viewPointArray["Infos"]["Info"])):
        # print(viewPoint)
        x=latitude-viewPointArray["Infos"]["Info"][viewPoint]["latitude"]
        y=longitude-viewPointArray["Infos"]["Info"][viewPoint]["longitude"]
        distance=math.sqrt(abs(x)**(2)+abs(y)**(2))
        viewPointArray["Infos"]["Info"][viewPoint]["distance"]=distance
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
    return jsonify(result)
# nearest_ViewPoint(121.7735869,25.1505495)