#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sensitive_app_look
#datetime: 2024-08-30T16:10:55.004796
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
		add_the_error('[sensitive_app_look.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_app.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[7]原语 b = load pq by sensitive/sensitive_app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'b', 'by': 'app:str,url_count:int,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[8]原语 alter b by app:str,url_count:int,srcip_count:int,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'b', 'Action': 'filter', 'filter': 'b', 'by': '_id == @_id'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[9]原语 b = filter b by _id == @_id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'b', 'as': '"app":"应用","url_count":"接口数量","srcip_count":"终端数量","account_count":"账号数量","sensitive_count":"敏感数据数量","s_num_sum":"敏感数据分类数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[10]原语 rename b as ("app":"应用","url_count":"接口数量","srcip_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'look'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[11]原语 push b as look 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_look.fbi]执行第[13]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],13

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



