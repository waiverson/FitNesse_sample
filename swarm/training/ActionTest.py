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
        self.actual = ""

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
    _typeDict["actual"] = "String"

    def url(self, s):
        self.__url = s

    def headers(self, s):
        self.__headers = dict(s)

    def params(self, s):
        self.__params = dict(s)

    def data(self, s):
        self.__data = dict(s)

    def result(self):
        return self.inspect_result(self.result)

    def status(self):
        return self.status

    def actual(self):
        return self.result

    def get_token(self):
        r = requests.post(self.__url, data=self.__data)
        self.status = r.status_code
        try:
            ActionTest._typeDict["token"] = json.loads(r.text)['result']['token']
            self.result = r.text
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

    # get the website access cookie
    def get_cookie(self):
        r = requests.post(self.__url, data=self.__data)
        self.status = r.status_code
        try:
            ActionTest._typeDict["cookie"] = requests.utils.dict_from_cookiejar(r.cookies)
            self.result = str(ActionTest._typeDict["cookie"])
        except:
            self.result = r.text

    # make a GET request with cookie
    def get_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.get(self.__url, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.json()
        else:
            r = requests.get(self.__url)
            self.status = r.status_code
            self.result = r.text

    # make a GET request
    def get(self):
        self.set_token()
        r = requests.get(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text

    # make a POST request
    def post(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=self.__data)
        self.status = r.status_code
        self.result = r.text

    # make a POST request with json data
    def post_json(self):
        self.set_token()
        r = requests.post(self.__url, params=self.__params, headers=self.__headers, data=json.dumps(self.__data))
        self.status = r.status_code
        self.result = r.text

    # make a POST request with cookie
    def post_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.post(self.__url, data=self.__data, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.text
        else:
            r = requests.post(self.__url, data=self.__data)
            self.status = r.status_code
            self.result = r.text

    # make a PUT request
    def put(self):
        self.set_token()
        r = requests.put(self.__url, params=self.__params, headers=self.__headers)
        self.status = r.status_code
        self.result = r.text

    # make a PUT request with cookie
    def put_by_cookie(self):
        if ActionTest._typeDict.has_key("cookie"):
            r = requests.put(self.__url, data=self.__data, cookies = ActionTest._typeDict["cookie"])
            self.status = r.status_code
            self.result = r.text
        else:
            r = requests.put(self.__url, data=self.__data)
            self.status = r.status_code
            self.result = r.text

    # inspect response content
    def inspect_result(self,result):
        # inspect the result :response content should include {key,value}: {status:0}
        try:
            return "pass" if json.loads(result)["status"] == 0 else result
        except ValueError:
            return  result

