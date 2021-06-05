from pymongo import MongoClient
from bson.objectid import ObjectId
import json  
connect = MongoClient("mongodb://localhost:27017/calculated")
db= connect.calculated
historyData=db.Station_history_data
hotCounter=0
years=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
for j in years:
    print(j)
    station=db.Station_list.find_one({'year':j}).get('datas')
    for k in station:
        target={}
        if(type(k)==dict):
            if(type(db.Station_history_data.find_one({'name':k.get('站名'),'year':j}))==dict):
                #lastTarget=db.Station_history_data.find_one({'name':k.get('站名'),'year':j-1}).get('datas')
                target=db.Station_history_data.find_one({'name':k.get('站名'),'year':j}).get('datas')
            else:
                continue
        s=[0,0,0,0,0]
        new_tag=target.copy()
        last2High=20
        last2Low=20
        lastHigh=20
        lastLow=20
        for i in target:
            new_tag.get(i)['dynamicTags']=[]
            if type(target.get(i).get('最高氣溫(C)'))==float:
                if(target.get(i).get('最高氣溫(C)')>=36):
                    #炎熱寒冷標籤由於資料顆粒度較粗 皆採用當日最高溫計算
                    if(target.get(i).get('最高氣溫(C)')>=38):
                        if((lastHigh>=38)and(last2High>=38)):
                            new_tag.get(i).get('dynamicTags').append('炎熱(紅燈)')
                        else:
                            new_tag.get(i).get('dynamicTags').append('炎熱(橘燈)')
                    else:
                        new_tag.get(i).get('dynamicTags').append('炎熱(黃燈)')
            if (type(target.get(i).get('最高氣溫(C)'))==float)and(type(target.get(i).get('最低氣溫(C)'))==float):
                if((target.get(i).get('最高氣溫(C)')<=6) and (lastLow<=6)):
                    new_tag.get(i).get('dynamicTags').append('寒冷(紅燈)')
                else:
                    if(target.get(i).get('最低氣溫(C)')<=6):
                        new_tag.get(i).get('dynamicTags').append('寒冷(橘燈)')
                    else: 
                        if((target.get(i).get('最低氣溫(C)')<=10) and (target.get(i).get('最高氣溫(C)')<=12) and (lastHigh<=12)):
                            new_tag.get(i).get('dynamicTags').append('寒冷(橘燈)')
                        else: 
                            if (target.get(i).get('最低氣溫(C)')<=10):
                                new_tag.get(i).get('dynamicTags').append('寒冷(黃燈)')

            if target.get(i).get('日最高紫外線指數')!=None:
                if(target.get(i).get('日最高紫外線指數')>=8):
                    new_tag.get(i).get('dynamicTags').append('強紫外線')
        
            if target.get(i).get('相對溼度(%)')!=None:
                if(target.get(i).get('相對溼度(%)')>=70):
                    new_tag.get(i).get('dynamicTags').append('潮濕')

            if target.get(i).get('最小相對溼度(%)')!=None:
                if(target.get(i).get('最小相對溼度(%)')<=40):
                    new_tag.get(i).get('dynamicTags').append('乾燥')

            if target.get(i).get('最大陣風(m/s)')!=None:
                if(target.get(i).get('最大陣風(m/s)')>=10.8):
                    new_tag.get(i).get('dynamicTags').append('強風')
            last2High=lastHigh
            if target.get(i).get('最高氣溫(C)')!=None:
                lastHigh=target.get(i).get('最高氣溫(C)')
            else:
                lastHigh=20
            last2Low=lastLow
            if target.get(i).get('最低氣溫(C)')!=None:
                lastLow=target.get(i).get('最低氣溫(C)')
            else:
                lastLow=20


        db.Station_history_data.update_one(
                {"name" : k.get('站名'),'year':j},
                {"$set":{
                "datas":new_tag
                }
                },upsert=True)