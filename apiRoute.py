import os
import smtplib
import json
import datetime
import uuid
from flask_jwt_extended import JWTManager
from Verification.login import login
from setup import create_app
from setup import get_calculated,get_event
from flask import Flask, request, render_template,Blueprint
from Event.AddEvent import AddEvent
from Data.GetChart import GetChart
from Event.GetCalendarMonth import GetCalendarMonth
from Event.DeleteEvent import DeleteEvent
from Data.update import update
app = create_app()
jwt = JWTManager()
app.config['SECRET_KEY'] = 'FIST'
app.config['JWT_SECRET_KEY'] = 'FISTBRO'
jwt.init_app(app)
app.config['JWT_TOKEN_LOCATION'] = ['headers','query_string']
app.config['PERMANENT_SESSION_LIFETIME'] =datetime.timedelta(hours=1)
calculatedDB = get_calculated()
app.register_blueprint(login)
app.register_blueprint(AddEvent)
app.register_blueprint(GetChart)
app.register_blueprint(GetCalendarMonth)
app.register_blueprint(DeleteEvent)
app.register_blueprint(GetChart)
jwt = JWTManager(app)
app.config["JSON_AS_ASCII"] = False
@app.route('/')
def index():
        return "Hello index"
if __name__ == '__main__':
    
    # schedule.every().day.at('17:42').do(Get_3Days_Data,0)
    # schedule.every().day.at('17:42').do(Get_7Days_Data,0)
    # schedule.every().day.at('17:42').do(Get_PM2_5Data)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # update()
    
    app.debug = True
    port = int(os.environ.get('PORT', 5603))
    app.run(host='0.0.0.0', port=port)
    