#/bin/python
# -*- coding: utf-8 -*- 


import happybase
import logging
import numpy as np
import pandas as pd
import struct
import sys

__author__ = 'emmanuel'

logger = logging.getLogger(__name__)


def read_hbase(con, table_name, key, cf=':'):
	"""Read a pandas DataFrame object from HBase table.

	:param con: HBase connection object
	:type con: happybase.Connection
	:param table_name: HBase table name to which the DataFrame should be read from
	:type table_name: str
	:param key: row key from which the DataFrame should be read
	:type key: str
	:param cf: Column Family name
	:type cf: str
	:return: Pandas DataFrame object read from HBase
	:rtype: pd.DataFrame
	"""
	table = con.table(table_name)
	if key !=":":
		if cf==":":
			rows = table.scan(row_prefix=key)
		else:
			rows = table.scan(row_prefix=key,columns=[cf])
	else:
		if cf==":":
			rows = table.scan()
		else:
			rows = table.scan(columns=[cf])

	indexs=[]
	data=[]
	for key,row in rows:
		indexs.append(key)
		data.append(row)
	df = pd.DataFrame(data,index=indexs)

	return df


def to_hbase(df, con, table_name, key, cf=':'):
	"""Write a pandas DataFrame object to HBase table.

	:param df: pandas DataFrame object that has to be persisted
	:type df: pd.DataFrame
	:param con: HBase connection object
	:type con: happybase.Connection
	:param table_name: HBase table name to which the DataFrame should be written
	:type table_name: str
	:param key: row key to which the dataframe should be written
	:type key: str
	:param cf: Column Family name
	:type cf: str
	"""
	table = con.table(table_name)
	
	#全转成字符串类型
	df.index = df.index.astype("unicode")
	for column in df.columns:
		df[ column ]= df[ column ].astype("unicode")

	with table.batch(transaction=True) as b:
		for index,row in df.iterrows():
			if key!=":":
				index = key+index
			row_value ={}
			if cf!=":":
				for column, value in row.iteritems():
					if not pd.isnull(value):
						row_value[':'.join((cf, column))] = value
			else:
				for column, value in row.iteritems():
					if not pd.isnull(value):
						row_value[column] = value
			b.put(index, row_value)



def test_readhbase():
	connection = None
	p=u"10.68.23.85,table-name,:,:"
	p2 = p.encode("utf-8").split(",")
	if len(p2) <4: raise Exception(u"参数不正确！正确格式:ip,table,key,cf")
	df2=pd.DataFrame()
	try:
		connection = happybase.Connection(p2[0].strip())
		connection.open()
		print (p2[3].strip())
		df2 = read_hbase(connection, p2[1].strip(), p2[2].strip(), cf=p2[3].strip())
	finally:
		if connection:
			connection.close()
	
	print (df2.head())
	return df2
	
def test_tohbase(df):
	connection = None
	p=u"10.68.23.85,table-name,:,:"
	p2 = p.encode("utf-8").split(",") #很重要，因为HBase使用的原始编码
	if len(p2) <4: raise Exception(u"参数不正确！正确格式:ip,table,key,cf")
	try:
		connection = happybase.Connection(p2[0].strip())
		connection.open()
		to_hbase(df,connection, p2[1].strip(), p2[2].strip(), cf=p2[3].strip())
	finally:
		if connection:
			connection.close()
	return df

if __name__ == "__main__":
	df = test_readhbase()
	test_tohbase(df)



