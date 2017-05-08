# encoding:utf-8
__author__ = 'xyc'


from swarm.core.variables import *
import unittest

replacement = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 170}]}
variables = {'SESSION-TOKEN':'%result@list[0]@token%'}

class VariablesTest(unittest.TestCase):

    def test_substitute_for_str(self):
        variables = {'SESSION-TOKEN':'%result[0]@token%'}
        self.assertEqual(Variables(replacement).substitute(variables),{'SESSION-TOKEN':'8LvAb5xK1t_170'})


if __name__ == '__main__':
    print Variables(replacement).substitute(variables)
    #unittest.main()
#testcase = unittest.TestLoader().loadTestsFromTestCase(Variables)
