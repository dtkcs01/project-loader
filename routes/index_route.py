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
    targets = []
    for content in dir_contents:
        row = []
        isfile = os.path.isfile(os.path.join(base, content))
        row.append(content)
        row.append('_blank' if isfile else '_self')
        row.append('file' if isfile else 'folder')
        targets.append(row)
    return targets

@index.route('/', methods=['GET'])
def home():
    if(request.method == 'GET'):
        if('location' not in request.args):
            return redirect(url_for('index.home', location = pathlib.Path.home().__str__()))
        dir_contents = os.listdir(request.args.get('location'))
        dir_contents.insert(0, '..')
        return render_template(
            'index.html',
            location = request.args.get('location'),
            dir_contents = generate_tragets(request.args.get('location'), dir_contents)
        )

@index.route('/handle/<name>', methods = ['GET'])
def add(name):
    name = name[5:]
    if(request.method == 'GET'):
        path = os.path.abspath(os.path.join(request.args.get('location'), name))
        if(os.path.isfile(path)):
            return 'FILE'
        else:
            return redirect(url_for('index.home', location = path))
