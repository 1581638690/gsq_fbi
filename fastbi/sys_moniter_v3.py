#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sys_moniter
#datetime: 2024-08-30T16:10:54.265119
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'PS.sys_baseinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[14]原语 c = @udf PS.sys_baseinfo 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c', 'Action': 'loc', 'loc': 'c', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[15]原语 c = loc c by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[16]原语 c = @udf c by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'c', 'to': 'ssdb', 'with': 'sysinfo'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[17]原语 store c to ssdb with sysinfo 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZNSM.calculate_logger_count', 'with': 'zichan'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[21]原语 a = @udf ZNSM.calculate_logger_count  with zichan 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'limit', 'limit': 'a', 'by': '-10,'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[22]原语 a = limit a by -10, 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'create,lines,errs'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[23]原语 a = loc a by create,lines,errs 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'create', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[24]原语 a = loc a by create to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'a', 'as': '{"lines":"发送","err":"错误数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[25]原语 rename a as {"lines":"发送","err":"错误数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'znsm:view:events'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[26]原语 store a to ssdb with znsm:view:events 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'p', 'Action': '@udf', '@udf': 'PS.proc_name_or_arg', 'with': '/opt/openfbi/bin/redis-server 127.0.0.1:6379'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[57]原语 p = @udf PS.proc_name_or_arg with /opt/openfbi/bin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'p', 'Action': 'filter', 'filter': 'p', 'by': "name == '内存(G)'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[58]原语 p = filter p by name == "内存(G)" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'p', 'Action': 'eval', 'eval': 'p', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[59]原语 p = eval p by (iloc[0,1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$p<=30', 'as': 'notice', 'with': 'redis内存空间大于30G'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[60]原语 assert $p<=30 as notice  with redis内存空间大于30G 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$p<=40', 'as': 'notice', 'with': 'redis内存空间大于40G,影响系统运行,请尽快处理'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sys_moniter.fbi]执行第[61]原语 assert $p<=40 as notice  with redis内存空间大于40G,影响系统运... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],61

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



