import os
import threading

from application_modules import Web

class Application(object):
    """docstring for Application."""

    def __init__(self, flask_app):
        super(Application, self).__init__()
        self._web_socket = Web()
        self.load_thread(flask_app)

    def load_thread(self, flask_app):
        self._thread = threading.Thread(target = flask_app.run, kwargs = {
            'host' : os.environ.get('APPLICATION.HOST_IP'),
            'port' : os.environ.get('FLASK_APP.HOST_PORT')
        })
        self._thread.setDaemon(True)

    def start(self):
        try:
            self._thread.start()
            self._web_socket.start()
        except KeyboardInterrupt as k:
            self._web_socket.stop()
            print('KeyboardInterrupt:: "/application_class.py" [ Application.start <- ]: Closing Application...')
        except Exception as e:
            print('Error:: "/application_class.py" [ Application.start <- ]: Closing Application...')
            print(e)
