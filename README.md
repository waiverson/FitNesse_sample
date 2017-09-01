# Swarm测试框架介绍
## 1、功能简要介绍
    swarm测试框架设计为结合fitnesse测试平台使用，适用于fitnesse平台下的ActionTest fixture。提供基于http+json接口层面的接口测试，支持GET | POST | PUT | DELETE等接口调用。用例形式上支持单接口测试，多接口组合测试，多种返回值校验方式等功能。
## 2、	用例管理与执行
    基于fitnesse平台的Action Fixture进行用例的设计和撰写，语法：wiki，具体fitnesse使用，详见：http://www.fitnesse.org/FitNesse.UserGuide
### 2.1 用例的编写 
    框架关键字：
    url				    请求地址
    params			    请求参数
    headers		        请求头
    data			    请求body
    validator		    校验器
    diff_by			    校验方式
    expect_result	    期望结果，assert校验时，因为会部分匹配，所以格式 
                          {“_s_path”:“定位表达式”,“_s_value”:“期望值”}
    slot			    中继值，支持对某个值进行缓存，供后续用例传递
    wait_time		    等待时长
    actual_result	    实际结果
    get				    HTTP GET方法
    post			    HTTP POST方法，body类型为json
    post_by_dict	    HTTP POST方法，body类型为表单
    put				    HTTP PUT方法
    delete			    HTTP DELETE方法

## 3、	校验器
    校验器在fitnesse中的运用WIKI语法：
    | enter | validator | JSON_SCHEMA or OBJECT or ASSERT |
    一般建议使用：JSON_SCHEMA校验器
    当校验器是指为OBJECT 或 ASSERT时需要给出校验方式：
    如为ASSERT时， | enter | diff_by | Equal or In or ItemsEqual or RegexpMatches or DictContainsSubset |
    如为OBEJCT时，| enter | diff_by | struct or kv|
### 3.1 JSON_SCHEMA
    JSON_SCHEMA校验支持draft3，draft4规范
    具体如何编写json schema：https://spacetelescope.github.io/understanding-json-schema/
### 3.2 ASSERT
    assert校验器支持的校验方式有：
    assertEqual，             fitnesse关键字表示为：Equal
    assertIn,                 fitnesse关键字表示为：In
    assertItemsEqual,         fitnesse关键字表示为：ItemsEqual
    assertRegexpMatches，     fitnesse关键字表示为：RegexpMatches
    assertDictContainsSubset，fitnesse关键字表示为：DictContainsSubset
### 3.3 OBJECT
    OBJECT校验方式支持：
    	Struct：只对返回json的key和value的类型进行校验.
     	Kv：对返回json的key和value的值进行校验.

## 4、	定位器
    对返回值中的某个值进行定位抽取，以并其作为下一个接口的所需参数传递。定位器表达式可以嵌套到params，slot，data，headers，url等关键字中。表达式的查找对象总是上次接口调研的返回值。
    如：| enter | params | {“id”: ”% $.result[@.orgid is 75].id[0]% ”} |  
设计有两种：
### 4.1、路径使用“.” 定位符
    定位器表达式：$.attributeName1 [ selector ].attributeName2
    其中$是根元素，选择从节点的所有直接子元素，attributeName1指定到具体子元素，[selector]限制子元素中的结果，attributeName2从前面计算过的结果中选择子元素。
#### 4.1.1、完整语法
    操作符						    描述
    $					          根对象
    @							  当前的对象/元素
    .							  子对象/元素操作符
    ..							  递归下降
    *                             通配符。匹配所有的对象/元素
    [ ]							  选择器（selector）操作符
#### 4.1.2、选择器（selector）
    selector选择满足其表达式的数组元素。支持嵌套路径，使用比较运算符或者参考数据集的其他部分。
    选择器表达式被写入 [ ] 操作符中。
    例1、	表达式为数字，表示从数组中获取第n个元素
    >>>	 $.*[ 1 ]  #数组中的第2个元素
    例2、	表达式为字符串，行为类似于 . 操作符
    >>>	 $..*[‘string’] is  $..string  true
    例3、	查找一个元素
    >>>	 $..*[@.attribute is ‘ok’]  #查找数组中属性名是ok的元素
    例4、	支持boolean多条件查找
    >>>	$..*[@.attribute is ‘ok’ or  len(@.*[1]) is 2]  #查找属性名为ok或者数组中第2个元素是2的元素。
    例5、	在天气预报结果中，查找满足温度大于25摄氏度和无云的城市
    >>>	$..*[@..temp > 25 and @.clouds.all is 0].name
    @表达式匹配当前元素，selector表达式遍历左表达式的结果（结果一般是数组），@将匹配当前检查的元素或表达式
    例6
    object1 = {“status”:0, “result”:[
    {“first_login”:Flase，“is_active”:True, “user_type”:1,“orgid”:74, “id”:170},
    {“first_login”:Flase，“is_active”:True, “user_type”:1,“orgid”:75, “id”:171}
    ]}
    >>>	$.result[@.orgid is 75].id[0]
    >>>	171
#### 4.1.3 在fitnesse中的运用：
    对定位表达式需要在前面附加 “ % ”
    如：| enter | params | {“id”: ”% $.result[@.orgid is 75].id[0]% ”}|   
### 4.2路径使用 “@”定位符
    表达式：result[0]@is_active，获取result数组中第一个元素的is_active属性的值
    object1 = {“status”:0, “result”:[
    {“first_login”:Flase，“is_active”:Flase, “user_type”:1,“orgid”:74, “id”:170},
    {“first_login”:Flase，“is_active”:True, “user_type”:1,“orgid”:75, “id”:171}
    ]}
    >>>	result[0]@is_active
    >>>	Flase

## 5、	中继器
    关键字：slot ，缓存特定值（图表ID）用于多接口中的传递，避免反复获取，目前不支持集合类型的赋值。
    fitnesse赋值： | enter | slot | % $.result[@.orgid is 75].id[0]% |
    fitnesse传递： | enter |  params  | {“id”： “%slot%”} |

## 6、	fitnesse用例sample
    slot，json_schema的例子
    !include .SWARM.host
    !include .SWARM.pythonenv_new
    
    !style_caps{!style_fit_label[SetUp-创建dashboard测试资源]}
    !|ActionFixture|
    |start|Core|
    |enter|url|${host1}/login|
    |enter|data|{${admin_user}}|
    |press|post_by_dict|
    |enter|url|${host1}/dashboard|
    |enter|headers|{'SESSION-TOKEN':'%result@token%'}|
    |enter|params|{'name':'automation_shared_dashboard','app_id':3,'type':1}|
    |enter|data|${json_schema}|
    |enter|validator|JSON_SCHEMA|
    |press|post|
    |check|actual_result||
    |enter|url|${host1}/dashboard/|
    |enter|validator|JSON_SCHEMA|
    |press|get|
    |check|actual_result||
    |enter|slot|%$.result.list[@.name is 'automation_shared_dashboard'].id[0]%|

-------

    !style_ignore(!style_collapse_rim[分享])
    !|ActionFixture|
    |start|Core|
    |enter|url|${host1}/share|
    |enter|expect_result|${json_schema}|
    |enter|validator|JSON_SCHEMA|
    |enter|data|{"id":'%slot%',"uids":'1'}|
    |press|post_by_dict|
    |check|actual_result||
    |check|diff_result|PASS|

-------

    !style_caps{!style_fit_grey[TearDown-删除测试数据]}
    !|ActionFixture|
    |start|Core|
    |enter|url|${host1}/dashboard|
    |enter|data|{'ids':'%slot%'}|
    |enter|expect_result|${json_schema}|
    |enter|validator|JSON_SCHEMA|
    |press|post_by_dict|
    |check|actual_result||
    |check|diff_result|PASS|

-------

       assert断言
       !include .SWARM.host
       !include .SWARM.pythonenv_new
       
       !style_ignore(!style_collapse_rim[登录-获取Token])
       !|ActionFixture|
       |start|Core|
       |enter|url|${host1}/auth|
       |enter|data|{${admin}}|
       |press|post_by_dict|
       |enter|headers|{'SESSION-TOKEN':'%result@token%'}|
       
       !style_ignore(!style_collapse_rim[获取图表信息])
       !|ActionFixture|
       |start|Core|
       |enter|url|${host1}/hotspot|
       |enter|params|{"app_id":3}|
       |enter|validator|JSON_SCHEMA|
       |enter|expect_result|${json_schema}|
       |press|get|
       |check|actual_result||
       |check|diff_result|PASS|
       
       !style_ignore(!style_collapse_rim[获取热点配置])
       !|ActionFixture|
       |start|Core|
       |enter|url|${host1}/hotspot|
       |enter|validator|ASSERT|
       |enter|diff_by|DictContainsSubset|
       |enter|expect_result|{"_s_path":"%$.result.*%","_s_value":{"push_days":90}}|
       |press|get|
       |check|actual_result||
       |check|diff_result|PASS|









