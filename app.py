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

@app.before_request
def clean_session():
    # 'ids' denotes the tabs and their designated 'ids' for a particular 'user_id'
    if('ids' in session):
        ids = session['ids']
        user_id = request.cookies.get('user_id')
        cleaned_session_data = ''
        with open('clean.txt', 'r') as source:
            lines = [ line.strip() for line in source.readlines() if len(line.strip()) > 0 ]
            for line in lines:
                uid, id = line.split(' ')
                if(uid == user_id):
                    url = urllib.parse.urlparse(request.url)
                    if(url.path.split('/')[-1] != id):
                        if(id in ids):
                            del ids[id]
                    else:
                        cleaned_session_data += '{}\n'.format(line)
            source.close()
        with open('clean.txt', 'w+') as target:
            target.write(cleaned_session_data)
            target.close()

# Register routes
app.register_blueprint(index, url_prefix = '/')

app.config['ENV'] = 'development'
application = Application(app)
application.start()
