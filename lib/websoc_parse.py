# -*- coding: utf-8 -*-
'''
@说明 ：该脚本的作用是将嵌套字典类型的数据进行连接输出即：info_status
'''
import os
import sys
import csv
import datetime

'''
@date : 2017/10/30
@函数 ：makeTheDictOut
@描述 ：重新组装字典的key，变为value.key形式
@返回 ：字典
'''
def makeTheDictOut(key,value):
	_dic = dict()
	for _key,_value in value.items():
		key1 = "%s_%s"%(key,_key)
		if _key == "keywords":
			_list = []
			for per in _value:
				if not isinstance(per,dict):
					_list.append(per)
				else:
					_list.append(per.get("keyword"))
			_value = _list
		_dic[key1] = _value
	return _dic
	
	
'''
@date : 2017/10/30
@函数 ：dealTheData
@描述 ：处理获取的json数据，将值为dict类型的转换出来
@返回 ：字典
'''
def dealTheData(data):
	while 1:
		_list = []
		for key, value in data.items():
			if isinstance(value, dict):
				_list.append(key)
				newValue = makeTheDictOut(key, value)
				data = dict(data, **newValue)
			else:
				continue
		if not _list:
			break
		for per in _list:
			del data[per]
	return data
