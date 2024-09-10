#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/psutil
#datetime: 2024-08-30T16:10:57.229159
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'PS.sys_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[6]原语 a = @udf PS.sys_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'PS.disk_usage'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[9]原语 d = @udf PS.disk_usage 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd1', 'Action': '@udf', '@udf': 'PS.disk_usage', 'with': '/'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[10]原语 d1 = @udf PS.disk_usage with / 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'disk', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[12]原语 disk = eval d by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$disk >10', 'as': 'notice', 'with': '警告: 磁盘剩余容量不足10G'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[13]原语 assert $disk >10 as notice with 警告: 磁盘剩余容量不足10G 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd2', 'Action': '@udf', '@udf': 'PS.disk_usage', 'with': '/dev/shm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[16]原语 d2 = @udf PS.disk_usage with /dev/shm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'shm', 'Action': 'eval', 'eval': 'd2', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[17]原语 shm = eval d2 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$shm >1', 'as': 'notice', 'with': '警告: /dev/shm剩余容量不足1G'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[18]原语 assert $shm >1 as notice with 警告: /dev/shm剩余容量不足1G... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'PS.sys_baseinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[21]原语 c = @udf PS.sys_baseinfo 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c', 'Action': 'loc', 'loc': 'c', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[22]原语 c = loc c by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[23]原语 c = @udf c by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'c', 'to': 'ssdb', 'with': 'sysinfo'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[24]原语 store c to ssdb with sysinfo 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'PS.sys_stats'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[27]原语 s = @udf PS.sys_stats 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mem', 'Action': 'eval', 'eval': 's', 'by': 'iloc[3,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[28]原语 mem = eval s by iloc[3,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$mem < 0.8', 'as': 'notice', 'with': '警告: 内存使用超过80%'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[29]原语 assert $mem < 0.8 as notice with 警告: 内存使用超过80% 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'cpu', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[31]原语 cpu = eval s by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$cpu < 95', 'as': 'notice', 'with': '警告: CPU使用超过95%'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[32]原语 assert $cpu < 95 as notice with 警告: CPU使用超过95% 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'n', 'Action': '@udf', '@udf': 'PS.net_conns'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[35]原语 n = @udf PS.net_conns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'l', 'Action': '@udf', '@udf': 'PS.net_listens'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[38]原语 l = @udf PS.net_listens 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'fbi', 'Action': 'filter', 'filter': 'l', 'by': '本地端口>= 9000 and 本地端口< 9999'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[41]原语 fbi = filter l by 本地端口>= 9000 and 本地端口<  9999 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'fbi', 'by': 'df.index.size >=8', 'as': 'notice', 'with': '警告: FBI引擎异常，小于最低数量8个'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[42]原语 assert fbi by df.index.size >=8 as notice with 警告:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'redis', 'Action': 'filter', 'filter': 'l', 'by': '本地端口==6379'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[45]原语 redis =  filter l by 本地端口==6379 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'redis', 'by': 'df.index.size ==1', 'as': 'notice', 'with': '警告: Redis服务异常，没有启动'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[46]原语 assert redis by df.index.size ==1 as notice with 警... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ssdb', 'Action': 'filter', 'filter': 'l', 'by': '本地端口==8888'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[49]原语 ssdb =  filter l by 本地端口==8888 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'ssdb', 'by': 'df.index.size ==1', 'as': 'notice', 'with': '警告: SSDB服务异常，没有启动'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[50]原语 assert ssdb by df.index.size ==1 as notice with 警告... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'port', 'Action': '@udf', '@udf': 'PS.net_open_port', 'with': '9001'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[53]原语 port = @udf PS.net_open_port with 9001 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'p', 'Action': '@udf', '@udf': 'PS.proc_name', 'with': 'json_out.py'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[70]原语 p = @udf PS.proc_name with json_out.py 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'p', 'Action': '@udf', '@udf': 'PS.pids_name', 'with': 'json_out.py'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/psutil.fbi]执行第[73]原语 p = @udf PS.pids_name with json_out.py 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],75

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



