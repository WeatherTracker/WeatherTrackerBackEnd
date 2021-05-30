import os
import base64
import smtplib
import json
import jwt
import datetime
import uuid
import time
from itsdangerous import TimedJSONWebSignatureSerializer,BadSignature,SignatureExpired
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, create_refresh_token,get_jwt_identity,decode_token,create_access_token
from flask import Flask, request, render_template,Blueprint,current_app,session
from flask_pymongo import pymongo
from flask.json import jsonify
from . import recommendPoint
#from . import recommendEvent
from setup import get_calculated,getUser
recommand = Blueprint('recommand',__name__)
@recommand.route('/recommandScene')
def recommandScene():
    x=request.form["Px"]
    y=request.form["Py"]
    number=request.form.get("number")
    return(recommendPoint(x,y,number=5))
#@recommand.route('/recommandEvent')
#def recommandActivity():
#    x=request.form["Px"]
#    y=request.form["Py"]
#    number=request.form.get("number")
#    return(recommendEvent(x,y,number=5))
