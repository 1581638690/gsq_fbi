#/bin/python
# -*- coding: utf-8 -*- 

"""
@add by gjw  on 20140706
 add the get by id case
 
@add by gjw on 20140707
 add the  doc_type query ,sample flow:
 select * from index.doc_type
 select * from index.doc_type1.doc_type2
 
@add by gjw on 20140709
	change the id to _id, smaple flow:
	select * from car2012 where _id=2000001010


@add by gjw on 20140707
 add the aggregation support
 sample flow:
 select min(speed) as min_speed from index 
 select count(*) as doc_count from index group by wayid
 select count(*) as doc_count, avg(speed) as avg_speed from index group by wayid direction
 select count(*) as doc_count, avg(speed) as avg_speed from index group by speed[0-100,100-200,300]
 select count(*) as doc_count, avg(speed) as avg_speed from index where xzqh="hangzh" group by speed[0-100,100-200,300]
 
 
@add by gjw on 20140711
  support min,max,sum,avg,count,
  select count(*) as doc_count, avg(speed) as avg_speed ,min(speed) as min_speed from index where UTC between to group by wayid, direction
  count(*) can not write as
  only support group by two field
  support the query and group
 
@add by gjw on 20140712
	support the range,ip_range,histogram,date_histogram buckets 
  
"""

"""
@add by gjw on 20140712 v1.0
	comb the ESql_query and ESql_aggs to Esql

@add by gjw on 20140713 v1.0.1
	result is "type":"query" or "type":"aggs"
	aggs result comb a one []
	result=[{"g1":"","g2":"","count":0,"field1":0,"field2":0}]

@add by gjw on 20140714 v1.0.2
	get_id parse the doc_type


@add by gjw on 20140717 v1.0.3
	add the exception deal
	
@add by gjw on 20140718 v1.0.4
	transfor the hits["_source"] to result
	
@add by gjw on 20140721 v1.0.5
	support the highlight 
	change the where deal type
	add list_remove fun to optimize the code
	add the fun transfor_get
	
@add by gjw on 20140722 v1.0.6
    filter the invalid char

@add by gjw on 20140722 v1.0.7
	support the DDL sql

@add by gjw on 20140723 v1.0.8
	support the exe sql cost time
	support the Exception print
	change the result is self.result
	modify the terms aggregation size =0

@add by gjw on 20140724 v1.0.9
	add the json deal the dict and list and tuple type
	
@add by gjw on 20140725 v1.1.0
    deal the josn dumps chinese coder
    
@add by gjw on 20140725 v1.20
	select support the order by field
	
@add by gjw on 20140730 v1.3.0
	support the group by  field.kw

@add by gjw on 20140730 v1.3.1
	add the logging
	add the desc table
	add the insert into
	add the delete 
	
@add by gjw on 20140731 v1.40
	support the  where field in (blue,pill) 

@add by gjw on 20140801
	modify the where logic with the "or" 
	
@add by gjw on 20140805 v 1.5.0
	add the unkonw sql support
	websql es connect add sniff_on_start=True,sniff_on_connection_fail=True,sniffer_timeout=5 

@add by gjw on 20140806 v1.5.1
	insert into sql replace  the \, to , and relace the " to space
	support the flush table
	support the create table
	support the drop the table.type

@add by gjw on 20140807 v1.5.2
	modify the create table bug
	
@add by gjw on 20140811 v1.6
	support the <> or != query
@add by gjw on 20140812 v1.6.2
	support the >,>= ,<,<=

@add by gjw on 2014-08-18 v1.7
	support the is null or is not null

@add by gjw on 2014-08-18 v1.8
	support the parent-child query
	support the "create table test.c2(_parent type pp) with 10,1 "

@add by gjw on 201408-19 v1.8.1
	support the batch with begin 

@add by gjw on 201408-19 v1.8.2
	fix the bug with get_id

@add by gjw on 2014-08-21 v1.8.3
	catch the Exception on ddl

@add by gjw on 2014-08-26 v1.8.4
	support the post method

@add by gjw on 2014-08-27 v1.9
	support the insert not have _id
	support the ddl "alter meta ..." and "get meta "

@add by gjw on 2014-08-27 v1.9.1
	support the ddl "show nodes"

@add by gjw on 2014-09-02 v1.9.2
	fix the bug with get meta

@add by gjw on 2014-09-02 v1.9.3
	create table yes is not_analyzed

@add by gjw on 2014-09-02 v1.9.4
	get meta support the 1024 field

@add by gjw on 2014-09-03 v1.9.5
	add the ddl "show version"
	add the ddl "update"

@add by gjw on 2014-09-04 v1.9.6
	fix the jsonp bug and esql.js
	
@add by gjw on 2014-09-04 v1.9.7
	support the between to have the space

@add by gjw on 2014-09-11 v1.9.8
	support ignore index if index is not exits 

@add by gjw on 2014-09-11 v1.9.9
	fix the scan bug
	optimize the insert and update ,support the "=;"
	support the bulk into {}{}{}{}

@add by gjw on 2014-09-16 v1.9.10
	support the index meta and show tables add the zh
	alter meta vehicle_type._self(车辆大表)
	get meta *

@add by gjw on 2014-0919 v1.9.11
	support the ins and optimize the get_id query

@add by gjw on 2014-0924 v1.9.12
	modify the aggs count,
	support the no group by sum,avg etc.
	support the aggs of terms type order by filed asc or field desc

@add by gjw on 20140925 v1.9.13
	group have key_as_string field to ip field
	
@add by gjw on 20140925 v1.9.14
	support the aggs of histogram type soft, and order by field default asc flag

@add by gjw on 20140929 v1.9.15
	support the  len <3 +""
	ins must all include terms
	
@add by gjw on 20140929 v1.9.16
	support the delete_by_query
	
@add by gjw on 20141009 v1.9.17
	modify the start script

@add by gjw on 20141011 v1.9.18
	support the union all
	
@add by gjw on 20141011 v1.9.19
	optimize the gte,lte etc a > 1 and a< b equal a between 1 to b 

@add by gjw on 20141015 v1.9.20
	support the distinct

@add by gjw on 20141016 v1.9.21
	add meta field type and table calalog service
	
@add by gjw on 20141017 v1.9.22
	improve the routing support 
	
@add by gjw on 20141105 v1.9.23
	improve the term length <3 and not include the * or ? ,the term add ""
	
@add by gjw on 20141107 v1.9.24
	improve the update sql, can deal the 
	update xxx set filed=select * from tablea where fielda='a\,dd=2', f1=122 where _id=1

@add by gjw on 20141108 v1.9.25
	improve the get_id and update

@add by gjw on 20141118 v1.9.26
	add the in child query

@add by gjw on 20141122 v1.9.27
	add the having support count =2 ,count >2, count < 2
	
@add by gjw on 20141123 v1.9.28
	fix the 1.9.26 and 1.9.27 bug, and support the  in() group by
	such as:
  select count(*) from test-index1 where ZJHM in (select ZJHM from test-index order by ZJHM)
  group by ZJHM having count >=2
  
  select * from test-index2 where ZJHM in (select ZJHM from test-index1 group by  ZJHM having count >=2)

@add by gjw on 20141124 v1.9.29
	add the  join on  query support,like 
	select * from car1 order by ZJHM limit 10000 as a  
	join select * from car2 order by ZJHM limit 10000 as b on a.ZJHM = b.ZJHM 
	join select * from car3 order by ZJHM limit 10000 as c on c.ZJHM = a.ZJHM
	
@add by gjw on 20141202 v1.9.30
	add the fast join SQL, like:
	select * from cs_all 
	fastjoin hc where mdd=beijing  and kssj = 2014-11-10
	fastjoin hc where mdd=hangzhou and kssj = 2014-11-12
@add by gjw on 20141205 v1.9.31
	fix the get_id bug , because v1.9.30

@add by gjow on 20141211 v1.9.32
 join the result max is 100000
	select * from car1   as a  
	join select * from car2 where ZJHM=7   as b on a.ZJHM = b.ZJHM 
	join select * from car3  as c on c.ZJHM = a.ZJHM

@add by gjw on 20141223 v1.9.33
	add the request_timeout=100

@add by gjw on 20141229 v1.9.34
	support the muli grup by

@add by gjw on 20141230 v1.9.35
	change ajax time out 120s
	
@add by gjw on 20150107 v1.9.36
	support the length() search
	
@add by gjw on 20150121 v1.9.37
	support the "minimum_should_match" : 1,
	
@add by gjw on 20150123 v1.9.38
	fix the createtable bug
	support the  where _all = a b c ,and the a b c is the and logic 

@add by gjw on 20150209-20150210 v1.9.39
	optimize the query order by memory and log the result with count took cost

@add by gjw on 20150210 v1.9.40
	fix the aggs bug,when result is none ,the count show zero
	and log the aggs result with count took cost

@add by gjw on 20150305 v1.9.41
	delete when the term's length <3 add the ""
	add the score by support
	 
@add by gjw on 20150309 v1.9.42
	create table support the sortable
	
@add by gjw on 20150309 v1.9.43
	support the 
	--show segments 
	--show shards
	--show recovery
	--show fielddata
@add by gjw on 20150310 v1.9.44
	add the ddl clear cache

@add by gjw on 20150312 v1.9.45
	modify the optimize max_semgent = 2
	
@add by gjw on 20150312 v1.9.46
	fix the order by bug

@add by gjw on 20150313 v1.9.47
	add the "show meminfo"

@add by gjw on 20150315 v1.9.48
	add the "show cpuinfo"
	
@add by gjw on 20150316 v1.9.49
	add the "service start|stop|status

@add by gjw on 20150318 v1.9.50
	fix the and condition bug

@add by gjw on 20150318 v1.9.51
	support the q= query

@add by gjw on 20150320 v1.9.52
	fix the query bug

@add by gjw on 20150320 v1.9.53
	fix the _all bug 

@add by gjw on 20150323 v1.9.54
	fix the score_by bug to agg

@add by gjw on 20150324 v1.9.55
	support  the crate table options
	and suport the desc table show muliti fields

@add by gjw on 20150325 v1.9.56
	show segments limit 2048
	add the show thread_pool and show cluster
	
@add by gjw on 20150330 v1.9.57
	fix the show meminfo bug

@add by gjw on 20150402 v1.9.58
	add the "create view from","show views", "drop view " 

@add by gjw on 20150403 v1.9.59
	add the "reload" ddl
@add by gjw on 20150403 v1.9.60
	add the red secret key 
	
@add by gjw on 20150505 v1.9.61
	fix the insert into bug , deal the ()
	modify the sql log length ,max=240
	fix the sql dispatch bug, add the sql.find("select") ==0 and

@add by qs on 2015-05-15 v20.8-62 
	add multi fields query,support Wildcard 
	select * from qs_all_info where  nam*,d* = 张三 highlight * limit 0,100

@add by qs on 2015-05-26 v20.8-63 
	add nested query,like: 'lg' and 'wb' is nested type
	select * from people_all 
	insideq lg where mdd=beijing  and kssj = 2014-11-10
	insideq wb where mdd=hangzhou and kssj = 2014-11-12


@add by qs on 2015-06-15 v20.8.64
	in fastjoin,parent query support conditons:
	select * from cs_all where dx=xxx and kssj between 2014-11-10 to 2014-11-12
	fastjoin hc where mdd=beijing  and kssj = 2014-11-10
	fastjoin hc where mdd=hangzhou and kssj = 2014-11-12

@add by qs on 2016-01-06 v20.8.66
	logging add TimedRotatingFileHandler 
	search use elasticsearch sort 


@add by qs on 2016-01-14 v20.8.67
	change default operator from OR to AND


@add by qs on 2016-01-15 v20.8.68
	highlight fragment_size 65535
	
@add by gjw on 2016-07-15 v20.8.70
	1去掉日志管理线程
	2去掉装载红名单
	3增加scan时可以指定字段
	4增加scan时可以指定type

@add by gjw on 20161124 scroll
出错再取一次，仍出错则返回-1

@add by gjw on 20171220
修正select不能选择字段的bug
FEA使用的是这个版本

@add by gjw on 20200726 
使用es6的驱动来支持es7

"""
import sys

sys.path.append("../lib")

from datetime import datetime
from .elasticsearch6 import Elasticsearch,helpers
import time
import json
import traceback
import copy
from . import cfg
#import cfg

import logging
import logging.handlers
import hashlib

import pandas as pd
import numpy as np
import re
import os,signal

__version__="7.0.1"
# update by qs 20151119 for 2.8.65

# 创建一个logger
logger = logging.getLogger('esql7')
logger.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建一个handler，用于写入日志文件
from logging.handlers import RotatingFileHandler
#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大10M
fh =  RotatingFileHandler('logs/esql7.log', maxBytes=10*1024*1024,backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# 再创建一个handler，用于输出到控制台
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#ch.setFormatter(formatter)

# 给logger添加handler
#logger.addHandler(ch)

# 创建一个handler，用于输出到日志文件
#rf=logging.handlers.TimedRotatingFileHandler('logs/esql.log', 'D', 1, 0)  
#rf.setFormatter(formatter)
#rf.setLevel(logging.DEBUG)

#logger.addHandler(rf)


#add by gjw on 20150315
import urllib3
http = urllib3.PoolManager()

#add by gjw on 20140721
def list_remove(l,b):
	l2 = []
	[l2.append(i) for i in l if i !=b]
	return l2

#add by gjw on 20150313
def memsize_to_unit(x):
	unit=["b","kb","mb","gb","tb","pb"]
	i=0
	while True:
		d = x /1024.0
		if d <=1:
			break
		else:
			x =d
		i +=1
	return "%.1f%s"%(x,unit[i])

def to_gb(x):
	if type(x)==str:
		x = x.strip()
		if x.endswith("gb"):
			return float(x[:-2])
		if x.endswith("tb"):
			return float(x[:-2])*1024
		if x.endswith("mb"):
			return float(x[:-2])/1024.0
		if x.endswith("kb"):
			return float(x[:-2])/1024.0/1024.0
		return 0
	elif x==None:
		return 0
	else:
		return x/1024/1024

def sum_memsize(x,y,z):
	gb_sum = to_gb(x) + to_gb(y) + to_gb(z)	
	return "%.1fgb"%(gb_sum)
	
#add by gjw on 20150324
#处理多个{}扩展选项的问题
def trans_ct_sql(sql):
	new_sql=[]
	options_start=0
	start = 0
	for i,s in enumerate(sql):
		if s=="{":
			options_start +=1
		elif s=="}":
			options_start -=1
		elif s==",":
			if options_start ==0:
				new_sql.append(sql[start:i])
				start =i+1
		else:
			pass
	new_sql.append(sql[start:])
	return new_sql

from datetime import date
import shutil
def log_manager(tid):
	elog="logs/esql.log"
	ptime = date.today()
	while  True:
		ctime =  date.today()
		if (ctime - ptime).days != 0:
			bk_file = elog + "." + ptime.strftime('%Y-%m-%d')
			if os.path.isfile(bk_file) is False:
				fp = open(bk_file,'w')
				fp.close()
				shutil.copyfile(elog,bk_file)
				fp = open(elog,'w')
				fp.close()
		time.sleep(3600)
		ptime=ctime



class ESql():
	"""
	处理select语句
	"""
	def __init__(self,es):
		self.es = es
		self.query = ESql_query(self.es)
		self.aggs = ESql_aggs(self.es)
		self.ddl = ESql_ddl(self.es,self.query,self.aggs)
		#update by gjw on 20160715
		self.redkeys = []
		#self.redkeys= self.load_redkeys()
		#thread.start_new_thread(log_manager, (1,))


	def load_redkeys(self):	#add by gjw on 20150403
		res= self.query.do_sql("select * from redkeys limit 30000")
		redkeys=[]
		for r in res["result"]:
			redkeys.append("%s"%(r["secret_key"]))
		print("rekeys have %d"%(len(redkeys)))
		return redkeys
	
	def do_check_before(self,sql):	#add by gjw on 20150403 update by qs on 20160518
		for redkey in self.redkeys:
			if sql.find(redkey) >=0:
				return False
		return False
	
	def do_check_after(self,result):	#add by gjw on 20150403 update by qs on 20160518		
		for r in result["result"]:
			isRed=False
			if '_index' in r and r['_index'] == 'redkeys':
				continue
			for k,v in r.items():
				v = "%s"%(v)
				if v in self.redkeys:
					isRed=True
			if isRed==True:
				for k,v in r.items():
					if k not in ['_id','_index','_type']:
						r[k] = '****************************'

		return result
		
	
	def do_sql(self,sql):		
		#add 20140722
		sql = sql.replace("\n"," ").replace("\r"," ").replace("\t"," ").strip()
		
		#modify by gjw by 20150505
		logger.info(sql)
		
		b0=time.time()
		#add by gjw on 20150403
		result={"type":"ddl","count":0,"took":20,"cost":20,"result":[],
			"msg":"ERROR the sql has the secret key,don't to execute!"}
		
		#add by gjw on 20141118 add the in(select ) query
		if sql.find("select") ==0 and (sql.find(" in (select") >0 or sql.find(" in ( select") >0):
			result= self.ddl.do_in_child_query(sql)
		elif sql.find("select") ==0 and sql.find(" join ") >0 and sql.find(" on ") >0:
			result= self.ddl.do_join_on(sql)
		#add by gjw on 20141202 support the fast join
		elif sql.find("select") ==0 and sql.find(" fastjoin ") >0:
			result= self.ddl.do_fast_join(sql)
		#add by qs on 20150525 support insideq	
		elif sql.find("select") ==0 and sql.find(" insideq ") >0:
			result= self.ddl.do_inside_query(sql)
		elif sql.find("select") ==0 and (sql.find("count(*)") >0 or sql.find("group by") >0 or sql.find(" as ") >0):
			result= self.aggs.do_sql(sql)
		elif sql.find("select") ==0 and sql.find("union all") >0:
			result= self.ddl.do_sql(sql)
		elif sql.find("select") ==0 or sql.find("scan")==0 or sql.find("scroll")==0:
			result= self.query.do_sql(sql)
		else:
			result= self.ddl.do_sql(sql)
		
		result["cost"] = int((time.time()-b0)*1000)
		return result
	
	#end fun do_sql
#end the class ESql


def deal_in_not_in(cond,n,l):
	fname = cond[0:n].strip()
	tags = cond[n+l:].replace("(","").replace(")","").split(",")
	tags = [i.replace('"',"").strip() for i in tags]
	return (fname,tags)


def build_parent_child_query_body(body,sql_tree):
	#add by gjw on 2014-08-08
	"""
	{"has_child" : {
						"type" : "cc",
						"query" : {
							"query_string" : {
								"default_field":"text",
								"query" : "问题"
							}
						}
					 }
					}
	"""	
	sql_tree2={}
	doc_types=[]
	for cond in sql_tree["where"]["must"]:
		n=cond.find(".")
		if n >1:
			doc_type=cond[0:n].strip()
			if doc_type not in doc_types:
				doc_types.append(doc_type)
				sql_tree2[doc_type]={"where":{"must":[],"must_not":[],"should":[]}}
			sql_tree2[doc_type]["where"]["must"].append(cond[n+1:])
	
	for cond in sql_tree["where"]["should"]:
		n=cond.find(".")
		if n >1:
			doc_type=cond[0:n].strip()
			if doc_type not in doc_types:
				doc_types.append(doc_type)
				sql_tree2[doc_type]={"where":{"must":[],"must_not":[],"should":[]}}
			sql_tree2[doc_type]["where"]["should"].append(cond[n+1:])
	
	for doc_type in doc_types:
		body2={
			 "query":{
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				}
			}
		}
		build_query_body(body2,sql_tree2[doc_type])
		b = {
			"has_child":{
				"type": doc_type,
			}
		}
		b["has_child"]["query"] = body2["query"]
		body["query"]["bool"]["must"].append(b)
	#print body
	return body		

def build_haschild_query(doc_type,sql_tree):
	body2={
			 "query":{
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				}
			}
		}
	build_query_body(body2,sql_tree)
	b = {
			"has_child":{
				"type": doc_type,
			}
		}
	b["has_child"]["query"] = body2["query"]
	return b	
	


def build_nested_highlight(body):
	if ("highlight" in body) == False:
		return
	body["highlight"]["highlight_query"] = {
		"bool": {
			"must":[],
			"must_not":[],
			"should":[]
		}
	}
	for n_query in body["query"]["bool"]["must"]:
		if "nested" in n_query:
			#print body["highlight"]["highlight_query"]["bool"]["must"]
			#body["highlight"]["highlight_query"]["bool"]["must"].append(n_query["nested"]["query"]["bool"]["must"]) 
			body["highlight"]["highlight_query"]["bool"]["must"] += n_query["nested"]["query"]["bool"]["must"]
			body["highlight"]["highlight_query"]["bool"]["must"] += n_query["nested"]["query"]["bool"]["should"]

		else:
			body["highlight"]["highlight_query"]["bool"]["must"].append(n_query)
			#body["highlight"]["highlight_query"]["bool"]["must"] += n_query

	



			
#add by qs 20150525	
def build_nested_query(field,sql_tree):
	body2={
			 "query":{
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				}
			}
		}
	
	build_query_body(body2,sql_tree)
	b = {
			"nested":{
				"path": field,
			}
		}
	b["nested"]["query"] = body2["query"]
	return b		

def build_query_body(body,sql_tree):
	
	#add by gjw on 20141011
	range_conds={}
	score_val="*"
	
	#deal the and 
	for cond in sql_tree["where"]["must"]:
		#add by gjw on 20150106 support the length() search
		if cond.find(".length()")>0:
			cond= cond.replace(".length()","")
			key_value = cond.split(">=")
			body["query"]["bool"]["must"].append({"regexp":{key_value[0].strip():{"value":".{%s,}"%(key_value[1].strip())}}})
			continue
		
		#add by gjw on 20140812 support the >= etc
		cond = cond.replace(">="," gte ").replace(">"," gt ").replace("<="," lte ").replace("<", " lt ")
		
		#modify by gjw on 20140731 deal the in keywork,sample : field in (aa,xx)
		n = cond.find(" not in ")
		if n >0:
			fname,tags = deal_in_not_in(cond,n,len(" not in "))
			body["query"]["bool"]["must_not"].append({"terms":{fname:tags}})
		else:
			n = cond.find(" in ")
			if n >0:
				fname,tags = deal_in_not_in(cond,n,len(" in "))
				body["query"]["bool"]["must"].append({"terms":{fname:tags}})
			
			#add by gjw on 20140919
			n = cond.find(" ins ")
			if  n>0:
				"""
				fname,tags = deal_in_not_in(cond,n,len(" ins "))
				for tag in tags:
					body["query"]["bool"]["should"].append({"query_string":{"default_field":fname,"query":tag}})
				"""
				#add by gjw on 20140929
				fname,tags = deal_in_not_in(cond,n,len(" ins "))
				body["query"]["bool"]["must"].append({"terms":{fname:tags,"minimum_should_match":len(tags)}})
			else:
				a = cond.split("!=")
				if len(a) >=2:
					#add by qs on 20150515 20.8-62
					fds = a[0].split(",")
					if len(fds) >=2 :
						fields=[]
						for fd in fds:
							fields.append(fd.strip())
						body["query"]["bool"]["must_not"].append({"query_string":{"fields":fields,"query":a[1].strip()}})
					else:
						body["query"]["bool"]["must_not"].append({"query_string":{"default_field":a[0].strip(),"query":a[1].strip()}})
				else:
					a = cond.split("=")
					if len(a) >=2:
						#the case is " key = value"
						#add by 20140929
						value = a[1].strip();
						#delete by gjw on 20150305
						"""
						#add by gjw on 20141105
						if len(value) <=3 and value.find("*")==-1 and value.find("?")==-1 and value.isdigit() ==False :
							value = '"%s"'%(value)
						"""
						if a[0].strip() == "_all": #deal the socre
							score_val = value
						
						#add by gjw on 20150319
						if a[0].strip() == "q":
							score_weight=100
							fields=[]
							if ("score_by" in sql_tree) == False:
								sql_tree["score_by"]=[]
							for score_field in sql_tree["score_by"]:
								fields.append("%s^%d"%(score_field,score_weight))
								score_weight=score_weight/2
							fields.append("_all")
							body["query"]["bool"]["must"].append(
							{"query_string":{"fields":fields,"query":value,"default_operator":"AND"}})
						else:
							#add by qs on 20150515 20.8-62
							#updated by qs on 20160114 20.8.-67
							fds = a[0].split(",")
							if len(fds) >=2 :
								fields=[]
								for fd in fds:
									fields.append(fd.strip())
								body["query"]["bool"]["must"].append({"query_string":{"fields":fields,"query":value,"default_operator":"AND"}})
							else:
								body["query"]["bool"]["must"].append({"query_string":{"default_field":a[0].strip(),"query":value,"default_operator":"AND"}})
					
					else:
						#modify by gjw on 20140904 
						b = cond.find(" between ")
						if b >0:
							#deal the case "field between 2 to 20"
							field_name = cond[0:b].strip()
							t = cond.find(" to ")
							b1 = cond[b+len(" between "):t].strip()
							b2 = cond[t+len(" to "):].strip()

							body["query"]["bool"]["must"].append({ "range": {field_name:{"gte":b1,"lte":b2}}})
						else:
							#add by gjw 2014-08-18 deal the is null or is not null
							#add by gjwon 2020-07-27 missing关键字换成了exists
							n = cond.find("is null")
							if n >0:
								body["query"]["bool"]["must_not"].append({
										"constant_score" : {
											"filter" : {
												"exists" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
								
							n = cond.find("is not null")
							if  n >0:
								body["query"]["bool"]["must"].append({
										"constant_score" : {
											"filter" : {
												"exists" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
							
							for mark in [" gte "," gt "," lte "," lt "]:
								a = cond.split(mark)
								if len(a) >=2:
									#add by gjw on 20141011
									if a[0].strip() in range_conds:
										range_conds[a[0].strip()].append((mark.strip(),a[1].strip()))
									else:
										range_conds[a[0].strip()]=[(mark.strip(),a[1].strip())]
									break;
	#add by gjw on 20141011
	for k,v in list(range_conds.items()):
		if len(v)==1:
			body["query"]["bool"]["must"].append({ "range": {k:{v[0][0]: v[0][1] }}})
		else:
			body["query"]["bool"]["must"].append({ "range": {k:{v[0][0]:v[0][1],v[1][0]:v[1][1]}}})
					
	#deal the or	
	for cond in sql_tree["where"]["should"]:
		#add by gjw on 20150106 support the length() search
		if cond.find(".length()")>0:
			cond= cond.replace(".length()","")
			key_value = cond.split(">=")
			body["query"]["bool"]["should"].append({"regexp":{key_value[0].strip():{"value":".{%s,}"%(key_value[1].strip())}}})
			continue
			
		#add by gjw on 20140812 support the >= etc
		cond = cond.replace(" >="," gte ").replace(" >"," gt ").replace(" <="," lte ").replace(" <", " lt ")
		
		#modify by gjw on 20140731 deal the in keywork,sample : field in (aa,xx)
		n = cond.find(" not in ")
		if n >0:
			fname,tags = deal_in_not_in(cond,n,len(" not in "))
			body["query"]["bool"]["must_not"].append({"terms":{fname:tags}})
		else:
			n = cond.find(" in ")
			if n >0:
				fname,tags = deal_in_not_in(cond,n,len(" in "))
				body["query"]["bool"]["should"].append({"terms":{fname:tags}})
			
			else:
				a = cond.split("!=")
				if len(a) >=2:
					#add by qs on 20150515 20.8-62
					fds = a[0].split(",")
					if len(fds) >=2 :
						fields=[]
						for fd in fds:
							fields.append(fd.strip())
						body["query"]["bool"]["must_not"].append({"query_string":{"fields":fields,"query":a[1].strip()}})
					else:
						body["query"]["bool"]["must_not"].append({"query_string":{"default_field":a[0].strip(),"query":a[1].strip()}})
				else:
					a = cond.split("=")
					if len(a) >=2:
						#the case is " key = value"
						#add by 20140929
						value = a[1].strip();
						"""
						if len(value) <=3 and value.find("*")==-1 and value.find("?")==-1:
							value = '"%s"'%(value)
						"""
						if a[0].strip() == "_all":
							score_val = value	
												
						#add by gjw on 20150319 add the q= search
						if a[0].strip() == "q":
							score_weight=100
							fields=[]
							for score_field in sql_tree["score_by"]:
								fields.append("%s^%d"%(score_field,score_weight))
								score_weight=score_weight/2
							fields.append("_all")				
							body["query"]["bool"]["should"].append(
							{"query_string":{"fields":fields,"query":value,"default_operator":"AND"}})
						else:
							#add by qs on 20150515 20.8-62
							fds = a[0].split(",")
							if len(fds) >=2 :
								fields=[]
								for fd in fds:
									fields.append(fd.strip())
								body["query"]["bool"]["should"].append({"fields":{"default_field":fields,"query":value}})
							else:
								body["query"]["bool"]["should"].append({"query_string":{"default_field":a[0].strip(),"query":value}})
					
					else:
						#modify by gjw on 20140904 
						b = cond.find("between")
						if b >0:
							#deal the case "field between 2 to 20"
							field_name = cond[0:b].strip()
							t = cond.find("to")
							b1 = cond[b+len("between"):t].strip()
							b2 = cond[t+len("to"):].strip()
							body["query"]["bool"]["should"].append({ "range": {field_name:{"gte":b1,"lte":b2}}})
						else:
							#add by gjw 2014-08-18 deal the is null or is not null
							n = cond.find("is null")
							if n >0:
								body["query"]["bool"]["should"].append({
										"constant_score" : {
											"filter" : {
												"exists" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
								
							n = cond.find("is not null")
							if  n >0:
								body["query"]["bool"]["must_not"].append({
										"constant_score" : {
											"filter" : {
												"exists" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
							for mark in [" gte "," gt "," lte "," lt "]:
								a = cond.split(mark)
								if len(a) >=2:
									body["query"]["bool"]["should"].append({ "range": {a[0].strip():{mark.strip():a[1].strip()}}})
									break;
	
	#add by gjw on 20150121
	#modify by gjw on 2020-1127
	if "should" in body["query"]["bool"] and len(body["query"]["bool"]["should"]) >=2:
		body["query"]["bool"]["minimum_should_match"]=1
	#body["query"]["bool"]["boost"]=1.0
	
	#deal the highlight on 20140721
	if "highlight" in sql_tree and  len( sql_tree["highlight"] ) >0:
		fields = "".join(sql_tree["highlight"])
		h = {"fields":{}}
		for field in fields.split(","):
			if field =="" : continue
			#add by qs on 2016-01-15 20.8.68
			h["fields"][field]={"fragment_size":65535}
		body["highlight"]=h
		
	#deal the score by on 20150305
	if  score_val!="*":
		body["query"]["bool"]["minimum_should_match"]=0
		score_weight=1.0
		for score_field in sql_tree["score_by"]:
			body["query"]["bool"]["should"].append(
				{"query_string":{"default_field":score_field,
				"query":score_val,
				"boost":score_weight}})
			
			score_weight=score_weight/2

	logger.info(body)
	return body


#处理mapings的字段信息
def map_properties(d,k,v):
	for k1,v1 in v["properties"].items(): 
		if "properties" in v1:
			map_properties(d,"%s.%s"%(k,k1),v1)
		else:
			v_copy = v1.copy()
			if "type" in v1 : del v_copy["type"]
			d["%s.%s"%(k,k1)] = {"name":"%s.%s"%(k,k1),"type":v1["type"],"x": str(v_copy)}

#递归处理生成的字段信息
def map_build_fields(b,k,k1,a):
	field_name = k1
	if field_name.find(".") >0: # 递归处理各个字段
		if k not in b:
			b[k]={"properties":{}}
		fs = field_name.split(".")
		map_build_fields(b[k]["properties"],fs[0],".".join(fs[1:]),a)
	else:
		if k not in b:
			b[k]={"properties":{}}
		if len(a) ==2:
			b[k]["properties"][field_name]={"type":a[1].strip()}
		elif len(a) >2:
			x = " ".join(a[2:])
			d = json.loads(x.replace("'",'"'))
			d["type"] =a[1].strip()
			b[k]["properties"][field_name]=d
		else:
			raise Exception(" %s 是非法的,不能创建索引%s !" %(item,index_name))


class ESql_ddl():
	"""
	处理ddl语句 add by gjw on 20120722
	
	show tables
	show tables with tname
	desc tname
	drop table tname
	create table tname with pri:10,rep:1
	optimize tname1,t2,t3
	insert into table.doc_type {_id:111,name:dddd,}
	
	"""
	def __init__(self,es,query,aggs):
		self.es = es
		self.esql_query = query
		self.query = query
		self.aggs = aggs
		
	
	def do_sql(self,sql):
		sql = sql.strip()
		b0 = time.time()
		res = {"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		try:
			if sql.find("show tables") ==0:
				res= self.do_showtables(sql)
			elif sql.find("show segments") ==0:
				res= self.do_show_segments(sql)
			elif sql.find("show shards") ==0:
				res= self.do_show_shards(sql)
			elif sql.find("show recovery") ==0:
				res= self.do_show_recovery(sql)
			elif sql.find("show fielddata") ==0:
				res= self.do_show_fielddata(sql)
			elif sql.find("show meminfo") ==0:
				res= self.do_show_meminfo(sql)
			elif sql.find("show cpuinfo") ==0:
				res= self.do_show_cpuinfo(sql)
			elif sql.find("drop table")==0:
				res= self.do_droptable(sql)
			elif sql.find("optimize")==0:
				res= self.do_optimize(sql)
			elif sql.find("get_settings")==0:
				res= self.do_get_settings(sql)
			elif sql.find("readonly")==0:
				res= self.do_readonly(sql)
			elif sql.find("clear cache")==0:
				res= self.do_clear_cache(sql)
			elif sql.find("flush")==0:
				res= self.do_flush(sql)
			elif sql.find("desc") ==0:
				res = self.do_desctable(sql)
			elif sql.find("insert into") ==0:
				res = self.do_insert_into(sql)
			elif sql.find("create table")==0:
				res= self.do_createtable(sql)
			elif sql.find("delete")==0:
				res= self.do_delete_data(sql)
			elif sql.find("begin")==0:
				res = self.do_batch_sql(sql)
			elif sql.find("alter meta")==0:
				res = self.do_alter_meta(sql)
			elif sql.find("get meta")==0:
				res = self.do_get_meta(sql)			
			elif sql.find("show nodes")==0:#add by 20150326
				res = self.do_show_fun(self.es.cat.nodes,['host','ip','heap.percent','ram.percent','load','node.role','master,name','disk.avail'])			
			elif sql.find("show thread_pool")==0:#add by 20150326
				res = self.do_show_fun(self.es.cat.thread_pool)			
			elif sql.find("show cluster")==0:#add by 20150326
				res = self.do_show_fun(self.es.cat.health)
			elif sql.find("show tasks")==0:#add by 20150326
				res = self.do_show_fun(self.es.cat.tasks)
			elif sql.find("show version")==0:
				res = self.do_show_version(sql)
			elif sql.find("update")==0:
				res = self.do_update_data(sql)
			elif sql.find("bulk into")==0:
				res = self.do_bulk_into(sql)
			elif sql.find("union all")>0:
				res = self.do_union_all(sql)			
			elif sql.find("create view")>=0:#add by gjw 20150402
				res = self.do_create_view_from(sql)
			elif sql.find("show views")>=0:
				res = self.do_show_views(sql)
			elif sql.find("drop view")>=0:
				res = self.do_drop_view(sql)
			else:
				res["msg"]="not support the SQL!"
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			
		res["took"] = int((time.time()-b0)*1000)
		res["cost"] = res["took"]
		return res
	
	#add by gjw on 2014-08-19
	def do_batch_sql(self,sql):
		sql = sql[len("begin"):]
		sqls = sql.split(";")
		res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		for sql in sqls:
			if sql.find("end")>=0:
				break;
			res = self.do_sql(sql)
			if res["msg"] !="":
				res["msg"] = sql +res["msg"]
				break;
		return res
		
	#add by gjw on 20141011
	def do_union_all(self,sql):
		sqls = sql.split("union all")
		res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		for qsql in sqls:
			result = self.esql_query.do_sql(qsql.strip())
			res["result"] += result["result"]
		
		res["count"]=len(res["result"])
		return res
	
	
	#add by gjw on 20150403
	def do_reload(self):
		res={"type":"ddl","count":0,"took":0,"result":[],"msg":"reload ok"}
		
		os.kill(os.getppid(),signal.SIGHUP)
		
		return res
		
		
	#add by gjw on 20141118 
	def do_in_child_query(self,sql):
		b0 = time.time()		
		p_in = sql.find(" in ")		
		sql2 = sql[p_in:]
		a1= sql2.find("(")
		e1 = sql2.find(")")
		in_sql = sql2[a1+1:e1]
		
		res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		try:
			res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
			#exec child query
			result = self.do_sql2(in_sql+" limit 1000")
			
			# such as : select ZJHM from 
			# len(select ) =7
			field =  in_sql[7 : 7+in_sql[7:].find(" ")]
			
			in_res=""
			for r in result["result"]:
				in_res += "%s,"%(r[field])

			fsql = sql[:p_in+a1+1]+in_res+sql[p_in+e1:]
			#print fsql
					
			result = self.do_sql2(fsql)		
			result["took"] = int((time.time()-b0)*1000)
			result["cost"] = result["took"]
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res
			
	#add by gjw on 20141124
	def do_join_on(self,sql):
		b0 = time.time()		
		try:
			res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
			
			join_sqls = sql.split(" join ")
			
			dfs={}
			df = None
			for join_sql in join_sqls:
				a1 = join_sql.find(" as ")
				real_sql = join_sql[:a1]
				o1 = join_sql.find(" on ")
				if o1 ==-1:
					df_label = join_sql[a1+4:].strip()
				else:
					df_label = join_sql[a1+4:o1].strip()
					on_sql = join_sql[o1+4:].strip()
					key={}
					ons = on_sql.split("=")
					for on_words in ons:
						on_words = on_words.split(".")
						key[on_words[0].strip()]=on_words[1].strip()
						if on_words[0].strip() != df_label:
							other_key = on_words[0].strip()
					print(key)
					print(df_label, other_key)
				
				#exec query
				result = self.do_sql2(real_sql+" limit 100000") # modify by gjw on 20141211
				dfs[df_label] = pd.DataFrame(result["result"])
				
				if o1==-1:
					df = dfs[df_label]
				else:
					df = pd.merge(df,dfs[df_label],
					left_on=key[other_key] ,right_on=key[df_label],
					suffixes=("."+other_key,"."+df_label),how="inner")
			
			#transmit the final resut
			s = df.count()
			m2=[]
			for a in df.values:
				d={}
				i=0
				for j in a:
					if type(j)==float and j.__str__()=="nan":
						j=""
					d[df.columns[i]]=j
					i +=1
				m2.append(d)
			result["result"]= m2
			result["count"] = len(m2)
			result["took"] = int((time.time()-b0)*1000)
			result["cost"] = result["took"]
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res	

	#add by gjw on 20150313
	def do_show_meminfo(self,sql):
		b0 = time.time()		
		try:
			res={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		
			#exec query with segments memory
			result = self.do_show_segments("show segments",show_all=True) 
			logger.info(result)
			if result["count"]==0:
				return res
			seg_info= pd.DataFrame(result["result"][:-1])
			
			ip_group = seg_info.groupby("ip",as_index=True).sum()
			#the segment memory,docs.count,docs.deleted
			seg_mems = ip_group.loc[:,["docs.count","docs.deleted","size.memory"]]
			
			#the segment count
			seg_count = seg_info.groupby("ip",as_index=True).size()
			seg_mems["segment.count"] = seg_count
			
			#the segment sotresize
			seg_size={}
			for ip,seg_sizes in seg_info.groupby("ip",as_index=True)["size"]:
				gb_sum=0.0
				for a in seg_sizes:
					gb_sum += to_gb(a)
					#print gb_sum,to_gb(a)
				seg_size[ip]="%.1fgb"%(gb_sum)

			seg_mems["segment.size"] = pd.Series(seg_size)
			
			#ecec query with fielddata memory
			result = self.do_sql("show fielddata")
			fielddata = pd.DataFrame(result["result"])
			field_mems = fielddata.loc[:,["_parent","ip","total"]]
			
			df = seg_mems.merge(field_mems, left_index=True,right_on="ip")
			
			df = df.rename(columns={"_parent" : "parent","total":"fielddata",
					"size.memory":"segment.memory"})
			
			df1 = df["segment.memory"].map(memsize_to_unit)
			
			df = df.drop("segment.memory",axis=1)
			df["segment.memory"]=df1
			
			total_dict={}
			for row_index, row in df.iterrows():
				#print row_index,row["parent"],row["fielddata"],row["segment.memory2"]
				total_dict[row_index]= sum_memsize(row["parent"],row["fielddata"],row["segment.memory"])
			
			df["total"] = pd.Series(total_dict)
			
			#transmit the final resut
			m2=[]
			for a in df.values:
				d={}
				i=0
				for j in a:
					if type(j)==float and j.__str__()=="nan":
						j=""
					d[df.columns[i]]=j
					i +=1
				m2.append(d)
			result["result"]= m2
			result["count"] = len(m2)
			result["took"] = int((time.time()-b0)*1000)
			result["cost"] = result["took"]
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res	
	
	
			
	#add by gjw on 20141202 
	def do_fast_join(self,sql):
		b0 = time.time()		
		try:
			res={"type":"query","count":0,"took":0,"result":[],"msg":""}
			
			join_sqls = sql.split(" fastjoin ")
			body={
				 "query":{
					"bool": {
					"must":[],
					"must_not":[],
					"should":[],
					}
				}
			}
			self.query.parse_sql(join_sqls[0])
			
			for join_sql in join_sqls[1:]:
				words = join_sql.split(" where ")
				doc_type = words[0].strip()
				cond = words[1].strip()
				sql_tree={}
				self.parse_where(cond,sql_tree)
				cq_body = build_haschild_query(doc_type,sql_tree)
				body["query"]["bool"]["must"].append(cq_body)
			
			#add by qs on 20150615
			sql_tree = self.query.parse_sql(join_sqls[0])
			if sql_tree["where"] == None:
				sql_tree["where"]={"must":[],"should":[]}
			build_query_body(body,sql_tree)
			
			#print body

			res = self.query.query_search(body)
			result={"type":"query","count":0,"took":0,"result":[],"msg":""}
			result["count"]=res['hits']['total']
			result["took"] = res['took']
			result["result"] = self.query.transfor_hits(res['hits']['hits'])
			result["cost"] = int((time.time()-b0)*1000)
			logger.info("return result count=%s,took=%sms,cost=%sms "
				%(result["count"],result["took"],result["cost"]))
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res		
	

	#add by qs on 20150525
	def do_inside_query(self,sql):
		b0 = time.time()		
		try:
			res={"type":"query","count":0,"took":0,"result":[],"msg":""}
			
			join_sqls = sql.split(" insideq ")
			body={
				 "query":{
					"bool": {
					"must":[],
					"must_not":[],
					"should":[],
					}
				}
			}
			
			n_fields = []
			for join_sql in join_sqls[1:]:
				words = join_sql.split(" where ")
				field = words[0].strip()
				cond = words[1].strip()
				sql_tree={}
				self.parse_where(cond,sql_tree)
				cq_body = build_nested_query(field,sql_tree)
				body["query"]["bool"]["must"].append(cq_body)
				n_fields.append(field)
			
			sql_tree = self.query.parse_sql(join_sqls[0])

			#add by qs on 20150602 
			if sql_tree["where"] == None:
				sql_tree["where"]={"must":[],"should":[]}
			
			build_query_body(body,sql_tree)

			build_nested_highlight(body)
			
			#print body
			
			res = self.query.query_search(body)
			result={"type":"query","count":0,"took":0,"result":[],"msg":""}
			result["count"]=res['hits']['total']
			result["took"] = res['took']
			result["result"] = self.query.transfor_hits(res['hits']['hits'])
			result["cost"] = int((time.time()-b0)*1000)
			logger.info("return result count=%s,took=%sms,cost=%sms "
				%(result["count"],result["took"],result["cost"]))
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res

	#add by gjw on 20200812
	"""
	create table mytest4 (
	name keyword {"fields":{"text": {"type": "text", "norms": false}}},
	age long,
	bri date) with 5,1
	
	create table my (name keyword {"ignore_above": 1024},age long, bri date {"format" : "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"}) with 5,1

	"""
	def do_createtable(self,sql):
		#sql: create table tname with 10,1
		sql =sql[len("create table"):]
		
		opts = sql.split("(")
		index_name = opts[0].strip()
		res={}
		result={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		
		words = opts[1].split("with")
		try:
			# deal the setttings
			if len(words)==1:
				body={"settings" : {
				"number_of_shards" : 5,
				"number_of_replicas" : 0}
				}
			else:
				a = words[1].split(",")
				body={"settings" : {
				"number_of_shards" : int(a[0].strip()),
				"number_of_replicas" : int(a[1].strip())}
				}
				
			sql_body = words[0].replace(")","") 
			
			#add by gjw on 20200812 处理新的建表语法的问题
			fields = trans_ct_sql(sql_body)
			body["mappings"]={}
			body["mappings"]["properties"]={}
			for item in fields:
				a = re.split("\s+",item)
				a = list_remove(a,"")
				if len(a)==0 :continue
				field_name = a[0].strip()
				if field_name.find(".") >0: # 递归处理各个字段
					fs = field_name.split(".")
					map_build_fields(body["mappings"]["properties"],fs[0],\
					".".join(fs[1:]),a)
				else:
					if len(a) ==2:
						body["mappings"]["properties"][field_name]={"type":a[1].strip()}
					elif len(a) >2: #有json
						x = " ".join(a[2:])
						d = json.loads(x.replace("'",'"'))
						d["type"] =a[1].strip()
						body["mappings"]["properties"][field_name]=d
					else:
						raise Exception(" %s 是非法的,不能创建索引%s !" %(item,index_name))
			
			logger.info(str(body))
			
			if index_name.endswith("*"):#创建的是模板
				body["index_patterns"]=[index_name]
				res = self.es.indices.put_template(name=index_name[:-1],body=body,create=True)
				res = self.es.indices.create(index="%s-0"%(index_name[:-1]),ignore=400,wait_for_active_shards=0)
			else:
				res = self.es.indices.create(index=index_name,body=body,ignore=400,wait_for_active_shards=0)
		except  Exception as e:
			logger.error(traceback.format_exc())
			logger.error(e)
			result["msg"] ="%s"%e;
		result["result"] = [res]
		return result
	
	
	def do_droptable(self,sql):
		l=sql[len("drop table"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			for a in l:
				#index_type = a.split(".")
				#if len(index_type)==2:
				#	res = self.es.indices.delete_mapping(index=index_type[0].strip(),doc_type=index_type[1].strip(),ignore=[400, 404])
				#else:
				res = self.es.indices.delete(index=a.strip(),ignore=[400, 404])
			
			result["result"] = [res]
		except  Exception as e:
			logger.error(traceback.format_exc())
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20150402
	def do_drop_view(self,sql):
		l=sql[len("drop view"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			for a in l:
				res = self.do_sql("show views with %s"%(a.strip()))
				indexs = res["result"][0]["indexs"].split(",")
				res = self.es.indices.delete_alias(index=indexs,name=a.strip())
				
			result["result"] = [res]
		except  Exception as e:
			logger.error(traceback.format_exc())
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20150402
	def do_create_view_from(self,sql):
		sql = sql.replace("from",",")
		a=sql[len("create view "):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.put_alias(index=[i.strip() for i in a[1:]],name=a[0].strip())			
			result["result"] = [res]
		except  Exception as e:
			logger.error(traceback.format_exc())
			result["msg"] ="%s"%e;
		return result
	
	def do_optimize(self,sql):	
		l=sql[len("optimize"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.forcemerge(index=[ i.strip() for i in l],max_num_segments=1)			
			result["result"] = [res["_shards"]]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
			if result["msg"].find("Read timed out") !=-1:
				result["msg"]=""
		return result
	
	
	def do_readonly(self,sql):	
		l=sql[len("readonly"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.put_settings(index=[ i.strip() for i in l],body={"index.blocks.read_only_allow_delete":True})
			result["result"] = [res.__str__()]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
			if result["msg"].find("Read timed out") !=-1:
				result["msg"]=""
		return result
	
	
	def do_get_settings(self,sql):	
		l=sql[len("get_settings"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.get_settings(index=[ i.strip() for i in l])
			for k,v in res.items():
				result["result"].append([k,v["settings"].__str__()])
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
			if result["msg"].find("Read timed out") !=-1:
				result["msg"]=""
		return result
	
		
	def do_flush(self,sql):	
		l=sql[len("flush"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.flush(index=[ i.strip() for i in l])			
			result["result"] = [res["_shards"]]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
		
	def do_clear_cache(self,sql):	
		l=sql[len("clear cache"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.clear_cache(index=[ i.strip() for i in l])			
			result["result"] = [res["_shards"]]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20140730
	def do_desctable(self,sql):
		l=sql[len("desc"):]
		
		index = l.strip()
		
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.get(index=index)
			try:
				#取第一个元素对应的key
				if index not in res: 
					index = list(res.keys())[0]
				mappings = res[index]["mappings"]
			except:
				raise Exception("%s or it's mappings info not found !"%(index))
			#重构字段列表
			d={}
			for k,v in mappings["properties"].items(): 
				if "properties" in v:
					map_properties(d,k,v)
				else:
					v_copy = v.copy()
					if "type" in v : del v_copy["type"]
					d[k] = {"name":k,"type":v["type"],"x": str(v_copy)}
			
			for k,v in d.items():
				result["result"].append(v)
			result["count"] = len(result["result"])
		except  Exception as e:
			logger.error(traceback.format_exc())
			result["msg"] ="%s"%e;
		return result
		
		#add by gjw on 20140730
		#insert into table.doc_type （_id:111,name:"dddd",）
	def do_insert_into(self,sql):
		try:
			result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
			
			#add by gjw on 20140806 
			sql = sql.replace("\,","`")
			
			#modify the gjw on 20150505
			b = len("insert into")
			
			l=sql.find("(")
			index_name = sql[b:l].strip()

			kvs = sql[l+1:-1]
			
			fields =  kvs.split(",")
			id = None
			b={}
			_parent=None
			#add by gjw on 20140911
			for field  in fields:
				p = field.find("=")
				if p<0:
					continue
				k_v=[field[0:p],field[p+1:]]

				if k_v[0].strip()=="_id":
					id = k_v[1].strip()
					continue;
				if k_v[0].strip()=="_parent":
					_parent = k_v[1].strip()
					continue;
				
				try:
					b[k_v[0].strip()] = int(k_v[1].strip());
				except:
					try:
						b[k_v[0].strip()] = float(k_v[1].strip());
					except:
						#字符串 modify by gjw on 20200801
						string_s= k_v[1].replace("`",",").replace('"',"").strip();
						if (string_s[0]=="'" and string_s[-1]=="'") or (string_s[0]=='"' and string_s[-1]=='"'):
							string_s = string_s[1:-1]
						b[k_v[0].strip()] = string_s
			
			if _parent !=None:
				res = self.es.index(index=index_name,doc_type="_doc",body= b,id=id, parent= _parent )
			else:
				res = self.es.index(index=index_name,doc_type="_doc",body= b,id=id )

			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
		
		#add by gjw on 20140827
		#alter meta table.doc_type （fileld_name:中文,）
	def do_alter_meta(self,sql):
		try:
			result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}			

			l=sql[len("alter meta"):].split("(")
			index_type = l[0].strip().split(".")
			
			if len(index_type) <2:
				index_type.append("_type") # default the type is the base
				
			kvs = l[1].replace(")","")
			fields =  kvs.split(",")
			a=[]
			index = index_type[0].strip()
			doc_type = index_type[1].strip()
			#add by gjw on 20140906 
			if doc_type=="_self": #sample: alter meta vehicle_type._self(车大表)
				doc={
					'index': index,
					'type': doc_type,
					"field": index,
					'zh': fields[0].strip(),
					"cc": fields[1].strip(),
					'timestamp': datetime.today(),
					'timestamp2':time.time(),
					}
				res = self.es.index(index="sys_meta",doc_type="base",body=doc,id="%s:%s:%s"%(index,doc_type,index))
			else:
				#add by gjw
				if doc_type !="_type":
					desc_ret = self.do_sql("desc %s.%s"%(index,doc_type));
					field_types = {}
					for r in desc_ret["result"]:
						field_types[r["field"]] =r["type"] 

					for field  in fields:
						k_v = field.split("=")
						b={ "index" : { "_index" : "sys_meta", "_type" : "base", "_id" :"%s:%s:%s"%(index,doc_type,k_v[0].strip())}}
						doc={
						'index': index,
						'type': doc_type,
						"field": k_v[0].strip(),
						'zh': k_v[1].strip(),
						'cc': field_types[k_v[0].strip()],
						'timestamp': datetime.today(),
						'timestamp2':time.time(),
						}
						a.append(b)
						a.append(doc)
				else:
					for field  in fields:
						k_v = field.split("=")
						b={ "index" : { "_index" : "sys_meta", "_type" : "base", "_id" :"%s:%s:%s"%(index,doc_type,k_v[0].strip())}}
						doc={
						'index': index,
						'type': doc_type,
						"field": k_v[0].strip(),
						'zh': k_v[1].strip(),
						'timestamp': datetime.today(),
						'timestamp2':time.time(),
						}
						a.append(b)
						a.append(doc)
				res = self.es.bulk(body= a)
			self.es.indices.flush(index="sys_meta")	
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20140827
	def do_get_meta(self,sql):
		l=sql[len("get meta"):].split(".")
		if len(l) <2:
			l.append("_type") # default the type is the base
			
		index_name = l[0].strip()
		
		#add by gjw on 20150402 check the index is exist
		#update by qs on 20150623,get meta * 
		if index_name!="*":
			#print self.es.indices.exists_alias(name=index_name)
			if  self.es.indices.exists_alias(name=index_name):
				res = self.do_show_views("show views with %s" %(index_name))
				if res["count"] >0:
					index_name  =res["result"][0]["indexs"].split(",")[0]
		
		doc_type = l[1].strip()
				
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			if index_name=="*": #add by gjw on 20140916
				sql = 'select field,zh,cc from sys_meta where type=_self limit 5120'
			elif index_name== "all_indexs": #add by gjw on 20141016
				sql = 'select field,zh from sys_meta where type=_self and cc="index" limit 5120'
			elif index_name== "all_tables": #add by gjw on 20141016
				sql = 'select field,zh from sys_meta where type=_self and cc ="table" or cc=null limit 5120'				
			else:
				sql = 'select field,zh,cc from sys_meta where index="%s" and type="%s" limit 5120'%(index_name,doc_type)
			
			res = self.esql_query.do_sql(sql); 
			for r in res["result"]:
				r.pop("_id")
				r.pop("_index")
				r.pop("_type")
			result["result"] = res["result"]
			result["count"] = len(result["result"])
			
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20140730
	#delete  table.doc_type  where _id=
	def do_delete_data(self,sql):
		try:
			result={"type":"ddl","count":1,"took":20,"result":[],"msg":""}
			
			l=sql[len("delete"):].split("where")
			index_type = l[0].strip()
			
			#add by gjw 20140919 deal the _id
			n =sql.find(" _id") 
			if n>0:			
				id = 0
				k_v = l[1].split("=")
				if k_v[0].strip()=="_id":
					id = k_v[1].strip()			
				
				res = self.es.delete(index=index_type,doc_type="_doc",id=id )
			else:
				sql_tree={}
				self.parse_where(l[1],sql_tree)
				body={
				 "query":{
					"bool": {
					"must":[],
					"must_not":[],
					"should":[],
					}
					}
				}				
				body = build_query_body(body,sql_tree)
				res = self.es.delete_by_query(index=index_type,doc_type="_doc",body=body )
				
			#end if
			
			self.es.indices.flush(index=index_type)
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20140929
	def parse_where(self,where_cond,sql_tree):
		sql_tree["where"]={}
		#先解析and
		sql_tree["where"]["must"]=where_cond.split(" and ")
		#print sql_tree["where"]["must"]
		sql_tree["where"]["should"]=[]
		del_must=[]
		#parser or word 
		for must in sql_tree["where"]["must"]:
			b =must.split(" or ")
			if len(b) >=2:
				#del by gjw 20140801
				#sql_tree["where"]["must"].append(b[0])
				for or_cond in b:
					sql_tree["where"]["should"].append(or_cond)
				del_must.append(must)
		for must in del_must:
			sql_tree["where"]["must"].remove(must)	
	
	#add by gjw on 20140903
	#update  table  set f1=v1,f2=v2 where _id=1
	def do_update_data(self,sql):
		try:
			result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
			
			#add by gjw on 20141107
			sql = sql.replace("\,","`")
			n=sql.rfind("where")
			if n == -1:
				result["msg"] ="not find the where condition!";
				return result
				
			s=[sql[len("update"):n],sql[n+5:]]
			
			#add by gjw on 20141108
			n1 = s[0].find("set")
			if n1 == -1:
				esult["msg"] ="update sql not find the set keyword!";
				return result
			
			l = [s[0][:n1],s[0][n1+3:]]
			
			#deal the index and type
			index_type = l[0].strip().split(".")
			if len(index_type) <2:
				index_type.append("_doc") # default the type is the base				
			#deal id
			id = 0
			k_v = s[1].split("=")
			if k_v[0].strip()=="_id":
				id = k_v[1].strip()
			else:
				result["msg"] ="not find the _id field, no update!";
				return result
			
			#deal the set
			usql=""
			fv_s = l[1].split(",")
			for field in fv_s:
				p = field.find("=")
				if p<0:
					continue
				f_v=[field[0:p],field[p+1:]]
				
				usql+="ctx._source.%s = \"%s\"; "%(f_v[0].strip(),f_v[1].strip().replace("`",","))
			
			u={"script" : usql}
			print(id,u)
			res = self.es.update(index=index_type[0].strip(),doc_type=index_type[1].strip(), id=id, body=u)
			
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	def do_showtables(self,sql):
		
		w = sql.find("with")
		if  w==-1:
			res = self.es.cat.indices(v=True,bytes="b")
		else:
			l=sql[w+4:].split(",")			
			res = self.es.cat.indices(index=[ i.strip() for i in l],v=True,bytes="b")
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			#print values
			for value in values:
				try:
					d[keys[i]]=int(value)
				except:
					if keys[i] !="index":
						d[keys[i]]=value
					else:
						d["_index"]=value
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		
		#add a sum to result
		d = {"_index":"total","docs.deleted":0,"docs.count":0,"store.size":0,"pri.store.size":0,"pri":0,"rep":0}
		for r in result["result"]:
			try:
				d["docs.deleted"] += r["docs.deleted"]
				d["docs.count"] += r["docs.count"]
				d["store.size"] += r["store.size"]
				d["pri.store.size"] += r["pri.store.size"]
				d["pri"] += r["pri"]
				d["rep"] += r["rep"]
			except:
				pass
		
		result["result"].append(d)
		return result
	#end fun showabels
	
	
	def do_show_segments(self,sql,show_all=False):		
		w = sql.find("with")
		if  w==-1:
			res = self.es.cat.segments(v=True)
		else:
			l=sql[w+4:].split(",")			
			res = self.es.cat.segments(index=[ i.strip() for i in l],v=True)
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			#print values
			for value in values:
				try:
					d[keys[i]]=int(value)
				except:
					d[keys[i]]=value
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		
		#add a sum to result
		d = {"index":"total","docs.deleted":0,"docs.count":0,"size.memory":0,
		"ip":"","prirep":"","segment":"","generation":"","size":"","committed":"",
		"searchable":"", "version":"","compound":""}
		for r in result["result"]:
			try:
				d["docs.deleted"] += r["docs.deleted"]
				d["docs.count"] += r["docs.count"]
				d["size.memory"] += r["size.memory"]
			except:
				pass		
		result["result"].insert(0,d)
		
		if show_all ==False:
			result["result"] = result["result"][:2048]
		return result
	#end fun do_show_segments
	
	
	def do_show_shards(self,sql):		
		w = sql.find("with")
		if  w==-1:
			res = self.es.cat.shards(v=True)
		else:
			l=sql[w+4:].split(",")			
			res = self.es.cat.shards(index=[ i.strip() for i in l],v=True)
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			#print values
			for value in values:
				try:
					d[keys[i]]=value
				except:
					pass
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		return result
	#end fun do_show_shards
	
	def do_show_views(self,sql):		
		w = sql.find("with")
		res={}
		if  w==-1:
			res = self.es.indices.get_alias()
		else:
			l=sql[w+4:].split(",")			
			res = self.es.indices.get_alias(name=[ i.strip() for i in l])

		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		print(res)
		views={}
		for k,v in res.items():
			if "aliases" in v:
				for k1,v1 in v["aliases"].items():
					if k1 in views:
						views[k1].append(k)
					else:
						views[k1]=[k]
		
		for k,v in views.items():
			d={"view_name":k,"indexs":",".join(v)}
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		return result
	#end fun do_show_views
	
	def do_show_recovery(self,sql):		
		w = sql.find("with")
		if  w==-1:
			res = self.es.cat.recovery(v=True)
		else:
			l=sql[w+4:].split(",")			
			res = self.es.cat.recovery(index=[ i.strip() for i in l],v=True)
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			#print values
			for value in values:
				try:
					d[keys[i]]=value
				except:
					pass
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		return result
	#end fun do_show_recovery

	def do_show_fielddata(self,sql):		
	
		res = self.es.cat.fielddata(v=True)
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {"_parent":"0b"}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			for value in values:
				if i==4 and value[-1]!="b":
					d[keys[i-1]] +=value
					continue
				try:
					d[keys[i]]=value
				except:
					pass
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])	
		return result
	#end fun do_show_recovery


	def do_show_fun(self,fun,h=None):
		if (h != None):
			res = fun(v=True,h=h)
		else:
			res = fun(v=True)
		
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		lines = res.split("\n")
		lines = list_remove(lines, "")
		keys = lines[0].split(" ")
		keys = list_remove(keys, "")
		#print keys
		for line in lines[1:]:
			d = {}
			i=0
			values = line.split(" ")
			values = list_remove(values, "")
			#print values
			for value in values:
				d[keys[i]]=value
				i +=1			
			result["result"].append(d)
			
		result["count"] = len(result["result"])
		return result
	#end fun do_show_nodes
	
	def do_show_version(self,sql):
		#transfor the result
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		
		ret = self.es.info()
		result["result"].append(ret["version"])
		result["count"] = len(result["result"])
		return result
	#end fun 
	
	#add by gjw on 20150315
	def do_show_cpuinfo(self,sql):
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		
		result["count"] = len(result["result"])
		return result
	#end fun do_show_nodes
	
	def do_bulk_into(self,sql):
		try:
			result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
			
			s=sql[len("bulk into "):]
			u=json.loads(s)
			res = self.es.bulk(body=u)
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	#end fun do_show_nodes




#end class ESql_ddl

"""
@add by gjw  on 20140706
 add the get by id case
 
@add by gjw on 20140707
 add the  doc_type query ,sample flow:
 select * from index.doc_type
 select * from index.doc_type1.doc_type2
 
@add by gjw on 20140709
	change the id to _id, smaple flow:
	select * from car2012 where _id=2000001010
"""

class ESql_query():
	"""
	处理select语句
	"""
	def __init__(self,es):
		self.es = es
		self.result={"type":"query","count":0,"took":0,"cost":0,"result":[],"msg":""}
		#the limit default seting
		self.begin=0
		self.size=10
		self.d2s=[]
		
	"""
	执行SQL
	"""
	def do_sql(self,sql):
		#print sql
		sql = sql.strip()
		b0 = time.time()
		self.begin=0
		self.size=10
		try:
			self.sql_tree = self.parse_sql(sql)
		except  Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s the SQL can't parse !"%(sql)
			return self.result
		
		try:
			res=[]
			if self.sql_tree["type"]=="get":
				res = self.get_id()
			elif self.sql_tree["type"]=="select":
				res =self.do_select()
			elif self.sql_tree["type"]=="scan":
				res= self.do_scan()
			else:
				pass
			res["cost"] = int((time.time()-b0)*1000)
			logger.info("return result count=%s,took=%sms,cost=%sms "%(res["count"],res["took"],res["cost"]))
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"] ="SQL exec has error with %s"%e;
			return self.result	
		return res
	

	#update by qs on 20160106		
	def do_select(self):
		result={"type":"query","count":0,"took":0,"result":[],"msg":""}
		
		if self.sql_tree["where"] == None:
			body = {"query": {"match_all": {}}}
			res =  self.matchall_search()
		else:
			body = self.build_body()
			res =  self.query_search(body)
		result["took"] = res["took"]
		result["result"] = self.transfor_hits(res['hits']['hits'])
		if "count" in res:
			result["count"]=res["count"]
		else:
			result["count"] = len(result["result"])
		return result



	#add by gjw on 20140718
	def transfor_hits(self,hits):
		a=[]
		
		#add by gjw on 20141015
		dist = "".join(self.sql_tree["distinct"])
		dist_fields = dist.split(",")
		dict_dist = {}
		
		for b in hits:
			d={"_index":b["_index"],
			"_id":b["_id"],
			}			
			for (k,v) in list(b["_source"].items()):
				#add on 20140724
				if type(v) is list or type(v) is tuple:
					d[k]=json.dumps(v,ensure_ascii=False)
				elif type(v) is dict :
					for k1,v1 in v.items():
						self.build_dict(d,"%s.%s"%(k,k1),v1)
				else:
					d[k] = datetime.fromtimestamp(v/1000).isoformat()[:-3] if k in self.d2s else v
				
					
			if "fields" in b:
				for (k,v) in list(b["fields"].items()):
					#add on 20140724
					d[k] = v[0]
				
			if "highlight" in b:
				for (k,v) in list(b["highlight"].items()):
					d["HL_"+k]=v[0]
			
			#add by gjw on 20141015
			if dist !="":
				try:
					key = "".join(map(d.get,dist_fields))
					#md5_key = hashlib.md5(key).hexdigest()
				except:
					a.append(d)
					continue;
						
				if key not in dict_dist:
					dict_dist[key]=1
					a.append(d)
			else:			
				a.append(d)
		return a
		
	#add by gjw on 20140721 get is one result
	def transfor_get(self,b):
		a=[]
		d={"_index":b["_index"],
		"_id":b["_id"],
		}			
		for (k,v) in list(b["_source"].items()):
			#add on 20140724
			if type(v) is list or type(v) is tuple:
				d[k]=json.dumps(v,ensure_ascii=False)
			elif type(v) is dict :
				for k1,v1 in v.items():
					self.build_dict(d,"%s.%s"%(k,k1),v1)
			else:
				d[k] = datetime.fromtimestamp(v/1000).isoformat()[:-3] if k in self.d2s else v
		a.append(d)
		return a
	
	def build_dict(self,d,k,v):
		if type(v) is list or type(v) is tuple:
			d[k]=json.dumps(v,ensure_ascii=False)
		elif type(v) is dict :
			for k1,v1 in v.items():
				self.build_dict(d,"%s.%s"%(k,k1),v1)
		else:
			d[k] = datetime.fromtimestamp(v/1000).isoformat()[:-3] if k in self.d2s else v
	
	def get_id(self):
		result={"type":"query","count":0,"took":1,"result":[],"msg":""}
		res = self.es.get(index= self.tables, id=self.sql_tree["get_id"], _source=self.fields,doc_type="_doc")
		result["count"]=1
		result["result"]=self.transfor_get(res)
		return result

		
	def do_scan(self):
		self.scan_options={"size":1000000,"routing":None}
		
		result={"type":"query","count":0,"took":0,"cost":0,"result":[],"msg":""}
		#print self.sql_tree["with"]
		
		
		if len(self.sql_tree["with"]) >0:
			opt = " ".join(self.sql_tree["with"])			
			a = opt.split(" and ")
			for o in a:
				options=o.split("=")
				self.scan_options[options[0].strip()]= int(options[1].strip()) 
		
		if self.sql_tree["where"] == None:
			body = {"query": {"match_all": {}}}
			
		else:
			body = self.build_body()
			
		res2 = self.es.count(request_timeout=100,index=self.tables,body=body,ignore_unavailable=True)
		if res2["count"] >self.scan_options["size"]:
			raise Exception("scan行数[%s]超过限制[%s],请加入条件或增大size设置！"%(res2["count"],self.scan_options["size"]))
		res =  helpers.scan(self.es, query=body, index = self.tables,doc_type="_doc", _source=self.fields,ignore_unavailable=True)
		
		#最后的结果
		a=[]
		for d in res:
			a.append(d)
			
		result["result"]=self.transfor_hits(a)
		result["count"]=len(result["result"])
		return result
	
	def do_scroll(self):
		"""
		 sql sample :
		 "scan from c2NhbjsxOzE0Mjg1NDpOenc2TTJMMVN5cVpVcXREanppV0F3OzE7dG90YWxfaGl0czoyNjI7"
		"""
		#最后的结果
		result={"type":"query","count":0,"took":0,"cost":0,"result":[],"msg":""}
		try:
			res = self.es.scroll(scroll_id=self.sql_tree["from"][0].strip(),scroll="10m")		
		except:
			#add by gjw on 20161124 scroll出错再取一次，仍出错则返回-1
			try:
				res = self.es.scroll(scroll_id=self.sql_tree["from"][0].strip(),scroll="10m")	
			except Exception as e:
				logger.error(traceback.format_exc())
				result["count"] == -1
				return result
		
		result["count"]=len(res['hits']['hits'])
		result["took"] = res['took']
		result["id"] = res["_scroll_id"]
		result["result"] = self.transfor_hits(res['hits']['hits'])		
		return result	


	#update by qs on 20160106	
	def matchall_search(self):	
		#modify by gjw on 20200726
		res = self.es.search(request_timeout=100,index=self.tables, body={"query": {"match_all": {}}},\
					from_=self.begin,size=self.size,_source=self.fields,sort=self.sql_tree["order"],ignore_unavailable=True)
		res2 = self.es.count(request_timeout=100,index=self.tables,body={"query": {"match_all": {}}},ignore_unavailable=True)
		res["count"] = res2["count"]
		return res
	
	"""
	def matchall_scan(self):
		if  self.scan_options["routing"] ==None:	
			res = self.es.search(request_timeout=100,index=self.tables, doc_type=self.doc_types , body={"query": {"match_all": {}}},size=self.scan_options["size"], search_type="scan",scroll="1m", _source=self.fields)
			#res = self.es.search(request_timeout=100,index=self.tables,  body={"query": {"match_all": {}}},size=self.scan_options["size"],scroll="10m", _source=self.fields)
		else:
			res = self.es.search(request_timeout=100,index=self.tables, doc_type=self.doc_types ,body={"query": {"match_all": {}}},size=self.scan_options["size"], preference="_shards:%s"%(self.scan_options["routing"]),search_type="scan", scroll="1m", _source=self.fields)
		
		return res
	"""
	
	def build_body(self):
		body={
			 "query":{
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				},
			  },
		}

		if (len(self.doc_types)>=1 and self.doc_types[0]=="ALL"):
			self.doc_types=[] # ALL is []
			return build_parent_child_query_body(body,self.sql_tree)
		
		return build_query_body(body,self.sql_tree)

		
	def query_search(self,body):
		#update by qs 20200730
		res = self.es.search(request_timeout=100, index=self.tables,doc_type=self.doc_types,body=body,from_=self.begin,size=self.size, _source=self.fields, sort=self.sql_tree["order"],ignore_unavailable=True)
		#res = self.es.search(request_timeout=100, index=self.tables,doc_type=self.doc_types ,body=body,from_=self.begin,size=self.size, _source=self.fields,ignore_unavailable=True)
		res2 = self.es.count(request_timeout=100,index=self.tables,body=body,ignore_unavailable=True)
		res["count"] = res2["count"]
		return res
	
	#add by gjw on 20150210 support the ES order by ,but it cost the large memory
	def query_search_order(self,body):
		res = self.es.search(request_timeout=100, index=self.tables,
			doc_type=self.doc_types ,body=body,from_=self.begin,size=self.size,
			_source=self.fields, sort=self.sql_tree["order"],
			ignore_unavailable=True)

		return res
	
	def query_scan(self):
		if  self.scan_options["routing"] ==None:
			res = self.es.search(request_timeout=100, index=self.tables, doc_type=self.doc_types,body=self.build_body(),size=self.scan_options["size"], search_type="scan",scroll="1m", _source=self.fields,ignore_unavailable=True)
		else:
			res = self.es.search(request_timeout=100, index=self.tables,doc_type=self.doc_types ,body=self.build_body(),size=self.scan_options["size"], preference="_shards:%s"%(self.scan_options["routing"]), search_type="scan",scroll="1m", _source=self.fields,ignore_unavailable=True)
		return res
	
	"""
	解析SQL
	"""
	def parse_sql(self,sql):
		words = sql.split(" ")
		sql_tree={}
		
		sql_tree["type"]=words[0].strip()
		sql_tree["select"]=[]
		sql_tree["scan"]=[]
		sql_tree["from"]=[]
		sql_tree["limit"]=[]
		sql_tree["with"]=[]
		sql_tree["highlight"]=[]
		sql_tree["where"]=[]
		sql_tree["order"]=[]
		sql_tree["distinct"]=[]
		#add by gjw on 20150305
		sql_tree["score"]=[]
		
		key=""
		#处理 select 和 from 
		for word in words:
			if word=="select":
				key = "select"
			elif word =="scan":
				key = "scan"
			elif word =="from":
				key = "from"
			elif word =="limit":
				key = "limit"
			elif word =="highlight": # add by gjw on 20140721
				key="highlight"
			elif word =="with":
				key = "with"
			elif word =="where":
				key ="where"
			elif word =="order":
				key = "order"
			elif word == "distinct":
				key = "distinct"
			elif word == "score":
				key = "score"
			else:
				if key!="" and word !="":
					sql_tree[key].append(word)
		
		#move in the parse_sql function by gjw on 20141202
		self.sql_tree = sql_tree
		# deal the index
		self.tables = []
		for a in self.sql_tree["from"]:
			for b in a.split(","):
				self.tables.append(b)
		
		
		#add by gjw deal the doc_type
		self.doc_types=[]
		
		#add by gjw on 20171220
		if len(sql_tree["select"])!=0:
			string_fields = "".join(self.sql_tree["select"])		
		#add by gjw on 20160715	
		if len(sql_tree["scan"])!=0:
			string_fields = "".join(self.sql_tree["scan"])
		
		#add by gjw on 20200806 用来处理要转化的字段，d2s
		self.fields = []
		fs = string_fields.split(",")
		for field in fs:
			field = field.strip()
			if field.startswith("d2s("):
				self.d2s.append(field[4:-1])
				self.fields.append(field[4:-1])
			else:
				self.fields.append(field)
		
		#add by gjw 20140919 deal the _id
		n =sql.find(" _id") 
		if n>0:
			sql_tree["type"]="get"
			_ids = sql[n:].split("=")
			sql_tree["get_id"] = _ids[1].strip()
			return sql_tree
		
		#处理where
		#add by gjw 20140721
		where_cond = " ".join(sql_tree["where"])
		#print where_cond
		self.parse_where(where_cond,sql_tree)
		
		#deal the limit
		if len(sql_tree["limit"])>=1:
			a = sql_tree["limit"][0].split(",")
			#modify by gjw 2014/07/07 
			if len(a)>=2:
				# limit 2,100
				self.begin = int(a[0])
				self.size = int(a[1])
			else:
				# limit 100
				self.size = int(a[0])
		
		#deal the order
		if len(sql_tree["order"])>0:
			self.parse_order(sql_tree)
			
		#deal the score on 20150305
		sql_tree["score_by"]=[]
		if len(sql_tree["score"])>0:
			self.parse_score(sql_tree)
		return sql_tree
		
	def parse_where(self,where_cond,sql_tree):
		if len(sql_tree["where"])==0:
			sql_tree["where"]=None #没有where
			#sql_tree["where"]={"must":[],"should":[]}
		else:
			sql_tree["where"]={}
			#先解析and
			sql_tree["where"]["must"]=where_cond.split(" and ")
			#print sql_tree["where"]["must"]
			sql_tree["where"]["should"]=[]
			del_must=[]
			#parser or word 
			for must in sql_tree["where"]["must"]:
				b =must.split(" or ")
				if len(b) >=2:
					#del by gjw 20140801
					#sql_tree["where"]["must"].append(b[0])
					for or_cond in b:
						sql_tree["where"]["should"].append(or_cond)
					del_must.append(must)
			for must in del_must:
				sql_tree["where"]["must"].remove(must)	
			
	#add on 20140725
	def parse_order(self,sql_tree):
		#sql : order by  field , field desc ,field asc 		
		order_sql = " ".join(sql_tree["order"])
		orders = order_sql[len("by "):].split(",")
		a=[]
		b=[] #add by gjw on 20150210
		sql_tree["order2_flag"] = "asc"
		for o in orders:
			fields = o.split(" ")
			fields = list_remove(fields,"")
			if len(fields)==2:
				s ="%s:%s"%( fields[0],fields[1] )
				sql_tree["order2_flag"] = fields[1]
			else:
				s = "%s:asc"%( fields[0] )
			b.append(fields[0])
			a.append(s)
		sql_tree["order"] = a
		sql_tree["order2_fields"] = b 
	#end parse_order
		
	#add on 20150305
	def parse_score(self,sql_tree):
		#sql : order by  field , field desc ,field asc 		
		score_sql = " ".join(sql_tree["score"])
		scores = score_sql[len("by "):].split(",")
		sql_tree["score_by"] = scores
	#end parse_score
	


"""

@add by gjw on 20140707
 add the aggregation support
 sample flow:
 select min(speed) as min_speed from index 
 select count(*) as doc_count from index group by wayid
 select count(*) as doc_count, avg(speed) as avg_speed from index group by wayid direction
 select count(*) as doc_count, avg(speed) as avg_speed from index group by speed[0-100,100-200,300]
 select count(*) as doc_count, avg(speed) as avg_speed from index where xzqh="hangzh" group by speed[0-100,100-200,300]
 
 
@add by gjw on 20140711
  support min,max,sum,avg,count,
  select count(*) as doc_count, avg(speed) as avg_speed ,min(speed) as min_speed from index where UTC between to group by wayid, direction
  count(*) can not write as
  only support group by two field
  support the query and group
 
@add by gjw on 20140712
	support the range,ip_range,histogram,date_histogram buckets 
  
"""
class ESql_aggs():
	"""
	处理aggregations语句
	"""
	def __init__(self,es):
		self.es = es
		self.result={"type":"aggs","count":0,"took":0,"cost":0,"result":[],"msg":""}
		
	"""
	执行SQL
	"""
	def do_sql(self,sql):
		#print sql
		self.b0 = time.time()
		try:
			self.sql_tree = self.parse_sql(sql)
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s the SQL can't parse !"%(sql)
			return self.result
		# self.sql_tree		
		
		#add by gjw deal the doc_type
		self.doc_types=[]
		
		self.tables = self.sql_tree["from"]
		
		#print "parse over!"
		try:
			result= self.do_aggs()
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s the SQL exec has error %s !"%(sql,e)
			return self.result
		
		result["cost"] = int((time.time()-self.b0)*1000)
		logger.info("return result  count=%s, took=%sms, cost=%sms"%(result["count"],result["took"],result["cost"])) #add on 20150210
		return result
		
	def do_aggs(self):
		body = self.build_body()
		if body["aggs"]=={}:
			#求count 
			del body["aggs"]
			res = self.es.count(request_timeout=100,index=self.tables,body=body,ignore_unavailable=True)
		else:
			res = self.es.search(request_timeout=100,index=self.tables,body=body,size=self.size,ignore_unavailable=True,sort=["doc_count: desc"])
			
		#logger.info( res )
		result={"type":"aggs","count":0,"took":0,"cost":0,"result":[],"msg":""}
		result["took"]=int((time.time()-self.b0)*1000)
		result["result"] =[]		
		
		self.result = result
		if "aggregations" in res:
			# add by gjw 20140713 deal the result
			
			if self.sql_tree["group_num"]==0: #add by gjw on 20140924
				r={}
				r1 =  res["aggregations"]
				for s1 in self.sql_tree["select"]:
						r[s1["sname"]] = r1[s1["sname"]]["value"]
				result["result"].append(r)
			
			if self.sql_tree["group_num"]==1:
				for r1 in res["aggregations"][self.sql_tree["group"][0]["agg_name"]]["buckets"]:
					r={}
					r[self.sql_tree["group"][0]["agg_name"]] = r1["key"]
					if "key_as_string" in r1:
						r[self.sql_tree["group"][0]["agg_name"]+"_string"]=r1["key_as_string"]
					r["count"] = r1["doc_count"]
					for s1 in self.sql_tree["select"]:
						r[s1["sname"]] = r1[s1["sname"]]["value"]
					result["result"].append(r)
				
			#have the g2
			if self.sql_tree["group_num"]>=2:
				for r1 in res["aggregations"][self.sql_tree["group"][0]["agg_name"]]["buckets"]:
					r={}
					r[self.sql_tree["group"][0]["agg_name"]] = r1["key"]
					self.transfor_aggs(r1[self.sql_tree["group"][1]["agg_name"]]["buckets"],r,1)
					"""
					for r2 in r1[self.sql_tree["group"][1]["agg_name"]]["buckets"]:
						r={}
						r[self.sql_tree["group"][0]["agg_name"]] = r1["key"]
						if r1.has_key("key_as_string"):
							r[self.sql_tree["group"][0]["agg_name"]+"_string"]=r1["key_as_string"]
						
						r[self.sql_tree["group"][1]["agg_name"]] = r2["key"]
						if r2.has_key("key_as_string"):
							r[self.sql_tree["group"][1]["agg_name"]+"_string"]=r2["key_as_string"]
						
						r["count"] = r2["doc_count"]
						for s1 in self.sql_tree["select"]:
							r[s1["sname"]] = r2[s1["sname"]]["value"]
						result["result"].append(r)
					"""
		else:
			# only have the count add by gjw on 20120721
			if "count" in res:			
				result["result"] =[{"count":res["count"]}]
			else:
				result["result"] =[{"count":-1}]
		#end if 				

		#add by gjw on 20141122 by support the having
		if self.sql_tree["having"] !="":
			#print self.sql_tree["having"]
			m = result["result"]
			dr1 = pd.DataFrame(m).query(self.sql_tree["having"])
			s = dr1.count()
			m2=[]
			for a in dr1.values:
				d={}
				i=0
				for j in a:
					d[dr1.columns[i]]=j
					i +=1
				m2.append(d)
			result["result"]= m2
		
		
		#add by gjw on 20140924
		result["count"] = len(result["result"])
		return result
		
	
	"""
	#add by gjw on 20141229
	aggs = res["aggregations"]
	"""
	def transfor_aggs(self,aggs,rr,n):
		
		if n < self.sql_tree["group_num"]-1:
			
			for agg in aggs:
				rr[self.sql_tree["group"][n]["agg_name"]] = agg["key"]
				if "key_as_string" in agg:
					rr[self.sql_tree["group"][n]["agg_name"]+"_string"]=agg["key_as_string"]
				self.transfor_aggs(agg[self.sql_tree["group"][n+1]["agg_name"]]["buckets"],rr,n+1)
				
		else:
			for r2 in aggs:
				r=copy.copy(rr)
				r[self.sql_tree["group"][n]["agg_name"]] = r2["key"]
				if "key_as_string" in r2:
					r[self.sql_tree["group"][n]["agg_name"]+"_string"]=r2["key_as_string"]
				
				r["count"] = r2["doc_count"]
				for s1 in self.sql_tree["select"]:
					r[s1["sname"]] = r2[s1["sname"]]["value"]
				self.result["result"].append(r)
					
	
	
	def build_body(self):
		body={}
		
		# deal the group with Metrics
		aggs2={}
		for g in self.sql_tree["select"]:
			aggs2[g["sname"]]={g["fun"]:{"field":g["field"]}}
			
		
		# deal the  group with bucket
		aggs_b=[]
		for g in self.sql_tree["group"]:
			
			#modify gjw on 20140730  add agg_name
			if "script" in g:
				o={g["agg_name"]:{g["type"]:{"script":{"inline":g["script"]}}}}
			else:
				o={g["agg_name"]:{g["type"]:{"field":g["field"]}}}
			
			#add by gjw on 20140926
			
			orders = self.sql_tree["order by"].split(" ")
			if len(orders)==1:orders.append("asc")
			
			#add by gjw on 20140723 add the size=0 ,not limit the terms count
			
			if g["type"]=="terms":
				o[g["agg_name"]][g["type"]]["size"]=self.size				
				o[g["agg_name"]][g["type"]]["order"]={orders[0]:orders[1]}
			
			if "ranges" in g: # range can't have the order
				o[g["agg_name"]][g["type"]]["ranges"]=g["ranges"]
			
			if "options" in g: #histogram have hte options
				o[g["agg_name"]][g["type"]]["order"]={orders[0]:orders[1]}
				for (k,v) in g["options"]:
					if g["type"]== "date_histogram" and k=="interval":
						o[g["agg_name"]][g["type"]][k]=v
					else:
						o[g["agg_name"]][g["type"]][k]=int(v)				
			
			aggs_b.append(o)
			
		# end for 
		self.aggs_b = aggs_b
		self.aggs2 = aggs2
		
		#deal the top group
		if len(aggs_b)==0: #no have the group
			body["aggs"] = aggs2
		elif len(aggs_b)==1:
			body["aggs"]=aggs_b[0]
			body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"] = aggs2
		elif len(aggs_b)>=2:
			"""
			#del by gjw on 20141229
			o = aggs_b[0]
			del o[self.sql_tree["group"][0]["agg_name"]][self.sql_tree["group"][0]["type"]]["order"]
			{self.sql_tree["group"][1]["agg_name"]+">"+orders[0]:orders[1]}
			
			body["aggs"]=o
			body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"] = aggs_b[1]
			"""
			self.digui_aggs_codn(body,0)
			#body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"][self.sql_tree["group"][1]["agg_name"]]["aggs"] = aggs2
		
		if self.sql_tree["where"] !=None:
			self.build_qbody(body)
		
		#print "build body over"
		#logger.info(json.dumps(body))
		return body

	#add by gjw on 20141229
	def digui_aggs_codn(self,aggs_codn,n):
		if n < len(self.aggs_b):
			print(n,self.aggs_b[n])
			aggs_codn["aggs"] = self.aggs_b[n]
			self.digui_aggs_codn(aggs_codn["aggs"][self.sql_tree["group"][n]["agg_name"]],n+1)
		else:
			aggs_codn["aggs"] = self.aggs2	
		
	
	def build_qbody(self,body):
		if self.sql_tree["where"]==None: return body
		body["query"]={
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				}
		}
		return build_query_body(body,self.sql_tree)
	#end build_qbody()

	"""
	解析SQL
	select  count(*),  avg(timestamp2) as dd from test-index1 group by ZJHM  having  count >2 order by dd desc size 5000
	"""
	def parse_sql(self,sql):
		sql_tree={}
			
		#select
		select_words = sql[6:sql.index("from")]
		self.parse_select(select_words,sql_tree)
		
		#from
		from_words = sql.split("from")[1].lstrip(" ")
		if from_words.find(" ") == -1:
			sql_tree["from"] = from_words
		else:
			sql_tree["from"] = from_words[:from_words.find(" ")]
		
		#处理where
		where_cond = sql.split("group by")[0].split("where")
		self.parse_where(where_cond,sql_tree)
		
		sql1 = sql
		#add by gjw on 20140730
		#limit
		size = sql.split("limit")
		if len(size)>=2:
			self.size = int(size[1].strip())
			sql1 = size[0].strip()
		else:
			self.size = 10000

		#add by gjw on 20140924
		sql_tree["order by"]="_count desc"
		sort = sql1.split(" order by ")
		if len(sort)>=2:
			sql_tree["order by"]=sort[1].strip()
			sql_tree["order by"] = sql_tree["order by"].replace("count","_count")
			sql1 = sort[0].strip()
			
		#add by gjw support the having on 20141122
		sql_tree["having"]=""
		having = sql1.split(" having ")
		if len(having) >=2:
			sql_tree["having"] = having[1].strip()
			sql_tree["having"] = sql_tree["having"].replace(" ="," ==")
			sql1 = having[0].strip()
			
		#group by, the group by is the sql end
		sql_tree["group"]=[]
		sql_tree["group_num"]=0
		n =sql1.find("group by") 
		if  n>=0:
			#add by gjw on 2014-0924
			group_words = sql1[n+8:]
			self.parse_groupby(group_words,sql_tree)		
		else:
			sql_tree["group"]=[]
		
		#add by gjw on 20150323
		sql_tree["score_by"]=[]
		
		return sql_tree

	def parse_select(self,select_words,sql_tree):
		
		"sampe: count(*), avg(speed) as avg_speed ,min(speed) as min_speed"
		sl = select_words.split(",")
		
		sql_tree["select"]=[]
		for a in sl:
			b = a.replace("(","|").replace(")","|").replace("as","|")
			ff = b.split("|")
			if len(ff) <=2:continue
			f={"fun":ff[0].strip(),"field":ff[1].strip(),"sname":ff[-1].strip()}
			
			if(f["fun"]!="count"): # count default have
				sql_tree["select"].append(f)
		#print sql_tree
		return sql_tree
		
	"""
	@add by gjw on 2014/07/12
	
	"""
	def parse_groupby(self,group_words,sql_tree):
		"""
		group by field[(0-100)(101-200)(200-)] , field2
		group by field.ip_range[(192.168.2.0/24)(192.168.3.0/24)(192.168.4.1-192.168.4.20)]

		"""		
		groups = group_words.split(",")
		
		"""
		#add by gjw on 20200806 多个字段的聚合要采用新的逻辑了，而且只能是普通字段，不能是区间字段
		if len(groups) >=2:
			#"sexprof": {
			#	"terms": {
            #    "script": {
            #        "inline": "doc['SEX.keyword'].value +'-split-'+ doc['PROF.keyword'].value "
            #    }
			#	}
			#}
			a=[]
			for g in groups:
				#item = "String.valueOf(doc['%s'].value) "%(g.strip())
				item = "doc['%s'].value "%(g.strip())
				a.append(item)
			
			sql_tree["group"].append({"agg_name":"mulname","script":"+'--'+".join(a),"type":"terms"})
		else:
		"""
		for g in groups:
			b = g.find("[")
			if b >0:
				g_dict={}
				
				# deal the field and type
				field_type = g[0:b]
				a = field_type.split(".")
				if len(a)==1:
					g_dict["agg_name"] = a[0].strip()
					g_dict["field"] = a[0].strip()
					g_dict["type"] = "range"
				else:
					g_dict["agg_name"] = a[0].strip()
					g_dict["field"] = a[0].strip()
					g_dict["type"]=a[1].strip()
				
				#deal the ranges
				conds = g[b+1:]  # +1 del the [ ;
				conds = conds.replace(" ","")
				
				if g_dict["type"].find("range") >=0:
					# the range type use the ()
					ranges2 = conds.replace("]","").replace(")(","|").replace("(","").replace(")","")
					
					g_dict["ranges"]=[]
					for o in ranges2.split("|"):
						r = o.find("-")
						r_dict={}
						if o[0:r].strip() !="":
							r_dict["from"]= o[0:r].strip()
						if  o[r+1:].strip() !="" :
							r_dict["to"]= o[r+1:].strip()
							
						g_dict["ranges"].append(r_dict)
				else:
					# the histogram type use the {}
					g_dict["options"]=[]
					conds2 = conds.replace("]","").replace("}{","|").replace("{","").replace("}","")
					for o in conds2.split("|"):
						r = o.find(":")
						g_dict["options"].append((o[0:r].strip(),o[r+1:].strip()))					
					
				sql_tree["group"].append(g_dict)
			else: #not found the []
				
				#modify gjw on 20140730
				n = g.strip().find(".")
				if n== -1:
					sql_tree["group"].append({"agg_name":g.strip(),"field":g.strip(),"type":"terms"})
				else:
					sql_tree["group"].append({"agg_name":g.strip()[0:n],"field":g.strip(),"type":"terms"})
				
		#end for
		
		sql_tree["group_num"] = len(sql_tree["group"])
	#end def parse_groupby

	def parse_where(self,where_cond,sql_tree):
		if len(where_cond)==1:
			sql_tree["where"]=None #没有where
		else:
			sql_tree["where"]={}
			#先解析and
			sql_tree["where"]["must"]=where_cond[1].split(" and ")
			#print sql_tree["where"]["must"]
			sql_tree["where"]["should"]=[]
			del_must=[]
			#parser or word 
			for must in sql_tree["where"]["must"]:
				b =must.split(" or ")
				if len(b) >=2:
					#del by gjw on 20140801 
					#sql_tree["where"]["must"].append(b[0])
					for or_cond in b:
						sql_tree["where"]["should"].append(or_cond)
					del_must.append(must)
			for must in del_must:
				sql_tree["where"]["must"].remove(must)	
#end class ESql_agg


if __name__=="__main__":
	
	
	#es = Elasticsearch(cfg.udbserver)

	es = Elasticsearch()
	
	esql = ESql(es)
	"""
	sql0="select * from car201110 "
	sql1="select * from car201110 where _all ='东' highlight _all order by speed , wayid desc"
	sql2="select * from car201110 where base.plateNumber.ngram_min_size7 ='浙G2775*' "
	sql3="select * from car201110 where laneName ='万塘路' and CarColor= '黄色'  and wayid=1 and status=1  limit 0,20"
	sql4="select plateNumber from car201110 where   plateNumber.ngram_min_size7 ='浙G*' and speed  between 50 to 100 limit 0,20"
	sql5="select plateNumber from _all limit 0,10 "
	sql51="select * from car201110 limit 0,10 "
	sql52="select * from car201110,car201109,car201205 limit 0,10 "
	sql6 = "select * from test-index where _parent=tt#1 limit 100"
	sql7 = "select * from test-index.tt where _id =1 "
	sql8 = "select * from test-index.cc where _id =1000 " #has error the routing must spec
	sql9 = "select * from test-index.cc.tt where text =1002 "
	sql10="select * from people where _all =东 highlight _all  " #invalid
	sql11="select * from people where name =东 highlight name  "
	sql12="select * from people where _all =东 highlight name ,kouyin  limit 3"
	sql13="select * from car201110 where _all =东 and speed  between 50 to 100 and  CarColor= '黄色' highlight name ,kouyin  limit 3"
	sql14="select * from car  where _id =2011100000000000003"
	
	sql15 = "select * from car201110 where create_date between 2014-07-21T19:15 to 2014-07-21T19:20"
	asql = "select min(speed) as min_speed from car201110 group by wayid "
	asql1 ="select count(*) from car201110"
	
	asql2 = "select avg(speed) as avg_speed ,min(speed) as min_speed from bb  where UTC between 1404201315 to 1504209315 group by plateColor,wayid,direction"
	asql3 = "select avg(speed) as avg_speed ,min(speed) as min_speed from bb.base where UTC between 1404201315 to 1504209315 group by plateColor,wayid,direction"
	
	asql4 = "select count(*) as min_speed from bb"
	asql5 = "select min( speed ) as min from bb group by passTime"
	asql6= "select min( speed ) as min, max(speed) as mm from car201110 group by speed[  (- 50) (50-1  00) (100-) ] "
	asql7= "select min( speed ) as min from car201110 group by wayid,speed[(0-50)(50-100)(100-)] "
	asql8= "select min( speed ) as min from car201110 group by wayid[(0-2)(2-6)(6-)] ,speed[(0-50)(50-100)(100-)] "
	asql9= "select min( speed ) as min from bb group by speed.ip_range[(192.168.1.1-192.168.1.23)(192.168.1.23-)] "
	asql10= "select count(*) from car201110 group by speed.histogram[{interval:10}{min_doc_count: 80}] "
	asql11= "select count(*) from bb group by passTime.date_histogram[{interval:2h}] "
	asql12= "select avg(speed) as avg_speed ,min(speed) as min_speed  from car201110 group by passTime.date_histogram[ { interval: 2h } {min_doc_count: 10}] ,  speed[(0-50)(50-100)(100-)]"
	
	asql13 = "select count(*), avg(speed) as avg  from bb201211 group by wayid"
	
	asql14 = "select count(*), avg(speed) as avg ,max(speed) as max from bb201211 group by datepart"
	asql15 = "select count(*),sum(docs.count) as sum_total from sys_total where index=total group by timestamp.date_histogram[{interval:2m}"
	
	
	dsql="show tables"
	dsql1 = "show tables with book , bb "
	dsql2 = "optimize bb,car"
	dsql3 = "drop table bb2"
	"""
	dsql4 = "create table bb2 (HPHM string no ,HPHM.kw string no )  with 10,2"
	"""
	sql40= "desc car201111"
	isql = 'insert into table1.doc_type (_id=111,name=dddd,yyy=中图,dd=110100,tt=2014-12-21T12:12:12)'
	isql2 = 'insert into table3.doc_type7 (_id=112,name=dddd,yyy=中图,dd=20141221,tt=2014-12-21,ss=True,ff=12.5)'
	dsql = "delete table1.doc_type where _id=111"
	sql41 = "select * from track_20140506,car201001 where CarColor in (红色,黑色)"
	sql = "select count(*) from car201111 where CarColor.kw in (红色,黑色)  group by CarColor.kw"
	
	
	ntsql  = 'select * from zjl_nested_test insideq lg where lg.ROOM = 1605'
	"""
	bsql = 'bulk into [{ "index" : { "_index" : "test-gjw", "_type" : "pp",  "_id":"1"}},{"name":123,"value":"黑色"},{ "index" : { "_index" : "test-gjw", "_type" : "pp",  "_id":"2"}},{"name":124,"value":"红色"}]'
	
	import sys
	#res = esql.do_sql(sys.argv[1])
	
	#res = esql.do_sql("create table test-gjw.pp (name int no ,value string no ) with 10,1")
	res = esql.do_sql(bsql)
	res = esql.do_sql("show tables")
	print("count:%s took:%s  cost: %s %s"%(res["count"],res["took"], res["cost"],res["msg"]))

	#time.sleep(60)
