import os
import random
import pathlib
from flask import session
from flask import request
from flask import url_for
from flask import redirect
from flask import Blueprint
from flask import make_response
from flask import render_template

index = Blueprint('index', __name__)

def create_navbar(location):
    flag = True
    navbar = []
    while(flag):
        navbar.insert(0, (os.path.basename(location), location))
        tmp = os.path.realpath(os.path.join(location, '..'))
        if(tmp == location):
            break
        location = tmp
    return navbar

def create_user_id():
    user_id = ''
    for i in range(int(os.environ.get('USER_ID_LENGTH'))):
        r = random.randint(0, 25)
        user_id += str(random.choice([ r%10, chr(97 + r), chr(65 + r) ]))
    return user_id

@index.route('/', methods=['POST', 'GET'])
def home():
    if(request.method == 'GET'):
        session.setdefault('tabs', {})
        tabs = session['tabs']
        while True:
            id = str(random.randint(1000, 9999))
            if(id in tabs):
                continue
            if('redirect' in request.args):
                print(session)
                tabs[id] = request.args['redirect'].strip()
            else:
                tabs[id] = pathlib.Path.home().__str__()
            break
        session['tabs'] = tabs
        res = make_response(redirect(url_for('index.display', id = id)))
        if('user_id' not in request.cookies):
            res.set_cookie('user_id', create_user_id())
        return res

@index.route('/display/<id>', methods=['POST', 'GET'])
def display(id):
    if(request.method == 'GET'):
        navbar = create_navbar(session['tabs'][id])
        web_config = {
            'id': id,
            'location': session['tabs'][id],
            'ip': os.environ.get('APPLICATION.HOST_IP'),
            'user': request.cookies.get('user_id'),
            'port': os.environ.get('WEB_SOCKET.PORT'),
            'ping_interval': int(os.environ.get('WEB_SOCKET.PING_INTERVAL'))
        }
        return render_template(
            'index.html',
            web_config = web_config,
            navbar = navbar
        )

@index.route('/redirect_id/<id>', methods=['POST', 'GET'])
def redirect_id(id):
    if(request.method == 'GET'):
        web_config = {
            'id': id,
            'location': session['tabs'][id],
            'ip': os.environ.get('APPLICATION.HOST_IP'),
            'port': os.environ.get('WEB_SOCKET.PORT'),
            'ping_interval': int(os.environ.get('WEB_SOCKET.PING_INTERVAL'))
        }
        return render_template(
            'index.html',
            web_config = web_config
        )

@index.route('/close/<id>', methods=['POST', 'GET'])
def close(id):
    if(request.method == 'GET'):
        if('tabs' in session):
            session['tabs'] = { nid: location for nid, location in session['tabs'].items() if nid != id }
            return 'id: {} closed...'.format(id)
        else:
            return 'Error id: {}...'.format(id)
