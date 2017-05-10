# encoding:utf-8
__author__ = 'xyc'

import unittest, os, sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../core' % PATH)
from swarm.core.Compare import *


class CompareTest(unittest.TestCase):

    replacement2 = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

    replacement = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

    def test_assertCompareMode_of_dict_equals(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff(self.replacement, self.replacement2))

    def test_assertCompareMode_of_list_equals(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff([1,2,3], [1,2,3]))

    def test_assertCompareMode_of_set_equals(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff((1,2,3), (1,2,3)))

    def test_assertCompareMode_of_In(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff(0, [1,2,3,0], 'In'))

    def test_assertCompareMode_of_ItemsEqual(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff([1,2,3,0], [1,0,3,2], 'ItemsEqual'))

    def test_assertCompareMode_of_DictContainsSubset(self):
        validator = AssertCompareMode()
        self.assertEqual(None, validator.diff({"status":0}, self.replacement2, 'DICTCONTAINSSUBSET'))