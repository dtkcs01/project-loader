from colorama import Fore, Back, Style

class Logger(object):
    """docstring for Logger."""
    __is_logging__ = False
    __origin_color__ = Back.LIGHTBLUE_EX
    __info_color__ = Fore.WHITE
    __debug_color__ = Fore.GREEN
    __warn_color__ = Fore.YELLOW
    __error_color__ = Fore.LIGHTRED_EX
    __critical_color__ = Fore.RED
    __reset__ = Style.RESET_ALL
    types = {
        0: __origin_color__,
        1: __info_color__,
        2: __debug_color__,
        3: __warn_color__,
        4: __error_color__,
        5: __critical_color__
    }

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
