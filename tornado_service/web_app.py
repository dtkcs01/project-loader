import os
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.websocket
from web_socket import WebSocketHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/d/.*", MainHandler), (r"/chatsocket", WebSocketHandler)]
        settings = dict(
            cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            debug =True
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        dir_branch = [ name for name in self.request.uri.split('/') if(len(name.strip()) > 0) ][1:]
        path = os.path.join(os.path.abspath(os.sep), *dir_branch)
        d = os.listdir(path)
        for dd in d:
            WebSocketHandler.update_cache({"id": "asdasd", "body":dd})
        self.render("index.html", messages=WebSocketHandler.cache)
