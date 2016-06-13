1. cell value不能存在空字典，空列表，空元祖，如：
|enter|expect_result	{'status':0,'result':{"is_open": 1, "app_key": "G94DWJOZ182bg7mM"}}|  ---OK
|enter|expect_result	{'status':0,'result':{}}|  ---fail 因为result的值为空字典
报错信息：
Traceback (most recent call last):
  File "C:\Python27\Lib\site-packages\fit\fit\TypeAdapter.py", line 610, in parseAndSet
    result = self.parse(cell)
  File "C:\Python27\Lib\site-packages\fit\fit\TypeAdapter.py", line 634, in parse
    return self.protocol.parse(cell)
  File "C:\Python27\Lib\site-packages\fit\fit\taProtocol.py", line 39, in parse
    return self.ta.parse(cell.text())
  File "C:\Python27\Lib\site-packages\fit\fit\taBase.py", line 563, in parse
    result = self._safeEval(stripped)
  File "C:\Python27\Lib\site-packages\fit\fit\taBase.py", line 79, in _safeEval
    result = self._safeAssemble(nodes[0])
  File "C:\Python27\Lib\site-packages\fit\fit\taBase.py", line 114, in _safeAssemble
    values = map(self._safeAssemble, values)
  File "C:\Python27\Lib\site-packages\fit\fit\taBase.py", line 112, in _safeAssemble
    keys, values = zip(*node.items)
ValueError: need more than 0 values to unpack


2、缩写fixture文件必须不存在任何错误，否则提示找不到module

3、上个case设置的类property值，会被外延到下个case，有时需要在下个case中重新置值 