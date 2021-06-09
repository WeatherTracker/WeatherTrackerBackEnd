from pymongo import MongoClient
import math
from flask import request,jsonify,Blueprint
from fuzzywuzzy import fuzz
#from setup import get_event
def search_event(keyWord):
    hobbyList=["健行","賞鳥","散步","旅遊","賽車","開車兜風","騎單車",'網球','羽球','博弈','桌球',"聚餐","釣魚",
    "游泳","水上活動","拖曳傘","撞球","保齡球","棒球","籃球","高爾夫球","排球","打拳","靜坐","有氧","健身","瑜珈","登山"
    ,"健行","慢跑","跑步","彈奏樂器","舞蹈","攝影","書法","藝文展覽","表演欣賞","手工藝","閱讀","園藝","上網","電競","桌遊"
    "益智遊戲","密室逃脫","博弈","電視","錄影帶","電影","KTV","聽音樂","泡湯","SPA","按摩","遊樂園","娛樂中心","逛街購物",
    "下午茶","禮拜","團康","親子活動","打掃","睡覺","做家事"]
    client = MongoClient("localhost", 27017)
    eventDb=client.event
    recommendEvent=eventDb.currentEvent.find({"isPublic":True})
    searchResult=[]
    for j in hobbyList:
        if(fuzz.partial_ratio(j,keyWord))>=50:
            hobbyEvent=eventDb.currentEvent.find({"staticHobbyTag":j,"isPublic":True})
            for k in hobbyEvent:
                print(k)
                k['ratio']=fuzz.partial_ratio(keyWord,j)
                searchResult.append(k)
    for i in recommendEvent:
        if(fuzz.partial_ratio(keyWord, i.get("eventName"))>=50):
            i['ratio']=fuzz.partial_ratio(keyWord, i.get("eventName"))
            if not (i in searchResult):
                searchResult.append(i)
    #searchResult.sort(key=lambda s: s.get('ratio'))
    for i in searchResult:
        i.pop("ratio")
        i.pop("_id")
        i["startTime"]=i.get("startTime").strftime("%Y-%m-%d %H:%M")
        i["endTime"]=i.get("endTime").strftime("%Y-%m-%d %H:%M")
    print(searchResult)
    return searchResult 