#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/cluster
#datetime: 2024-08-30T16:10:57.180830
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
	
	
	ptree={'runtime': runtime, 'Action': 'set', 'set': 'cluster', 'by': 'addnode', 'as': 'node170', 'with': '192.168.1.170,admin,IamFBI@2020'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[7]原语 set cluster by addnode as node170 with 192.168.1.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'set', 'set': 'cluster', 'by': 'addnode', 'as': 'node172', 'with': '192.168.1.172,admin,IamFBI@2020'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[8]原语 set cluster by addnode as node172 with 192.168.1.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'set', 'set': 'cluster', 'by': 'addnode', 'as': 'node173', 'with': '192.168.1.173,admin,IamFBI@2020'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[9]原语 set cluster by addnode as node173 with 192.168.1.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'm', 'Action': '@udf', '@udf': 'FBI.ssdb_master', 'with': 'm.conf,./var,0.0.0.0,19999'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[12]原语 m = @udf FBI.ssdb_master with m.conf,./var,0.0.0.0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'FBI.ssdb_start', 'with': 'm.conf'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[13]原语 t = @udf FBI.ssdb_start with m.conf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't2', 'Action': '@udf', '@udf': 'FBI.ssdb_stop', 'with': 'm.conf'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[14]原语 t2 = @udf FBI.ssdb_stop with m.conf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'i', 'Action': '@udf', '@udf': 'FBI.ssdb_info', 'with': 'm.conf'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[15]原语 i = @udf FBI.ssdb_info with m.conf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'ssdb_my', 'as': '192.168.1.22:19999'}
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[18]原语 define ssdb_my as 192.168.1.22:19999 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'sample/SSDB.fbi@node173', 'with': 'data=/var,host=192.168.1.173,port=1999,id=node173,mip=192.168.1.22,mport=19999'}
	ptree['run'] = replace_ps(ptree['run'],runtime)
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {} with {}'.format(ptree['run'],ptree['with']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[20]原语 run sample/SSDB.fbi@node173 with data=/var,host=19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'sample/SSDB.fbi@node172:9001', 'with': 'data=/var,host=192.168.1.172,port=1999,id=node172,mip=192.168.1.22,mport=19999'}
	ptree['run'] = replace_ps(ptree['run'],runtime)
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {} with {}'.format(ptree['run'],ptree['with']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[21]原语 run sample/SSDB.fbi@node172:9001 with data=/var,ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'i2', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb_my', 'with': 'SSDB:node173'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[24]原语 i2 = load ssdb by ssdb_my with SSDB:node173 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'i2', 'to': 'ssdb', 'by': 'ssdb_my', 'with': 'SSDB:0', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[26]原语 store i2 to ssdb by ssdb_my with SSDB:0 as Q 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'i3', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb_my query2 qpop,SSDB:0,10,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/cluster.fbi]执行第[27]原语 i3 = load ssdb by ssdb_my query2 qpop,SSDB:0,10,- 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],28

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



