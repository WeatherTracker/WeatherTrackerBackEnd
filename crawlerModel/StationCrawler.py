import json
import urllib.request as req
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
# for i in range(1999,2020):
#     url = "https://e-service.cwb.gov.tw/wdps/obs/state.htm"
#     with req.urlopen(url) as response:
#         data = response.read().decode("utf-8")
#     root = BeautifulSoup(data, "html.parser")
#     data = root.find(
#         "table", class_='download_html_table black_table table-condensed')

#     rows = iter(root.find(
#         'table', class_="download_html_table black_table table-condensed").find_all('tr'))

#     # skip first row
#     next(rows)
#     sum = 0
#     with open("python/"+str(i)+".json", mode='w', encoding='UTF-8') as f:
#         f.write("[")
#         for row in rows:
#             if row.select('td:nth-of-type(1)')[0].text[:2] != "C1" and int(row.select('td:nth-of-type(8)')[0].text[:4]) <= i:
#                 count = 0
#                 sum += 1
#                 f.write("{\"sum\":\""+str(sum)+"\",")
#                 for cell in row.find_all('td'):
#                     if count % 12 == 0:
#                         f.write("\"站號\":\""+cell.string+"\",")
#                     elif count % 12 == 1:
#                         f.write("\"站名\":\""+cell.string+"\",")
#                     elif count % 12 == 2:
#                         f.write("\"海拔高度(m)\":\""+cell.string+"\",")
#                     elif count % 12 == 3:
#                         f.write("\"經度\":\""+cell.string+"\",")
#                     elif count % 12 == 4:
#                         f.write("\"緯度\":\""+cell.string+"\",")
#                     elif count % 12 == 5:
#                         f.write("\"城市\":\""+cell.string+"\",")
#                     elif count % 12 == 6:
#                         f.write("\"地址\":\""+cell.string+"\",")
#                     elif count % 12 == 7:
#                         f.write("\"資料起始日期\":\""+cell.string+"\",")
#                     elif count % 12 == 8:
#                         if cell.string == None:
#                             f.write("\"撤站日期\":\"none\"")
#                         else:
#                             f.write("\"撤站日期\":\"opps\"")
#                     count += 1
#                 f.write("},")
#         f.write("]")

# 美化

# for i in range(1999, 2021):
#     final_data = {}
#     final_data["year"] = i
#     final_data["datas"] = []
#     with open("python/"+str(i)+".json", "r", encoding="utf-8") as f:
#         json_data = json.load(f)
#     for index in range(len(json_data)):
#         if json_data[index]["站名"][-3:] == "雷達站":
#             continue
#         json_data[index].pop("sum")
#         final_data["datas"].append(json_data[index])
#     with open("python/"+str(i)+".json", "w", encoding="utf-8")as f:
#         f.write(json.dumps(final_data, ensure_ascii=False))


def updateStationList(year):
    ############################################ 記得修改 ##########################################
    client = MongoClient('localhost', 27017)
    db = client['calculated']
    collect = db['Station_list']
    ############################################ 記得修改 ##########################################
    today = datetime.datetime.today()
    targetURL = "https://e-service.cwb.gov.tw/wdps/obs/state.htm"

    with req.urlopen(targetURL) as response:
        responseData = response.read().decode("utf-8")
        root = BeautifulSoup(responseData, "html.parser")

    titleList = ["站號", "站名", "海拔高度(m)", "經度", "緯度", "城市", "地址", "資料起始日期", "撤站日期"]
    # for year in range(1999, 2022):  # 資料庫建立好後就不需要for loop了，改為用datetime驅動更新這一天當年的那份doc
    rows = iter(root.find('table', class_="download_html_table black_table table-condensed").find_all('tr'))
    # skip first row
    next(rows)
    datas = []
    for row in rows:
        data = {}
        if row.select('td:nth-of-type(1)')[0].text[:2] != "C1" and int(row.select('td:nth-of-type(8)')[0].text[:4]) <= year:
            count = 0
            for cell in row.find_all('td'):
                index = count % 12
                count += 1
                if index > 8:
                    continue
                elif index < 8:
                    if index == 2 or index == 3 or index == 4:
                        data[titleList[index]] = float(cell.string)
                    elif index == 7:
                        data[titleList[index]] = datetime.datetime.strptime(cell.string, "%Y/%m/%d")
                    else:
                        data[titleList[index]] = cell.string
                else:
                    if cell.string == None:
                        data[titleList[index]] = None
                    else:
                        data[titleList[index]] = cell.string
            if data["站名"] == "五分山雷達站" or data["站名"] == "墾丁雷達站":
                print("跳過", data["站名"])
            else:
                datas.append(data)
    collect.update_one({"year": year}, {"$set": {"datas": datas}}, True)


# if __name__ == "__main__":
#     updateStationList()