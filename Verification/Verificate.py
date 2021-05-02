import email.message
from flask_jwt_extended import create_access_token
from .tokenGenerator import create_confirm_token
from Verification import tokenGenerator
from flask_pymongo import pymongo
import smtplib
import uuid
from setup import get_calculated,getUser
# CONNECTION_STRING = "mongodb://localhost:27017/calculated"
# client = pymongo.MongoClient(CONNECTION_STRING)
# user=client.user
user=getUser()

def testMail(target,password):
    msg=email.message.EmailMessage()
    msg["From"] = "fistjavamailtest@gmail.com"
    msg["To"] = str(target)
    msg["Subject"] = "您的WeatherTracker驗證信"
    token=str(setId(target,password)).split('\'')
    msg.set_content("https://6c6955385a90.ngrok.io/tryMe?token="+token[1])
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("fistjavamailtest@gmail.com","GodHasAPen2021")
    server.send_message(msg)
    server.close()

def setId(email,password):
    userId=str(uuid.uuid4())
    token=tokenGenerator.create_confirm_token(email,password,expires_in=600)
    #token=create_access_token(identity=email)
    print(token)
    return token
   