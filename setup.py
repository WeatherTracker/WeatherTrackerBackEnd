from flask import Flask,request
from pymongo import MongoClient
import json
app = Flask(__name__)
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
calculated = client.calculated
serverIP="https://b0db8975d97d.ngrok.io"
#"http:140.121.197.130:5603"
#123
station=client.station
user=client.user
file='Verification./keys.json'
with open(file, 'r') as obj:
    keyData = json.load(obj)
def get_key():
    return keyData
def get_station():
    return client.station
def get_calculated():
    return client.calculated
def get_test():
    return client.test
def getSever():
    return serverIP
def get_event():
    return client.event
def create_app():
    return app
def getUser():
    return user
def getSever():
    return serverIP
def getViewPoint():
    return client.viewPoint