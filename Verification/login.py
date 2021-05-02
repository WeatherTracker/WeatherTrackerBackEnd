import os
import base64
import smtplib
import json
import jwt
import datetime
import uuid
from Verification import Verificate
import time
from itsdangerous import TimedJSONWebSignatureSerializer,BadSignature,SignatureExpired
from .tokenGenerator import des_decrypt,create_token
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, create_refresh_token,get_jwt_identity,decode_token,create_access_token
from flask import Flask, request, render_template,Blueprint,current_app
from flask_pymongo import pymongo
from flask.json import jsonify
from setup import get_calculated,getUser
login = Blueprint('login',__name__)
@login.route('/123')
def flask_mongodb_atlas():
    return "Welcome to flask demo"
@login.route('/tryMe',methods=['GET'])
def tryMe():
    token=request.args['token']
    decoded = jwt.decode(token, 'FISTBRO', algorithms=['HS512'])
    s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=600)
    print(decoded)
    try:
        data = s.loads(token)  # 驗證
        hashed=data.get('hash_password').split('\'')
        passwordbit=des_decrypt("FIST2021",hashed[1])
        password=str(passwordbit).split('\'')
        user=getUser()
        user.auth.update(
        {"email" : data.get('email')},
        {"$set":{
           "password":passwordbit
        }
        },upsert=True)
        return "驗證成功"
    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤`
        return('SignatureExpired, over time')
    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        return('BadSignature, No match')
    except:
        return "驗證失敗"
    
@login.route('/getTest',methods=['GET'])
def getTest():
    try:
        identity = get_jwt_identity()
        print(identity)
        #jwt.decode(b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzY5ODM1MiwianRpIjoiMDZhYTE3ZDktMTQ3ZS00YWI3LWI3NTAtZTMyNzIwMDQ4MDllIiwibmJmIjoxNjE3Njk4MzUyLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoicXdlMTI1Mzk3QGdtYWlsLmNvbSIsImV4cCI6MTYxNzY5OTI1Mn0.SU9U0i_47V9JpXNHZkN3nSFd3pyTc91v0D9xXqRZbow',"FISTBRO",algorithms=['HS256'])
        return {
            'mail': "驗證完成",
            "code":200,
        }
    except:
        return "過期拉"

@login.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        target=request.form['email']
        password=request.form['password']
        Verificate.testMail(target,password)
        ack={"code":200,
            "msg":"驗證信已發送"
            }
        return ack
    else:
        return'水喔'

@login.route('/signIn',methods=['POST'])
def signIn():
    user=getUser()
    email=request.form['email']
    password=request.form['password']
    if(user.auth.findone.find_one({'email':email,'password':password})):
        token=create_token(email)
        ack={"code":200,
            "msg":token
        }
        return ack
    else:
        ack={"code":400,
            "msg":"帳號或密碼錯誤"
        }
        return ack

@login.route('/mailTest',methods=['POST'])
def mailTest():
        email=request.form['email']
        password=request.form['password']
        Verificate.testMail(email,password)
        return "WOW"

@login.route('/dateTimeTest',methods=['POST'])
def dateTimeTest():
    #dateTimeData=request.form['dateTime']
    #datetime.datetime.strptime(dateTimeData,"%Y-%m-%d %H:%M")
    return {"code":"200",
            "msg":"OK"
    }