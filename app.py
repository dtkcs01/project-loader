import os
import pathlib
from flask import Flask
from flask import session

from routes import index

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get("SESSION")

app.register_blueprint(index, url_prefix = '/')

app.config['ENV'] = 'development'
app.run(
    host = 'localhost',
    port = int(os.environ.get('PORT')),
    debug = True
)
