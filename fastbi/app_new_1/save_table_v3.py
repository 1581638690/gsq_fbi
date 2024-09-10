#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_new_1/save_table
#datetime: 2024-08-30T16:10:56.516323
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
		add_the_error('[app_new_1/save_table.fbi]执行第[28]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[31]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[32]原语 app = eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'qq', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app from data_app_new where app='$app'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[33]原语 qq = load db by mysql1 with select app from data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'qq', 'by': 'df.index.size <=0', 'as': 'break', 'with': '应用已存在！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[app_new_1/save_table.fbi]执行第[34]原语 assert qq by df.index.siz... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[34]原语 assert qq by df.index.size <=0 as break with 应用已存在... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'app,name,app_type,api_num,imp_api_num,visits_num,visits_flow,sj_num,monitor_flow,first_time,dstip_num,srcip_num,account_num,sensitive_label,app_status,active,merge_state,dstip,sx,scope'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[35]原语 a = loc a by app,name,app_type,api_num,imp_api_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'api_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[36]原语 a = add api_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'imp_api_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[37]原语 a = add imp_api_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'visits_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[38]原语 a = add visits_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'visits_flow', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[39]原语 a = add visits_flow by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'sj_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[40]原语 a = add sj_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'monitor_flow', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[41]原语 a = add monitor_flow by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'first_time', 'by': 'str(datetime.now())'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[42]原语 a = add first_time by str(datetime.now()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'dstip_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[43]原语 a = add dstip_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'srcip_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[44]原语 a = add srcip_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'account_num', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[45]原语 a = add account_num by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'sensitive_label', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[46]原语 a = add sensitive_label by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'app_status', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[47]原语 a = add app_status by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'active', 'by': '3'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[48]原语 a = add active by 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'sx', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[49]原语 a = add sx by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'merge_state', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[50]原语 a = add merge_state by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'app_sum', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[51]原语 a = add app_sum by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[54]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('b',ptree)", 'as': 'alert', 'to': '保存成功！', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[55]原语 assert find_df("b",ptree) as  alert  to 保存成功！ with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'btn_show', 'by': "'1,1,1,1,0'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[56]原语 b = add btn_show by ("1,1,1,1,0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[62]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table.fbi]执行第[64]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],64

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



