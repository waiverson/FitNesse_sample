!define COMMAND_PATTERN {python "%m" %p}
!define TEST_RUNNER {C:/Python27/Lib/site-packages/fit/FitServer.py}
!path C:\SOFTWARE\fitness_framework\swarm\core\

!| ActionFixture |
| start | Core | |
| enter | url | http://172.20.0.226:16001/WEBAPI/auth/accessToken/ |
| enter | data | {'user':'liuweiwei5@163.com','password':'liuweiwei'} |
| press | post_by_dict |
| check | actual_result | |
| enter | url | http://172.20.0.226:16001/WEBAPI/webserver/appkey/get |
| enter | headers | {'SESSION-TOKEN':'%result@token%'} |
| enter | expect_result | {'status':0,'result':{"is_open": 1, "app_key": "G94DWJOZ182bg7mM"}} |
| enter | diff_by | struct |
| press | get |
| check | actual_result | |
| check | diff_result | PASS |
