from MyPy import io

def log_default(name, msg, a, w):
    if a is False:
        if w is True:
            print(io.bcolors.WARNING + io.bcolors.BOLD + name + io.bcolors.ENDC + '\t>> {}'.format(msg), end='')
        else:
            print(io.bcolors.OKGREEN + io.bcolors.BOLD + msg + io.bcolors.ENDC)
    else:
        print(io.bcolors.WARNING + io.bcolors.BOLD + name + io.bcolors.ENDC + '\t>> ' + io.bcolors.WARNING + msg + io.bcolors.ENDC, end='')

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
        if type(msg) != str:
            msg = str(msg)
        self.__log(self.__name, msg + '\n', a, w)

    def log1(self, msg):
        if type(msg) != str:
            msg = str(msg)
        self.__log(self.__name, msg, a=False, w=True)

    def log2(self, msg):
        if type(msg) != str:
            msg = str(msg)
        self.__log(self.__name, msg, a=False, w=False)

    def boot(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass
