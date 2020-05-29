import os
import json
import uuid
import urllib
import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.options
import tornado.websocket
from tracker import Logger_Class
__file_location__ = os.path.realpath(__file__)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for WebSocketHandler."""
    active_clients = set()

    def get_compression_options(self):
        # check this out
        return {}

    def open(self):
        url = urllib.parse.urlparse(self.request.full_url())
        dirs = list(filter(lambda x: len(x) > 0, url.path.split('/')))[1:]
        self._location = os.path.join(os.path.abspath(os.sep), *dirs)
        self._data = { 'folders': set(), 'files': set() }
        WebSocketHandler.active_clients.add(self)
        print('[ WebSocketHandler.open ]:: Client connected for path "{}"...'.format(self._location))

    def on_close(self):
        WebSocketHandler.active_clients.remove(self)
        print('[ WebSocketHandler.on_close ]:: Client disconnected from path "{}"...'.format(self._location))

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        diff = self.load_diff()
        if(diff):
            self.write_message(json.dumps(diff))

    def load_diff(self):
        dirs = set(os.listdir(self._location))
        tmp = {}
        tmp['files'] = set(filter(lambda x: os.path.isfile(os.path.join(self._location, x)), dirs))
        tmp['folders'] = dirs - tmp['files']
        diff = { 'files': [] , 'folders': []}
        for key in self._data.keys():
            v0 = self._data[key]
            v1 = tmp[key]
            added = v1 - v0
            removed = v0 - v1
            diff[key] += [ (name, True) for name in added ] + [ (name, False) for name in removed ]
            self._data[key].update(added)
            self._data[key] = self._data[key] - removed
        return diff
