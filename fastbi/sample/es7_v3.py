#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/es7
#datetime: 2024-08-30T16:10:57.196032
#copyright: OpenFBI

import sys 
sys.path.append("./")
sys.path.append("/opt/openfbi/fbi-bin")
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
import threading
import time
from avenger.fglobals import *
from avenger.fbiobject import *
from avenger.fbiprocesser import *
from avenger.fbicluster import run_cluster


#参数替换
def replace_ps(p,runtime):	
	for k in runtime.keys:
		p = p.replace(k,runtime.ps[k])	
	return p

#处理单值变量的替换
def deal_sdf(work_space="",prmtv=""):	
	if prmtv.find("$")==-1: #未找到需要替换的变量
		return prmtv

	#仅适用当前工作区
	d = fbi_global.get_runtime().get_cur_ws().workspace	
	
	#处理单值$,不能跨区 add by gjw on 20220507
	keys = list(d.keys())
	#倒序，越长的越在最前面
	keys.sort(key=len,reverse = True)
	
	for k in keys:
		if d[k].type==2:
			try:
				if isinstance(d[k].vue,str):
					prmtv = prmtv.replace("$%s"%(k),d[k].vue)
				else:
					prmtv = prmtv.replace("$%s"%(k),str(d[k].vue))
			except:
				try:
					if isinstance(d[k].vue,str):
						prmtv = prmtv.replace("$%s"%(k),str(d[k].vue,"utf-8"))
				except:
					prmtv = prmtv.replace("$%s"%(k),str(d[k].vue,"gbk"))
	return prmtv
#end 




#begin

#主入口
def fbi_main(ptree):
	import resource
	resource.setrlimit(resource.RLIMIT_NOFILE,(10000,10000))
	t = threading.current_thread()
	if t.ident not in global_tasks:
		init_task(t,"")
	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]
	
	workspace = ptree["work_space"]
	
	
	ptree={'runtime': runtime, 'Action': 'define', 'define': 'es75', 'with': '192.168.1.175:59200'}
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[11]原语 define es75 with 192.168.1.175:59200 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'show tables'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[13]原语 a = load es by es75 with show tables 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'select * from auditlogsql*'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[14]原语 b = load es by es75 with select * from auditlogsql... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'get_settings auditlogsql*'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[15]原语 d = load es by es75 with get_settings auditlogsql*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'readonly auditlogsql0000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[16]原语 d = load es by es75 with readonly auditlogsql0000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'drop table test2'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[18]原语 d = load es by es75 with drop table test2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'desc test3'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[20]原语 a = load es by es75 with desc test3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'select count(*) from zichan3 group by src_ip.keyword'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[21]原语 a = load es by es75 with select count(*) from zich... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': "create table test3 ( field1 long, field2 keyword, field3 date, field4 text, field5 text, field6 text {'fields': {'keyword': {'type': 'keyword', 'ignore_above': 10}}} ) with 10,0"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[22]原语 c = load es by es75 with  create table test3 ( fie... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'i', 'Action': 'load', 'load': 'es', 'by': 'es75', 'with': 'insert into test(_id=111,field1=12 ,field2=中图,field3=2014-12-21T12:12:12)'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[33]原语 i = load es by es75 with "insert into test(_id=111... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from auditlogfuc*'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[35]原语 b1 = load es by es7 with select * from auditlogfuc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql*'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[37]原语 c = load es by es7 with select count(*) from audit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogfuc* where @timestamp>=2020-03-18'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[38]原语 c1 = load es by es7 with select count(*) from audi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* group by sqlCategory'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[40]原语 d1 = load es by es7 with select count(*) from audi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* group by link_username,sqlAction'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[41]原语 d2 = load es by es7 with select count(*) from audi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd3', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* where @timestamp>=2020-03-18 group by link_username,sqlAction'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[43]原语 d3 =  load es by es7 with select count(*) from aud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd4', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* where @timestamp>=2020-03-11 and @timestamp <=2020-03-15 group by link_username,sqlAction'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[44]原语 d4 =  load es by es7 with select count(*) from aud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd5', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* group by @timestamp.date_histogram[{interval:1d}]'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[46]原语 d5 =  load es by es7 with select count(*) from aud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd6', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* where @timestamp=2020-03-18 group by @timestamp.date_histogram[{interval:1h}]'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[48]原语 d6 =  load es by es7 with select count(*) from aud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'scan * from auditlogsql_20200312'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[51]原语 s = load es by es7 with scan * from  auditlogsql_2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'scan colFiters from auditlogsql* where @timestamp=2020-03-20'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[52]原语 s2 = load es by es7 with scan colFiters from  audi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date', 'Action': '@udf', '@udf': 'udf0.new_df_daterange', 'with': '2020-02-01,2020-03-22,1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[56]原语 date = @udf udf0.new_df_daterange with (2020-02-01... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd5', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from auditlogsql* where @timestamp>=2020-02-01 and @timestamp <=2020-03-22 group by @timestamp.date_histogram[{interval:1d}]'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[58]原语 d5 =  load es by es7 with select count(*) from aud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'd5', 'Action': 'add', 'add': 'd1', 'with': 'df["@timestamp_string"].str[0:10]'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[60]原语 d5 = add d1 with df["@timestamp_string"].str[0:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'd5', 'Action': 'add', 'add': 'd2', 'with': 'df["@timestamp_string"].map(lambda x:x[0:10])'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[61]原语 d5 = add d2 with df["@timestamp_string"].map(lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'd5', 'Action': 'add', 'add': 'd3', 'with': 'df.apply(lambda x:x["d1"]+x["d2"],)'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[62]原语 d5 = add d3 with df.apply(lambda x:x["d1"]+x["d2"]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'd8', 'Action': 'join', 'join': 'd5,date', 'by': 'd1,start_day', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[66]原语 d8 = join d5,date by d1,start_day with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'd8', 'Action': 'loc', 'loc': 'd8', 'by': 'start_day,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[67]原语 d8 = loc d8 by start_day,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd8', 'Action': '@udf', '@udf': 'd8', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[68]原语 d8 = @udf d8 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event where dstport in (80,443)'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[71]原语 a = load es by ev_es with select * from  event whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event where srcip in (192.168.1.9,192.168.1.188)'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[73]原语 d = load es by ev_es with select * from  event whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd,count', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'select srcip,collector_ip,timestamp_lo,lrecepttime,eventname from event_2022-06-21 where lrecepttime>=1655776909666 and lrecepttime<=1655863309666 and eventname.keyword in (流数据,DNS流量) limit 100'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[76]原语 d,count = load es by es201 with select srcip,colle... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event where proto in (TCP)'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[79]原语 d = load es by ev_es with select * from  event whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event where proto=TCP'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[81]原语 d = load es by ev_es with select * from  event whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event where event_type in (netflow)'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[83]原语 d = load es by ev_es with select * from  event whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event group by srcip order by count desc limit 20'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[86]原语 c = load es by ev_es with select * from  event gro... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'es', 'by': 'ev_es', 'with': 'select * from event group by srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[88]原语 c = load es by ev_es with select * from  event gro... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'select min(lrecepttime) as time, max(lrecepttime) as time2 from event_2022-06-21 where srcip.keyword in (192.168.1.192) group by srcip.keyword limit 100'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[94]原语 ip =  load es by es201 with select min(lrecepttime... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'es', 'by': 'es', 'with': 'select avg(speed) as avg_speed ,min(speed) as min_speed from bb where UTC between 1404201315 to 1504209315 group by plateColor,wayid,direction'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[97]原语 data =  load es by es with  select avg(speed) as a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'show segments'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[105]原语 d = load es by es201 with show segments 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'show segments with rawlog_2022-05-19'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[107]原语 d = load es by es201 with show segments  with rawl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'show segments with event_2022-06-15,event_2022-06-14'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[109]原语 d = load es by es201 with show segments  with even... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'optimize rawlog_2022-05-19'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[112]原语 d = load es by es201 with optimize rawlog_2022-05-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'optimize event_2022-06-15,event_2022-06-14'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[114]原语 d = load es by es201 with optimize event_2022-06-1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fielddata', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'show fielddata'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[117]原语 fielddata  = load es by es201 with show fielddata 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'es', 'by': 'es201', 'with': 'show shards'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/es7.fbi]执行第[120]原语 d = load es by es201 with show shards 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],130

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



