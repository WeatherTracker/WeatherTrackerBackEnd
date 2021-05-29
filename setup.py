from flask import Flask,request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
serverIP="https://00edba4bf4f8.ngrok.io"
station=client.station
user=client.user
def get_station():
    return client.station
def get_calculated():
    return client.calculated
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