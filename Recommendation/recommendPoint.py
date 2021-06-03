from pymongo import MongoClient
import math
from setup import get_event
def nearest_ViewPoint(lat,lon):
    eventDb=get_event()
    viewPointArray=eventDb.viewPoint.find_one({"Listname":"1"}).get("Infos").get("Info")
    result=[]
    sample={}
    resultNumber=5
    for viewPoint in viewPointArray:
        y=float(lat)-viewPoint.get("Py")
        x=float(lon)-viewPoint.get("Px")
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
    ask=[]
    for i in range(len(result)):
        result_dict={}
        result_dict.update({"Name":result[i]["Name"],"Description":result[i]["Description"],"Tel":result[i]["Tel"],"Add":result[i]["Add"],"Orgclass":result[i]["Orgclass"],"Ticketinfo":result[i]["Ticketinfo"],"Remarks":result[i]["Remarks"],"Changetime":result[i]["Changetime"],"Px":result[i]["Px"],"Py":result[i]["Py"]})
        ask.append(result_dict)
    return ask