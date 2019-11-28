from .__base import BBase

class BMod(BBase):

    def __init__(self, name, log_func=None):
        BBase.__init__(self, name=name, log_func=log_func)

    def get_classes(self=None):
        c = list(BMod.__base__.get_classes())
        c.append(BMod)
        return tuple(c)
