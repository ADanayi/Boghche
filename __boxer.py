from .__net import BNet
from .__entities import add_to_app_t as __add_to_app
from flask import render_template_string
import os
from .__entities import add_handler_to_app

class BBoxer(BNet):

    def __init__(self, name, endpoint, app=None, log_func=None):
        BNet.__init__(self, endpoint=endpoint, name=name, app=app, log_func=log_func)
        self.__Goodies = {}
        self.__Handler = {}
        self.__temp_dir = os.path.join('.', 'templates', 'boxers', self.name)
        if not os.path.exists(self.__temp_dir):
            os.makedirs(self.__temp_dir)

    def get_classes(self=None):
        c = list(BBoxer.__base__.get_classes())
        c.append(BBoxer)
        return tuple(c)

    def add_to_goodies(self, kw, val):
        self.__Goodies[kw] = val

    @property
    def goodies(self):
        return self.__Goodies.copy()

    def boot(self, app, root):
        self.log('\t{} >> Booting: '.format(self.name), w=True)
        self.net_boot(app, root)
        self.log('[Done]', a=True)

    def add_handler(self, endpoint, handler_function, endpoint_name):
        self.log('\t{} >> Added handler: {} -> {}'.format(self.name, endpoint_name,self.endpoint + endpoint))
        self.__Handler[endpoint] = handler_function
        self.add_to_goodies(endpoint_name, self.endpoint + endpoint)
        self.root.add_to_goodies(self.name + '_' + endpoint_name, self.endpoint + endpoint)
        add_handler_to_app(self.app, self.endpoint + endpoint, self.name + '_' + endpoint_name, handler_function)

    def render(self, template_file, **kwargs):
        temp_file_dir = os.path.join(self.__temp_dir, template_file)
        if not os.path.exists(os.path.join(self.__temp_dir, template_file)):
            print('ERROR: FILE NOT EXISTS.', self.__temp_dir, template_file, temp_file_dir)
            return ('Internal error')
        with open(temp_file_dir, 'r') as html_file:
            html_str = html_file.read()
        return render_template_string(html_str, **self.root.goodies, **self.goodies, **kwargs)
        # return render_template(temp_file_dir, **self.root.goodies, **self.goodies, **kwargs)
