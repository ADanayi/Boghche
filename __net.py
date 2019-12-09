from .__mod import BMod

class BNet(BMod):

    def __init__(self, name, endpoint=None, app=None, log_func=None):
        BMod.__init__(self, name=name, log_func=log_func)
        self.__app = app
        self.__endpoint = endpoint
        self.__BE = None

    def net_boot(self, app, root):
        self.__app = app
        self.__root = root

    def get_app(self):
        return self.__app

    @property
    def app(self):
        return self.__app

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def root(self):
        return self.__root

    def get_endpoint(self):
        return self.__endpoint

    def get_classes(self=None):
        c = list(BNet.__base__.get_classes())
        c.append(BNet)
        return tuple(c)

    def get_mod(self, mod_name):
        return self.__root.get_mod(mod_name)
