# encoding:utf-8
__author__ = 'xyc'

import unittest, os, sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../core' % PATH)
from swarm.core.Compare import *


test_json = {"result": {"group": "","list": [{
        "axis_err": [400,800,1200,1600,2000],
        "axis_value": [10,20,30],
        "err": [2000.0,2000.0,2000.0,2000.0,2000.0,""],
        "name": "SATA 1",
        "predicted": [20.0,20.0,20.0,20.0,20.0,20.0],
        "real": [10.0,0.0,0.0,0.0,0.0,""]
      },
      {
        "axis_err": [3000,6000,9000,12000,15000,18000],
        "axis_value": [40,80,120,160],
        "err": [15900.0,15900.0,15900.0,15900.0,15900.0,""],
        "name": "NL SAS 4T",
        "predicted": [159.0,159.0,159.0,159.0,159.0,159.0],
        "real": [0.0,0.0,0.0,0.0,0.0,""]
      }
    ],
    "open_sku": 0,
    "title": [
      "2016",
    ],
    "total": 40
  },
  "status": 0
}

replacement2 = {"statuss": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}

replacement = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}


class CompareTest(unittest.TestCase):

    def test_assertCompareMode_of_equals(self):
        validator = AssertCompareMode()
        rs = validator.diff(replacement, replacement2)
        print rs
        self.assertEqual('', rs)
