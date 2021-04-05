import os
import smtplib
import json
import datetime
import uuid
from Verification.login import login
from Data.getQuery import getQuery
from setup import create_app
from setup import get_calculated
from flask import Flask, request, render_template,Blueprint
app = create_app()
calculatedDB = get_calculated()
app.register_blueprint(login)
app.register_blueprint(getQuery)
app.config["JSON_AS_ASCII"] = False
@app.route('/')
def index():
        return "Hello index"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)