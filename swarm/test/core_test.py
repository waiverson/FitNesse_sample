# encoding:utf-8
__author__ = 'xyc'

import unittest, os, sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../core' % PATH)
from swarm.core.Core import *

class CoreTest(unittest.TestCase):

    expect = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

    def test_get_slot_substituted_variable(self):
        actual = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "%slot%","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.slot('8LvAb5xK1t_170')
        core.headers(actual)
        self.assertEqual(self.expect, core._header)

    def test_get_slot_substituted_variable_of_boolean(self):
        actual = {"status": 0,"result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.slot(False)
        core.headers(actual)
        self.assertEqual(self.expect, core._header)

    def test_variable_substitute(self):
        core = Core()
        core.last_response(RestResponse(self.expect))
        id_name = '%$..result[@.orgid is 75].token[0]%'
        variables = {'name':{'id_name':(id_name,)}}
        self.assertEqual({'name':{'id_name':('8LvAb5xK1t_171',)}}, core.realistic(variables))

    def test_substitute_of_headers(self):
        actual = {"status": 0,"result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.slot(False)
        core.headers(actual)
        core.last_response(RestResponse(self.expect))
        self.assertEqual(self.expect, core._header)

    def test_substitute_of_data(self):
        actual = {"status": 0, "result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.last_response(RestResponse(self.expect))
        id_name = '%$..result[@.orgid is 75].token[0]%'
        core.data({'name':{'id_name':(id_name,)}})
        self.assertEqual({'name':{'id_name':('8LvAb5xK1t_171',)}}, core._data)

    def test_substitute_of_header_params_data(self):
        actual = {"status": 0,"result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.slot(False)
        core.headers(actual)
        core.params(actual)
        core.last_response(RestResponse(self.expect))
        id_name = '%$..result[@.orgid is 75].token[0]%'
        core.data({'name':{'id_name':(id_name,)}})
        self.assertEqual(self.expect, core._header)
        self.assertEqual(self.expect, core._params)
        self.assertEqual({'name':{'id_name':('8LvAb5xK1t_171',)}}, core._data)

    def test_slot(self):
        actual = {"status": 0,"result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.last_response(RestResponse(actual))
        core.slot('%$..result[@.orgid is 75].token[0]%')
        self.assertEqual('8LvAb5xK1t_171', Core.g_slot)

    def test_compare_of_assert_mode(self):
        #to do
        pass

    def test_do_method(self):
        uri = "http://172.20.0.223/lae/auth/login"
        data = {'user':'2215649033@qq.com','password':'123456@a'}
        method = "POST"
        resp = Core().do_method(method=method, url=uri, data=data)
        self.assertIn("token", resp.content)

    def test_do_verify_by_equal(self):
        expert = 90
        data = {
                  "errcode": 0,
                  "result": {
                    "push_condition": {"att_value": "2", "col_name": "industry", "att_type": "int", "col_desc": "\u884c\u4e1a-KOM", "att_name": "new_num", "att_desc": "\u6700\u5c0f\u65b0\u589e\u9879\u76ee\u6570(\u4e2a)"},
                    "push_days": 90,
                    "status": 1
                  },
                  "status": 0
                }
        ce = Core()
        ce._diff_by = "Equal"
        resp = ce.verify(expert, data["result"]["push_days"], "Assert")
        self.assertEqual("PASS", resp)

    def test_do_verify_by_dict_contains(self):
        expert = {"_s_path":"%result%","_s_value":{"push_days":90}}
        data = {
                  "errcode": 0,
                  "result": {
                    "push_condition": {"att_value": "2", "col_name": "industry", "att_type": "int", "col_desc": "\u884c\u4e1a-KOM", "att_name": "new_num", "att_desc": "\u6700\u5c0f\u65b0\u589e\u9879\u76ee\u6570(\u4e2a)"},
                    "push_days": 90,
                    "status": 1
                  },
                  "status": 0
                }
        ce = Core()
        ce._diff_by = "DICTCONTAINSSUBSET"
        resp = ce.verify(expert, data, "Assert")
        self.assertEqual("PASS", resp)

    def test_do_verify_by_dict_contains_2(self):
        expert = {"_s_path":"%$.result.*%","_s_value":{"push_days":90,"status": 1}}
        data = {
                  "errcode": 0,
                  "result": {
                    "push_condition": {"att_value": "2", "col_name": "industry", "att_type": "int", "col_desc": "\u884c\u4e1a-KOM", "att_name": "new_num", "att_desc": "\u6700\u5c0f\u65b0\u589e\u9879\u76ee\u6570(\u4e2a)"},
                    "push_days": 90,
                    "status": 1
                  },
                  "status": 0
                }
        ce = Core()
        ce._diff_by = "DICTCONTAINSSUBSET"
        resp = ce.verify(expert, data, "Assert")
        self.assertEqual("PASS", resp)