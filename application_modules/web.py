import os
import sys
import json

import asyncio
import websockets

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from fs import File_System

class Web(object):
    """docstring for Web."""

    def __init__(self):
        super(Web, self).__init__()
        self._listen = True
        self._fs = File_System()

    def start(self):
        print('Message:: "application_modules/web.py" [ Web.start <- ]:  Initializing WebSocket...')
        self._socket = websockets.serve(
            self.handler,
            os.environ.get('APPLICATION.HOST_IP'),
            int(os.environ.get('WEB_SOCKET.PORT'))
        )
        asyncio.get_event_loop().run_until_complete(self._socket)
        asyncio.get_event_loop().run_forever()

    async def handler(self, socket, path):
        i = 0
        config = {}
        while self._listen:
            try:
                config = json.loads(await socket.recv())
                await socket.send(json.dumps(self._fs.explore(config['location'])))
            except Exception as e:
                self._fs.add_clean_session_id(config['id'], config['user'])
                print('Message:: "application_modules/web.py" [ Web.handler <- ]:  Client Away...')
                break
            i += 1

    def stop(self):
        print('Message:: "application_modules/web.py" [ Web.stop <- ]:  Closing WebSocket...')
        self._listen = False
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()
