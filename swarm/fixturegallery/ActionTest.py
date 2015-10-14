# encoding:utf-8
__author__ = 'abear'


from fit.Fixture import Fixture

import requests, json


class ActionTest(Fixture):

    _typeDict = {}

    def __init__(self):
        Fixture.__init__(self)
        self.__url = ""
        self.__headers = None
        self.__params = None
        self.status = ""
        self.result = ""

    _typeDict["url"] = "String"
    _typeDict["headers"] = "Dict"
    _typeDict["params"] = "Dict"
    _typeDict["get"] = "Default"
    _typeDict["post"] = "Default"
    _typeDict["get_token"] = "Default"
    _typeDict["status"] = "Int"
    _typeDict["result"] = "String"

    def url(self, s):
        self.__url = s

    def headers(self, s):
        self.__headers = dict(s)

    def params(self, s):
        self.__params = dict(s)

    def result(self):
        return self.result

    def status(self):
        return self.status

    def get_token(self):
        r = requests.post(self.__url, self.__params)
        self.status = r.status_code
        try:
            self.result = json.loads(r.text)['result']['token']
            ActionTest._typeDict["token"] = self.result
        except:
            self.result = r.text

    def get(self):
        self.__headers['SESSION-TOKEN'] = ActionTest._typeDict["token"]
        r = requests.get(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text

    def post(self):
        self.__headers['SESSION-TOKEN'] = ActionTest._typeDict["token"]
        r = requests.post(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text[:100]





