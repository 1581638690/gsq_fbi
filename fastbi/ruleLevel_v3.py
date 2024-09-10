#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: ruleLevel
#datetime: 2024-08-30T16:10:54.666087
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
		add_the_error('[ruleLevel.fbi]执行第[1]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'atemp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[2]原语 a = load ssdb by ssdb0 with atemp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'a', 'by': 'Rule.splitA', 'with': '@val'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[3]原语 df= @udf a by Rule.splitA with @val 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'con', 'Action': 'eval', 'eval': 'df', 'by': "get_value(0,'con')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[4]原语 con=eval df by (get_value(0,"con")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'level', 'Action': 'eval', 'eval': 'df', 'by': "get_value(0,'level')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[5]原语 level=eval df by (get_value(0,"level")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'Rule.sql', 'with': '$con'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[6]原语 a= @udf a by Rule.sql with $con 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sql_df', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.get_sql', 'with': 'event*'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[7]原语 sql_df = @udf a by CRUD.get_sql with (event*) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sql_str', 'Action': 'eval', 'eval': 'sql_df', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[8]原语 sql_str= eval sql_df by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'nowq', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': '$sql_str'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[9]原语 nowq=load es by es7 with $sql_str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'nowq', 'Action': 'add', 'add': 'level', 'by': "'$level'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[10]原语 nowq= add level by ("$level") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'base_df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'base_df'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[11]原语 base_df= load ssdb by ssdb0 with base_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'base_df', 'Action': 'union', 'union': 'base_df,nowq'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[12]原语 base_df= union (base_df,nowq) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'base_df', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'base_df'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[ruleLevel.fbi]执行第[13]原语 store base_df to ssdb by ssdb0 with base_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

