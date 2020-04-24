import os
import pathlib
from flask import session
from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import render_template

index = Blueprint('index', __name__)

def generate_tragets(base, dir_contents):
    targets = [
        [content , ('_blank' if os.path.isfile(os.path.join(base, content)) else '_self')]
        for content in dir_contents
    ]
    return targets

@index.route('/', methods=['GET'])
def home():
    if('DIR' not in session):
        session['DIR'] = pathlib.Path.home().__str__()
    if(request.method == 'GET'):
        dir_contents = os.listdir(session['DIR'])
        dir_contents.insert(0, '..')
        return render_template(
            'index.html',
            location = session['DIR'],
            dir_contents = generate_tragets(session['DIR'], dir_contents)
        )

@index.route('/handle/<name>', methods = ['GET'])
def add(name):
    name = name[5:]
    if(request.method == 'GET'):
        path = os.path.join(session['DIR'], name)
        if(os.path.isfile(path)):
            return 'FILE'
        else:
            session['DIR'] = path
            return redirect(url_for('index.home'))
