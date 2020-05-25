import os
import sys
import urllib
import threading

from flask import Flask
from flask import request
from flask import session

from routes import index
from application_class import Application

app = Flask(__name__, static_url_path = '/static')
app.secret_key = os.environ.get("FLASK_APP.SECRET_KEY")

# Register routes
app.register_blueprint(index, url_prefix = '/')

app.config['ENV'] = 'development'
application = Application(app)
application.start()
