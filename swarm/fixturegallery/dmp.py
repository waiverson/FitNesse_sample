# encoding:utf-8
__author__ = 'xyc'


from fit.Fixture import Fixture

import requests, json


class RestApiTest(Fixture):

    _typeDict = {}

    def __init__(self):
        Fixture.__init__(self)
        self.__url = ""
        self.__headers = None
        self.__params = None
        self.__data = None
        self.__status = ""
        self.__result = ""
        self.__actual = ""

    _typeDict["url"] = "String"
    def url(self, s):
        self.__url = s

    _typeDict["headers"] = "Dict"
    def headers(self, s):
        self.__headers = dict(s)

    _typeDict["params"] = "Dict"
    def params(self, s):
        self.__params = dict(s)

    _typeDict["data"] = "Dict"
    def data(self, s):
        self.__data = dict(s)

    _typeDict["result"] = "String"
    def result(self):
        return self.inspect_result(self.__result)

    _typeDict["status"] = "Int"
    def status(self):
        return self.__status

    _typeDict["actual"] = "String"
    def actual(self):
        return self.__result

    _typeDict["get_token"] = "Default"
    def get_token(self):
        r = requests.post(self.__url, data=self.__data)
        self.__status = r.status_code
        try:
            RestApiTest._typeDict["token"] = json.loads(r.text)['result']['token']
            self.__result = r.text
        except:
            self.__result = r.text

    _typeDict["get_detail"] = "Default"
    def get_detail(self):
        if RestApiTest._typeDict.has_key("token"):
            self.params({'token': RestApiTest._typeDict["token"]})
        r = requests.get(self.__url, params=self.__params)
        self.__status = r.status_code
        self.__result = r.text

    def set_token(self):
        if RestApiTest._typeDict.has_key("token") and isinstance(self.__headers,dict) and self.__headers.has_key('SESSION-TOKEN'):
            self.__headers['SESSION-TOKEN'] = RestApiTest._typeDict["token"]

    # make a GET request
    _typeDict["get"] = "Default"
    def get(self):
        self.set_token()
        r = requests.get(self.__url, params=self.__params, headers=self.__headers)
        self.__status = r.status_code
        self.__result = r.text

    # make a POST request
    _typeDict["post"] = "Default"
    def post(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=self.__data)
        self.__status = r.status_code
        self.__result = r.text

    # make a POST request with json data
    _typeDict["post_json"] = "Default"
    def post_json(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=json.dumps(self.__data))
        self.__status = r.status_code
        self.__result = r.text

    # make a PUT request
    _typeDict["put"] = "Default"
    def put(self):
        self.set_token()
        r = requests.put(self.__url, params=self.__params, headers=self.__headers)
        self.__status = r.status_code
        self.__result = r.text

    # inspect response content
    def inspect_result(self, result):
        # inspect the result :response content should include {key,value}: {status:0}
        try:
            return "pass" if json.loads(result)["status"] == 0 else result
        except ValueError:
            return  result

    def get_task(self):
        pass