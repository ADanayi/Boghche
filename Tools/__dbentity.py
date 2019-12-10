from bson import ObjectId
import json

class DBEntity:
    Types_Mux = {}

    def __init__(self, _id, _type):
        self.__id = _id
        self.__type = _type

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    def to_dict(self):
        return {}

    def __str__(self):
        return '<DBEntity:{}>: {}'.format(self.__type, self.to_dict())

    @staticmethod
    def from_dict(D):
        type_name = D['type']
        try:
            cls = DBEntity.Types_Mux[type_name]
            return cls.from_dict(D)
        except:
            return None
