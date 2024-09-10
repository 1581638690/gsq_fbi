#/bin/python
# -*- coding: utf-8 -*- 

import urllib3,json
import traceback

"""
	author:	gjw
	version:1.0
	date: 20150320
	support the python 2.x and 3.x


"""

http = urllib3.PoolManager(timeout=600.0)

class Esql_Client():
	def __init__(self,server,port):
		self.server = server
		self.port = port
		self.url = 'http://%s:%d/json_out'%(self.server,self.port)
		
	"""
	the result struct
	result={}
	result["count"] = int
	result["took"]	= int
	result["cost"] = int 
	result["result"] = []
	result["msg"] = str	
	"""
	def do_sql(self,sql):
		q={"sql":sql}
		d={"msg":""}
		try:
			r = http.request("POST",self.url,q)			
			if r.status ==200:
				d = json.loads(r.data.decode())
			else:
				d["msg"]="server retun status %s" %(r.status)
		except Exception as e:
			print((traceback.format_exc()))
			d["msg"]="ERROR %s"%(e)
			raise e
		return d
#end Esql_Client


if __name__=="__main__":
	esql = Esql_Client("127.0.0.1",8000)
	ret = esql.do_sql("select * from people_all")
	ret = esql.do_sql("select * from people_all where q=军")
	ret = esql.do_sql("show tables")
	print(ret)
	

	


