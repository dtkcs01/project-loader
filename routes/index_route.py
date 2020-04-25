import os
import pathlib
from flask import session
from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import render_template

index = Blueprint('index', __name__)

def compute_navigation(path):
    navigation = []
    while(len(os.path.basename(path)) > 0):
        navigation.insert(0, (os.path.basename(path), path))
        path = os.path.abspath(os.path.join(path, '..'))
    navigation.insert(0, ('', path))
    return navigation

def compute_size(s):
    units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']
    i = 0
    while(s//1024 > 0):
        s = s//1024
        i += 1
    return '{} {}'.format(s, units[i])

def generate_tragets(base, dir_contents):
    targets = []
    for content in dir_contents:
        path = os.path.join(base, content)
        isfile = os.path.isfile(path)
        row = {
            'name' : content,
            'is_file' : isfile,
            'icon' : 'file' if isfile else 'folder',
            'target' : '_blank' if isfile else '_self',
            'size' : compute_size(os.path.getsize(path)) if isfile else '-'
        }
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
            dir_contents = generate_tragets(request.args.get('location'), dir_contents),
            navigation = compute_navigation(request.args.get('location'))
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
