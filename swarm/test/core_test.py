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
        core.get_slot_substituted_variable(core._header)
        self.assertEqual(self.expect, core._header)

    def test_get_slot_substituted_variable_of_boolean(self):
        actual = {"status": 0,"result": [{"first_login": "%slot%","is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}
        core = Core()
        core.slot(False)
        core.headers(actual)
        core.get_slot_substituted_variable(core._header)
        self.assertEqual(self.expect, core._header)

    def test_variable_substitute(self):
        core = Core()
        core.last_response(RestResponse(self.expect))
        id_name = '%$..result[@.orgid is 75].token[0]%'
        variables = {'name':{'id_name':(id_name,)}}
        self.assertEqual({'name':{'id_name':('8LvAb5xK1t_171',)}}, core.variable_substitute(variables))

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

    def test_get(self):
        #to do
        pass