import email.message
import tokenGenerator
from flask_pymongo import pymongo
import smtplib
import uuid
CONNECTION_STRING = "mongodb://localhost:27017/calculated"
client = pymongo.MongoClient(CONNECTION_STRING)
user=client.user
def setId(email,password):
    userId=str(uuid.uuid4())
    token=tokenGenerator.create_confirm_token(userId, expires_in=3600)
    print(token)
    user.auth.insert(
        {
            "email":email,
            "password":password,
            "userId":userId,
            "token":token
        }
    )
    return token
   

def testMail(email,password):
    msg=email.message.EmailMessage()
    msg["From"] = "fistjavamailtest@gmail.com"
    msg["To"] = email
    msg["Subject"] = "您的WeatherTracker驗證信"
    msg.set_content("https://a81c4d7b1bc5.ngrok.io/getTest"+setId(email,password))
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("fistjavamailtest@gmail.com","GodHasAPen2021")
    server.send_message(msg)
    server.close()