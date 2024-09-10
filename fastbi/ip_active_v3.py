#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: ip_active
#datetime: 2024-08-30T16:10:54.878491
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
	
	
	ptree={'runtime': runtime, 'Action': 'use', 'use': '@FID'}
	ptree['use'] = replace_ps(ptree['use'],runtime)
	try:
		use_fun(ptree)
		workspace=ptree['work_space']
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,left(firsttime,10) first_time,left(lasttime,10) last_time,curdate() now,active from data_ip_new where lasttime != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[7]原语 a = load db by mysql1 with select id,left(firsttim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a', 'by': 'first_time:datetime64,last_time:datetime64,now:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[8]原语 alter a by first_time:datetime64,last_time:datetim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:0 if x[2] == x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[13]原语 a1 = @udf a by udf0.df_row_lambda with x:0 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[14]原语 a1 = rename a1 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': 'active1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[15]原语 a1 = filter a1 by active1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[16]原语 a1 = @udf a1 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[17]原语 a1 = filter a1 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'a1', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[18]原语 a1 = loc a1 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[19]原语 a1 = rename a1 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:1 if x[2] != x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[20]原语 a2 = @udf a by udf0.df_row_lambda with x:1 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[21]原语 a2 = rename a2 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': 'active1 == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[22]原语 a2 = filter a2 by active1 == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a2', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[23]原语 a2 = @udf a2 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[24]原语 a2 = filter a2 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a2', 'Action': 'loc', 'loc': 'a2', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[25]原语 a2 = loc a2 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[26]原语 a2 = rename a2 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'a', 'Action': 'union', 'union': 'a1,a2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[27]原语 a = union a1,a2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[28]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': 'mysql1,data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[29]原语 @udf a by CRUD.save_table with (mysql1,data_ip_new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[ip_active.fbi]执行第[31]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],31

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



