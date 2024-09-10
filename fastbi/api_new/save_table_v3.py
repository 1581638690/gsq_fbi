#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_new/save_table
#datetime: 2024-08-30T16:10:58.833297
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
		add_the_error('[api_new/save_table.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[20]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[21]原语 api = eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'qq', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select url from data_api_new where url='$api'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[22]原语 qq = load db by mysql1 with select url from data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'qq', 'by': 'df.index.size <=0', 'as': 'break', 'with': '接口已存在！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[api_new/save_table.fbi]执行第[23]原语 assert qq by df.index.siz... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[23]原语 assert qq by df.index.size <=0 as break with 接口已存在... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'url,name,api,dstip,protocol,app,dstport,method,api_type,api_status,data_type,auth_type,active,scope,merge_state,sensitive_label,risk_level,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[24]原语 a = loc a by url,name,api,dstip,protocol,app,dstpo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'active', 'by': '3'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[25]原语 a = add active by 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'merge_state', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[26]原语 a = add merge_state by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'visits_flow', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[27]原语 a = add visits_flow by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'url_sum', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[28]原语 a = add url_sum by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'risk_label', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[29]原语 a = add risk_label by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'visits_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[30]原语 a = add visits_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[32]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('b',ptree)", 'as': 'alert', 'to': '保存成功！', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[33]原语 assert find_df("b",ptree) as  alert  to 保存成功！ with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'btn_show', 'by': "'1,1,1,1,0'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[34]原语 b = add btn_show by ("1,1,1,1,0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[39]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_new/save_table.fbi]执行第[41]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],41

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



