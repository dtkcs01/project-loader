import os
import tornado.web
from helper import Logger
from web_socket import WebSocketHandler

TAG = os.path.realpath(__file__)

class Application(tornado.web.Application):
    def __init__(self):
        Logger.debug(TAG, 'Initialising Tornado Application...')
        handlers = self.define_handlers()
        settings = self.define_settings()
        super(Application, self).__init__(handlers, **settings)

    def define_handlers(self):
        return [
            (r'/d/?.*', MainHandler),
            (r'/websocket/?.*', WebSocketHandler)
        ]

    def define_settings(self):
        return dict(
            cookie_secret = os.environ.get('COOKIE_SECRET'),
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies = True,
            debug = True
        )

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
