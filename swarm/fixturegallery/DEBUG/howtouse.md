!define COMMAND_PATTERN {python "%m" %p}
!define TEST_RUNNER {C:/Python27/Lib/site-packages/fit/FitServer.py}
!path C:\SOFTWARE\fitness_framework\swarm\core\


#场景-01 先获取用户token，接着获取API访问appkey，再搜索企业名录，依据企业名录获取企业详情
!|ActionFixture| 
|start|Core||
|enter|url|http://172.20.0.226:16001/WEBAPI/auth/accessToken/|
|enter|data|{'user':'liuweiwei5@163.com','password':'liuweiwei'}|
|enter|expect_result|{"status": 0, "errcode": 0, "result": {"first_login": False, "is_active": True, "user_type": 1, "token": "iT17rAqgLm_170", "orgid": 74, "id": 170}}|
|press|post_by_dict|
|check|actual_result||
|enter|url|http://172.20.0.226:16001/WEBAPI/webserver/appkey/get|
|enter|headers|{'SESSION-TOKEN':'%result@token%'}|
|enter|expect_result|{'status':0,'result':{"is_open": 1, "app_key": "G94DWJOZ182bg7mM"}}|
|enter|diff_by      |struct|
|press|get|
|check|actual_result||
|check|diff_result  |PASS|
|enter|url|http://172.20.0.226:16001/api/current/client/matches/|
|enter|headers|{'APPKEY':'%result@app_key%'}|
|enter|params|{'name':'105'}|
|enter|expect_result|{"status":0,"result":{"list":[{"id":"str","name":"str"}]}}|
|enter|diff_by|struct|
|press|get|
|check|actual_result||
|check|diff_result|PASS|
|enter|url|http://172.20.0.226:16001/api/current/client/detail/|
|enter|params|{'id':'%result@list[0]@industry_id%'}|
|enter|expect_result|{"status":0,"errcode":0,"result":{"base_info":{"entity_name":"str","area":"str","type":"str"}}}|
|press|get|
|check|actual_result||
|check|diff_result|PASS|
