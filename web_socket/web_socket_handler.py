import os
import sys
import tornado.escape
import tornado.websocket
from helper import Logger
TAG = os.path.realpath(__file__)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from live_loader import Live_Loader

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for WebSocketHandler."""
    active_clients = set()

    def get_compression_options(self):
        # check this out
        return {}

    def open(self):
        self._loader = Live_Loader(self.request.full_url())
        WebSocketHandler.active_clients.add(self)
        Logger.warn(TAG, 'Started watching [ "{}" ] for changes...'.format(self._loader.location))

    def on_close(self):
        WebSocketHandler.active_clients.remove(self)
        Logger.warn(TAG, 'Stopped watching [ "{}" ] for changes...'.format(self._loader.location))

    def on_message(self, message):
        packet = self._loader.load()
        if(packet):
            self.write_message(packet)
