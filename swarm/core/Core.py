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
        self._params = {}
        self._data = {}
        self._expect_result = None
        self._diff_by = ""
        self._diff_result = ""
        self._actual_result = ""
        self._last_response = ""
        self._validator = ""
        self._wait_time = ""
        self._slot = None
        self._set_request_field_func = {'url': self._url,
                                        'headers': self._header,
                                        'params': self._params,
                                        'data': self._data}

    _typeDict["url"] = "String"
    def url(self, s):
        self._url = s

    _typeDict["headers"] = "Dict"
    def headers(self, s):
        self._header.update(dict(s))

    _typeDict["params"] = "Dict"
    def params(self, s):
        self._params.update(dict(s))

    _typeDict["data"] = "Dict"
    def data(self, s):
        self._data.update(dict(s))

    _typeDict["expect_result"] = "Dict"
    def expect_result(self, s):
        self._expect_result = dict(s)

    _typeDict["diff_by"] = "String"
    def diff_by(self, s):
    # 提供校验方式："kv"：key&value值校验，"struct":比较key&value类型校验
        self._diff_by = s

    _typeDict["diff_result"] = "String"
    def diff_result(self):
        return self._diff_result

    _typeDict["actual_result"] = "String"
    def actual_result(self):
    #将比较完的结果返回到fitnesse
        return self._actual_result

    _typeDict["last_response"] = "Default"
    def last_response(self, s):
    # 提供将调用完的结果返回到fitnesse（必要时）
        self._last_response = s

    _typeDict["validator"] = "String"
    def validator(self, s):
    # 设置校验器类型：OBJECT | JSON_SCHEMA | ASSERT
        self._validator = s

    _typeDict["wait_time"] = "String"
    def wait_time(self, s):
    # 设置等待时长，单位：秒
        self._wait_time = s

    _typeDict["slot"] = "String"
    def slot(self, s):
    # 将某值缓存起来，以便后续接口直接使用
        self._slot = s

    _typeDict["debug"] = "String"
    def debug(self):
    #通过|check|debug||,将self._url（其他self字段）返回到fitnesse下，用于调试。
        return str(self._url)

    def clean_last_quary_condition(self):
        self._params.clear()
        self._data.clear()
        self._wait_time = None

    def clean_diff_result(self):
        self._diff_result = ""

    def clean_actual_result(self):
        self._actual_result = ""

    def clean_last_result(self):
        self.clean_diff_result()
        self.clean_actual_result()

    def setup(self):
        self.clean_last_result()
        self.substitute()

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

    _typeDict["get"] = "Default"
    def get(self):
        self.setup()
        resp = requests.get(self._url, params=self._params, headers=self._header)
        self.tearDown(resp)

    _typeDict["post_by_dict"] = "Default"
    def post_by_dict(self):
    #默认body为dict格式
        self.setup()
        resp = requests.post(self._url, params=self._params, headers=self._header, data=self._data)
        self.tearDown(resp)

    _typeDict["post"] = "Default"
    def post(self):
    #默认body为json格式
        self.setup()
        resp = requests.post(self._url, params=self._params, headers=self._header, data=json.dumps(self._data))
        self.tearDown(resp)

    def set_last_response(self,body):
        self.last_response(RestResponse(body))

    def slot_substitute_stub(self):
    #缓存值替换
        if self._slot:
            if self._url and '%slot%' in self._url:
                self._url.replace("%slot%", self._slot)
            for query_param in [x for x in [self._header, self._params, self._data] if x and '%slot%' in x.values()]:
                slot_key = query_param.keys()[query_param.values().index('%slot%')]
                query_param[slot_key] = self._slot

    def get_slot_substituted_variable(self, variable):

        def get_slot(var):
            if self._slot is None:
                return var
            if var == '%slot%':
                return self._slot
            elif '%slot%' in var:
                return var.replace("%slot%", str(self._slot))
            else:
                return var

        if isinstance(variable, dict) and variable:
            for k in variable.keys():
                substituted_v = self.get_slot_substituted_variable(variable[k])
                variable.update({k: substituted_v})
            return variable
        elif isinstance(variable, list) and variable:
            return [self.get_slot_substituted_variable(v) for v in variable]
        elif isinstance(variable, tuple) and variable:
            return tuple([self.get_slot_substituted_variable(v) for v in variable])
        else:
            return get_slot(variable) if isinstance(variable, str) else variable

    def substitute(self):
    # 替换url,header,params,data中包含的wrapper变量
        for key, var in self._set_request_field_func.iteritems():
            if var:
                substituted_var = self.variable_substitute(self.get_slot_substituted_variable(var))
                getattr(self, key)(substituted_var)

    def variable_substitute(self, variable):
        from variables import Variables
        if self._last_response:
            vs = Variables(self._last_response.body)
            return vs.substitute(variable)

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




