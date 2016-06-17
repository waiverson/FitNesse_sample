# encoding:utf-8
__author__ = 'xyc'

import sys,inspect,json,traceback


class CompareMode(object):

    JSON_MODE = "JSON"
    OBJECT_MODE = "OBJECT"
    DICT_MODE = "DICT"

    def __init__(self):
        self.diff_result = {}

    @staticmethod
    def get_compare_mode(mode):
        if mode.upper() == CompareMode.JSON_MODE:
            return JsonCompareMode()
        elif mode.upper() == CompareMode.DICT_MODE:
            return DictCompareMode()
        elif mode.upper() == CompareMode.OBJECT_MODE:
            return InstanceCompareMode()

    def diff(self):
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


class JsonCompareMode(CompareMode):

    def __init__(self):
        pass

    def diff(self, json1, json2):
        pass

class DictCompareMode(CompareMode):

    def diff(self, dict1, dict2):
        return json.dumps(dict1) == json.dumps(dict2)


if __name__ == '__main__':
    test_dict = {'a':1, 'd2':3, 'c':'test', 'd':{'d1':{},'D2':4,'D9':[1,2,3]},'code':200}
    test_dict2 = {'a':1, 'd2':3, 'c':'test', 'd':{'d1':{'d4':3},'D2':4,'D9':[1,2]},'code':200}
    cc = {
    "status": 0,
    "message": "ok",
    "result": {
    "name": "百度大厦员工食堂",
    "location": {
    "lng": 116.308022,
    "lat": 40.056892
    },
    "address": "海淀区上地十街10号(近辉煌国际)",
    "detail": 1,
    "uid": "5a8fb739999a70a54207c130",
    "detail_info": {
    "tag": "美食;其他",
    "detail_url": "http://api.map.baidu.com/place/detail?uid=5a8fb739999a70a54207c130&output=html&source=placeapi_v2"}}}

    compare = CompareMode.get_compare_mode("OBJECT")
    print compare.diff(compare.dict_to_object(test_dict), compare.dict_to_object(test_dict2),'kv')


