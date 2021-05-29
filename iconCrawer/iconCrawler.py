import json
from bs4 import BeautifulSoup
import codecs
from MinDistance import weatherIcon
# def crawler():
#     base = "https://www.cwb.gov.tw/V8/assets/img/weather_icons/weathers/svg_icon/"
#     f = codecs.open("1.txt", 'r', 'utf-8')
#     soup = BeautifulSoup(f, "html.parser")
#     trs = soup.find("tbody")
#     json_data = []
#     for tr in trs:
#         count = 1
#         last = ""
#         temp_data = {}
#         for td in tr:
#             if count % 3 == 0:
#                 temp_data["夜晚"] = base+"night/"+last
#             elif count % 2 == 0:
#                 last = td.find("img")["src"][-6:]
#                 temp_data["白天"] = base+"day/"+td.find("img")["src"][-6:]
#             else:
#                 temp_data["天氣描述"] = td.text
#             count += 1
#         json_data.append(temp_data)

#     with open('data.json',"w",encoding="utf-8") as json_file:
#         json_file.write(json.dumps(json_data,ensure_ascii=False))

# with open('data.json',"r",encoding="utf-8") as obj:
#     ans=json.load(obj)
#     for i in ans:
#         url=i["白天"]
#         url2=url.split("/")
#         result=(url2[-2]+"_"+url2[-1]).replace("svg","png")
#         i["白天"]=result
#         url=i["夜晚"]
#         url2=url.split("/")
#         result=(url2[-2]+"_"+url2[-1]).replace("svg","png")
#         i["夜晚"]=result
#     changeUrl=ans
# file = 'data.json'
# with open(file, 'w',encoding='utf8') as obj:
#     json.dump(changeUrl, obj, ensure_ascii=False)#把結果寫入CWS.json檔
weatherIcon(25.1505447,121.7735869)