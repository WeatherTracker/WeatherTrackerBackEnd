import os
import smtplib
import json
import datetime
import uuid
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from Verification.login import login
from setup import create_app
from setup import get_calculated,get_event
from flask import Flask, request, render_template,Blueprint
from Event.AddEvent import AddEvent
from Data.GetChart import GetChart
from Event.GetCalendarMonth import GetCalendarMonth
from Event.DeleteEvent import DeleteEvent
from Event.EditEvent import EditEvent
from Event.GetCalendarDay import GetCalendarDay
import threading
from Data.CWS_3Days import Get_3Days_Data
from Data.CWS_7Days import Get_7Days_Data
from Data.PM2_5 import Get_PM2_5Data
app = create_app()
jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = 'FISTBRO'
jwt.init_app(app)
app.config['JWT_TOKEN_LOCATION'] = ['headers','query_string']
calculatedDB = get_calculated()
app.register_blueprint(login)
app.register_blueprint(AddEvent)
app.register_blueprint(GetChart)
app.register_blueprint(GetCalendarMonth)
app.register_blueprint(DeleteEvent)
app.register_blueprint(EditEvent)
app.register_blueprint(GetCalendarDay)
jwt = JWTManager(app)
app.config["JSON_AS_ASCII"] = False

def job1_task():
    threading.Thread(target=Get_3Days_Data).start()
def job2_task():
    threading.Thread(target=Get_7Days_Data).start()
def job3_task():
    threading.Thread(target=Get_PM2_5Data).start()
class Config(object):
    SCHEDULEER_API_ENABLE=True
    JOBS=[
        {
            'id':'job1',
            'func':'__main__:job1_task',
            'trigger':'interval',
            'start_date':'2021-05-08 11:20:00',
            'hours':6
        },
        {
            'id':'job2',
            'func':'__main__:job2_task',
            'trigger':'interval',
            'start_date':'2021-05-08 11:20:00',
            'hours':6
        },
        {
            'id':'job3',
            'func':'__main__:job3_task',
            'trigger':'interval',
            'start_date':'2021-05-08 10:35:00',
            'hours':6
        }
    ]
@app.route('/')
def index():
        return "Hello index"
if __name__ == '__main__':
    app.config.from_object(Config())# 為例項化的flask引入配置
    scheduler=APScheduler()  # 例項化APScheduler
    scheduler.init_app(app)  # 把任務列表放進flask
    scheduler.start() # 啟動任務列表
    app.debug = True
    port = int(os.environ.get('PORT', 5603))
    app.run(host='0.0.0.0', port=port)