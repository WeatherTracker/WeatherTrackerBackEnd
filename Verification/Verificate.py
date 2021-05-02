import email.message
from flask_jwt_extended import create_access_token
from .TokenGenerator import create_confirm_token
from Verification import TokenGenerator
from flask_pymongo import pymongo
import smtplib
import uuid
from setup import get_calculated,getUser
def testMail(target,password):
    msg=email.message.EmailMessage()
    msg["From"] = "fistjavamailtest@gmail.com"
    msg["To"] = str(target)
    msg["Subject"] = "您的WeatherTracker驗證信"
    token=str(setId(target,password)).split('\'')
    msg.set_content("http:140.121.197.130:5603/tryMe?token="+token[1])
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("fistjavamailtest@gmail.com","GodHasAPen2021")
    server.send_message(msg)
    server.close()

def setId(email,password):
    userId=str(uuid.uuid4())
    token=TokenGenerator.create_confirm_token(email,password,expires_in=600)
    #token=create_access_token(identity=email)
    print(token)
    return token
   