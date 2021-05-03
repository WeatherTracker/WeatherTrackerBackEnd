import os
import base64
import smtplib
import json
import jwt
import datetime
import uuid
from . import Verificate
import time
from itsdangerous import TimedJSONWebSignatureSerializer,BadSignature,SignatureExpired
from .TokenGenerator import des_decrypt,create_token
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, create_refresh_token,get_jwt_identity,decode_token,create_access_token
from flask import Flask, request, render_template,Blueprint,current_app,session
from flask_pymongo import pymongo
from flask.json import jsonify
from setup import get_calculated,getUser
login = Blueprint('login',__name__)
@login.route('/123')
def flask_mongodb_atlas():
    return "Welcome to flask demo"
@login.route('/verify',methods=['GET'])
def tryMe():
    token=request.args['token']
    decoded = jwt.decode(token, 'FISTBRO', algorithms=['HS512'])
    s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=600)
    print(decoded)
    try:
        data = s.loads(token)  # 驗證
        email=data.get('email')
        if(session.get(token)!=email):
            session[str(token)]=email
            session.permanent = True
            hashed=data.get('hash_password').split('\'')
            passwordbit=des_decrypt("FIST2021",hashed[1])
            password=str(passwordbit).split('\'')
            user=getUser()
            user.auth.update(
            {"email" : email},
            {"$set":{
            "password":password[1]
            }
            },upsert=True)
            return "驗證成功"
        else:
            return "這個連結驗證過ㄌ"
    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤`
        return('SignatureExpired, over time')
    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        return('BadSignature, No match')
    except:
        return "驗證失敗"

@login.route('/signUp',methods=['GET', 'POST'])
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
    if(user.auth.find_one({'email':email,'password':password})):
        token=create_token(email)
        ack={"code":200,
            "msg":str(token)
        }
        return ack
    else:
        ack={"code":400,
            "msg":"帳號或密碼錯誤"
        }
        return ack