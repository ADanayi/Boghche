from flask import Flask, jsonify, request
import urllib
from base64 import b64decode

class JSONTOJSONEndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        req = request.get_json(force=True)
        header = request.headers.get("Authorization")
        # print("Header of request == {}".format(header))
        if req != None:
            return  jsonify(self.action(req))
        else:
            return jsonify({'err':'Error!'})

class JSONTOJSONEndpointAction_basicAuth(object):
    def __init__(self, action, name=__name__):
        self.action = action
        self.__name__ = name

    def __call__(self, *args):
        req = request.get_json(force=True)
        header = request.headers.get("Authorization")
        # print("Header of request == {}".format(header))
        if header == None:
            return jsonify({'err':'auth error'})
        if req != None:
            if header != None:
                user, password = b64decode(header.split(' ')[1]).decode().split(':')
                req['auth_password'] = password
                req['auth_user'] = user
            return jsonify(self.action(req))
        else:
            return jsonify({'status':'error'})

# class FlaskAppWrapper(object):
#     app = None

#     def __init__(self, name, tokening=False):
#         self.app = Flask(name)
#         self.tokening = tokening

#     def run(self, ip, Port, debug=False):
#         self.app.run(host = ip, port = Port)

#     def add_jsonToJsonEndpoint(self, endpoint=None, endpoint_name=None, handler=None):
#         if not self.tokening:
#             self.app.add_url_rule(endpoint, endpoint_name, JSONTOJSONEndpointAction(handler), methods=['GET', 'POST'])
#         else:
#             self.app.add_url_rule(endpoint, endpoint_name, JSONTOJSONEndpointAction_basicAuth(handler), methods=['GET', 'POST'])

def add_to_app_t(app, endpoint=None, endpoint_name=None, handler=None, fetch_auth=True):
    if fetch_auth:
        app.add_url_rule(endpoint, endpoint_name, JSONTOJSONEndpointAction_basicAuth(handler), methods=['GET', 'POST'])
    else:
        app.add_url_rule(endpoint, endpoint_name, JSONTOJSONEndpointAction(handler), methods=['GET', 'POST'])

def add_handler_to_app(app, endpoint=None, endpoint_name=None, handler=None):
    app.add_url_rule(endpoint, endpoint_name, handler, methods=['GET', 'POST'])

# def action():
#     return {"status":"OK"}

# a = FlaskAppWrapper('wrap')
# a.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action)
# a.run()
