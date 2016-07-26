# encoding:utf-8
__author__ = 'xyc'

class RestData(object):

    def __init__(self):
        self.raw = ""

    @property
    def body(self):
        if not self.raw:
            return None
        else:
            return self.raw
    @body.setter
    def body(self, raw_body):
        self.raw = raw_body



class RestResponse(RestData):

    def __init__(self, raw):
        super(RestResponse,self).__init__()
        self.body = raw
        self._status_code = 200

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, scode):
        self._status_code = scode


    def __str__(self):
        return "{self._status_code},{self.body}".format(self=self)

