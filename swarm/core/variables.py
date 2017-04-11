# encoding:utf-8
__author__ = 'xyc'

import re

from json2obejct import recursive_json_loads


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

# variable中某变量的dsl表达式为：%result@industry_id% 或者 %result@list[0]@industry_id%
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

if __name__ == '__main__':

    Variables().substitute({"text":[1,2,3]})