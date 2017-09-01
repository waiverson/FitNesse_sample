# encoding:utf-8
__author__ = 'xyc'

import re

from json2obejct import recursive_json_loads
import objectpath

class Variables(object):

    VARIABLES_PATTERN = re.compile("\%(.+?)\%")

    def __init__(self, resp_body=None):
        if not resp_body:
            self.replacement = None
        else:
            self.replacement = self.byteify(resp_body)

    def byteify(self, input):
        # 转换unicode输入为str输出
        if isinstance(input, dict):
            return {self.byteify(key):self.byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def substitute(self, variable):
        return self.get_substituted_variable(self.byteify(variable))

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
            :return:生成器或具体值，取决于查询表达式
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
            return slot_values
        else:
            return replacement[dsl_path_expr]

    def substitute_for_path(self, variable):
        # 替换variable中的“路径查找表达式”
        if self._is_expr(variable) and self.replacement:
            match_expr = Variables.VARIABLES_PATTERN.findall(variable)
            if len(match_expr) > 1 or not self._is_pure_expr(variable):
                for expr in match_expr:
                    v = self.path_find(expr, self.replacement)
                    variable = variable.replace("%", "")
                    variable = variable.replace(expr, str(v))
                return variable
            else:
                return self.path_find(match_expr[0], self.replacement)
        return variable

    def get_substituted_variable(self, variable):
        if isinstance(variable, dict) and variable:
            for k in variable.keys():
                substituted_v = self.get_substituted_variable(variable[k])
                variable.update({k:substituted_v})
            return variable
        elif isinstance(variable, list) and variable:
            return [self.get_substituted_variable(v) for v in variable]
        elif isinstance(variable, tuple) and variable:
            return tuple([self.get_substituted_variable(v) for v in variable])
        elif isinstance(variable, str):
                return self.substitute_for_path(variable)
        else:
            return variable

    def _is_expr(self, text):
        if isinstance(text, str) and "%" in text:
            return True
        else:
            False

    def _is_pure_expr(self, expr):
        return expr.startswith('%') and expr.endswith('%')