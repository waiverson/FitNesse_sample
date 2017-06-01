# encoding:utf-8
__author__ = 'xyc'

import requests

class DefaultHttpRequest(object):

    def __init__(self,):
        self._uri=None
        self._method = None
        self._headers = {}
        self._params = {}
        self._data = {}
        self._session = None
        self._timeout = None

    def uri(self):
        return self._uri

    def with_uri(self, uri):
        self._uri = uri
        return self

    def method(self):
        return self._method

    def with_method(self, method):
        self._method = method
        return self

    def headers(self):
        return self._headers

    def with_headers(self, params):
        self._headers = params
        return self

    def params(self):
        return self._params

    def with_params(self, params):
        self._params = params
        return self

    def data(self):
        return self._data

    def with_data(self, data):
        self._data = data
        return self

    def session(self):
        return self._session

    def with_session(self, session=None):
        if not session:
            self._session = self.session_supplier()
            return self

    def session_supplier(self,):
            return requests.session()

    def timeout(self):
        return self._timeout

    def with_timeout(self, timeout=None):
        self._timeout = timeout
        return self

    def send(self):
        self._session.headers.update(self._headers)
        req = requests.Request(self._method.upper(), url=self._uri, params=self._params, data=self._data)
        prepped = self._session.prepare_request(req)
        return self._session.send(prepped, timeout=self._timeout)