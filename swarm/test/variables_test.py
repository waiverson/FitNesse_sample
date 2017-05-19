# encoding:utf-8
__author__ = 'xyc'


from swarm.core.variables import *
import unittest

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

replacement = {"status": 0,"result": [{"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_170","orgid": 74,"id": 170},
                                             {"first_login": False,"is_active": True,"user_type": 1,"token": "8LvAb5xK1t_171","orgid": 75,"id": 171}]}


class VariablesTest(unittest.TestCase):

    def test_get_substitued_variable_by_dsl(self):
        variables = {'SESSION-TOKEN':'%result[0]@token%'}
        self.assertEqual({'SESSION-TOKEN':'8LvAb5xK1t_170'}, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_dsl_negtive(self):
        result = {
                  "errcode": 0,
                  "result": {
                    "list": [
                      {
                        "desc": "默认管理员",
                        "id": 0,
                        "name": "管理员"
                      },
                      {
                        "desc": "描述信息",
                        "id": 5098,
                        "name": "1"
                      },
                      {
                        "desc": "描述信息",
                        "id": 5097,
                        "name": "角色名称过长00000"
                      }
                    ]
                  },
                  "status": 0
                }
        variables = {'ids':'%result@list[-1]@id%,%result@list[-2]@id%'}
        self.assertEqual({'ids':'5097,5098'}, Variables(result).substitute(variables))

    def test_get_substitued_variable_by_dsl(self):
        variables = 'SESSION-TOKEN:%result[0]@token%'
        self.assertEqual('SESSION-TOKEN:8LvAb5xK1t_170', Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_dsl_2(self):
        variables = '%result[0]@is_active%'
        self.assertEqual(True, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path(self):
        variables = 'SESSION-TOKEN:%$..result[@.orgid is 75].token[0]%'
        self.assertEqual('SESSION-TOKEN:8LvAb5xK1t_171', Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path_int(self):
        variables = 'SESSION-TOKEN:%$..result[@.orgid is 75].id[0]%'
        self.assertEqual('SESSION-TOKEN:171', Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path(self):
        variables = {'SESSION-TOKEN':'%$..result[@.orgid is 75].token[0]%'}
        self.assertEqual({'SESSION-TOKEN':'8LvAb5xK1t_171'}, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_elements_1(self):
        path = '%$..result[@.orgid is 75].token[0]%'
        variables = {'SESSION-TOKEN':path}
        self.assertEqual({'SESSION-TOKEN':'8LvAb5xK1t_171'}, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_of_boolean(self):
        path = '%$.result[@.orgid is 75].first_login[0]%'
        variables = {'SESSION-TOKEN':path,'test':True}
        self.assertEqual({'SESSION-TOKEN':False,'test':True}, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path_array_element(self):
        path = '%$.result.list[1].name%'
        variables = {'name':path}
        self.assertEqual({'name':'NL SAS 4T'}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_elements_2(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        variables = {'predicted':path}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0]}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_elements_3(self):
        id = '%$.result[@.orgid is 75].id[0]%'
        variables = {'id':id}
        self.assertEqual({'id':171}, Variables(replacement).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_element_4(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        name = '%$.result.total%'
        variables = {'predicted':path, 'name':name}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0], 'name':40}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_element_5(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        id_name = '%$.result.total%'
        variables = {'predicted':path, 'name':{'id_name':id_name}}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0], 'name':{'id_name':40}}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_element_6(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        id_name = '%$.result.total%'
        variables = {'predicted':path, 'name':{'id_name':[id_name,]}}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0], 'name':{'id_name':[40]}}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable_by_object_path_specific_element_7(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        id_name = '%$.result.total%'
        variables = {'predicted':path, 'name':{'id_name':(id_name,)}}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0], 'name':{'id_name':(40,)}}, Variables(test_json).substitute(variables))

    def test_get_substitued_variable(self):
        path = '%$.result.list[@.name is "SATA 1"].predicted[0]%'
        id_name = '%$.result.total%'
        variables = {'predicted':path, 'name':[{'id_name': [id_name,path]},]}
        self.assertEqual({'predicted':[20.0, 20.0, 20.0, 20.0, 20.0, 20.0], 'name':[{'id_name':[40,[20.0, 20.0, 20.0, 20.0, 20.0, 20.0]]},]}, Variables(test_json).substitute(variables))

if __name__ == '__main__':

   unittest.main()
