from pymongo import MongoClient
import numpy as np
import datetime
import sys

client = MongoClient('localhost', 27017)
db = client['test']
db_currentEvent = db['currentEvent']
db_API = db['API']
db_event = db['Event']
db_user = db['user']
data2 = db_API.find_one({"name": "sample2"})
data2 = data2["content"]
data7 = db_API.find_one({"name": "sample7"})
data7 = data7["content"]

# day2 = {"AQI": 24, "POP": 6, "UV": 24, "humidity": 3, "temperature": 3, "windSpeed": 3}
day2 = {"POP": 6, "UV": 24, "humidity": 3, "temperature": 3, "windSpeed": 3}
day7 = {"POP": 12, "UV": 24, "humidity": 12, "temperature": 12, "windSpeed": 12}
table = None
bundary = None


def getBlockIndex(date):
    firstBlock = data2["POP"][0]["time"]
    if firstBlock.hour == 0 or firstBlock.hour == 12:
        firstBlock = firstBlock - datetime.timedelta(hours=6)
    distance = date - firstBlock
    distance = distance.days*24 + distance.seconds/3600
    distance = int(distance)  # 片段開始時間離第一個API多遠(小時)
    index = distance//3+1
    return index


def createTable():
    global table
    global bundary
    table = []
    bundary = data2["temperature"][-1]["time"]+datetime.timedelta(hours=3)
    print("bundary", bundary)
    for k in day2.keys():
        row = []
        if k == "POP":
            for i in data2[k]:
                if i["dynamicTag"] != None:
                    row += 2 * [1]
                else:
                    row += 2 * [0]
        elif k == "UV":
            for i in data2[k]:
                if i["dynamicTag"] != None:
                    row += 8 * [1]
                else:
                    row += 8 * [0]
        else:
            for i in data2[k]:
                if i["dynamicTag"] != None:
                    row += [1]
                else:
                    row += [0]
        table.append(row)

    for k in day7.keys():
        row = []
        if k != "UV":
            for i in data7[k]:
                if i["time"] < bundary:
                    continue
                if i["dynamicTag"] != None:
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


def judgeByWeather(resultList):
    sum = 0
    total = 0
    for i in resultList:
        s = getBlockIndex(i["blockStart"])
        e = getBlockIndex(i["blockEnd"])
        total += (e-s+1)*7
        try:
            sum += table[e]-table[s-1]
        except Exception:
            sum += table[-1]-table[s-1]
    # print("sum", sum)
    # print("tagsSum", total)
    # print("天氣好: ", (total - sum) / total * 100)
    return (total - sum) / total * 100


def judgeByReserve(resultList, windowSize, participants):
    # users = db.user.find({"userId": {"$in": participants}})
    participants = [{"freeTime": [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [1, 1, 1],
        [1, 1, 1]
    ]}]
    sum = 0
    total = 0
    for participant in participants:
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
        return sum/total*100
    except Exception:  # 完全在凌晨舉辦的活動
        # print("完全在凌晨舉辦", 0)
        return 0


def judgeByRationality(blockStart, whiteList, blackList):
    bias = 0
    today = datetime.datetime.strptime("2021-04-29 18:00", "%Y-%m-%d %H:%M")  # 要改成now
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
    print(startTime+datetime.timedelta(hours=index))
    print(startTime+datetime.timedelta(hours=index+windowSize))


if __name__ == '__main__':
    userId = ""
    eventId = ""
    whiteList = np.array(["06:00 12:00", "16:00 18:00"])
    blackList = np.array(["00:00 06:00"])
    whiteList = np.char.split(whiteList)
    blackList = np.char.split(blackList)
    # AHPPreference = (db_user.find_one({"userId": userId}))["AHPPreference"]
    # participants = (db_user.find_one({"eventId": eventId}))["participants"]
    AHPPreference = [0.9, 0.05, 0.05]
    participants = ["user1"]
    #------------------------------------------------------------------------------------------------------------#
    list1 = []
    list2 = []
    list3 = []

    createTable()
    # print(table)

    eventStart = datetime.datetime.strptime("2021-01-10 00:00", "%Y-%m-%d %H:%M")
    eventEnd = datetime.datetime.strptime("2021-01-10 05:00", "%Y-%m-%d %H:%M")
    windowSize = eventEnd-eventStart
    windowSize = windowSize.days*24 + windowSize.seconds/3600

    blockStart = datetime.datetime.strptime("2021-04-29 18:00", "%Y-%m-%d %H:%M")  # 起始要改成now
    initblockStart = blockStart
    blockEnd = blockStart+datetime.timedelta(hours=windowSize)
    # cutBlock(blockStart, blockEnd)
    while blockEnd <= datetime.datetime.strptime("2021-05-07 06:00", "%Y-%m-%d %H:%M"):  # 終止條件要改成API7的最後一個時間
        resultList = divideBlock(blockStart, blockEnd)
        # for i in resultList:
        #     print("----------------------")
        #     print(i["blockStart"])
        #     print(i["blockEnd"])
        #     print("----------------------")
        list1.append(judgeByWeather(resultList))
        list2.append(judgeByReserve(resultList, windowSize, participants))
        list3.append(judgeByRationality(blockStart, whiteList, blackList))
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
    showBlockTime(initblockStart, 5, windowSize)
