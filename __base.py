def log_default(name, msg, a, w):
    if a is False:
        print('{} >> {}'.format(name, msg), end = '' if w else '\n')
    else:
        print(msg, end = '' if w else '\n')

import os

class BBase:

    def __init__(self, name, log_func=None):
        self.__name = name
        self.__log = log_func if log_func is not None else log_default
        self.__dir = os.path.join('.', 'Mod_files', self.__name)
        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)

    @property
    def dir(self):
        return self.__dir

    @staticmethod
    def get_classes(self=None):
        return (BBase,)

    @property
    def name(self):
        return self.__name

    def get_name(self):
        return self.__name

    def log(self, msg, a=True, w=False):
        self.__log(self.__name, msg, a, w)

    def boot(self):
        pass

    def load(self):
        pass
