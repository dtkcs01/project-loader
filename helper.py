from colorama import Fore, Back, Style

class Logger(object):
    """docstring for Logger."""
    __is_logging__ = False
    types = {
        0: Back.LIGHTBLUE_EX, # Origin (i.e. TAG) Color
        1: Fore.WHITE, # Info (i.e. Logger.info) Color
        2: Fore.GREEN, # Debug (i.e. Logger.debug) Color
        3: Fore.YELLOW, # Warn (i.e. Logger.warn) Color
        4: Fore.LIGHTRED_EX, # Error (i.e. Logger.error) Color
        5: Fore.RED # Critical Error (i.e. Logger.critical) Color
    }
    __reset__ = Style.RESET_ALL

    def __init__(self):
        super(Logger, self).__init__()

    @classmethod
    def switch_logging(self, flag = None):
        self.__is_logging__ = (not self.__is_logging__) if flag == None else flag

    @classmethod
    def color(self, message, type):
        return '{}{}{}'.format(
            self.types[type],
            message,
            self.__reset__
        )

    @classmethod
    def info(self, TAG, message):
        print('{} {}'.format(
            self.color('[ {} ]::'.format(TAG), 0),
            self.color(message, 1)
        ))

    @classmethod
    def debug(self, TAG, message):
        print('{} {}'.format(
            self.color('[ {} ]::'.format(TAG), 0),
            self.color(message, 2)
        ))

    @classmethod
    def warn(self, TAG, message):
        print('{} {}'.format(
            self.color('[ {} ]::'.format(TAG), 0),
            self.color(message, 3)
        ))

    @classmethod
    def error(self, TAG, message, err = None):
        print('{} {}\n {}'.format(
            self.color('[ {} ]::'.format(TAG), 0),
            self.color(message, 4),
            self.color(err, 4)
        ))

    @classmethod
    def critical(self, TAG, message, err = None):
        print('{} {}\n {}'.format(
            self.color('[ {} ]::'.format(TAG), 0),
            self.color(message, 5),
            self.color(err, 5)
        ))
