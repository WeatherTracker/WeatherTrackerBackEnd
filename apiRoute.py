import os
import smtplib
import json
import datetime
import uuid
from Verification.login import login
from setup.setup import create_app
from setup.setup import get_db
from flask import Flask, request, render_template,Blueprint
app = create_app()
db = get_db()
app.register_blueprint(login)
app.config["JSON_AS_ASCII"] = False
@app.route('/')
def index():
        return "Hello index"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)