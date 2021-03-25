from flask import Flask,request
from flask_pymongo import pymongo
app = Flask(__name__)
CONNECTION_STRING = "mongodb://localhost:27017/calculated"
client = pymongo.MongoClient(CONNECTION_STRING)
calculated = client.calculated
station=client.station
def get_calculated():
    return calculated

def get_station():
    return station

def create_app():
    return app