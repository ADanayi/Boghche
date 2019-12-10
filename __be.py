from .__mod import BMod

class BBE(BMod):

    def __init__(self, name, log_func=None):
        BMod.__init__(self, name=name,log_func=log_func)

    def get_classes(self=None):
        c = list(BBE.__base__.get_classes())
        c.append(BBE)
        return tuple(c)

    @property
    def root(self):
        return self.__root

    def boot(self, root):
        self.__root = root
