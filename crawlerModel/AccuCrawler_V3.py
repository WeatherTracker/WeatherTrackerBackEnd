import requests
import re
from bs4 import BeautifulSoup
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


def check(str):
    result = ""
    for c in str:
        if is_number(c):
            result += c
    if result == "":
        result = 0.0
    return float(result)


def crawler(area_name, url, target_date, day):
    finalURL = url+str(day)
    response = requests.get(finalURL, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.findAll('div', class_='half-day-card')
    day_data = {"date": target_date,
                "area": area_name}
    dic = {}
    for j in range(2):
        if j == 0:
            dic["最高氣溫(C)"] = check(cards[j].find('div', class_="temperature").contents[0].strip())
            dic["天氣描述"] = cards[j].find('div', class_="phrase").text.strip()
            dic["體感高溫(C)"] = check(cards[j].find('div', class_="real-feel").find('div').text.strip())
        else:
            dic["最低氣溫(C)"] = check(cards[j].find('div', class_="temperature").contents[0].strip())
            dic["天氣描述"] += "/" + cards[j].find('div', class_="phrase").text.strip()
            dic["體感低溫(C)"] = check(cards[j].find('div', class_="real-feel").find('div').text.strip())
        panels = cards[j].findAll('p', class_="panel-item")
        for panel in panels:
            if panel.contents[0] in dic:
                dic[panel.contents[0]] = max(check(panel.contents[1].text), dic[panel.contents[0]])
            else:
                dic[panel.contents[0]] = check(panel.contents[1].text)
    day_data["datas"] = dic
    return day_data
