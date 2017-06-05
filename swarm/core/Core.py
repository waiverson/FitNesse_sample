# encoding:utf-8
__author__ = 'xyc'


from fit.Fixture import Fixture
import requests, json, sys, time,traceback
from restdata import RestResponse
from conversion import Conversion
from default_http_request import DefaultHttpRequest
from Compare import CompareMode

reload(sys)
sys.setdefaultencoding("utf-8")


class Core(Fixture):

    _typeDict = {}

    # 用于fitnesse case间传递
    g_session = requests.session()
    g_header = {}
    g_slot = None
    g_last_resp = ""
    connect_timeout = None
    read_time = None
    g_timeout = (connect_timeout, read_time)

    def __init__(self):
        Fixture.__init__(self)
        self._url = ""
        self._header = {}
        self._params = {}
        self._data = {}
        self._expect_result = None
        self._diff_by = ""
        self._diff_result = ""
        self._actual_result_for_dis = ""
        self._validator = ""
        self._wait_time = ""

    _typeDict["url"] = "String"
    def url(self, s):
        if s:
            self._url = Core.realistic(str(s))

    _typeDict["headers"] = "Dict"
    def headers(self, s):
        if s:
            real_v = Core.realistic(dict(s))
            self._header.update(real_v)
            Core.g_session.headers.update(real_v)
            Core.g_header.update(real_v)

    _typeDict["params"] = "Dict"
    def params(self, s):
        if s:
            self._params.update(Core.realistic(dict(s)))

    _typeDict["data"] = "Dict"
    def data(self, s):
        if s:
            self._data.update(Core.realistic(dict(s)))

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
    #将http response的结果返回到fitnesse显示
        return self._actual_result_for_dis

    _typeDict["last_response"] = "Default"
    def last_response(self, s):
    # 提供将调用完的结果返回到fitnesse（必要时）
        Core.g_last_resp = s

    _typeDict["validator"] = "String"
    def validator(self, s="JSON_SCHEMA"):
    # 设置校验器类型：OBJECT | JSON_SCHEMA | ASSERT
        self._validator = s

    _typeDict["wait_time"] = "String"
    def wait_time(self, s):
    # 设置等待时长，单位：秒
        self._wait_time = s

    _typeDict["slot"] = "String"
    def slot(self, s):
    # 将某值缓存起来，以便后续接口直接使用
        Core.g_slot = Core.realistic(s)

    _typeDict["debug"] = "String"
    def debug(self):
    #通过|check|debug||,将self._url（其他self字段）返回到fitnesse下，用于调试。
        return "url:{url}\nheader:{header}\nparameter:{params}\nbody:{data}\nslot:{slot}".format(url=self._url,
                                                               header=str(self._header or Core.g_header),
                                                               params = str(self._params),
                                                               data = str(self._data),
                                                               slot = str(Core.g_slot))

    def set_last_response(self, resp_content):
        self.last_response(RestResponse(resp_content))

    def clean_last_quary_condition(self):
        self._params.clear()
        self._data.clear()
        self._wait_time = None

    def clean_diff_result(self):
        self._diff_result = ""

    def clean_actual_result(self):
        self._actual_result_for_dis = ""

    def clean_last_result(self):
        self.clean_diff_result()
        self.clean_actual_result()

    def setup(self):
        self.clean_last_result()

    def teardown(self):
        self.clean_last_quary_condition()

    _typeDict["get"] = "Default"
    def get(self):
        resp = self.do_method(session=Core.g_session, method="GET", url=self._url,
                                      params=self._params, timeout=Core.g_timeout)
        self.exercise(self._expect_result, resp, self._validator)

    _typeDict["post_by_dict"] = "Default"
    def post_by_dict(self):
        #传递表单形式的数据
        resp = self.do_method(session=Core.g_session, method="POST", url=self._url,
                                      params=self._params, data=self._data, timeout=Core.g_timeout)
        self.exercise(self._expect_result, resp, self._validator)

    _typeDict["post"] = "Default"
    def post(self):
        #传递json形式的数据
        data = json.dumps(self._data)
        resp = self.do_method(session=Core.g_session, method="POST", url=self._url,
                                      params=self._params, data=data, timeout=Core.g_timeout)
        self.exercise(self._expect_result, resp, self._validator)

    _typeDict["put"] = "Default"
    def put(self):
        resp = self.do_method(session=Core.g_session, method="PUT", url=self._url,
                                      params=self._params, timeout=Core.g_timeout)
        self.exercise(self._expect_result, resp, self._validator)

    _typeDict["delete"] = "Default"
    def delete(self):
        resp = self.do_method(session=Core.g_session, method="DELETE", url=self._url,
                                      params=self._params, timeout=Core.g_timeout)
        self.exercise(self._expect_result, resp, self._validator)

    def exercise(self, expect, resp, verify_mode):
        self.setup()
        try:
            response_v = resp.json()
            self.set_last_response(response_v)
            self._actual_result_for_dis = resp.text.decode("unicode_escape")
            rs = self.verify(expect, response_v, verify_mode)
            self._diff_result = rs
            if self._wait_time:
                time.sleep(int(self._wait_time))
        except ValueError:
            self._actual_result_for_dis = "返回信息：\t{}\n异常信息：\n{}".format(resp.text, traceback.format_exc())
        finally:
            resp.close()
            self.teardown()

    def verify(self, expect, actual, mode):
        if mode.upper() == "OBJECT":
            expect = self.bool_convert(expect)
        rs = self.compare(expect, actual, mode, by=self._diff_by)
        if isinstance(rs, dict):
            rs.update({rs.keys()[0]: filter(self.null_convert, rs[rs.keys()[0]])})
            if not rs.values()[0]:
                return "PASS"
        return "PASS" if not rs else str(rs)

    def do_method(self, session=None, method="GET", url=None, headers={},
                          params=None, data=None, timeout=None):
        http_request = DefaultHttpRequest().with_uri(url) \
                                           .with_method(method) \
                                           .with_headers(headers) \
                                           .with_params(params) \
                                           .with_data(data) \
                                           .with_session(session=session) \
                                           .with_timeout(timeout=timeout) \
                                           .new_request()

        resp = http_request.send()
        return resp

    @classmethod
    def realistic(cls, variable):
        return Conversion.with_expr(Conversion.with_slot(variable, body=cls.g_slot),
                                    body=cls.g_last_resp.body if cls.g_last_resp else None)

    def compare(self, actual, expect, mode, by):
        validator = CompareMode.get_compare_mode(mode)
        if not actual or not expect:
            return None
        return validator.diff(actual, expect, by)

    def bool_convert(self, data):
        #fitnesse不支持bool值,用str代替
        def type_handler(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        type_handler(v)
                    if isinstance(v, str) and v.lower() in ("false", "true"):
                        data.update({k:json.loads(v.lower())})
                return data
        return type_handler(data)

    def null_convert(self, data):
        # because fitnesse cell in table is not support null collection(dict,list,set,tuple),so use '%s' for placeholder .
        # so,'%s' should be ignore
        def is_placeholder(data):
            """
            Takes {k, v} dict, returns True if it's a placeholder.
            """
            for k, v in data.items():
                return not bool(
                    k == '%s'
                )
		return is_placeholder(kv)




