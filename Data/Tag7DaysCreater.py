import json
def fun1(condition,data,priority,resultTag):
    relation=condition["relation"]
    value=condition["value"]
    if relation==">=":
        for i in range(1,len(data)):
            if data[i]==None:
                resultTag[i-1]=0
            elif data[i]>=value:
                resultTag[i-1]=priority
    elif relation=="<=":
        for i in range(1,len(data)):
            if data[i]==None:
                resultTag[i-1]=0
            elif data[i]<=value:
                resultTag[i-1]=priority
    # elif relation==">":
    #     for i in range(1,len(data)):
    #         if data[i]>value:
    #             resultTag[i-1]=priority
    # print(condition,"priority : "+str(priority))
    # print(resultTag)
    # print("relation & value")
def fun2(condition,data,priority,resultTag,tagCondition):
    relation=condition["relation"]
    value=condition["value"]
    duration=condition["duration"]
    if tagCondition=="炎熱":
        flag1=0
        flag2=0
        flag3=0
        for i in range(1,3):
            if data[i]==None:
                continue
            elif data[i]>=value:
                flag1=1
                break
        for i in range(3,5):
            if data[i]==None:
                continue
            elif data[i]>=value:
                flag2=1
                break
        for i in range(5,7):
            if data[i]==None:
                continue
            elif data[i]>=value:
                flag3=1
                break
        # print(flag1,flag2,flag3)
        if flag1==1 and flag2==1 and flag3==1:
            for i in range(len(resultTag)):
                resultTag[i]=priority
    elif tagCondition=="寒冷":
        count=0
        for i in range(1,len(data)):
            if data[i]==None:
                count=0
                continue
            if data[i]<=value:
                count+=1
            else:
                count=0
            if count==2:
                for j in range(i-2,i):
                    resultTag[j]=priority
            elif count>2:
                resultTag[i-1]=priority
    # print(condition,"priority : "+str(priority))
    # print(resultTag)
    # print("relation & value & duration")
def fun3(condition,data,priority,resultTag):
    relation=condition["relation"]
    value=condition["value"]
    duration=condition["duration"]
    min=condition["min"]
    count=0
    for i in range(1,len(data)):
        if data[i]==None:
            count=0
            continue
        flag=0
        if data[i]<=value:
            count+=1
        else:
            count=0
        if count>=2:
            for j in range(i-1,i+1):
                if data[j]<=min:
                    flag=1#溫度小於等於min
            if flag==0:
                count=0
        if flag==1:
            if count==2:
                for j in range(i-2,i):
                    resultTag[j]=priority
            elif count>2:
                resultTag[i-1]=priority
    # print(condition,"priority : "+str(priority))
    # print(resultTag)
    # print("relation & value & duration & min")
def fun4():
    print("Condition is not find")
def tagCreater(data):
    # print(data)
    with open('tag.json','r',encoding='utf-8')as obj:
        ans=json.load(obj)
        resultTag=[]
        for i in range(len(data)-1):
            resultTag.append(0)
        # print(resultTag)
        tag=[]
        for item in ans:
            if item["targetAttribute"] == data[0]:
                tags=item.get("tags")
                for i in tags:
                    result=i["conditions"]
                    priority=i["priority"]
                    tag.append(i["tag"])
                    for condition in result:
                        if "duration" not in condition and "min" not in condition:
                            fun1(condition,data,priority,resultTag)
                        elif "duration" in condition and "min" not in condition:
                            fun2(condition,data,priority,resultTag,item["tag"])
                        elif "duration" in condition and "min" in condition:
                            fun3(condition,data,priority,resultTag)
                        else:
                            fun4()
        #         print("----------------------------------")
        # print(tag)
        for i in range(len(resultTag)):
            if resultTag[i]!=0:
                resultTag[i]=tag[resultTag[i]-1]
            else:
                resultTag[i]=None
        resultTag.insert(0,data[0])
        # print("標籤判斷結果")
        # print(resultTag)
        return resultTag
def add7DaysTagToDB(data,result):
    part=1
    for i in data:
        for j in i["data"]:
            if "平均溫度" in j and result[0]=="temperature":
                j.update({"tag":result[part]})
                part=part+1
            elif "平均相對濕度" in j and result[0]=="humidity":
                j.update({"tag":result[part]})
                part=part+1
            elif "最大風速" in j and result[0]=="windSpeed":
                j.update({"tag":result[part]})
                part=part+1
            elif "12小時降雨機率" in j and result[0]=="POP":
                j.update({"tag":result[part]})
                part=part+1
            elif "紫外線指數" in j and result[0]=="UV":
                j.update({"tag":result[part]})
                part=part+1
    return data
# if __name__ =='__main__':
#     # data=['temperature', 28, 26, 26, 25, 24, 29, 30, 30, 28, 27, 26, 25, 25, 29, 30]
#     # data=['temperature', 14, 5, 8, 10, 25, 16, 14, 13, 15, 15, 15, 15, 15, 29, 30]
#     # data=['temperature',6,6,6,6,6,6,6,6,6,7,6,36,6,6,6]
#     data=['temperature',18,12,10,12,10,12,10,12,12,12,6,36,6,6,6]
#     # data=["POP",20,20,20,25,20,25,0,0,10,0,0,50,62,70,80]
#     # data=["humidity",20,20,20,25,70,25,0,0,70,0,0,50,62,70,80]
#     # data=["UV",2,5,7,10,1,1,1]
#     # data=["AQI",100,80,70,70]
#     # data=["windSpeed",6,2,20,25,7,25,0,0,20,0,0,20,22,10,10]
#     tagCreater(data)