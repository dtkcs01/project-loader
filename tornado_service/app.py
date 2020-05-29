import os
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.websocket

from web_app import Application
from tracker import Logger_Class
Logger_Class.switch_logger_state()
app = Application()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
