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

    def _dict_to_object(self, kv):

        """
        :param kv: 需要转为object的dict
        :return:用于比较结果的实例
        """

        if not bool(kv or isinstance(kv, dict)):
            return exception.TypeError

        class Sample(object):
            pass

        sample = InstanceMatcher.Instance()

        for _k in kv:
            if type(kv[_k]) == dict:
                # setattr(sample, _k, InstanceMatcher.Instance(**kv[_k]))
                setattr(sample, _k, self._dict_to_object(kv[_k]))
            else:
                setattr(sample, _k, kv[_k])

        return sample

    def match_by_struct(self, ex_result, ac_result):

        try:
            expect = self._dict_to_object(ex_result)
            actual = self._dict_to_object(ac_result)

        except exception.TypeError, e:
            print ("Failed to convert to object: %s", e)
            sys.exit(-1)

        def diff(expect, actual):
            if isinstance(expect.__dict__, dict) and isinstance(actual.__dict__, dict):
                for k, v in expect.__dict__.items():
                    if isinstance(v, InstanceMatcher.Instance):
                        if diff(v, actual.__getattribute__(k)):
                            continue
                        else:
                            return False
                    if type(v) != type(actual.__getattribute__(k)):
                        return False
                return True
            else:
                return False

        return diff(expect, actual)

    def match_by_all(self, ex_result, ac_result):
        try:
            expect = self._dict_to_object(ex_result)
            actual = self._dict_to_object(ac_result)
        except exception.TypeError, e:
            print ("Failed to convert to object: %s", e)
            sys.exit(-1)

        def diff(expect, actual):
            if isinstance(expect.__dict__, dict) and isinstance(actual.__dict__, dict):
                for k, v in expect.__dict__.items():
                    if isinstance(v, InstanceMatcher.Instance):
                        if diff(v, actual.__getattribute__(k)):
                            continue
                        else:
                            return False
                    if v != actual.__getattribute__(k):
                        return False
                return True
            else:
                return False

        return diff(expect, actual)


test_dict = {'a':1, 'b':2, 'c':'test', 'd':{'d1':{'d1':2},'D2':3},'code':200}
test_dict2 = {'a':1, 'b':2, 'c':'test', 'd':{'d1':{'d1':2},'D2':4},'code':200}
print InstanceMatcher().match_by_struct(test_dict, test_dict2)
print InstanceMatcher().match_by_all(test_dict, test_dict2)


