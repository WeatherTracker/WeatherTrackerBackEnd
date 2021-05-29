from flask import Flask,request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
calculated = client.calculated
serverIP="http:140.121.197.130:5603"
station=client.station
user=client.user
def get_calculated():
    return calculated
def get_station():
    return client.station
def get_calculated():
    return client.calculated
def getSever():
    return serverIP
def get_event():
    return client.event
def create_app():
    return app

def getUser():
    return user