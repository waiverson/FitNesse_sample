# encoding:utf-8
__author__ = 'xyc'


from fit.Fixture import Fixture

import requests, json
from Compare import CompareMode


class core(Fixture):

    _typeDict = {}

    def __init__(self):
        Fixture.__init__(self)
        self._url = ""
        self._header = {}
        self._params = None
        self._data = None
        self._expect_result = None
        self._diff_by = ""
        self._diff_result = ""
        self._actual_result = ""

    _typeDict["url"] = "String"
    def url(self, s):
        self._url = s

    _typeDict["headers"] = "Dict"
    def headers(self, s):
        self._header.update(dict(s))

    _typeDict["params"] = "Dict"
    def params(self, s):
        self._params = dict(s)

    _typeDict["data"] = "Dict"
    def data(self, s):
        self._data = dict(s)

    _typeDict["expect_result"] = "Dict"
    def expect_result(self, s):
        self.__expect_result = dict(s)

    _typeDict["diff_by"] = "String"
    def diff_by(self, s):
        self._diff_by = s

    _typeDict["diff_result"] = "String"
    def diff_result(self):
        return self._diff_result

    _typeDict["actual_result"] = "String"
    def actual_result(self):
        return self._actual_result

    _typeDict["get_token"] = "Default"
    def get_token(self):
        r = requests.post(self._url, data=self._data)
        response_content = json.loads(r.content)
        self._actual_result = r.content
        Core._typeDict.update({"token": response_content['result']['token']})
        self._diff_result = self.compare(self.__expect_result, response_content, self._diff_by)

    _typeDict["set_token"] = "Default"
    def set_token(self):
        if bool(Core._typeDict.has_key("token")
                and isinstance(self._header, dict)):
            self._header.update({'SESSION-TOKEN': Core._typeDict["token"]})

    _typeDict["get_accesskey"] = "Default"
    def get_accesskey(self):
        r = requests.get(self._url, params=self._params, headers=self._header)
        response_content = json.loads(r.content)
        self._actual_result = r.content
        Core._typeDict.update({"accesskey": response_content['result']['app_key']})
        self._diff_result = self.compare(self.__expect_result, response_content, self._diff_by)

    _typeDict["set_accesskey"] = "Default"
    def set_accesskey(self):
        if bool(Core._typeDict.has_key("accesskey")
                and isinstance(self._header, dict)):
            self._header.update({"APPKEY": Core._typeDict["accesskey"]})

    _typeDict["get"] = "Default"
    def get(self):
        r = requests.get(self._url, params=self._params, headers=self._header)
        response_content = json.loads(r.content)
        self._actual_result = r.content
        self._diff_result = self.compare(self.__expect_result, response_content, self._diff_by)

    _typeDict["post"] = "Default"
    def post(self):
        r = requests.post(self._url, params=self._params, headers=self._header, data=self._data)
        response_content = json.loads(r.content)
        self._actual_result = r.text
        self._diff_result = self.compare(self.__expect_result, response_content, self._diff_by)

    # inspect response content
    def compare(self, ob1, ob2, diff_by):
        # inspect the result by  compare

        def type_handler(text):
            for k, v in text.items():
                if isinstance(v, dict):
                    type_handler(v)
                if isinstance(v, str) and v.lower() in ("false", "true"):
                    text.update({k:json.loads(v.lower())})
            return text

        def is_placeholder(kv):
            """
            Takes {k, v} dict, returns True if it's a placeholder.
            """
            for k, v in kv.items():
                return not bool(
                    k == '%s'
                )

        compare = CompareMode.get_compare_mode("OBJECT")
        result = compare.diff(compare.dict_to_object(type_handler(ob1)), compare.dict_to_object(ob2), diff_by)

        # because fitnesse cell in table is not support null collection(dict,list,set,tuple),so use '%s' for placeholder .
        # so,'%s' should be ignore
        result.update({result.keys()[0]:filter(is_placeholder, result[result.keys()[0]])})
        for k, v in result.items():
            if not v :
                return 'PASS'
            else:
                return str(result)


if __name__ == '__main__':
    core = Core()
    core._expect_result = {"status": 0,"%s": 0,"result": {"first_login": 'false',"is_active": 'true',"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170}}
    core._url = "http://172.20.0.226:16001/WEBAPI/auth/accessToken/"
    _url2 = "http://172.20.0.226:16001/WEBAPI/webserver/appkey/get"
    core._data = {'user':'liuweiwei5@163.com','password':'liuweiwei'}
    r = requests.post(core._url, data=core._data)
    response_content = json.loads(r.content)
    core._diff_by = 'kv'
    print core.compare(core._expect_result, response_content, core._diff_by)


