1. cell value���ܴ��ڿ��ֵ䣬���б���Ԫ�棬�磺
|enter|expect_result	{'status':0,'result':{"is_open": 1, "app_key": "G94DWJOZ182bg7mM"}}|  ---OK
|enter|expect_result	{'status':0,'result':{}}|  ---fail ��Ϊresult��ֵΪ���ֵ�
������Ϣ��
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


2����дfixture�ļ����벻�����κδ��󣬷�����ʾ�Ҳ���module

3���ϸ�case���õ���propertyֵ���ᱻ���ӵ��¸�case����ʱ��Ҫ���¸�case��������ֵ 