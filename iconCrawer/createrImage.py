from bs4 import BeautifulSoup
import requests
import os
import json
if not os.path.exists("images"):
    os.mkdir("images")  # 建立資料夾

with open("data.json","r",encoding="utf-8") as obj:
    ans=json.load(obj)
    for i in ans:
        dayImg = requests.get(i["白天"])  # 下載圖片
        nightImg=requests.get(i["夜晚"])
        with open("images/day-"+i["天氣描述"]+".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
            file.write(dayImg.content)  # 寫入圖片的二進位碼
        with open("images/night-"+i["天氣描述"]+".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
            file.write(nightImg.content)  # 寫入圖片的二進位碼