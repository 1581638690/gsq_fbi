#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_risk_export_table
#datetime: 2024-08-30T16:10:55.299805
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
		add_the_error('[app_risk_export_table.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[7]原语 day = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[8]原语 day = @sdf format_now with ($day,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datas', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_risk.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[10]原语 datas = load pq by dt_table/app_risk.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[12]原语 ss = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'ss.index.size != 0', 'with': '""\nss = eval ss by iloc[0,0]\ndatas = filter datas by $ss\n""'}
	try:
		ptree['lineno']=13
		ptree['funs']=block_if_13
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[13]原语 if ss.index.size != 0 with "ss = eval ss by iloc[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': "'app':'应用','app_name':'应用名','dest_ip_sum':'服务器IP','api_num':'接口总数','api_count':'接口弱点量','state_num':'弱点状态分布','type_num':'弱点类型分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[17]原语 rename datas as ("app":"应用","app_name":"应用名","dest... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datas', 'to': 'csv', 'by': '应用弱点_$day.csv'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[18]原语 store datas to csv by 应用弱点_$day.csv 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'name', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'file_name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[20]原语 name = @udf udf0.new_df with file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'name', 'Action': '@udf', '@udf': 'name', 'by': 'udf0.df_append', 'with': '应用弱点_$day.csv'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[21]原语 name = @udf name by udf0.df_append with 应用弱点_$day.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'name', 'as': 'file_name'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[22]原语 push name as file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_risk_export_table.fbi]执行第[24]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],24

#主函数结束,开始块函数

def block_if_13(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'eval', 'eval': 'ss', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第13行if语句中]执行第[14]原语 ss = eval ss by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'datas', 'Action': 'filter', 'filter': 'datas', 'by': '$ss'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第13行if语句中]执行第[15]原语 datas = filter datas by $ss 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_13

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



