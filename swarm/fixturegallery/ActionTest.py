# encoding:utf-8
__author__ = 'xyc'


from fit.Fixture import Fixture

import requests, json


class ActionTest(Fixture):

    _typeDict = {}

    def __init__(self):
        Fixture.__init__(self)
        self.__url = ""
        self.__headers = None
        self.__params = None
        self.__data = None
        self.status = ""
        self.result = ""

    _typeDict["url"] = "String"
    _typeDict["headers"] = "Dict"
    _typeDict["params"] = "Dict"
    _typeDict["data"] = "Dict"
    _typeDict["get"] = "Default"
    _typeDict["post"] = "Default"
    _typeDict["put"] = "Default"
    _typeDict["get_token"] = "Default"
    _typeDict["post_json"] = "Default"
    _typeDict["post_by_cookie"] = "Default"
    _typeDict["get_detail"] = "Default"
    _typeDict["get_cookie"] = "Default"
    _typeDict["get_by_cookie"] = "Default"
    _typeDict["put_by_cookie"] = "Default"
    _typeDict["status"] = "Int"
    _typeDict["result"] = "String"

    def url(self, s):
        self.__url = s

    def headers(self, s):
        self.__headers = dict(s)

    def params(self, s):
        self.__params = dict(s)

    def data(self, s):
        self.__data = dict(s)

    def result(self):
        return self.result

    def status(self):
        return self.status

    def get_token(self):
        r = requests.post(self.__url, data=self.__data)
        self.status = r.status_code
        try:
            self.result = json.loads(r.text)['result']['token']
            ActionTest._typeDict["token"] = self.result
        except:
            self.result = r.text

    def get_detail(self):
        if ActionTest._typeDict.has_key("token"):
            self.params({'token': ActionTest._typeDict["token"]})
        r = requests.get(self.__url, params=self.__params)
        self.status = r.status_code
        self.result = r.text

    def set_token(self):
        if ActionTest._typeDict.has_key("token") and isinstance(self.__headers,dict) and self.__headers.has_key('SESSION-TOKEN'):
            self.__headers['SESSION-TOKEN'] = ActionTest._typeDict["token"]

    def get_cookie(self):
        r = requests.post(self.__url, data=self.__data)
        self.status = r.status_code
        try:
            ActionTest._typeDict["cookie"] = requests.utils.dict_from_cookiejar(r.cookies)
            self.result = str(ActionTest._typeDict["cookie"])
        except:
            self.result = r.text

    def get_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.get(self.__url, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.text
        else:
            r = requests.get(self.__url)
            self.status = r.status_code
            self.result = r.text

    def get(self):
        self.set_token()
        r = requests.get(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text

    def post(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=self.__data)
        self.status = r.status_code
        self.result = r.text[:100]

    def post_json(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=json.dumps(self.__data))
        self.status = r.status_code
        self.result = r.text[:100]

    def post_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.post(self.__url, data=self.__data, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.text
        else:
            r = requests.post(self.__url, data=self.__data)
            self.status = r.status_code
            self.result = r.text

    def put(self):
        self.set_token()
        r = requests.put(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text[:100]

    def put_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.put(self.__url, data=self.__data, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.text
        else:
            r = requests.put(self.__url, data=self.__data)
            self.status = r.status_code
            self.result = r.text



