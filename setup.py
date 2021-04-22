from flask import Flask,request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("localhost", 27017)  # 連線到 localhost:27017
def get_station():
    return client.station
def get_calculated():
    return client.calculated
def create_app():
    return app