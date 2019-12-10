from .__base import BBase
from .__gate import BGate
from .__be import BBE
from .__boxer import BBoxer
from .__net import BNet

from flask import Flask

class BRoot(BBase):

    def __init__(self, name, log_func=None):
        BBase.__init__(self, name=name, log_func=log_func)
        self.__Mod = {
            'boxer': {},
            'gate': {},
            'be': {}
        }
        self.__Goodies = {}


    def __proc_get_type(self, mod):
        cl = mod.get_classes()[-1]
        if cl == BBoxer:
            return 'boxer'
        elif cl == BGate:
            return 'gate'
        elif cl == BRoot:
            return 'root'
        elif cl == BBE:
            return 'be'

    def get_classes(self=None):
        c = list(BRoot.__base__.get_classes())
        c.append(BRoot)
        return tuple(c)

    def __add_to_godies(self, module):
        if BNet in module.get_classes():
            self.__Goodies[module.name] = module.endpoint

    @property
    def goodies(self):
        return self.__Goodies.copy()

    def add_to_goodies(self, prop, value):
        self.__Goodies[prop] = value

    def add_module(self, module):
        if self.__proc_get_type(module) == 'root':
            self.log('Passing Root to Root?!')
            return
        self.__add_to_godies(module)
        self.__Mod[self.__proc_get_type(module)][module.name] = module
        self.log('Added module {}.'.format(module.name))

    def get_mod(self, mod_name):
        for _type, mods in self.__Mod.items():
            if mod_name in mods:
                return mods[mod_name]
        return None

    def boot(self, import_name):
        self.log('Booting...')

        self.log('Creating the Flask app: ', w=True)
        self.__app =  Flask(import_name)
        self.log('[Done]', a=True)

        self.log('\tBEs:')
        for (name, be) in self.__Mod['be'].items():
            be.boot(self)

        self.log('\tGates:')
        for (name, gate) in self.__Mod['gate'].items():
            gate.boot(self.__app, self)
        
        self.log('\tBoxers:')
        for (name, boxer) in self.__Mod['boxer'].items():
            boxer.boot(self.__app, self)
        
        self.log('Booting finished...')

    def load(self):
        self.log('Loading...')

        self.log('\tBEs:')
        for (name, be) in self.__Mod['be'].items():
            be.load()

        self.log('\tGates:')
        for (name, gate) in self.__Mod['gate'].items():
            gate.load()
        
        self.log('\tBoxers:')
        for (name, boxer) in self.__Mod['boxer'].items():
            boxer.load()
        
        self.log('Loading finished...')

    def run(self, *args, **kwargs):
        self.__app.run(*args, **kwargs)
