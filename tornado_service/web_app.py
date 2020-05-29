import os
import urllib
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.websocket
from web_socket import WebSocketHandler
from tracker import Logger_Class

__file_location__ = os.path.realpath(__file__)

class Application(tornado.web.Application):
    def __init__(self):
        print('[ web_app.py ( Application.__init__ ) ]:: Initialising Tornado Application...')
        handlers = [(r"/d/?.*", MainHandler), (r"/websocket/?.*", WebSocketHandler)]
        settings = dict(
            cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            debug = True
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
