#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/load_pq
#datetime: 2024-08-30T16:10:57.150043
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'pq', 'by': '01094.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_pq.fbi]执行第[7]原语 a = load pq by 01094.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'pq', 'by': '01094.pq', 'with': "[('dest_ip','==','192.168.5.122')]"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_pq.fbi]执行第[11]原语 b = load pq by 01094.pq with [("dest_ip","==","192... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'pq', 'by': '01094.pq', 'with': "[('dest_ip','==','192.168.5.122'),('srcip','==','192.168.1.104')]"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_pq.fbi]执行第[14]原语 c = load pq by 01094.pq with [("dest_ip","==","192... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'pq', 'by': '01094.pq', 'with': "[[('dest_ip','==','192.168.5.122')],[('srcip','==','192.168.1.104')]]"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_pq.fbi]执行第[17]原语 d = load pq by 01094.pq with [[("dest_ip","==","19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'e', 'Action': 'load', 'load': 'pq', 'by': '01094.pq', 'with': "[[('dest_ip','==','192.168.5.122'),('srcip','==','192.168.1.104')],[('length','>=',4000)]]"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_pq.fbi]执行第[20]原语 e = load pq by 01094.pq with [[("dest_ip","==","19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],20

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



