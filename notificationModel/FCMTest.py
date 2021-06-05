import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("./weathertracker-e5de2-firebase-adminsdk-ip69p-0c904aa772.json")
firebase_admin.initialize_app(cred)
token = ["czclbIFxQY-5BzHLrex4vc:APA91bF8Iffcyi5tcvWdCgsB16iYIbgUrIHRYTXIkWa_64TuHILbp4GNDNGk7HA81dSQ9q7kCRSx9_AN5nJBFFV55elpxWzTiU7cXFkkG9IqRplWYE2bdMuQeKlJiES9uo2Y84YcmBHa"
         ]


def sendFCM(fcm_tokens, titleText, msg, data_message=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=titleText,
            body=msg
        ),
        data={
            "title": titleText,
            "body": msg
        },
        tokens=fcm_tokens
    )
    response = messaging.send_multicast(message)
    print("success", response)

def getFCMtoken():
    sendFCM(token, "hi", "45245")
# getFCMtoken()