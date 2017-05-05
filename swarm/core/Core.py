# encoding:utf-8
__author__ = 'xyc'


from fit.Fixture import Fixture
import requests, json, sys, time
from restdata import RestResponse
from variables import Variables

reload(sys)
sys.setdefaultencoding("utf-8")

class Core(Fixture):

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
        self._last_response = ""
        self._validator = ""
        self._wait_time = ""
        self._slot = ""

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
        self._expect_result = dict(s)

    # 提供校验方式："kv"：key&value值校验，"struct":比较key&value类型校验
    _typeDict["diff_by"] = "String"
    def diff_by(self, s):
        self._diff_by = s

    _typeDict["diff_result"] = "String"
    def diff_result(self):
        return self._diff_result

    #提供将比较完的结果返回到fitnesse
    _typeDict["actual_result"] = "String"
    def actual_result(self):
        return self._actual_result

    # 提供将调用完的结果返回到fitnesse（必要时）
    _typeDict["last_response"] = "Default"
    def last_response(self, s):
        self._last_response = s

    # 设置校验器类型：OBJECT | DICT | JSON_SCHEMA | JSON
    _typeDict["validator"] = "String"
    def validator(self, s):
        self._validator = s

    # 设置等待时长，单位：秒
    _typeDict["wait_time"] = "String"
    def wait_time(self, s):
        self._wait_time = s

    # 将某值缓存起来，以便后续接口直接使用
    _typeDict["slot"] = "String"
    def slot(self, s):
        self._slot = s

    #通过|check|debug||,将self._url（其他self字段）返回到fitnesse下，用于调试。
    _typeDict["debug"] = "String"
    def debug(self):
        return str(self._url)

    def clean_params(self):
        self._params = None

    def clean_data(self):
        self._data = None
        self._wait_time = None

    def clean_last_quary_condition(self):
        self.clean_params()
        self.clean_data()

    def clean_diff_result(self):
        self._diff_result = ""

    def clean_actual_result(self):
        self._actual_result = ""

    def clean_last_result(self):
        self.clean_diff_result()
        self.clean_actual_result()

    #请求开始前，准备
    def setup(self):
        self.clean_last_result()
        self.substitute()

    _typeDict["get"] = "Default"
    def get(self):
        self.setup()
        resp = requests.get(self._url, params=self._params, headers=self._header)
        self.tearDown(resp)

    #默认body为dict格式
    _typeDict["post_by_dict"] = "Default"
    def post_by_dict(self):
        self.setup()
        resp = requests.post(self._url, params=self._params, headers=self._header, data=self._data)
        self.tearDown(resp)

    #默认body为json格式
    _typeDict["post"] = "Default"
    def post(self):
        self.setup()
        resp = requests.post(self._url, params=self._params, headers=self._header, data=json.dumps(self._data))
        self.tearDown(resp)

    #请求结束时，清理
    def tearDown(self, resp):
        try:
            rc = json.loads(resp.content)
            self.set_last_response(rc)
            self._actual_result = resp.text.decode("unicode_escape")
            self._diff_result = self.compare(self._expect_result, rc, self._validator)
            if self._wait_time:
                time.sleep(int(self._wait_time))
            self.clean_last_quary_condition()
        except:
            self._actual_result = resp.text.decode("unicode_escape")

    def set_last_response(self,body):
        self.last_response(RestResponse(body))

    #缓存值替换
    def slot_substitute(self):
        if self._slot:
            if self._url and 'slot' in self._url:
                self._url.replace("slot", self._slot)
            for query_param in [x for x in [self._header, self._params, self._data] if x and 'slot' in x.values()]:
                slot_key = query_param.keys()[query_param.values().index('slot')]
                query_param[slot_key] = self._slot

    # 替换fitnesse输入的wrapper变量
    def substitute(self):
        self.slot_substitute()
        from variables import Variables
        if self._last_response:
            vs = Variables(self._last_response.body)
            if self._slot:self.slot(vs.substitute(self._slot))
            if self._url: self.url(vs.substitute(self._url))
            if self._header: self.headers(vs.substitute(self._header))
            if self._params:self.params(vs.substitute(self._params))
            if self._data:self.data(vs.substitute(self._data))

    # inspect response content
    def compare(self, ob1, ob2, validator):
        """
        :param ob1:expect result
        :param ob2: acutal result
        :param validator: validator mode
        :return:
        """
        from Compare import CompareMode
        compare = CompareMode.get_compare_mode(validator)
        if validator == "OBJECT":
            ob1 = self.object_in_filter(ob1)
            if self._diff_by:
                result = compare.diff(ob1, ob2, self._diff_by)
            else:
                result = compare.diff(ob1, ob2)
            result.update({result.keys()[0]:filter(self.object_out_filter, result[result.keys()[0]])})
            for k, v in result.items():
                if not v :
                    return 'PASS'
                else:
                    return str(result)
        else:
            result = compare.diff(ob1, ob2)
            return "PASS" if not result else str(result)

    def object_in_filter(self, data):
        def type_handler(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        type_handler(v)
                    if isinstance(v, str) and v.lower() in ("false", "true"):
                        data.update({k:json.loads(v.lower())})
                return data
        return type_handler(data)

    def object_out_filter(self, kv):
        # because fitnesse cell in table is not support null collection(dict,list,set,tuple),so use '%s' for placeholder .
        # so,'%s' should be ignore
        def is_placeholder(kv):
            """
            Takes {k, v} dict, returns True if it's a placeholder.
            """
            for k, v in kv.items():
                return not bool(
                    k == '%s'
                )
		return is_placeholder(kv)


if __name__ == '__main__':
    core = Core()
    core._expect_result = {"status": 0,"%s": 0,"result": {"first_login": 'false',"is_active": 'true',"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170}}
    _url = "http://172.20.0.224:16001/WEBAPI/auth/accessToken/"
    core.url(_url)
    core.data({'user':'xuetianshi.668899@163.com','password':'123456@a'})
    core.validator("OBJECT")
    core.post_by_dict()
    _url2 = "http://172.20.0.224:16001/WEBAPI/webserver/appkey/get"
    core.url(_url2)
    core.headers({'SESSION-TOKEN':'%result@token%'})
    core.get()
    core.headers({'APPKEY':'%result@app_key%'})
    _url3 = "http://172.20.0.224:16001/api/current/client/matches/address"
    core.url(_url3)
    core.params({'address':'105'})
    core.get()
    #response_content = json.loads(r.content)
    #core._diff_by = 'kv'
    #print core.compare(core._expect_result, response_content, core._diff_by)


