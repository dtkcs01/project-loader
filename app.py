import os
import colorama
import traceback
import tornado.ioloop
from helper import Logger
from web_app import Application
TAG = os.path.realpath(__file__)

def main():
    colorama.init()
    Logger.switch_logging(True)
    app = Application().listen(int(os.environ.get('PORT')))
    tornado.ioloop.IOLoop.current().start()

try:
    main()
except KeyboardInterrupt as k:
    Logger.warn(TAG, 'Closing application...')
except Exception as e:
    Logger.critical(TAG, 'Error while running application', traceback.format_exc())
