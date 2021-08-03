import email.message
from flask_jwt_extended import create_access_token
from .TokenGenerator import create_confirm_token,des_encrypt
from Verification import TokenGenerator
from flask_pymongo import pymongo
import smtplib
import uuid
from setup import get_calculated,getUser,getSever,get_key
def testMail(target,password,FCMToken):
    msg=email.message.EmailMessage()
    msg["From"] = get_key().get('mailBotAccount')
    msg["To"] = str(target)
    msg["Subject"] = "您的WeatherTracker驗證信"
    token=str(setId(target,password,FCMToken)).split('\'')
    #http:140.121.197.130:5603
    msg.set_content(getSever()+"/verify?token="+token[1])
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(get_key().get('mailBotAccount'),get_key().get('mailBotPass'))
    server.send_message(msg)
    server.close()

def newPassWordMail(target):
    msg=email.message.EmailMessage()
    msg["From"] = get_key().get('mailBotAccount')
    msg["To"] = str(target)
    msg["Subject"] = "您的WeatherTracker新密碼驗證信"
    #http:140.121.197.130:5603
    mail=des_encrypt(get_key().get('jwtKey'),target)
    token=str(newPassWordToken(mail)).split('\'')
    msg.set_content(getSever()+"/sendnewPassword?token="+token[1])
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(get_key().get('mailBotAccount'),get_key().get('mailBotPass'))
    server.send_message(msg)
    server.close()

def setId(email,password,FCMToken):
    userId=str(uuid.uuid4())
    token=TokenGenerator.create_confirm_token(email,password,FCMToken,expires_in=600)
    #token=create_access_token(identity=email)
    print(token)
    return token

def newPassWordToken(email):
    token=TokenGenerator.create_token(email,expires_in=600)
    #token=create_access_token(identity=email)
    print(token)
    return token
   