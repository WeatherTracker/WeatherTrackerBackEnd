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
from .TokenGenerator import des_decrypt,create_token,create_user_token
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, create_refresh_token,get_jwt_identity,decode_token,create_access_token
from flask import Flask, request, render_template,Blueprint,current_app,session
from flask_pymongo import pymongo
from flask.json import jsonify
from setup import get_calculated,getUser
login = Blueprint('login',__name__,template_folder="templates")
@login.route('/123')
def flask_mongodb_atlas():
    return "Welcome to flask demo"
@login.route('/verify',methods=['GET'])
def tryMe():
    token=request.args['token']
    decoded = jwt.decode(token, 'FISTBRO', algorithms=['HS512'])
    s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=600)
    try:
        data = s.loads(token)  # 驗證
        email=data.get('email')
        if(session.get(token)!=email):
            session[str(token)]=email
            session.permanent = True
            hashed=data.get('hash_password').split('\'')
            passwordbit=des_decrypt("FIST2021",hashed[1])
            password=str(passwordbit).split('\'')
            FCMToken=data.get('FCMToken')
            user=getUser()
            spaceArray=[]
            userId=uuid.uuid1()
            user.auth.update(
            {"email" : email},
            {"$set":{
            "password":password[1],
            'FCMToken':FCMToken,
            'userId':userId,
            'userName':"user",
            'pastEvents':spaceArray,
            'AHPPreference':spaceArray,
            'freeTime':spaceArray,
            'hobbies':spaceArray,
            'currentEvents':spaceArray
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

@login.route('/reprofile',methods=['POST'])
def reprofile():
    newName=request.form.get('userName')
    email=request.form.get('email')
    hobbies=request.form.get('hobbies')
    user=getUser()
    user.auth.update(
            {"email" :email },
            {"$set":{
            'userName':newName,
            'hobbies':hobbies
            }
            },upsert=True)
    return{"code":200,
            "msg":"修改完成"
            }
            
@login.route('/signUp',methods=['GET', 'POST'])
def register():
    target=request.form['email']
    user=getUser()
    if(user.auth.find_one({'email':target})):
        ack={"code":200,
            "msg":"這個email已經註冊過了"
            }
        return ack
    else:
        target=request.form['email']
        password=request.form['password']
        FCMToken=request.form['FCMToken']
        Verificate.testMail(target,password,FCMToken)
        ack={"code":200,
            "msg":"驗證信已發送"
            }
        return ack

@login.route('/signIn',methods=['POST'])
def signIn():
    user=getUser()
    email=request.form['email']
    password=request.form['password']
    if(user.auth.find_one({'email':email,'password':password})):
        userId=user.auth.find_one({'email':email,'password':password}).get("userId")
        token=create_user_token(userId)
        ack={"code":200,
            "msg":str(token)
        }
        return ack
    else:
        ack={"code":400,
            "msg":"帳號或密碼錯誤"
        }
        return ack

@login.route('/sendResetMail',methods=['POST'])
def sendResetMail():
    if request.method == 'POST':
        target=request.form['email']
        Verificate.newPassWordMail(target)
        ack={"code":200,
            "msg":"驗證信已發送"
            }
        return ack
    else:
        return'水喔'
@login.route('/sendnewPassword')
def passwordForm():
    token=str(request.args['token'])
    return render_template('newPassword.html',target=token)

@login.route('/newPassword',methods=['POST'])
def newpassword():
    if request.method == 'POST':
        mail=request.form.get('mail')       
        s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=600)
        try:
            data = s.loads(mail)  # 驗證
            email=data.get('email')
            if(session.get(mail)!=email):
                user=getUser()
                session[mail]=email
                print(email)
                email=str(des_decrypt("FIST2021",email.split('\'')[1]))
                print(email.split('\'')[1])
                session.permanent = True
                password=(request.form.get('password'))
                passwordack=(request.form.get('passwordack'))
                if(password==passwordack):
                    user.auth.update(
                    {"email" : email.split('\'')[1]},
                    {"$set":{
                    "password":password,
                    }
                    },upsert=True)
                    return "修改完成"
                else:
                    return "密碼與再次輸入不符"
            else:
                return "這個連結驗證過了"
        except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤`
            return('SignatureExpired, over time')
        except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
            return('BadSignature, No match')
        except:
            return "驗證失敗"