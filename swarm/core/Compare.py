# encoding:utf-8
__author__ = 'xyc'

import sys, inspect, json, traceback
from unittest import TestCase as assertValidate
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class CompareMode(object):

    OBJECT_MODE = "OBJECT"
    JSON_SCHEMA_MODE = "JSON_SCHEMA"
    ASSERT_MODE = "ASSERT"

    def __init__(self):
        self.diff_result = {}

    @staticmethod
    def get_compare_mode(mode="JSON_SCHEMA"):
        if mode.upper() == CompareMode.OBJECT_MODE:
            return InstanceCompareMode()
        elif mode.upper() == CompareMode.JSON_SCHEMA_MODE:
            return JsonSchemaCompareMode()
        elif mode.upper() == CompareMode.ASSERT_MODE:
            return AssertCompareMode()

    def diff(self, expect, actual, by):
        pass


class InstanceCompareMode(CompareMode):

    def __init__(self):
        super(InstanceCompareMode,self).__init__()
        self.diff_result["object1"] = []
        self.diff_result["object2"] = []

    class Instance(object):
        def __init__(self, **entries):
            self.__dict__.update(entries)

    def dict_to_object(self, kv):

        """
        :param kv: 需要转为object的dict
        :return:用于比较结果的实例
        """

        if not bool(kv or isinstance(kv, dict)):
            raise TypeError

        class Sample(object):
            pass

        sample = InstanceCompareMode.Instance()

        for _k in kv:
            if type(kv[_k]) == dict:
                setattr(sample, _k, self.dict_to_object(kv[_k]))
            else:
                setattr(sample, _k, kv[_k])

        return sample

    def diff(self, object1, object2, by="kv"):
        """
        :param object1: 基准对象，表示为期望结果
        :param object2: 校验对象，表示为实际结果
        :param by: ‘kv’：比较key和value，‘struct’：比较key和value的类型
        :return: {"object1":[{x:1},...],"obejct2":[{x:2},...]},{x:1},{x:2}为两者差异项（不包含其隶属关系）
        """
        if isinstance(object1, dict):
            object1 = self.dict_to_object(object1)
        if isinstance(object2, dict):
            object2 = self.dict_to_object(object2)
        for k, v in object1.__dict__.items():
            if isinstance(v, InstanceCompareMode.Instance):
                try:
                    object2.__getattribute__(k)
                    self.diff(v, object2.__getattribute__(k), by)
                except AttributeError:
                    self.diff_result["object1"].append({k:v})
            else:
                try:
                    if by == "struct":
                        if bool(type(v) != type(object2.__getattribute__(k))
                                and (type(v) != str
                                and type(object2.__getattribute__(k))!= unicode)):
                            self.diff_result["object1"].append({k:type(v)})
                            self.diff_result["object2"].append({k:type(object2.__getattribute__(k))})

                    if by == "kv":
                        if v != object2.__getattribute__(k):
                            self.diff_result["object1"].append({k:v})
                            self.diff_result["object2"].append({k:object2.__getattribute__(k)})

                except AttributeError:
                    self.diff_result["object1"].append({k:v})

        return self.diff_result


class JsonSchemaCompareMode(CompareMode):

    def __init__(self):
        pass

    def diff(self, json_schema, instance, by=None):
        """
        :param json_schema: json schema
        :param instance: json or dict
        :return:
        """
        try:
            return validate(instance, json_schema)
        except ValidationError, e:
            return '匹配失败原因:\t{}\n具体信息:\n{}'.format(e.message, traceback.format_exc())


class AssertCompareMode(assertValidate):

    def __init__(self):
        self._assert_funcs_ = {'EQUAL': 'assertEqual',
                               'IN':'assertIn',
                               'ITEMSEQUAL':'assertItemsEqual',
                               'REGEXPMATCHES':'assertRegexpMatches',
                               'DICTCONTAINSSUBSET':'assertDictContainsSubset'
                               }

    def assertEqual(self, first, second, msg=None):
        type_equality_func = {dict: 'assertDictEqual',
                                    list: 'assertListEqual',
                                    tuple: 'assertTupleEqual',
                                    set: 'assertSetEqual',
                                    frozenset: 'assertSetEqual'
                                }
        if type(first) is type(second):
            asserter = type_equality_func.get(type(first))
            if asserter is not None:
                    if isinstance(asserter, basestring):
                        asserter = getattr(self, asserter)
                    return asserter(first, second)
        else:
            return "expect is not consistent with actual's type, can not assert by assertEqual"

    def diff(self, expect, actual, by='EQUAL'):
        try:
            asserter = self._assert_funcs_.get(by.upper(), 'assertEqual')
            if asserter is not None:
                if isinstance(asserter, basestring):
                    asserter = getattr(self, asserter)
                    return asserter(expect, actual)
        except AssertionError, e:
            return '匹配失败原因:\t{}\n具体信息:\n{}'.format(e.message, traceback.format_exc())


