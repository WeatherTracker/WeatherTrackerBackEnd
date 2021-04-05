import os
import smtplib
import json
import datetime
import uuid
from Verification import Verification
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, create_refresh_token,get_jwt_identity
from flask import Flask, request, render_template,Blueprint,current_app
from flask_pymongo import pymongo
from flask.json import jsonify
login = Blueprint('login',__name__)
@login.route('/123')
def flask_mongodb_atlas():
    return "Welcome to flask demo"
@login.route('/getTest/<string:url>',methods=['GET'])
def getTest(url):
    print (url)
    return"驗證完成"

@login.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        target=request.form['email']
        password=request.form['password']
        Verification.testMail(target,password)
        ack={"code":200,
            "msg":"驗證信已發送"
            }
        return ack
    else:
        return'水喔'

@login.route('/signIn',methods=['POST'])
def signIn():
    email=request.form['email']
    password=request.form['password']
    ack={"code":200,
        "msg":"驗證信已發送"
        }
    return jsonify(access_token=access_token)

@login.route('/mailTest',methods=['POST'])
def mailTest():
        email=request.form['email']
        password=request.form['password']
        Verification.testMail(email,password)
        return "WOW"

@login.route('/dateTimeTest',methods=['POST'])
def dateTimeTest():
    #dateTimeData=request.form['dateTime']
    #datetime.datetime.strptime(dateTimeData,"%Y-%m-%d %H:%M")
    return {"code":"200",
            "msg":"OK"
    }