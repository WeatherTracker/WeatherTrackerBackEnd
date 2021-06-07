from flask.json import jsonify
from pymongo import MongoClient
import numpy as np
import datetime
from Data.MinDistance import Write_3Days,Write_3_To_7Days
from setup import get_event,getUser
client = MongoClient('localhost', 27017)
eventDb = get_event()
userDb=getUser()
db_currentEvent = eventDb['currentEvent']
# db_API = db['API']
db_user = userDb['auth']

# data2 = db_API.find_one({"name": "sample2"})
# data2 = data2["content"]
# data2=Write_3Days(now_lat,now_lon)

# data7 = db_API.find_one({"name": "sample7"})
# data7 = data7["content"]
# data7=Write_3_To_7Days(now_lat,now_lon)

# day2 = {"AQI": 24, "POP": 6, "UV": 24, "humidity": 3, "temperature": 3, "windSpeed": 3}
day2 = {"POP": 6, "UV": 24, "humidity": 3, "temperature": 3, "windSpeed": 3}
day7 = {"POP": 12, "UV": 24, "humidity": 12, "temperature": 12, "windSpeed": 12}
table = None
bundary = None


def getBlockIndex(date,data2):
    firstBlock=datetime.datetime.strptime(data2["POP"][0]["time"],"%Y-%m-%d %H:%M:%S")
    if firstBlock.hour == 0 or firstBlock.hour == 12:
        firstBlock = firstBlock - datetime.timedelta(hours=6)
    distance = date - firstBlock
    distance = distance.days*24 + distance.seconds/3600
    distance = int(distance)  # 片段開始時間離第一個API多遠(小時)
    index = distance//3+1
    return index


def createTable(data2,data7):
    global table
    global bundary
    table = []
    temp=datetime.datetime.strptime(data2["temperature"][-1]["time"],"%Y-%m-%d %H:%M:%S")
    bundary = temp+datetime.timedelta(hours=3)
    print("bundary", bundary)
    for k in day2.keys():
        row = []
        if k == "POP":
            for i in data2[k]:
                if i["tag"] != None:
                    row += 2 * [1]
                else:
                    row += 2 * [0]
        elif k == "UV":
            for i in data2[k]:
                if i["tag"] != None:
                    row += 8 * [1]
                else:
                    row += 8 * [0]
        else:
            for i in data2[k]:
                if i["tag"] != None:
                    row += [1]
                else:
                    row += [0]
        table.append(row)

    for k in day7.keys():
        row = []
        if k != "UV":
            for i in data7[k]:
                temp=datetime.datetime.strptime(i["time"],"%Y-%m-%d %H:%M:%S")
                if temp < bundary:
                    continue
                if i["tag"] != None:
                    row += 4 * [1]
                else:
                    row += 4 * [0]
            if k == "POP":
                table[0] += row
            elif k == "humidity":
                table[2] += row
            elif k == "temperature":
                table[3] += row
            elif k == "windSpeed":
                table[4] += row
    table[1] += [0, 0, 0, 0]
    table = np.array(table)
    table = table.sum(axis=0)
    table = np.insert(table, 0, 0, axis=0)
    table = np.cumsum(table)


def divideBlock(blockStart, blockEnd):
    resultList = []
    sHour = blockStart.hour
    eHour = blockEnd.hour
    if sHour < eHour:  # 沒換日
        while blockStart+datetime.timedelta(hours=eHour-sHour) <= blockEnd:
            resultList.append({"blockStart": blockStart,
                               "blockEnd": blockStart.replace(hour=eHour)})
            blockStart += datetime.timedelta(days=1)
    else:  # 換日
        while blockStart+datetime.timedelta(hours=24+eHour-sHour) <= blockEnd:
            resultList.append({"blockStart": blockStart,
                               "blockEnd": (blockStart+datetime.timedelta(days=1)).replace(hour=eHour)})
            blockStart += datetime.timedelta(days=1)
    return resultList


def judgeByWeather(resultList,data2):
    sum = 0
    total = 0
    for i in resultList:
        s = getBlockIndex(i["blockStart"],data2)
        e = getBlockIndex(i["blockEnd"],data2)
        total += (e-s+1)*7
        try:
            sum += table[e]-table[s-1]
        except Exception:
            sum += table[-1]-table[s-1]
    # print("sum", sum)
    # print("tagsSum", total)
    # print("天氣好: ", (total - sum) / total * 100)
    try:
        result=(total - sum) / total * 100
        return result
    except:
        return 0

def judgeByReserve(resultList, windowSize, participants):
    users = db_user.find({"userId": {"$in": participants}})
    sum = 0
    total = 0
    for participant in users:
        for i in resultList:
            timeStamp = i["blockStart"]
            blockEnd = i["blockEnd"]
        # timeStamp = blockStart
            while timeStamp < blockEnd:
                if timeStamp.hour >= 6:  # 過濾凌晨
                    weekno = timeStamp.weekday()
                    block = timeStamp.hour // 6 - 1  # 早上、下午、晚上
                    total += 1
                    if participant["freeTime"][weekno][block]:
                        sum += 1
                timeStamp += datetime.timedelta(hours=6)
    try:
        # print("保留度: ", sum/total*100)
        if users.count()==0:
            return 0.5
        else:
            return sum/total*100
    except Exception:  # 完全在凌晨舉辦的活動
        # print("完全在凌晨舉辦", 0)
        return 0


def judgeByRationality(blockStart, whiteList, blackList,eventStart):
    bias = 0
    today = datetime.datetime.now()  # 要改成now
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    for row in whiteList:
        h = int(row[0][:2])
        m = int(row[0][3:])
        h2 = int(row[1][:2])
        m2 = int(row[1][3:])
        if (blockStart.hour > h or (blockStart.hour == h and blockStart.minute >= m)) and (blockStart.hour < h2 or (blockStart.hour == h2 and blockStart.minute < m2)):
            bias += 0.5
            break
    for row in blackList:
        h = int(row[0][:2])
        m = int(row[0][3:])
        h2 = int(row[1][:2])
        m2 = int(row[1][3:])
        if (blockStart.hour > h or (blockStart.hour == h and blockStart.minute >= m)) and (blockStart.hour < h2 or (blockStart.hour == h2 and blockStart.minute < m2)):
            bias += 0.5
            break

    # if blockStart.hour<eventStart.hour+1 and  blockStart.hour>eventStart.hour-1:
    #     bias += 0.5
    return 0.5+bias
    # whiteList = whiteList - blockStart
    # blackList = blackList - blockStart
    # whiteMin = np.min(abs(whiteList))
    # blackMin = np.min(abs(blackList))
    # whiteDistance = whiteMin.days*24 + whiteMin.seconds/3600
    # blackDistance = blackMin.days*24 + blackMin.seconds/3600
    # if abs(whiteDistance) <= 0.5 or abs(blackDistance) <= 0.5:  # 是白名單或黑名單
    #     if whiteMin < blackMin:  # 白
    #         return 1.0
    #     else:  # 黑
    #         return 0.0
    # else:  # 普通的時間
    #     return 0.5
    # dis1 = blockStart - whiteList
    # dis1 = dis1.days*24 + dis1.seconds/3600
    # result = abs(dis1)
    # maxDist = max(result, maxDist)
    # print("合理性: ", result)
    # return result


def calculate(list1, list2, list3, AHPPreference):
    return np.round(np.dot(AHPPreference, [list1, list2, list3]), 2)


def listPrinter(L):
    for i in range(len(L)):
        print("{0:10.2f}".format(L[i]), end='')
        if (i+1) % 12 == 0:
            print("")
    print("")


def showBlockTime(startTime, index, windowSize):
    s1 = datetime.datetime.strftime(startTime+datetime.timedelta(hours=index),'%Y-%m-%d %H:%M')
    s2 = datetime.datetime.strftime(startTime+datetime.timedelta(hours=index+windowSize),'%Y-%m-%d %H:%M')
    return [s1,s2]


def getTime(userId,eventId,whiteList,blackList):
    eventObj=db_currentEvent.find_one({"eventId":eventId})
    eventStart = eventObj["startTime"]
    eventEnd = eventObj["endTime"]
    lat=eventObj["latitude"]
    lon=eventObj["longitude"]

    data2=Write_3Days(lat,lon)
    data7=Write_3_To_7Days(lat,lon)

    whiteList = np.array(whiteList)
    blackList = np.array(blackList)
    if len(whiteList)!=0:
        whiteList = np.char.split(whiteList)
    if len(blackList)!=0:
        blackList = np.char.split(blackList)

    AHPPreference = (db_user.find_one({"userId": userId}))["AHPPreference"]
    participants = (db_currentEvent.find_one({"eventId": eventId}))["participants"]
    #------------------------------------------------------------------------------------------------------------#
    # print("eventStart",eventStart)
    # print("eventEnd",eventEnd)
    # print("AHPPreference",AHPPreference)
    # print("participants",participants)
    list1 = []
    list2 = []
    list3 = []

    createTable(data2,data7)
    print(table)

    windowSize = eventEnd-eventStart
    windowSize = windowSize.days*24 + windowSize.seconds/3600

    blockStart = datetime.datetime.now()  # 起始要改成now
    initblockStart = blockStart
    blockEnd = blockStart+datetime.timedelta(hours=windowSize)
    # cutBlock(blockStart, blockEnd)
    terminal = datetime.datetime.strptime(data7["temperature"][-1]["time"],"%Y-%m-%d %H:%M:%S")
    terminal += datetime.timedelta(hours=12)
    while blockEnd <= terminal:  # 終止條件要改成API7的最後一個時間
        resultList = divideBlock(blockStart, blockEnd)
        list1.append(judgeByWeather(resultList,data2))
        list2.append(judgeByReserve(resultList, windowSize, participants))
        list3.append(judgeByRationality(blockStart, whiteList, blackList,eventStart))
        blockStart += datetime.timedelta(hours=1)
        blockEnd += datetime.timedelta(hours=1)

    # list3 = [(maxDist - element)/maxDist * 100 for element in list3]

    print("天氣良好: ")
    listPrinter(list1)
    print("參加者保留: ")
    listPrinter(list2)
    print("時間合理: ")
    listPrinter(list3)
    result = calculate(list1, list2, list3, AHPPreference)
    print("評分結果: ")
    listPrinter(result)
    
    max_number = result.argsort()[-3:]
    finalList = []
    for i in max_number:
        finalList+=showBlockTime(initblockStart, int(i), windowSize)
    # print(finalList)
    return finalList
# if __name__=="__main__":
#     getTime()