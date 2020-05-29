class Logger_Class(object):
    __flag__ = False

    def __init__(self):
        super(Logger_Class, self).__init__()

    @classmethod
    def switch_logger_state(self, state = None):
        if(state == None):
            Logger_Class.__flag__ = not Logger_Class.__flag__
        else:
            Logger_Class.__flag__ = state

    def log(self, log_type, invoker_location, message, error_obj = None):
        if(self.__flag__):
            print('{}:: [ "{}" <- ]: [ {} ]'.format(log_type, invoker_location, message))
            if(error_obj):
                print(error_obj)
