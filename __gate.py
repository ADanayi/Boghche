from .__net import BNet
from .__entities import add_to_app_t

class BGate(BNet):

    def __init__(self, name, endpoint, app=None, log_func=None):
        BNet.__init__(self, endpoint=endpoint, name=name, app=app, log_func=log_func)
        self.__F = {}

    def get_classes(self=None):
        c = list(BGate.__base__.get_classes())
        c.append(BGate)
        return tuple(c)

    def api_hello(self, req):
        return {'hi':'hi'}

    def __handler(self, req):
        try:
            username = req['auth_user']
            password = req['auth_password']
            t = req['type']
        except:
            return {'status':'error', 'error':'invalid args'}
        if not self.auth(username, password):
            return {'status':'error', 'error':'unathorized'}
        if not t in self.__F:
            try:
                f = eval('self.api_{}'.format(t), globals(), locals())
            except:
                return {'status':'error', 'error':'invalid type'}
            self.__F[t] = f
        try:
            ret = self.__F[t](req)
            ret['status'] = 'ok'
            return ret
        except:
            return {'status':'error', 'error':'internal error'}

    def auth(self, user_name, password):
        return True

    def boot(self, app, root):
        global add_to_app_t
        self.net_boot(app, root)
        self.log('Booting: ', w=True)
        add_to_app_t(
            app = self.get_app(),
            endpoint = self.get_endpoint(),
            endpoint_name = 'gate::{}'.format(self.get_name()),
            handler = self.__handler,
            fetch_auth=True
        )
        self.log('[Done]', a=True)
