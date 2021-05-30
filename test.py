import requests
from bs4 import BeautifulSoup
res = requests.get("https://charts.woobull.com/bitcoin-mvrv-ratio/")
soup = BeautifulSoup(res.text, "html.parser")
#print(soup.prettify())
script = soup.findAll("script")
print(str(script[4]).split("],")[3].split("[")[2])