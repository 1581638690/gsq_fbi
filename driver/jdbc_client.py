#/bin/python
# -*- coding: utf-8 -*- 

import urllib3
import traceback

#import simplejson as json
import time
#import cjson
import json

import urllib

"""
	author:	gjw
	version:1.0
	date: 20150320
	support the python 2.x and 3.x


"""

http = urllib3.PoolManager(timeout=3600.0)

class JDBC_Client():
	def __init__(self,server,port,db_name):
		self.server = server
		self.port = port
		self.db_name = urllib.parse.quote(db_name)
		self.query_url = 'http://%s:%d/rest/%s/query'%(self.server,self.port,self.db_name)
		self.post_url = 'http://%s:%d/rest/%s/'%(self.server,self.port,self.db_name)

	"""
	return 
	{

        "success": true,

		"columns":["id","age","name"],

		"data":[["1",12,"王五"],["2",20,"张三"]]

	} or
	{

	  "success": false,

	  "msg": "提交失败！",

	  "error": "具体错误信息"

	}
	
	"""
	def do_query(self,sql):
		q={"q":sql.encode("utf8")}
		d={"success":False,"error":"","msg":""}
		try:
			r = http.request("POST",self.query_url,q)			
			if r.status ==200:
				d = json.loads(r.data)	
				#s = unicode(r.data,"utf-8")		
				#d = cjson.decode(r.data)
			else:
				d["msg"]="server retun status %s" %(r.status)
		except Exception as e:
			print((traceback.format_exc()))
			d["msg"]="ERROR %s"%(e)
		return d
		
	def do_post(self,table,pk,data,types):
		q={"pkId":pk,"data":data,"types":types}
		post_url2 = self.post_url +urllib.parse.quote(table)
		#print self.post_url
		d={"success":False,"error":"","msg":""}
		try:
			r = http.request("POST",post_url2,q)			
			if r.status ==200:
				d = json.loads(r.data)
				#d = cjson.decode(unicode(r.data,"utf-8"))
			else:
				d["msg"]="server retun status %s" %(r.status)
		except Exception as e:
			print((traceback.format_exc()))
			d["msg"]="ERROR %s"%(e)
		return d
	
#end Esql_Client

if __name__=="__main__":
	esql = JDBC_Client("10.68.23.175",9600,"udba_175")
	begin = time.time()
	ret = esql.do_query("select * from bigdata3 where id<2000000")
	#print ret
	print(time.time()-begin)
	time.sleep(50)


	

	


