#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: GFSZnF/init
#datetime: 2024-08-30T16:10:56.324395
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
		add_the_error('[GFSZnF/init.fbi]执行第[7]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[8]原语 a1 = @udf udf0.new_df with key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'setting'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[9]原语 a1 = @udf a1 by udf0.df_append with (setting) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'manage_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[10]原语 a1 = @udf a1 by udf0.df_append with (manage_type) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[11]原语 a1 = @udf a1 by udf0.df_append with (alarm) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'agent'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[12]原语 a1 = @udf a1 by udf0.df_append with (agent) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'Traffic'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[13]原语 a1 = @udf a1 by udf0.df_append with (Traffic) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'json_wdgl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[14]原语 a1 = @udf a1 by udf0.df_append with (json_wdgl) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'disk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[15]原语 a1 = @udf a1 by udf0.df_append with (disk) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'loginl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[16]原语 a1 = @udf a1 by udf0.df_append with (loginl) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'qh_owasp'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[17]原语 a1 = @udf a1 by udf0.df_append with (qh_owasp) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'qh_send'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[18]原语 a1 = @udf a1 by udf0.df_append with (qh_send) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'sensitive'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[19]原语 a1 = @udf a1 by udf0.df_append with (sensitive) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'snmp_config'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[20]原语 a1 = @udf a1 by udf0.df_append with (snmp_config) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'model_config'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[21]原语 a1 = @udf a1 by udf0.df_append with (model_config)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_append', 'with': 'protocol_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[22]原语 a1 = @udf a1 by udf0.df_append with (protocol_data... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'SSDB.dump_keys2', 'with': 'setting'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[24]原语 a1 = @udf a1 by SSDB.dump_keys2 with setting 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[GFSZnF/init.fbi]执行第[26]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],26

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



