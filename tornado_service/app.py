import os
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.websocket

from web_app import Application
app = Application()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
