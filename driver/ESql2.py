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

"""

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
	fix the 1.9.16 and 1.9.27 bug, and support the  in() group by
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

@add by gjw on 20141217 v2.0.1
	add the qeury safe check
	
	20141219 add the aggs safe check
	
@add by gjw on 20141223 v2.0.2
	add the request_timeout=100

@add by gjw on 20141230 v2.0.3
	change ajax time out 120s

@add by gjw on 20150123 v2.0.6
	see the 1.9.38
	
@modify by gjw on 20160704
修改以嵌入到FEA中

"""

from datetime import datetime
from .elasticsearch import Elasticsearch
import time
import json
import traceback
import copy

import logging
import hashlib

import pandas as pd
import numpy as np

#import redis
from . import cfg
__version__="2.0.6"


# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
from logging.handlers import RotatingFileHandler
#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大10M
fh =  RotatingFileHandler('esql2.log', maxBytes=10*1024*1024,backupCount=3)
#fh = logging.FileHandler('esql.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)


#add by gjw on 20140721
def list_remove(l,b):
	l2 = []
	[l2.append(i) for i in l if i !=b]
	return l2
	
class ESql2():
	"""
	处理select语句
	"""
	def __init__(self,es):
		self.es = es
		self.query = ESql_query(self.es)
		self.aggs = ESql_aggs(self.es)
		self.ddl = ESql_ddl(self.es,self.query,self.aggs)
	
	def do_sql(self,role,sql):
		
		#add 20140722
		sql = sql.replace("\n"," ").replace("\r"," ").replace("\t"," ").strip()
		logger.info( sql )
		
		#add by gjw on 20141118 add the in(select ) query
		if sql.find(" in (select") >0 or sql.find(" in ( select") >0:
			return self.ddl.do_in_child_query(role,sql)
		elif sql.find(" join ") >0 and sql.find(" on ") >0:
			return self.ddl.do_join_on(role,sql)
		#add by gjw on 20141202 support the fast join
		elif sql.find(" fastjoin ") >0:
			return self.ddl.do_fast_join(role,sql)
		elif sql.find("count(*)") >0 or sql.find("group by") >0 or sql.find(" as ") >0:
			return self.aggs.do_sql(role,sql)
		elif sql.find("union all") >0:
			return self.ddl.do_sql(role,sql)
		elif sql.find("select") ==0 or sql.find("scan")==0 or sql.find("scroll")==0:
			return self.query.do_sql(role,sql)
		else:
			return self.ddl.do_sql(role,sql)
	
	#end fun do_sql

def deal_in_not_in(cond,n,l):
	fname = cond[0:n].strip()
	tags = cond[n+l:].replace("(","").replace(")","").split(",")
	tags = [i.replace('"',"").strip() for i in tags]
	return (fname,tags)

def deal_in_not_in2(cond,n,l):
	fname = cond[0:n].strip()
	tags = cond[n+l:].replace("(","").replace(")","").split(",")
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
				
		
		

def build_query_body(body,sql_tree):
	
	#add by gjw on 20141011
	range_conds={}
	
	#deal the and 
	for cond in sql_tree["where"]["must"]:
		#add by gjw on 20140812 support the >= etc
		cond = cond.replace(" >="," gte ").replace(" >"," gt ").replace(" <="," lte ").replace(" <", " lt ")
		
		#modify by gjw on 20140731 deal the in keywork,sample : field in (aa,xx)
		n = cond.find(" not in ")
		if n >0:
			fname,tags = deal_in_not_in(cond,n,len(" not in "))
			body["query"]["bool"]["must_not"].append({"terms":{fname:tags,"minimum_should_match":1}})
		else:
			n = cond.find(" in ")
			if n >0:
				
				fname,tags = deal_in_not_in(cond,n,len(" in "))
				body["query"]["bool"]["must"].append({"terms":{fname:tags,"minimum_should_match":1}})
				
				"""
				fname,tags = deal_in_not_in2(cond,n,len(" in "))
				for tag in tags:
					body["filter"]["bool"]["should"].append({"term":{fname:tag}})
				"""
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
					body["query"]["bool"]["must_not"].append({"query_string":{"default_field":a[0].strip(),"query":a[1].strip()}})
				else:
					a = cond.split("=")
					if len(a) >=2:
						#the case is " key = value"
						#add by 20140929
						value = a[1].strip();
						#add by gjw on 20141105
						if len(value) <=3 and value.find("*")==-1 and value.find("?")==-1 and value.isdigit() ==False :
							value = '"%s"'%(value)
						body["query"]["bool"]["must"].append({"query_string":{"default_field":a[0].strip(),"query":value}})
					else:
						#modify by gjw on 20140904 
						b = cond.find("between")
						if b >0:
							#deal the case "field between 2 to 20"
							field_name = cond[0:b].strip()
							t = cond.find("to")
							b1 = cond[b+len("between"):t].strip()
							b2 = cond[t+len("to"):].strip()

							body["query"]["bool"]["must"].append({ "range": {field_name:{"gte":b1,"lte":b2}}})
						else:
							#add by gjw 2014-08-18 deal the is null or is not null
							n = cond.find("is null")
							if n >0:
								body["query"]["bool"]["must"].append({
										"constant_score" : {
											"filter" : {
												"missing" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
								
							n = cond.find("is not null")
							if  n >0:
								body["query"]["bool"]["must_not"].append({
										"constant_score" : {
											"filter" : {
												"missing" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
							
							for mark in ["gte","gt","lte","lt"]:
								a = cond.split(mark)
								if len(a) >=2:
									#add by gjw on 20141011
									if a[0].strip() in range_conds:
										range_conds[a[0].strip()].append((mark,a[1].strip()))
									else:
										range_conds[a[0].strip()]=[(mark,a[1].strip())]
									break;
	#add by gjw on 20141011
	for k,v in list(range_conds.items()):
		if len(v)==1:
			body["query"]["bool"]["must"].append({ "range": {k:{v[0][0]:v[0][1]}}})
		else:
			body["query"]["bool"]["must"].append({ "range": {k:{v[0][0]:v[0][1],v[1][0]:v[1][1]}}})
					
	#deal the or	
	for cond in sql_tree["where"]["should"]:
		#add by gjw on 20140812 support the >= etc
		cond = cond.replace(" >="," gte ").replace(" >"," gt ").replace(" <="," lte ").replace(" <", " lt ")
		
		#modify by gjw on 20140731 deal the in keywork,sample : field in (aa,xx)
		n = cond.find(" not in ")
		if n >0:
			fname,tags = deal_in_not_in(cond,n,len(" not in "))
			body["query"]["bool"]["must_not"].append({"terms":{fname:tags,"minimum_should_match":1}})
		else:
			n = cond.find(" in ")
			if n >0:
				fname,tags = deal_in_not_in(cond,n,len(" in "))
				body["query"]["bool"]["should"].append({"terms":{fname:tags,"minimum_should_match":1}})
			
			else:
				a = cond.split("!=")
				if len(a) >=2:
					body["query"]["bool"]["must_not"].append({"query_string":{"default_field":a[0].strip(),"query":a[1].strip()}})
				else:
					a = cond.split("=")
					if len(a) >=2:
						#the case is " key = value"
						#add by 20140929
						value = a[1].strip();
						if len(value) <=3 and value.find("*")==-1 and value.find("?")==-1:
							value = '"%s"'%(value)
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
												"missing" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
								
							n = cond.find("is not null")
							if  n >0:
								body["query"]["bool"]["must_not"].append({
										"constant_score" : {
											"filter" : {
												"missing" : { "field" : cond[0:n-1].strip() }
											}
										}
									})
							for mark in ["gte","gt","lte","lt"]:
								a = cond.split(mark)
								if len(a) >=2:
									body["query"]["bool"]["should"].append({ "range": {a[0].strip():{mark:a[1].strip()}}})
									break;
	
	
	#deal the highlight on 20140721
	if "highlight" in sql_tree and  len( sql_tree["highlight"] ) >0:
		h = {"fields":{}}
		for field in sql_tree["highlight"]:
			if field =="" : continue
			h["fields"][field]={}
		body["highlight"]=h
	
	#print body
	return body




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
		
	
	def do_sql(self,role,sql):
		self.role = role
		sql = sql.strip()
		b0 = time.time()
		res = {"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		try:
			if sql.find("show tables") ==0:
				res= self.do_showtables(sql)
			elif sql.find("drop table")==0:
				res= self.do_droptable(sql)
			elif sql.find("optimize")==0:
				res= self.do_optimize(sql)
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
			elif sql.find("show nodes")==0:
				res = self.do_show_nodes(sql)
			elif sql.find("show version")==0:
				res = self.do_show_version(sql)
			elif sql.find("update")==0:
				res = self.do_update_data(sql)
			elif sql.find("bulk into")==0:
				res = self.do_bulk_into(sql)
			elif sql.find("union all")>0:
				res = self.do_union_all(sql)
			else:
				res["msg"]="not support the SQL!"
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			
		res["took"] = int((time.time()-b0)*1000)
		res["cost"] = res["took"]
		return res
		
	def do_sql2(self,role,sql):
		#add 20140722
		sql = sql.replace("\n"," ").replace("\r"," ").replace("\t"," ").strip()
		logger.info( sql )
		
		#add by gjw on 20141118 add the in(select ) query
		if sql.find(" in (select") >0 or sql.find(" in ( select") >0:
			return self.ddl.do_in_child_query(role,sql)
		elif sql.find("count(*)") >0 or sql.find("group by") >0 or sql.find(" as ") >0:
			return self.aggs.do_sql(role,sql)
		elif sql.find("union all") >0:
			return self.ddl.do_sql(role,sql)
		elif sql.find("select") ==0 or sql.find("scan")==0 or sql.find("scroll")==0:
			return self.query.do_sql(role,sql)
		else:
			return self.ddl.do_sql(role,sql)
	
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
	
	#add by gjw on 20141118 
	def do_in_child_query(self,role,sql):
		self.role = role
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
			result = self.do_sql2(self.role,in_sql+" limit 1000")
			
			# such as : select ZJHM from 
			# len(select ) =7
			field =  in_sql[7 : 7+in_sql[7:].find(" ")]
			
			in_res=""
			for r in result["result"]:
				in_res += "%s,"%(r[field])

			fsql = sql[:p_in+a1+1]+in_res+sql[p_in+e1:]
			#print fsql
					
			result = self.do_sql2(self.role,fsql)		
			result["took"] = int((time.time()-b0)*1000)
			result["cost"] = result["took"]
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res
			
	#add by gjw on 20141124
	def do_join_on(self,role,sql):
		self.role = role
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
				result = self.do_sql2(self.role,real_sql+" limit 100000") # modify by gjw on 20141211
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
	def do_fast_join(self,role,sql):
		self.role = role
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
			
			print(body)
			res = self.query.query_search(body)
			result={"type":"query","count":0,"took":0,"result":[],"msg":""}
			result["count"]=res['hits']['total']
			result["took"] = res['took']
			result["result"] = self.query.transfor_hits(res['hits']['hits'])
			result["cost"] = int((time.time()-b0)*1000)
			return result
		except Exception as e:
			logger.error(traceback.format_exc())
			res["msg"] = "SQL exec has error with %s"%(e)
			return res		
	
	def do_createtable(self,sql):
		#sql: create table tname with 10,1
		sql =sql[len("create table"):]
		
		opts = sql.split("(")
		index_type = opts[0].split(".")
		index_name = index_type[0].strip()
		type_name = index_type[1].strip() if len(index_type)==2 else "base"		
		res={}
		result={"type":"ddl","count":0,"took":0,"result":[],"msg":""}
		
		words = opts[1].split("with")
		
		try:
			
			if len(words)==1:		
				res = self.es.indices.create(index=index_name,ignore=400)
			else:
				a = words[1].split(",")
				
				body={"settings" : {
				"number_of_shards" : int(a[0].strip()),
				"number_of_replicas" : int(a[1].strip())
									}
					}				
				res = self.es.indices.create(index=index_name,body=body,ignore=400)
			#end if 
			
			#add by gjw on 20140806 put_mapping
			"""
			field string yes,
			field1.kw string not,
			
			"""
			items = words[0].replace(")","").split(",")
			body = {type_name:{"properties":{}}}
			#print items
			
			for item in items:
				field = item.strip().split(" ")
				#add by gjw on 20150123
				field = list_remove(field,"")
				if len(field) <3: continue;
				field_name = field[0].strip()
				field_sub = field_name.split(".")
				
				#add by gjw on 2014-08-18 sample: _parent type pp
				if field_name == "_parent" :
					body[type_name]["_parent"]={"type":field[2].strip()}
					continue
				
				body[type_name]["properties"][field_sub[0]]={"type":field[1].strip()}
				
				if (len(field_sub)==2):
					body[type_name]["properties"][field_sub[0]]["fields"]={field_sub[1]:{"type":field[1].strip(),"index": "not_analyzed" if field[2].strip()=="yes" else "analyzed"}}
				else:
					body[type_name]["properties"][field_sub[0]]["index"]= "not_analyzed" if field[2].strip()=="yes" else "analyzed"
			print(body)
			res = self.es.indices.put_mapping(index=index_name,doc_type=type_name,body=body)

			
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		result["result"] = [res]
		return result
	
	
	def do_droptable(self,sql):
		l=sql[len("drop table"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			for a in l:
				index_type = a.split(".")
				if len(index_type)==2:
					res = self.es.indices.delete_mapping(index=index_type[0].strip(),doc_type=index_type[1].strip(),ignore=[400, 404])
				else:
					res = self.es.indices.delete(index=index_type[0].strip(),ignore=[400, 404])
			
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	def do_optimize(self,sql):	
		l=sql[len("optimize"):].split(",")
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.optimize(index=[ i.strip() for i in l],max_num_segments=1,wait_for_merge=False)			
			result["result"] = [res["_shards"]]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
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
	
	#add by gjw on 20140730
	def do_desctable(self,sql):
		l=sql[len("desc"):].split(".")
		
		index_name = l[0].strip()
		
		result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
		try:
			res = self.es.indices.get_mapping(index=index_name,doc_type=[ i.strip() for i in l[1:] ] )			
			#print res
			a = res[index_name]["mappings"]
			result["result"]=[]
			
			for k,v in list(a.items()): # atype:properties{}
				for k1,v1 in list(v["properties"].items()):
					d = {"format":"","index":"","store":True}
					d["_type"]=k
					d["field"]= k1
					#sub={}
					for k2,v2 in list(v1.items()):
						"""
						#delete by gjw on 20141016
						if k2=="fields":
							sub = v2
							continue
						"""
						d[k2]=v2	
					if "type" not in d:
						d["type"]="Object"				
					result["result"].append(d)
					# deal the sub type
					"""
					#delete by gjw on 20141016
					for k3,v3 in sub.items(): #
						d = {"format":"","index":"","store":True}
						d["_type"]=k
						d["field"]= k1+"."+k3
						for k4,v4 in v3.items():
							d[k4]=v4
						result["result"].append(d)
					"""
			#print "====================="
			#print result["result"]
						
			result["count"] = len(result["result"])
			
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
		
		#add by gjw on 20140730
		#insert into table.doc_type （_id:111,name:"dddd",）
	def do_insert_into(self,sql):
		try:
			result={"type":"ddl","count":0,"took":20,"result":[],"msg":""}
			
			#add by gjw on 20140806 
			sql = sql.replace("\,","`")
			
			l=sql[len("insert into"):].split("(")
			index_type = l[0].strip().split(".")
			
			if len(index_type) <2:
				index_type.append("base") # default the type is the base
				
			kvs = l[1].replace(")","")
			
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
						b[k_v[0].strip()] = k_v[1].replace("`",",").replace('"',"").strip();
			
			if _parent !=None:
				res = self.es.index(index=index_type[0].strip(),doc_type=index_type[1].strip(),body= b,id=id, parent= _parent )
			else:
				res = self.es.index(index=index_type[0].strip(),doc_type=index_type[1].strip(),body= b,id=id )

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
			
			res = self.esql_query.do_sql(self.role,sql); 
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
			index_type = l[0].strip().split(".")
			if len(index_type) <2:
				index_type.append("base") # default the type is the base				
			
			#add by gjw 20140919 deal the _id
			n =sql.find(" _id") 
			if n>0:			
				id = 0
				k_v = l[1].split("=")
				if k_v[0].strip()=="_id":
					id = k_v[1].strip()			
				
				res = self.es.delete(index=index_type[0].strip(),doc_type=index_type[1].strip(),id=id )
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
				res = self.es.delete_by_query(index=index_type[0].strip(),doc_type=index_type[1].strip(),body=body )
				
			#end if
			
			self.es.indices.flush(index=index_type[0])
			result["result"] = [res]
		except  Exception as e:
			logger.error(e)
			result["msg"] ="%s"%e;
		return result
	
	#add by gjw on 20140929
	def parse_where(self,where_cond,sql_tree):
		sql_tree["where"]={}
		#先解析and
		sql_tree["where"]["must"]=where_cond.split("and")
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
	#update  table.doc_type  set f1=v1,f2=v2 where _id=1
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
				index_type.append("base") # default the type is the base				
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
		
		#add by gjw on v1.9.10 20140916
		res = self.do_sql(self.role,"get meta *")
		meta ={}
		for r in res["result"]:
			meta[r["field"]]=[r["zh"]]
		
		for r in result["result"]:
			try:
				d["docs.deleted"] += r["docs.deleted"]
				d["docs.count"] += r["docs.count"]
				d["store.size"] += r["store.size"]
				d["pri.store.size"] += r["pri.store.size"]
				d["pri"] += r["pri"]
				d["rep"] += r["rep"]
				if r["_index"] in meta:
					r["zh"] = meta[r["_index"]]
				else:
					r["zh"] =""
			except:
				pass
		
		result["result"].append(d)
		return result
	#end fun do_sql
	
	def do_show_nodes(self,sql):
		res = self.es.cat.nodes(v=True)
		
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
			
		result["result"].append({"version":__version__})
			
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
		#self.rdb = redis.Redis(host=cfg.rserver, port=6379, db=1)
	"""
	执行SQL
	"""
	def do_sql(self,role,sql):
		#print sql
		#add by gjw 
		self.role = role
		sql = sql.strip()
		b0 = time.time()
		try:
			self.sql_tree = self.parse_sql(sql)
		except  Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s"%(e)
			return self.result
		#print self.sql_tree
		
		
		try:
			res=[]
			if self.sql_tree["type"]=="get":
				res = self.get_id()
			elif self.sql_tree["type"]=="select":
				res =self.do_select()
			elif self.sql_tree["type"]=="scan":
				res= self.do_scan()
			elif self.sql_tree["type"]=="scroll":
				res= self.do_scroll()
			else:
				pass
			#res["count"]= len(res['result'])
			res["cost"] = int((time.time()-b0)*1000)
			
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"] ="SQL exec has error with %s"%e;
			return self.result	
		return res
			
	def do_select(self):
		
		result={"type":"query","count":0,"took":0,"result":[],"msg":""}
		
		if self.sql_tree["where"] == None:
			res =  self.matchall_search()
		else:
			body = self.build_body()
			res =  self.query_search(body)
		#print res		
		#最后的结果
		result["count"]=res['hits']['total']
		result["took"] = res['took']
		result["result"] = self.transfor_hits(res['hits']['hits'])
				
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
			"_type":b["_type"],
			"_id":b["_id"],
			}			
			for (k,v) in list(b["_source"].items()):
				#add on 20140724
				if type(v) is dict or type(v) is list or type(v) is tuple:
					d[k]=json.dumps(v, ensure_ascii=False)
				else:
					d[k] = v
				
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
		"_type":b["_type"],
		"_id":b["_id"],
		}			
		for (k,v) in list(b["_source"].items()):
			#add on 20140724
			if type(v) is dict or type(v) is list or type(v) is tuple:
				d[k]=json.dumps(v,ensure_ascii=False)
			else:
				d[k] = v
		a.append(d)
		return a
	
	def get_id(self):
		result={"type":"query","count":0,"took":1,"result":[],"msg":""}
		if len(self.doc_types)==0 :
			res = self.es.get(index= self.tables, id=self.sql_tree["get_id"], _source_include=self.fields)
		else:
			res = self.es.get(index= self.tables, doc_type= self.doc_types,id=self.sql_tree["get_id"], _source_include=self.fields)
		result["count"]=1
		result["result"]=self.transfor_get(res)
		return result

		
	def do_scan(self):
		self.scan_options={"size":10,"routing":None}
		
		#print self.sql_tree["with"]
		
		if len(self.sql_tree["with"]) >0:
			opt = " ".join(self.sql_tree["with"])			
			a = opt.split(" and ")
			for o in a:
				options=o.split("=")
				self.scan_options[options[0].strip()]= int(options[1].strip()) 
		
		#print self.scan_options
		
		if self.sql_tree["where"] == None:
			res =  self.matchall_scan()
		else:
			res =  self.query_scan()
				
		#最后的结果
		result={"type":"query","count":0,"took":0,"cost":0,"result":[],"msg":""}
		
		result["count"]=res['hits']['total']
		result["took"] = res['took']
		try:
			result["id"] = res["_scroll_id"]
			result["result"] = [{"_scroll_id":res["_scroll_id"]}]
		except:
			result["msg"]="can not support the SQL!"
		return result
	
	def do_scroll(self):
		"""
		 sql sample :
		 "scan from c2NhbjsxOzE0Mjg1NDpOenc2TTJMMVN5cVpVcXREanppV0F3OzE7dG90YWxfaGl0czoyNjI7"
		"""
		res = self.es.scroll(scroll_id=self.sql_tree["from"][0].strip(),scroll="1m")		
		
		
		#最后的结果
		result={"type":"query","count":0,"took":0,"cost":0,"result":[],"msg":""}
		
		result["count"]=len(res['hits']['hits'])
		result["took"] = res['took']
		result["id"] = res["_scroll_id"]
		result["result"] = self.transfor_hits(res['hits']['hits'])		
		return result	
	
	def matchall_search(self):		
		res = self.es.search(request_timeout=100,index=self.tables, doc_type=self.doc_types, body={"query": {"match_all": {}}},from_=self.begin,size=self.size, _source_include=self.fields, sort=self.sql_tree["order"],ignore_unavailable=True)
		return res
	
	def matchall_scan(self):
		if  self.scan_options["routing"] ==None:	
			res = self.es.search(request_timeout=100,index=self.tables, body={"query": {"match_all": {}}},size=self.scan_options["size"], search_type="scan",scroll="1m", _source_include=self.fields)
		else:
			res = self.es.search(request_timeout=100,index=self.tables, body={"query": {"match_all": {}}},size=self.scan_options["size"], preference="_shards:%s"%(self.scan_options["routing"]), search_type="scan",scroll="1m", _source_include=self.fields)
		
		return res
	
	def build_body(self):
		body={
			 "query":{
				"bool": {
				"must":[],
				"must_not":[],
				"should":[],
				}
			}
		}
		
		if (len(self.doc_types)>=1 and self.doc_types[0]=="ALL"):
			self.doc_types=[] # ALL is []
			return build_parent_child_query_body(body,self.sql_tree)
		
		return build_query_body(body,self.sql_tree)

		
	def query_search(self,body):
		
		res = self.es.search(request_timeout=100, index=self.tables,doc_type=self.doc_types ,body=body,from_=self.begin,size=self.size, _source_include=self.fields, sort=self.sql_tree["order"],ignore_unavailable=True)
		return res
	
	def query_scan(self):
		if  self.scan_options["routing"] ==None:
			res = self.es.search(request_timeout=100, index=self.tables,body=self.build_body(),size=self.scan_options["size"], search_type="scan",scroll="1m", _source_include=self.fields)
		else:
			res = self.es.search(request_timeout=100, index=self.tables,body=self.build_body(),size=self.scan_options["size"], preference="_shards:%s"%(self.scan_options["routing"]), search_type="scan",scroll="1m", _source_include=self.fields)
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
		tabs = copy.copy(self.tables)
		for a in tabs:
			b= a.split(".")
			if len(b)>=2:
				self.tables.remove(a)
				self.tables.append(b[0])
				for c in b[1:]:
					self.doc_types.append(c)
		
		str_select = "".join(self.sql_tree["select"])
		self.fields = str_select.split(",")
		
		"""
		#add by gjw on 20141217 for safe check 
		#check tables
		if not self.rdb.sismember("role:%s:tables"%(self.role),"_all"):			
			tables1 = copy.copy(self.tables)
			for t in tables1:
				if t=="_all": 
					self.tables=[x for x in self.rdb.smembers("role:%s:tables"%(self.role))]
					break;
				if not self.rdb.sismember("role:%s:tables"%(self.role),t):
					self.tables.remove(t)
			
			if len(self.tables)==0:# not access table
				raise Exception(" can't access the table!")
				
			#check types
			allow_types=[]			
			for t in self.tables:
				for doc_type in self.rdb.smembers("role:%s:%s:types"%(self.role,t)):
					allow_types.append(doc_type)
					
			if len(self.doc_types)==0: #not doc_types mean all the allow types
				self.doc_types=allow_types
			else: 
				if len(allow_types) !=0:
					temp_doc_types = copy.copy(self.doc_types)
					for doc_type in temp_doc_types:
						if doc_type not in allow_types:
							self.doc_types.remove(doc_type)
					if len(self.doc_types) ==0:
						raise Exception(" can't access the doc_type !")
		
			#check fields
			allow_fields=[]
			for t in self.tables:
				for doc_type in self.doc_types:
					for field in self.rdb.smembers("role:%s:%s:%s:fields"%(self.role,t,doc_type)):
						allow_fields.append(field)
			
			if "*" in self.fields:
				self.fields = allow_fields
			else:
				if len(allow_fields) !=0:
					temp_fields = self.fields
					for field in temp_fields:
						if field not in allow_fields:
							self.fields.remove(field)
					if len(self.fields) ==0:
						raise Exception(" can't access the field !")
			
			if sql_tree.has_key("highlight") and  len( sql_tree["highlight"] ) >0:
				sql_tree["highlight"]=self.fields
				if len(sql_tree["highlight"])==0:
					sql_tree["highlight"].append("*")
		
		#end for safe check
		"""
		#print self.tables
		#print self.doc_types
		
		
		
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
		self.begin=0
		self.size=10
		
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
			
		return sql_tree
		
	def parse_where(self,where_cond,sql_tree):
		if len(sql_tree["where"])==0:
			sql_tree["where"]=None #没有where
		else:
			sql_tree["where"]={}
			#先解析and
			sql_tree["where"]["must"]=where_cond.split("and")
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
		for o in orders:
			fields = o.split(" ")
			fields = list_remove(fields,"")
			if len(fields)==2:
				s ="%s:%s"%( fields[0],fields[1] )
			else:
				s = "%s:asc"%( fields[0] )
			a.append(s)
		sql_tree["order"] = a
	#end parse_order
	
				
			
			

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
		#self.rdb = redis.Redis(host=cfg.rserver, port=6379, db=1)
	"""
	执行SQL
	"""
	def do_sql(self,role,sql):
		self.role = role
		b0 = time.time()
		try:
			self.sql_tree = self.parse_sql(sql)
			# deal the index
			self.tables = []
			for b in self.sql_tree["from"].split(","):
				self.tables.append(b)
					
			#add by gjw deal the doc_type
			self.doc_types=[]
			tabs = copy.copy(self.tables)
			for a in tabs:
				b= a.split(".")
				if len(b)>=2:
					self.tables.remove(a)
					self.tables.append(b[0])
					for c in b[1:]:
						self.doc_types.append(c)
						
			#add by gjw on 20141219 for safe check 
			#check tables
			if not self.rdb.sismember("role:%s:tables"%(self.role),"_all"):			
				tables1 = copy.copy(self.tables)
				for t in tables1:
					if t=="_all": 
						self.tables=[x for x in self.rdb.smembers("role:%s:tables"%(self.role))]
						break;
					if not self.rdb.sismember("role:%s:tables"%(self.role),t):
						self.tables.remove(t)
				
				if len(self.tables)==0:# not access table
					raise Exception(" can't access the table!")
					
				#check types
				allow_types=[]			
				for t in self.tables:
					for doc_type in self.rdb.smembers("role:%s:%s:types"%(self.role,t)):
						allow_types.append(doc_type)
						
				if len(self.doc_types)==0: #not doc_types mean all the allow types
					self.doc_types=allow_types
				else: 
					if len(allow_types) !=0:
						temp_doc_types = copy.copy(self.doc_types)
						for doc_type in temp_doc_types:
							if doc_type not in allow_types:
								self.doc_types.remove(doc_type)
						if len(self.doc_types) ==0:
							raise Exception(" can't access the doc_type !")
			#end for safe check
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s"%(e)
			return self.result
		# self.sql_tree	
		
		#print "parse over!"
		try:
			result= self.do_aggs()
		except Exception as e:
			logger.error(traceback.format_exc())
			self.result["msg"]="%s the SQL exec has error %s !"%(sql,e)
			return self.result
		
		result["cost"] = int((time.time()-b0)*1000)
		return result
		
	def do_aggs(self):
		if len(self.doc_types)==0:
			res = self.es.search(request_timeout=100,search_type="count",index=self.tables,body=self.build_body(),size=self.size,ignore_unavailable=True,sort="")
		else:
			res = self.es.search(request_timeout=100,search_type="count",doc_type=self.doc_types,index=self.tables,body=self.build_body(),size=self.size,ignore_unavailable=True)
			
		#print res
		#print "exec over!"
		result={"type":"aggs","count":0,"took":0,"cost":0,"result":[],"msg":""}
		result["took"]=res["took"]
		result["result"] =[]		
		
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
					for r2 in r1[self.sql_tree["group"][1]["agg_name"]]["buckets"]:
						r={}
						r[self.sql_tree["group"][0]["agg_name"]] = r1["key"]
						if "key_as_string" in r1:
							r[self.sql_tree["group"][0]["agg_name"]+"_string"]=r1["key_as_string"]
						
						r[self.sql_tree["group"][1]["agg_name"]] = r2["key"]
						if "key_as_string" in r2:
							r[self.sql_tree["group"][1]["agg_name"]+"_string"]=r2["key_as_string"]
						
						r["count"] = r2["doc_count"]
						for s1 in self.sql_tree["select"]:
							r[s1["sname"]] = r2[s1["sname"]]["value"]
						result["result"].append(r)
		else:
			# only have the count add by gjw on 20120721
			result["result"] =[{"count":res["hits"]["total"]}]
		#end if 				
		#print "result data over!"
		
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
		
		#deal the top group
		if len(aggs_b)==0: #no have the group
			body["aggs"] = aggs2
		elif len(aggs_b)==1:			
			body["aggs"]=aggs_b[0]
			body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"] = aggs2
		elif len(aggs_b)>=2:
			o = aggs_b[0]
			del o[self.sql_tree["group"][0]["agg_name"]][self.sql_tree["group"][0]["type"]]["order"]
			#{self.sql_tree["group"][1]["agg_name"]+">"+orders[0]:orders[1]}
			
			body["aggs"]=o
			body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"] = aggs_b[1]
			body["aggs"][self.sql_tree["group"][0]["agg_name"]]["aggs"][self.sql_tree["group"][1]["agg_name"]]["aggs"] = aggs2
		
		if self.sql_tree["where"] !=None:
			self.build_qbody(body)
		#print body
		#print "build body over"
		return body
		
	
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
			self.size = 65536


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
		#print sql_tree["group"]
	#end def parse_groupby

	def parse_where(self,where_cond,sql_tree):
		if len(where_cond)==1:
			sql_tree["where"]=None #没有where
		else:
			sql_tree["where"]={}
			#先解析and
			sql_tree["where"]["must"]=where_cond[1].split("and")
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
	
	
	es = Elasticsearch([
	{'host':"10.68.23.81"}
	#{'host':"192.168.23.240"},{'host':"192.168.23.241"},    {'host':"192.168.23.242"},{'host':"192.168.23.243"},	
	])
	
	
	#es = Elasticsearch()
	
	esql = ESql2(es)
	sql =  "scan * from overlookcdesqllog where gro=info and type_name=select and day >=2016-04-01 and day <=2016-04-07 with size=500 )"
	print(sql)
	res = esql.do_sql("",sql)
	
	print("count:%s took:%s  cost: %s %s"%(res["count"],res["took"], res["cost"],res["msg"]))
	
