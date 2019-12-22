from .__net import BNet
from .__entities import add_to_app_t

import traceback


class BGate(BNet):

    def __init__(self, name, endpoint, app=None, log_func=None, needs_auth=True):
        BNet.__init__(self, endpoint=endpoint, name=name, app=app, log_func=log_func)
        self.__F = {}
        self.__needs_auth = needs_auth

    def get_classes(self=None):
        c = list(BGate.__base__.get_classes())
        c.append(BGate)
        return tuple(c)

    def api_hello(self, req):
        return True, {'hi':'hi'}

    def _fetch_type(self, req):
        return req['type']

    def _handler(self, req):
        try:
            username = req['auth_user'] if self.__needs_auth else None
            password = req['auth_password'] if self.__needs_auth else None
            t = self._fetch_type(req)
        except:
            return {'status':'error', 'error':'invalid args'}
        if self.__needs_auth:
            Valid, D = self.auth(username, password)
            if not Valid:
                return {'status':'error', 'error':'unauthorized (1)'}
            else:
                req['auth'] = D
                if not self.post_auth(req):
                    return {'status': 'error', 'error': 'unauthorized (2)'}
        if not t in self.__F:
            try:
                f = eval('self.api_{}'.format(t), globals(), locals())
            except:
                traceback.print_exc()
                return {'status':'error', 'error':'invalid type'}
            self.__F[t] = f
        try:
            ok, result = self.__F[t](req)
            if ok:
                ret = {'status':'ok', 'result': result}
            else:
                ret = {'status':'error', 'error':'handled error', 'result': result}
            return ret
        except:
            traceback.print_exc()
            return {'status':'error', 'error':'internal error'}

    def auth(self, user_name, password):
        if not self.__needs_auth:
            return True, {}
        else:
            raise Exception('Auth is not implemented')

    def post_auth(self, req):
        return True
    
    def boot(self, app, root):
        global add_to_app_t
        self.net_boot(app, root)
        self.log1('Booting: ')
        add_to_app_t(
            app = self.get_app(),
            endpoint = self.get_endpoint(),
            endpoint_name = 'gate::{}'.format(self.get_name()),
            handler = self._handler,
            fetch_auth=self.__needs_auth
        )
        self.log2('[Done]')
