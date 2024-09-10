#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/CRUD
#datetime: 2024-08-30T16:10:57.217419
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[6]原语 q = @udf udf0.new_df with name,value,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'time, 2020-09-01 00:00:00 ,>='}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[7]原语 q = @udf q by udf0.df_append with time, 2020-09-01... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'time, 2020-09-28 13:13:51,<='}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[8]原语 q = @udf q by udf0.df_append with 	time, 2020-09-2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'level,中,string'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[9]原语 q = @udf q by udf0.df_append with level,中,string 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'srcip,192.168.1.65,string'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[10]原语 q = @udf q by udf0.df_append with srcip,192.168.1.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'limit,100,sys'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[11]原语 q = @udf q by udf0.df_append with limit,100,sys 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'gmt_create,asc,order'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[12]原语 q = @udf q by udf0.df_append with gmt_create,asc,o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd1,c1', 'Action': '@udf', '@udf': 'q', 'by': 'CRUD.query_mtable', 'with': 'ev_mysql,moxing_alert'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[14]原语 d1,c1 = @udf q by CRUD.query_mtable with ev_mysql,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'CRUD.query_mtable2', 'with': "ev_mysql,moxing_alert,level='中', limit 10"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[17]原语 b = @udf CRUD.query_mtable2 with ev_mysql,moxing_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'CRUD.load_mysql_sql', 'with': "ev_mysql,select * from moxing_alert where level='中' limit 100"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[20]原语 d = @udf CRUD.load_mysql_sql with ev_mysql,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'CRUD.load_mysql_sql', 'with': "ev_mysql,select count(id) from moxing_alert where level='中' limit 100"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[21]原语 c = @udf CRUD.load_mysql_sql with ev_mysql,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'level,count(*),group'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[25]原语 q = @udf q by udf0.df_append with level,count(*),g... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'q', 'by': 'CRUD.group_mtable', 'with': 'ev_mysql,moxing_alert'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[26]原语 d = @udf q by CRUD.group_mtable with ev_mysql,moxi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'CRUD.load_mysql_sql', 'with': 'ev_mysql,select level,count(*) from moxing_alert group by level order by level desc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[28]原语 d = @udf CRUD.load_mysql_sql with ev_mysql,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'ev_mysql, ALTER TABLE moxing_alert ADD INDEX index_time (time);'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[32]原语 e = @udf RS.exec_mysql_sql with ev_mysql,  ALTER T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'ev_mysql, ALTER TABLE moxing_alert drop INDEX index_level;'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[33]原语 e = @udf RS.exec_mysql_sql with ev_mysql,  ALTER T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'ev_mysql, ALTER TABLE moxing_alert ADD INDEX index_z (time,level);'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[34]原语 e = @udf RS.exec_mysql_sql with ev_mysql,  ALTER T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ep', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "ev_mysql, SHOW STATUS LIKE 'Handler_read%';"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[38]原语 ep = @udf RS.load_mysql_sql with ev_mysql, SHOW ST... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'epi', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'ev_mysql, show index from moxing_alert;'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[39]原语 epi = @udf RS.load_mysql_sql with ev_mysql, show i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ep2', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "ev_mysql, EXPLAIN select count(id) from moxing_alert where (level='中' and time >= '2020-09-01 00:00:00' and time <= '2020-09-28 13:13:51') limit 100"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[41]原语 ep2 =@udf RS.load_mysql_sql with ev_mysql, EXPLAIN... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ep3', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "ev_mysql, EXPLAIN select count(id) from moxing_alert where (time >= '2020-09-01 00:00:00' and time <= '2020-09-28 13:13:51' and level='中') limit 100"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[43]原语 ep3 =@udf RS.load_mysql_sql with ev_mysql, EXPLAIN... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ep4', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "ev_mysql, EXPLAIN select level,count(id) from moxing_alert where (time >= '2020-09-01 00:00:00' and time <= '2020-09-28 13:13:51') group by level"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/CRUD.fbi]执行第[45]原语 ep4 =@udf RS.load_mysql_sql with ev_mysql, EXPLAIN... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],45

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



