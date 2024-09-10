#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_new/query_table
#datetime: 2024-08-30T16:10:58.871446
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
		add_the_error('[api_new/query_table.fea]执行第[20]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[23]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'eval', 'eval': 'a', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[24]原语 aa = eval a by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'num1', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$aa - 1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[27]原语 num1 = @sdf sys_eval with ($aa - 1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[$num1,0]'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[28]原语 tt1 = eval a by iloc[$num1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ss1', 'Action': 'if', 'if': "'$tt1' == 'visits_num' or '$tt1' == ''", 'with': 'a = filter a by index <= $num1'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=29
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[29]原语 ss1 = if "$tt1" == "visits_num" or "$tt1" == "" wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss1' == 'False'", 'with': 'num2 = @sdf sys_eval with ($aa - 2)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=30
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[30]原语 if "$ss1" == "False" with num2 = @sdf sys_eval wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss1' == 'False'", 'with': 'tt2 = eval a by iloc[$num2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=31
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[31]原语 if "$ss1" == "False" with tt2 = eval a by iloc[$nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ss2', 'Action': 'if', 'if': "'$tt2' == 'visits_num' or '$tt2' == ''", 'with': 'a = filter a by index <= $num2'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=32
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[32]原语 ss2 = if "$tt2" == "visits_num" or "$tt2" == ""  w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss2' == 'False' and '$ss1' == 'False'", 'with': 'num3 = @sdf sys_eval with ($aa - 3)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=33
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[33]原语 if "$ss2" == "False" and "$ss1" == "False" with nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss2' == 'False' and '$ss1' == 'False'", 'with': 'tt3 = eval a by iloc[$num3,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=34
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[34]原语 if "$ss2" == "False" and "$ss1" == "False" with tt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ss3', 'Action': 'if', 'if': "'$tt3' == 'visits_num' or '$tt3' == ''", 'with': 'a = filter a by index <= $num3'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=35
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[35]原语 ss3 = if "$tt3" == "visits_num" or "$tt3" == ""  w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss3' == 'False' and '$ss2' == 'False' and '$ss1' == 'False'", 'with': 'num4 = @sdf sys_eval with ($aa - 4)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=36
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[36]原语 if "$ss3" == "False" and "$ss2" == "False" and "$s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$ss3' == 'False' and '$ss2' == 'False' and '$ss1' == 'False'", 'with': 'tt4 = eval a by iloc[$num4,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[37]原语 if "$ss3" == "False" and "$ss2" == "False" and "$s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ss4', 'Action': 'if', 'if': "'$tt4' == 'visits_num' or '$tt4' == ''", 'with': 'a = filter a by index <= $num4'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=38
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[38]原语 ss4 = if "$tt4" == "visits_num" or "$tt4" == ""  w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@group_count'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[40]原语 d = load ssdb by ssdb0 with @group_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'd', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[41]原语 dd = eval d by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$dd == 0', 'with': 'b,c = @udf a by CRUD.query_mtable with (@link,@table,merge_state != 1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=45
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[45]原语 if $dd == 0 with b,c = @udf a by CRUD.query_mtable... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$dd == 1', 'with': '""\nd1 = eval d by iloc[0,0]\nb,c = @udf a by CRUD.query_mtable with (@link,@table,merge_state != 1 and $d1)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=47
		ptree['funs']=block_if_47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[47]原语 if $dd == 1 with "d1 = eval d by iloc[0,0]b,c = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$dd == 2', 'with': '""\nd1 = eval d by iloc[0,0]\nd2 = eval d by iloc[1,0]\nb,c = @udf a by CRUD.query_mtable with (@link,@table,merge_state != 1 and $d1 and $d2)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=52
		ptree['funs']=block_if_52
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[52]原语 if $dd == 2 with "d1 = eval d by iloc[0,0]d2 = eva... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$dd == 3', 'with': '""\nd1 = eval d by iloc[0,0]\nd2 = eval d by iloc[1,0]\nd3 = eval d by iloc[2,0]\nb,c = @udf a by CRUD.query_mtable with (@link,@table,merge_state != 1 and $d1 and $d2 and $d3)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=58
		ptree['funs']=block_if_58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[58]原语 if $dd == 3 with "d1 = eval d by iloc[0,0]d2 = eva... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$dd == 4', 'with': '""\nd1 = eval d by iloc[0,0]\nd2 = eval d by iloc[1,0]\nd3 = eval d by iloc[2,0]\nd4 = eval d by iloc[3,0]\nb,c = @udf a by CRUD.query_mtable with (@link,@table,merge_state != 1 and $d1 and $d2 and $d3 and $d4)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=65
		ptree['funs']=block_if_65
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[65]原语 if $dd == 4 with "d1 = eval d by iloc[0,0]d2 = eva... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'b.portrait_status.api_status', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[79]原语 alter b.portrait_status.api_status as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'btn_show', 'by': "b['portrait_status']+','+b['api_status']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[80]原语 b = add btn_show by (b["portrait_status"]+","+b["a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'b.btn_show', 'Action': 'lambda', 'lambda': 'btn_show', 'by': "x: '1,1,1,0,1,0,1' if x == '0,0' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[81]原语 b.btn_show = lambda btn_show by (x: "1,1,1,0,1,0,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'b.btn_show', 'Action': 'lambda', 'lambda': 'btn_show', 'by': "x: '1,1,1,0,0,1,1' if x == '0,1' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[82]原语 b.btn_show = lambda btn_show by (x: "1,1,1,0,0,1,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'b.btn_show', 'Action': 'lambda', 'lambda': 'btn_show', 'by': "x: '1,1,0,1,1,0,1' if x == '1,0' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[83]原语 b.btn_show = lambda btn_show by (x: "1,1,0,1,1,0,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'b.btn_show', 'Action': 'lambda', 'lambda': 'btn_show', 'by': "x: '1,1,0,1,0,1,1' if x == '1,1' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[84]原语 b.btn_show = lambda btn_show by (x: "1,1,0,1,0,1,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('b',ptree)", 'as': 'alert', 'with': '数据查询失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[87]原语 assert find_df("b",ptree) as  alert with 数据查询失败！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[89]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'c', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[90]原语 push c as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_new/query_table.fea]执行第[92]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],92

#主函数结束,开始块函数

def block_if_47(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd1', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第47行if语句中]执行第[48]原语 d1 = eval d by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_mtable', 'with': '@link,@table,merge_state != 1 and $d1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第47行if语句中]执行第[49]原语 b,c = @udf a by CRUD.query_mtable with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_47

def block_if_52(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd1', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第52行if语句中]执行第[53]原语 d1 = eval d by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[1,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第52行if语句中]执行第[54]原语 d2 = eval d by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_mtable', 'with': '@link,@table,merge_state != 1 and $d1 and $d2'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第52行if语句中]执行第[55]原语 b,c = @udf a by CRUD.query_mtable with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_52

def block_if_58(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd1', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[59]原语 d1 = eval d by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[1,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[60]原语 d2 = eval d by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd3', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[2,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[61]原语 d3 = eval d by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_mtable', 'with': '@link,@table,merge_state != 1 and $d1 and $d2 and $d3'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[62]原语 b,c = @udf a by CRUD.query_mtable with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_58

def block_if_65(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd1', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第65行if语句中]执行第[66]原语 d1 = eval d by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[1,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第65行if语句中]执行第[67]原语 d2 = eval d by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd3', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[2,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第65行if语句中]执行第[68]原语 d3 = eval d by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd4', 'Action': 'eval', 'eval': 'd', 'by': 'iloc[3,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第65行if语句中]执行第[69]原语 d4 = eval d by iloc[3,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_mtable', 'with': '@link,@table,merge_state != 1 and $d1 and $d2 and $d3 and $d4'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第65行if语句中]执行第[70]原语 b,c = @udf a by CRUD.query_mtable with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_65

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



