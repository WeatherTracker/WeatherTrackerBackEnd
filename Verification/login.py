import os
import smtplib
import json
import datetime
import uuid
import Verification
from flask import Flask, request, render_template,Blueprint
from flask_pymongo import pymongo
from flask.json import jsonify
login = Blueprint('login',__name__)
@login.route('/123')
def flask_mongodb_atlas():
    return "Welcome to flask demo"

@login.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        authData=request.form['email']
        ack={"code":200,
            "msg":"讚喔"
            }
        print (authData)
        return ack
    else:
        return'水喔'

@login.route('/mailTest',methods=['POST'])
def mailTest():
        target=request.form['email']
        Verification.testmail(target)
        return "WOW"

@login.route('/dateTimeTest',methods=['POST'])
def dateTimeTest():
    #dateTimeData=request.form['dateTime']
    #datetime.datetime.strptime(dateTimeData,"%Y-%m-%d %H:%M")
    return {"code":"200",
            "msg":"OK"
    }