# encoding:utf-8
__author__ = 'xyc'

import sys,inspect
import exception


class Matcher(object):

    pass

class InstanceMatcher(Matcher):

    def __init__(self):
        pass

    class Instance(object):
        def __init__(self, **entries):
            self.__dict__.update(entries)

    def _dict_to_object(self,kv):

        """
        :param kv: 需要转为object的dict
        :return:用于比较结果的，类的实例
        """

        if not bool(
            kv or isinstance(kv, dict)):
            return exception.TypeError

        class Sample: pass
        for _k in kv:
            if type(kv[_k]) == dict:
                setattr(Sample, _k, InstanceMatcher.Instance(**kv[_k]))
            else:
                setattr(Sample, _k, kv[_k])

        return Sample

    def by_struct(self,ex_result,ac_result):

        try:
            expect = self._dict_to_object(ex_result)
            actual = self._dict_to_object(ac_result)

        except exception.TypeError, e:
            print ("Failed to convert to object: %s", e)
            sys.exit(-1)

        def diff_struct(expect, actual):
            if isinstance(expect.__dict__,dict) and isinstance(actual.__dict__,dict):
                for k, v in expect.__dict__.items():
                    print v
                    if isinstance(v, InstanceMatcher.Instance):
                        diff_struct(v, actual.__dict__[k])
                    if type(v) != type(actual.__dict__[k]):
                        return False
                return True
            else:
                return False

        return diff_struct(expect, actual)

    def by_key_value(self,ex_result,ac_result):
        try:
            expect = self._dict_to_object(ex_result)
            actual = self._dict_to_object(ac_result)
        except exception.TypeError, e:
            print ("Failed to convert to object: %s", e)
            sys.exit(-1)

        def diff_value(expect, actual):
            if isinstance(expect.__dict__,dict) and isinstance(actual.__dict__,dict):
                for k, v in expect.__dict__.items():
                    print v
                    if isinstance(v, InstanceMatcher.Instance):
                        diff_value(v, actual.__dict__[k])
                    if v != actual.__dict__[k]:
                        return False
                return True
            else:
                return False

        return diff_value(expect, actual)


test_dict = {'a':1, 'b':2, 'c':'test', 'd':{'d1':'d1'},'code':200}
test_dict2 = {'a':1, 'b':2, 'c':'test', 'd':{'d1':'d1'},'code':200}
print InstanceMatcher().by_struct(test_dict,test_dict2)
print InstanceMatcher().by_key_value(test_dict,test_dict2)


