__author__ = 'Administrator'


import requests,json

url = 'http://172.20.0.213:16005/WEBAPI/userserver/otherapi/checkuser'
data = {'user':'2215649033@qq.com','password':'123456@a','domain':'987654321','orgid':5}
cookie = None

url2 = 'http://172.20.0.213:16005/WEBAPI/userserver/users'

def post():
    global cookie
    r = requests.post(url, data=data)
    status = r.status_code
    cookie = r.cookies
    print cookie
    print requests.utils.dict_from_cookiejar(cookie)

def get():
    print cookie
    r = requests.get(url2,cookies = requests.utils.dict_from_cookiejar(cookie))
    print r.request.headers
    b = json.loads(r.text)
    print b["status"]
post()
get()