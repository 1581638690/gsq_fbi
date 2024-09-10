#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_visit_hour
#datetime: 2024-08-30T16:10:53.813130
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
		add_the_error('[api_visit_hour.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'xlink/hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[22]原语 a = @udf ZFile.list_dir with xlink/hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.name', 'Action': 'lambda', 'lambda': 'filename', 'by': 'x:x.split("/")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[23]原语 a.name = lambda filename by (x:x.split("/")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_l2cs', 'with': 'name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[24]原语 a = @udf a by udf0.df_l2cs with name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'filename,n102'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[25]原语 a = loc a by filename,n102 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'a', 'as': "'n102':'name'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[26]原语 rename a as ("n102":"name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'hh', 'Action': 'group', 'group': 'a', 'by': 'name', 'agg': 'name:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[27]原语 hh = group a by name agg name:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hh', 'Action': '@udf', '@udf': 'hh', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[28]原语 hh = @udf hh by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'hh', 'with': 'file = $1', 'run': '""\nb = @udf ZFile.list_dir with xlink/hx/@file\n##分小时处理数据\nrun hour_visit.fbi\n""'}
	try:
		ptree['lineno']=30
		ptree['funs']=block_foreach_30
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[30]原语 foreach hh run "b = @udf ZFile.list_dir with xlink... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_visit_hour.fbi]执行第[36]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],36

#主函数结束,开始块函数

def block_foreach_30(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'xlink/hx/@file'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第30行foreach语句中]执行第[31]原语 b = @udf ZFile.list_dir with xlink/hx/@file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'hour_visit.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第30行foreach语句中]执行第[33]原语 run hour_visit.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_30

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



