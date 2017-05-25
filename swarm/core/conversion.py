# encoding:utf-8
__author__ = 'xyc'

from variables import Variables
class Conversion(object):

    @classmethod
    def with_slot(cls, variable, body=None):
    # 转换变量variable中的 %slot% 占位符
        def get_slot(var):
            if body is None:
                return var
            if var == '%slot%':
                return body
            elif '%slot%' in var:
                return var.replace("%slot%", str(body))
            else:
                return var

        if isinstance(variable, dict) and variable:
            for k in variable.keys():
                substituted_v = cls.with_slot(variable[k], body)
                variable.update({k: substituted_v})
            return variable
        elif isinstance(variable, list) and variable:
            return [cls.with_slot(v, body) for v in variable]
        elif isinstance(variable, tuple) and variable:
            return tuple([cls.with_slot(v, body) for v in variable])
        else:
            return get_slot(variable) if isinstance(variable, str) else variable

    @classmethod
    def with_expr(cls, expr, body=None):
        # 转换变量expr中的 定位表达式
        if body and expr:
            vs = Variables(body)
            return vs.substitute(expr)
        return expr
