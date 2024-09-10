#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_gov_clear_dd
#datetime: 2024-08-30T16:10:55.107909
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
		add_the_error('[data_gov_clear_dd.fbi]执行第[4]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,sysname from app_sx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[6]原语 dd = load db by mysql1 with select id,sysname from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '0,无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[7]原语 dd = @udf dd by udf0.df_append with (0,无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dd.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[8]原语 alter dd.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'dd', 'Action': 'order', 'order': 'dd', 'by': 'id', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[9]原语 dd = order dd by id with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'dd', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[10]原语 dd = loc dd by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_sx'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[11]原语 store dd to ssdb by ssdb0 with dd:app_sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type from api_label_library'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[13]原语 dd = load db by mysql1 with select type from api_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dd', 'Action': 'add', 'add': 'id', 'by': 'dd.type'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[14]原语 dd = add id by dd.type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '无,无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[15]原语 dd = @udf dd by udf0.df_append with (无,无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[16]原语 dd = @udf dd by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_label_library'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[17]原语 store dd to ssdb by ssdb0 with dd:api_label_librar... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type from app_label_library'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[18]原语 dd = load db by mysql1 with select type from app_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dd', 'Action': 'add', 'add': 'id', 'by': 'dd.type'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[19]原语 dd = add id by dd.type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '无,无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[20]原语 dd = @udf dd by udf0.df_append with (无,无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[21]原语 dd = @udf dd by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_label_library'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[22]原语 store dd to ssdb by ssdb0 with dd:app_label_librar... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type from ip_label_library'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[23]原语 dd = load db by mysql1 with select type from ip_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dd', 'Action': 'add', 'add': 'id', 'by': 'dd.type'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[24]原语 dd = add id by dd.type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '无,无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[25]原语 dd = @udf dd by udf0.df_append with (无,无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[26]原语 dd = @udf dd by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:ip_label_library'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[27]原语 store dd to ssdb by ssdb0 with dd:ip_label_library... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type from account_label_library'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[28]原语 dd = load db by mysql1 with select type from accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dd', 'Action': 'add', 'add': 'id', 'by': 'dd.type'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[29]原语 dd = add id by dd.type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '无,无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[30]原语 dd = @udf dd by udf0.df_append with (无,无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[31]原语 dd = @udf dd by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:account_label_library'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[32]原语 store dd to ssdb by ssdb0 with dd:account_label_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_gov_clear_dd.fbi]执行第[35]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],35

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



