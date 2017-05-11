# encoding:utf-8
__author__ = 'xyc'

import unittest, os, sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../core' % PATH)
from swarm.core.Core import *

class CompareTest(unittest.TestCase):

    expect = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

    actual = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "%slot%","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

    def test_slot_substitute(self):
        core = Core()
        core.slot('8LvAb5xK1t_170')
        core.headers(self.actual)
        core.slot_substitute(core._header)
        self.assertEqual(self.expect, core._header)
