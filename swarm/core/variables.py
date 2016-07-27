# encoding:utf-8
__author__ = 'xyc'

import re

from swarm.core.json2obejct import recursive_json_loads


# 转换unicode输入为str输出
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class Variables(object):

    VARIABLES_PATTERN = re.compile("\%(.+?)\%")

    def __init__(self, body=None):
        if not body:
            self.replacement = None
        else:
            self.replacement = recursive_json_loads(byteify(body))

    def substitute(self, variable):
        variable = byteify(variable)
        if not variable:
            return None
        if isinstance(variable, str):
            if self.check(variable) and self.replacement:
                match = Variables.VARIABLES_PATTERN.findall(variable)
                text = variable.replace("%", "")
                for m in match:
                    if "@" in m:
                        v = eval("self.replacement.{key}".format(self = self,
                                                           key=m.replace("@",".")))
                        text = text.replace(m, str(v))
                    else:
                        text =text.replace(m, str(self.replacement[m]))
                return text
            return variable
        elif isinstance(variable, dict):
            for k in variable.keys():
                if self.check(variable[k]) and self.replacement:
                    match = Variables.VARIABLES_PATTERN.findall(variable[k])
                    variable.update({k:variable[k].replace("%", "")})
                    for m in match:
                        if "@" in m:
                            v = eval("self.replacement.{key}".format(self = self,
                                                               key=m.replace("@",".")))
                            variable.update({k:variable[k].replace(m, str(v))})
                        else:
                            variable.update({k:variable[k].replace(m,str(self.replacement[m]))})
            return variable
        else:
            return variable

    def check(self, text):
        if isinstance(text, str) and "%" in text:
            return True
        else:
            False


if __name__ == "__main__":

    resource = "http://172.20.0.213:16001/getuserinfo/%tokenID%/%group@user@id[0]%"
    # 带列表的json定位
    bodycontent = {"user":"%status%","group":"%result@list[0]@industry_id%"}
    body = {"status":0,"result":{"list":[{"industry_id":3001,"id":"36854","name":"北京市105中学"}
            ,{"industry_id":3003,"id":"70433","name":"中国人民解放军51052部队医院"}
            ,{"industry_id":3001,"id":"15404","name":"贵阳市105地质队幼儿园"}
            ,{"industry_id":3003,"id":"68352","name":"中国人民解放军第105医院"}
            ,{"industry_id":3003,"id":"65556","name":"中国人民解放军第150医院"}
            ,{"industry_id":3003,"id":"67127","name":"中国人民解放军37015部队医院"}
            ,{"industry_id":3003,"id":"80435","name":"中国人民解放军51034部队桥东医院"}]}}

    va = Variables(body)
    #jobject = recursive_json_loads(va.RestResponse)
    #exec("print jobject.group.user.id")
    print va.substitute(bodycontent)

    #print recursive_json_loads(Variables.RestResponse).group.user.id
