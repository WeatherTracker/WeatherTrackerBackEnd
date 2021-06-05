import os
import smtplib
import json
import datetime
import uuid
from datetime import timedelta
import threading
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from setup import create_app
from setup import get_calculated,get_event
from flask import Flask, request, render_template,Blueprint
from Verification.login import login
from Event.updateEvent import updateEvent
from Event.AddEvent import AddEvent
from Event.GetCalendarMonth import GetCalendarMonth
from Event.DeleteEvent import DeleteEvent
from Event.EditEvent import EditEvent
from Event.GetCalendarDay import GetCalendarDay
from Event.InOrOutEvent import InOrOutEvent
from Recommendation.recommend import recommend
from Data.GetChart import GetChart
from Data.CWS_3Days import Get_3Days_Data
from Data.CWS_7Days import Get_7Days_Data
from Data.PM2_5 import Get_PM2_5Data
from Data.GetWeatherIcon import GetWeatherIcon
from Profile.ViewProfile import ViewProfile
from Profile.EditProfile import EditProfile
from crawlerModel.updater2 import weatherDataUpdater
from Recommendation.GetRecommendTime import GetRecommendTime
app = create_app()
jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = 'FISTBRO'
app.config['SECRET_KEY'] = 'FISTBRO'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
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
app.register_blueprint(GetWeatherIcon)
app.register_blueprint(InOrOutEvent)
app.register_blueprint(EditProfile)
app.register_blueprint(ViewProfile)
# app.register_blueprint(RecommendEvent)
app.register_blueprint(recommend)
app.register_blueprint(GetRecommendTime)
jwt = JWTManager(app)
app.config["JSON_AS_ASCII"] = False


def job1_task():
    threading.Thread(target=Get_3Days_Data).start()
def job2_task():
    threading.Thread(target=Get_7Days_Data).start()
def job3_task():
    threading.Thread(target=Get_PM2_5Data).start()
def job4_task():
    threading.Thread(target=updateEvent).start()
# def job5_task():
#     threading.Thread(target=weatherDataUpdater).start()
class Config(object):
    SCHEDULEER_API_ENABLE=True
    JOBS=[
        {
            'id':'job1',
            'func':'__main__:job1_task',
            'trigger':'interval',
            'start_date':'2021-05-25 06:00:00',
            'hours':6
            # 'start_date':'2021-06-05 12:50:00',
            # 'minutes':1
        },
        {
            'id':'job2',
            'func':'__main__:job2_task',
            'trigger':'interval',
            'start_date':'2021-05-25 06:00:00',
            'hours':6
            # 'start_date':'2021-06-05 12:50:00',
            # 'minutes':1
        },
        {
            'id':'job3',
            'func':'__main__:job3_task',
            'trigger':'interval',
            'start_date':'2021-05-25 10:35:00',
            'hours':6
            # 'start_date':'2021-05-22 16:37:00',
            # 'minutes':1
        },
        {
            'id':'job4',
            'func':'__main__:job4_task',
            'trigger':'interval',
            'start_date':'2021-05-30 00:00:00',
            'days':1
        }
        # {
        #     'id':'job5',
        #     'func':'__main__:job5_task',
        #     'trigger':'interval',
        #     'start_date':'2021-06-03 17:46:00',
        #     'days':1
        # }
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