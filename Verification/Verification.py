import email.message
import smtplib
def testmail(target):
    msg=email.message.EmailMessage()
    msg["From"] = "fistjavamailtest@gmail.com"
    msg["To"] = target
    msg["Subject"] = "GodHasAPen"
    msg.set_content("神來之筆")
    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("fistjavamailtest@gmail.com","GodHasAPen2021")
    server.send_message(msg)
    server.close()