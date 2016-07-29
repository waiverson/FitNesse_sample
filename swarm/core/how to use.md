

<br>!define COMMAND_PATTERN {python "%m" %p}
<br>!define TEST_RUNNER {C:/Python27/Lib/site-packages/fit/FitServer.py}
<br>!path C:\SOFTWARE\fitness_framework\swarm\core\




> 场景-01 先获取用户token，接着获取API访问appkey，再搜索企业名录，依据企业名录获取企业详情

!|ActionFixture|<br>|start|Core||
<br>|enter|url|http://172.20.0.226:16001/WEBAPI/auth/accessToken/|
<br>|enter|data|{'user':'liuweiwei5@163.com','password':'liuweiwei'}|
<br>|enter|expect_result|{"type":"object","properties":{"status":{"type":"integer"},"errcode":{"type":"integer"},"result":{"type":"object","properties":{"first_login":{"type":"boolean"},"is_active":{"type":"boolean"},"user_type":{"type":"integer"},"token":{"type":"string"},"orgid":{"type":"integer"},"id":{"type":"integer"}}}}}|
<br>|enter|validator|JSON_SCHEMA|
<br>|press|post_by_dict|
<br>|check|actual_result||
<br>|enter|url|http://172.20.0.226:16001/WEBAPI/webserver/appkey/get|
<br>|enter|headers|{'SESSION-TOKEN':'%result@token%'}|
<br>|enter|expect_result|{'status':0,'result':{"is_open": 1, "app_key": "G94DWJOZ182bg7mM"}}|
<br>|enter|diff_by|struct|
<br>|enter|validator|OBJECT|
<br>|press|get|
<br>|check|actual_result||
<br>|check|diff_result|PASS|
<br>|enter|url|http://172.20.0.226:16001/api/current/client/matches/|
<br>|enter|headers|{'APPKEY':'%result@app_key%'}|
<br>|enter|params|{'name':'105'}|
<br>|enter|expect_result|{"status":0,"result":{"list":[{"id":"str","name":"str"}]}}|
<br>|enter|diff_by|struct|
<br>|enter|validator|OBJECT|
<br>|press|get|
<br>|check|actual_result||
<br>|check|diff_result|PASS|
<br>|enter|url|http://172.20.0.226:16001/api/current/client/detail/|
<br>|enter|params|{'id':'%result@list[0]@industry_id%'}|
<br>|enter|expect_result|{"status":0,"errcode":0,"result":{"base_info":{"entity_name":"str","area":"str","type":"str"}}}|
<br>|enter|validator|OBJECT|
<br>|press|get|
<br>|check|actual_result||
<br>|check|diff_result|PASS|