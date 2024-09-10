#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_portrait_data
#datetime: 2024-08-30T16:10:53.764480
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
		add_the_error('[app_portrait_data.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'applist1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app,name,sx,visits_num,visits_flow,sj_num,monitor_flow,active,app_status,first_time,portrait_time from data_app_new where app = '@app' and merge_state != 1"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[19]原语 applist1 = load db by mysql1 with select app,name,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'applist1', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[20]原语 applist1 = @udf applist1 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'applist1.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': "x:0 if x == '' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[21]原语 applist1.visits_flow = lambda visits_flow by (x:0 ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 'applist1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[22]原语 app = eval applist1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_sx', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_sx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[24]原语 app_sx = load ssdb by ssdb0 with dd:app_sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sx', 'Action': 'loc', 'loc': 'app_sx', 'by': 'index', 'to': 'sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[25]原语 app_sx = loc app_sx by index to sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 'applist1', 'by': 'visits_num,visits_flow,sj_num,monitor_flow,active,app_status,first_time,portrait_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[27]原语 s = loc applist1 by (visits_num,visits_flow,sj_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.first_time', 'Action': 'str', 'str': 'first_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[28]原语 s.first_time = str first_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.first_time', 'Action': 'str', 'str': 'first_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[29]原语 s.first_time = str first_time by (replace("T"," ")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[30]原语 s.portrait_time = str portrait_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[31]原语 s.portrait_time = str portrait_time by (replace("T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'visits_num,visits_flow,sj_num,monitor_flow,active,app_status,first_time,portrait_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[32]原语 s = loc s by (visits_num,visits_flow,sj_num,monito... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[34]原语 alter s.visits_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_num', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[35]原语 v_num = eval s by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $v_num <= 1000000000', 'with': 's.visits_num = lambda visits_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=36
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[36]原语 if 100000 < $v_num <= 1000000000 with s.visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$v_num > 1000000000', 'with': 's.visits_num = lambda visits_num by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[37]原语 if $v_num > 1000000000 with s.visits_num = lambda ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[38]原语 alter s.visits_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $v_num <= 1000000000', 'with': "s.visits_num = lambda visits_num by (x:x+'万')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=39
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[39]原语 if 100000 < $v_num <= 1000000000 with s.visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$v_num > 1000000000', 'with': "s.visits_num = lambda visits_num by (x:x+'亿')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[40]原语 if $v_num > 1000000000 with  s.visits_num = lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_flow', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[42]原语 v_flow = eval s by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $v_flow < 1048576', 'with': 's.visits_flow = lambda visits_flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=43
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[43]原语 if 1024 <= $v_flow < 1048576 with s.visits_flow = ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $v_flow < 1073741824', 'with': 's.visits_flow = lambda visits_flow by (x:round(x/1024/1024,2)))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=44
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[44]原语 if 1048576 <= $v_flow < 1073741824 with s.visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 <= $v_flow', 'with': 's.visits_flow = lambda visits_flow by (x:round(x/1024/1024/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=45
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[45]原语 if 1073741824 <= $v_flow  with s.visits_flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_flow', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[46]原语 alter s.visits_flow as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $v_flow < 1024', 'with': "s.visits_flow = lambda visits_flow by (x:x+'(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[47]原语 if 0 <= $v_flow < 1024 with s.visits_flow = lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $v_flow < 1048576', 'with': "s.visits_flow = lambda visits_flow by (x:x+'(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=48
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[48]原语 if 1024 <= $v_flow < 1048576 with s.visits_flow = ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $v_flow < 1073741824', 'with': "s.visits_flow = lambda visits_flow by (x:x+'(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=49
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[49]原语 if 1048576 <= $v_flow < 1073741824 with s.visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 <= $v_flow', 'with': "s.visits_flow = lambda visits_flow by (x:x+'(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=50
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[50]原语 if 1073741824 <= $v_flow  with s.visits_flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.sj_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[52]原语 alter s.sj_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_num', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[53]原语 v_num = eval s by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $v_num <= 1000000000', 'with': 's.sj_num = lambda sj_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=54
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[54]原语 if 100000 < $v_num <= 1000000000 with s.sj_num = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$v_num > 1000000000', 'with': 's.sj_num = lambda sj_num by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=55
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[55]原语 if $v_num > 1000000000 with s.sj_num = lambda sj_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.sj_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[56]原语 alter s.sj_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $v_num <= 1000000000', 'with': "s.sj_num = lambda sj_num by (x:x+'万')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=57
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[57]原语 if 100000 < $v_num <= 1000000000 with s.sj_num = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$v_num > 1000000000', 'with': "s.sj_num = lambda sj_num by (x:x+'亿')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[58]原语 if $v_num > 1000000000 with  s.sj_num = lambda sj_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_flow1', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[60]原语 v_flow1 = eval s by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $v_flow1 < 1048576', 'with': 's.monitor_flow = lambda monitor_flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=61
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[61]原语 if 1024 <= $v_flow1 < 1048576 with s.monitor_flow ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $v_flow1 < 1073741824', 'with': 's.monitor_flow = lambda monitor_flow by (x:round(x/1024/1024,2)))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=62
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[62]原语 if 1048576 <= $v_flow1 < 1073741824 with s.monitor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 <= $v_flow1', 'with': 's.monitor_flow = lambda monitor_flow by (x:round(x/1024/1024/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=63
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[63]原语 if 1073741824 <= $v_flow1  with s.monitor_flow = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.monitor_flow', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[64]原语 alter s.monitor_flow as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $v_flow1 < 1024', 'with': "s.monitor_flow = lambda monitor_flow by (x:x+'(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=65
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[65]原语 if 0 <= $v_flow1 < 1024 with s.monitor_flow = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $v_flow1 < 1048576', 'with': "s.monitor_flow = lambda monitor_flow by (x:x+'(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=66
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[66]原语 if 1024 <= $v_flow1 < 1048576 with s.monitor_flow ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $v_flow1 < 1073741824', 'with': "s.monitor_flow = lambda monitor_flow by (x:x+'(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=67
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[67]原语 if 1048576 <= $v_flow1 < 1073741824 with s.monitor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 <= $v_flow1', 'with': "s.monitor_flow = lambda monitor_flow by (x:x+'(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=68
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[68]原语 if 1073741824 <= $v_flow1  with s.monitor_flow = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.active', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[69]原语 alter s.active as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.app_status', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[70]原语 alter s.app_status as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[71]原语 alter s.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.app_status', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[72]原语 alter s.app_status as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[74]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's,active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[75]原语 s = @udf s,active by SP.tag2dict with active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-status'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[77]原语 type = load ssdb by ssdb0 with dd:API-status 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's,type', 'by': 'SP.tag2dict', 'with': 'app_status'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[78]原语 s = @udf s,type by SP.tag2dict with app_status 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'by': '"visits_num":"访问量","visits_flow":"访问流量","sj_num":"审计访问量","monitor_flow":"审计流量","active":"活跃状态","app_status":"审计状态","first_time":"首次发现时间","portrait_time":"画像开启时间"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[79]原语 rename s by ("visits_num":"访问量","visits_flow":"访问流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[80]原语 s = @udf s by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'index', 'to': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[81]原语 s = loc s by index to name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'icon', 'by': "'F396','F352','F307','F146','F019','F298','F306','F150'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[82]原语 s = add icon by ("F396","F352","F307","F146","F019... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'as': "0:'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[83]原语 rename s as (0:"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'pageid', 'by': "'','','','','','','',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[84]原语 s = add pageid by ("","","","","","","","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': '参数', 'by': "'','','','','','','',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[85]原语 s = add 参数 by ("","","","","","","","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'name,value,icon,pageid,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[86]原语 s = loc s by name,value,icon,pageid,参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'z:@app:profile'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[87]原语 store s to ssdb with z:@app:profile 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'name1', 'Action': 'loc', 'loc': 'applist1', 'by': 'app,name,sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[90]原语 name1 = loc applist1 by app,name,sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'name1', 'by': '"app":"应用IP/域名"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[91]原语 rename name1 by ("app":"应用IP/域名") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'name1', 'by': '"name":"应用别名"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[92]原语 rename name1 by ("name":"应用别名") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'name1.sx', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[93]原语 alter name1.sx as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_sx.sx', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[94]原语 alter app_sx.sx as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'name1', 'Action': 'join', 'join': 'name1,app_sx', 'by': 'sx,sx', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[95]原语 name1 = join name1,app_sx by sx,sx with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'name1', 'Action': 'loc', 'loc': 'name1', 'drop': 'sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[96]原语 name1 = loc name1 drop sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'name1', 'by': '"sysname":"关联应用"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[97]原语 rename name1 by ("sysname":"关联应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'name1', 'to': 'ssdb', 'with': 'z:@app:name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[98]原语 store name1 to ssdb with z:@app:name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_portrait_data.fbi]执行第[101]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],101

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



