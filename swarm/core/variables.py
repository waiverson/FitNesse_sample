# encoding:utf-8
__author__ = 'xyc'

import re, json
from collections import Iterable

from json2obejct import recursive_json_loads
import objectpath

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

    def __init__(self, resp_body=None):
        if not resp_body:
            self.replacement = None
        else:
            self.replacement = byteify(resp_body)

    def substitute(self, variable):
        variable = byteify(variable)
        if not variable:
            return None
        if isinstance(variable, str):
            return self.substitute_for_str(variable)
        elif isinstance(variable, dict):
            return self.substitute_for_dict(variable)
        else:
            return variable

    def path_find(self, expr, replacement):
        if '$' in expr:
            return self.object_path_finder(expr, replacement)
        else:
            return self.dsl_path_finder(expr, replacement)

    def object_path_finder(self, object_path_expr, replacement):
        """
            基于objectpath查找
            :param object_path_expr: %$.result.list[@.name is "SATA 1"].predicted[0]% ,'%$.result.total%'
            :param replacement: dict,string,json,tuple
            :return:elements生成器, element
        """
        tree = objectpath.Tree(replacement)
        g = tree.execute(object_path_expr)
        return g

    def dsl_path_finder(self,dsl_path_expr, replacement):
        """
            基于dsl查找
            :param object_path_expr: %result@industry_id% , %result@list[n]@industry_id%
            :param replacement: dict,string,json,tuple
            :return:elements生成器, element
        """
        replacement = recursive_json_loads(replacement)
        if "@" in dsl_path_expr:
            slot_values = eval("replacement.{key}".format(self = self,
                                                   key=dsl_path_expr.replace("@",".")))
            return str(slot_values)
        else:
            return str(replacement[dsl_path_expr])

    def substitute_for_str(self, variable):
        # 替换字符串类型的variable中的“路径查找表达式”
        if self.check(variable) and self.replacement:
            match_expr = Variables.VARIABLES_PATTERN.findall(variable)
            actual_text = variable.replace("%", "")
            for expr in match_expr:
                v = self.path_find(expr, self.replacement)
                actual_text = actual_text.replace(expr, str(v))
            return actual_text
        return variable

    def substitute_for_dict(self, variable):
        # 替换字典类型的variable中的“路径查找表达式”
        for k in variable.keys():
            if self.check(variable[k]) and self.replacement:
                match_expr = Variables.VARIABLES_PATTERN.findall(variable[k])
                variable.update({k:variable[k].replace("%", "")})
                for expr in match_expr:
                    v = self.path_find(expr, self.replacement)
                    #variable.update({k:variable[k].replace(expr, v)})
                    variable.update({k:v})
        return variable

    def check(self, text):
        if isinstance(text, str) and "%" in text:
            return True
        else:
            False
