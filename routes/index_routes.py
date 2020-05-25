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

def create_id(is_user_id = False):
    user_id = ''
    length = int(os.environ.get('ID_LENGTH.USER')) if is_user_id else int(os.environ.get('ID_LENGTH.TABS'))
    for i in range(length):
        r = random.randint(0, 25)
        user_id += str(random.choice([ r%10, chr(97 + r), chr(65 + r) ]))
    return user_id

@index.route('/', methods=['POST', 'GET'])
def home():
    if(request.method == 'GET'):
        session.setdefault('ids', {})
        tabs = session['ids']
        while True:
            id = create_id()
            if(id not in tabs):
                if('redirect' in request.args):
                    tabs[id] = request.args['redirect'].strip()
                else:
                    tabs[id] = pathlib.Path.home().__str__()
                break
        session['ids'] = tabs
        res = make_response(redirect(url_for('index.display', id = id)))
        if('user_id' not in request.cookies):
            res.set_cookie('user_id', create_id(True))
        return res

@index.route('/id/<id>', methods=['POST', 'GET'])
def display(id):
    print(session['ids'])
    if(request.method == 'GET'):
        navbar = create_navbar(session['ids'][id])
        web_config = {
            'id': id,
            'location': session['ids'][id],
            'ip': os.environ.get('APPLICATION.HOST_IP'),
            'port': os.environ.get('WEB_SOCKET.PORT'),
            'ping_interval': int(os.environ.get('WEB_SOCKET.PING_INTERVAL'))
        }
        return render_template(
            'index.html',
            web_config = web_config,
            navbar = navbar
        )
