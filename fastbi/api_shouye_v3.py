#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_shouye
#datetime: 2024-08-30T16:10:54.453127
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
		add_the_error('[api_shouye.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[16]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[api_shouye.fbi]执行第[17]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[17]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[20]原语 day = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[21]原语 day = @sdf format_now with ($day,"%Y-%m-%d 00:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),19) as min_time,left(toString(max(time)),19) as max_time from api_visit_hour where time >= toDateTime('$day')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[23]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=24
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[24]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit1', 'by': 'visit_count:int,flow:int,min_time:str,max_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[25]原语 alter visit1 by visit_count:int,flow:int,min_time:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'max_visit1', 'Action': 'loc', 'loc': 'visit1', 'by': 'min_time,visit_count,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[26]原语 max_visit1 = loc visit1 by min_time,visit_count,fl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'max_visit1', 'as': "'min_time':'day'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[27]原语 rename max_visit1 as ("min_time":"day") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'max_visit1.day', 'Action': 'str', 'str': 'day', 'by': 'slice(0,10)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[28]原语 max_visit1.day = str day by (slice(0,10)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't_visit1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[29]原语 t_visit1 = loc visit1 by visit_count,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[33]原语 visit_1 = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_1', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[34]原语 rename visit_1 as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[35]原语 aa_num = eval visit_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_1 = add name by ('总访问量')"}
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
		add_the_error('[api_shouye.fbi]执行第[36]原语 if $aa_num < 100000 with visit_1 = add name by ("总... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/10000,2))'}
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
		add_the_error('[api_shouye.fbi]执行第[37]原语 if 100000 <= $aa_num < 1000000000 with visit_1.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_1 = add name by ('总访问量(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=38
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[38]原语 if 100000 <= $aa_num < 1000000000 with visit_1 = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/100000000,2))'}
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
		add_the_error('[api_shouye.fbi]执行第[39]原语 if $aa_num >= 1000000000 with visit_1.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_1 = add name by ('总访问量(亿次)')"}
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
		add_the_error('[api_shouye.fbi]执行第[40]原语 if $aa_num >= 1000000000 with visit_1 = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[41]原语 visit_1 = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[42]原语 tt1 = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt2', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[43]原语 tt2 = eval visit1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'details', 'by': '"自$tt1至$tt2以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[44]原语 visit_1 = add details by ("自$tt1至$tt2以来的总访问次数(HTTP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit_1', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[45]原语 visit_1 = loc visit_1 by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[49]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[50]原语 aa_num = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $aa_num < 1024', 'with': "flow = add name by ('应用总流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=51
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[51]原语 if 0 <= $aa_num < 1024  with flow = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': 'flow.flow = lambda flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=52
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[52]原语 if 1024 <= $aa_num < 1048576  with flow.flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': "flow = add name by ('应用总流量(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=53
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[53]原语 if 1024 <= $aa_num < 1048576  with flow = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': 'flow.flow = lambda flow by (x:round(x/1048576,2))'}
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
		add_the_error('[api_shouye.fbi]执行第[54]原语 if 1048576 <= $aa_num < 1073741824  with flow.flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': "flow = add name by ('应用总流量(M)')"}
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
		add_the_error('[api_shouye.fbi]执行第[55]原语 if 1048576 <= $aa_num < 1073741824  with flow = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=56
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[56]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow = add name by ('应用总流量(G)')"}
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
		add_the_error('[api_shouye.fbi]执行第[57]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1099511627776,2))'}
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
		add_the_error('[api_shouye.fbi]执行第[58]原语 if $aa_num > 10995116277760 with flow.flow = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow = add name by ('应用总流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=59
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[59]原语 if $aa_num > 10995116277760 with flow = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[60]原语 rename flow as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'icon', 'by': "'F352'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[61]原语 flow = add icon by ("F352") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'details', 'by': "'自$tt1至$tt2以来的总访问流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[62]原语 flow = add details by ("自$tt1至$tt2以来的总访问流量(HTTP协议)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'flow', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[64]原语 flow = loc flow by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'max_visit1 = @udf max_visit1 by udf0.df_append with (,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=66
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[66]原语 if max_visit1.index.size == 0 with max_visit1 = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'visit_count', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[67]原语 visit_m = order max_visit1 by visit_count with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[68]原语 dd = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[69]原语 visit_m = loc visit_m by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_m', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[70]原语 rename visit_m as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[71]原语 aa_num = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_m = add name by ('日最大访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=72
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[72]原语 if $aa_num < 100000 with visit_m = add name by ("日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=73
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[73]原语 if 100000 <= $aa_num < 1000000000 with visit_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_m = add name by ('日最大访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=74
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[74]原语 if 100000 <= $aa_num < 1000000000 with visit_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=75
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[75]原语 if $aa_num >= 1000000000 with visit_m.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_m = add name by ('日最大访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=76
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[76]原语 if $aa_num >= 1000000000 with visit_m = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[77]原语 visit_m = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大访问量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[78]原语 visit_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'flow', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[80]原语 flow_m = order max_visit1 by flow with desc limit ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[81]原语 dd = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_m', 'Action': 'loc', 'loc': 'flow_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[82]原语 flow_m = loc flow_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_m', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[83]原语 rename flow_m as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[84]原语 aa_num = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_m = add name by ('日最大流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=85
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[85]原语 if $aa_num <= 1024 with flow_m = add name by ("日最大... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_m.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=86
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[86]原语 if 1024 < $aa_num <= 1048576 with flow_m.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_m = add name by ('日最大流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=87
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[87]原语 if 1024 < $aa_num <= 1048576 with flow_m = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_m.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=88
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[88]原语 if 1048576 < $aa_num <= 1073741824 with flow_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_m = add name by ('日最大流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=89
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[89]原语 if 1048576 < $aa_num <= 1073741824 with flow_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=90
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[90]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_m = add name by ('日最大流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=91
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[91]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=92
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[92]原语 if $aa_num > 10995116277760 with flow_m.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_m = add name by ('日最大流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=93
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[93]原语 if $aa_num > 10995116277760 with flow_m = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'icon', 'by': "'F159'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[94]原语 flow_m = add icon by ("F159") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[95]原语 flow_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大流量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_t', 'Action': 'loc', 'loc': 't_visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[97]原语 visit_t = loc t_visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_t', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[98]原语 rename visit_t as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_t', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[99]原语 aa_num = eval visit_t by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_t = add name by ('今日访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=100
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[100]原语 if $aa_num < 100000 with visit_t = add name by ("今... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 100000000', 'with': 'visit_t.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=101
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[101]原语 if 100000 <= $aa_num < 100000000 with visit_t.valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 100000000', 'with': "visit_t = add name by ('今日访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=102
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[102]原语 if 100000 <= $aa_num < 100000000 with visit_t = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 100000000', 'with': 'visit_t.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=103
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[103]原语 if $aa_num >= 100000000 with visit_t.value = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 100000000', 'with': "visit_t = add name by ('今日访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=104
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[104]原语 if $aa_num >= 100000000 with visit_t = add name by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_t', 'Action': 'add', 'add': 'icon', 'by': "'F171'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[105]原语 visit_t = add icon by ("F171") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_t', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[106]原语 visit_t = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_t', 'Action': 'loc', 'loc': 't_visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[108]原语 flow_t = loc t_visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_t', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[109]原语 rename flow_t as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_t', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[110]原语 aa_num = eval flow_t by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_t = add name by ('今日流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=111
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[111]原语 if $aa_num <= 1024 with flow_t = add name by ("今日流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_t.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=112
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[112]原语 if 1024 < $aa_num <= 1048576 with flow_t.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_t = add name by ('今日流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=113
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[113]原语 if 1024 < $aa_num <= 1048576 with flow_t = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_t.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=114
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[114]原语 if 1048576 < $aa_num <= 1073741824 with flow_t.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_t = add name by ('今日流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=115
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[115]原语 if 1048576 < $aa_num <= 1073741824 with flow_t = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_t.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=116
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[116]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_t = add name by ('今日流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=117
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[117]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_t.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=118
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[118]原语 if $aa_num > 10995116277760 with flow_t.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_t = add name by ('今日流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=119
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[119]原语 if $aa_num > 10995116277760 with flow_t = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_t', 'Action': 'add', 'add': 'icon', 'by': "'F172'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[120]原语 flow_t = add icon by ("F172") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_t', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[121]原语 flow_t = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tj', 'Action': 'union', 'union': 'visit_1,flow,visit_m,flow_m,visit_t,flow_t'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[123]原语 tj = union visit_1,flow,visit_m,flow_m,visit_t,flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tj', 'Action': 'loc', 'loc': 'tj', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[124]原语 tj = loc tj by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tj', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days:tj_zdy_天'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[125]原语 store tj to ssdb by ssdb0 with visit_days:tj_zdy_天... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-0 week'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[128]原语 week = @sdf sys_now with -0 week 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$week,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[129]原语 week = @sdf format_now with ($week,"%Y-%m-%d 00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),10) as min_time,left(toString(max(time)),10) as max_time from api_visit_hour where time >= toDateTime('$week')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[131]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=132
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[132]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit1', 'by': 'visit_count:int,flow:int,min_time:str,max_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[133]原语 alter visit1 by visit_count:int,flow:int,min_time:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'max_visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select left(toString(time),10) as day,sum(visit_num) as visit_count,sum(visit_flow) as flow from api_visit_hour where time >= toDateTime('$week') group by day"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[134]原语 max_visit1 = load ckh by ckh with select left(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'max_visit1', 'by': 'visit_count:int,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[135]原语 alter max_visit1 by visit_count:int,flow:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[138]原语 visit_1 = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_1', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[139]原语 rename visit_1 as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[140]原语 aa_num = eval visit_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_1 = add name by ('总访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=141
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[141]原语 if $aa_num < 100000 with visit_1 = add name by ("总... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=142
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[142]原语 if 100000 <= $aa_num < 1000000000 with visit_1.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_1 = add name by ('总访问量(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=143
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[143]原语 if 100000 <= $aa_num < 1000000000 with visit_1 = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=144
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[144]原语 if $aa_num >= 1000000000 with visit_1.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_1 = add name by ('总访问量(亿次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=145
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[145]原语 if $aa_num >= 1000000000 with visit_1 = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[146]原语 visit_1 = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[147]原语 tt1 = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt2', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[148]原语 tt2 = eval visit1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'details', 'by': '"自$tt1至$tt2以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[149]原语 visit_1 = add details by ("自$tt1至$tt2以来的总访问次数(HTTP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit_1', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[150]原语 visit_1 = loc visit_1 by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[153]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[154]原语 aa_num = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $aa_num < 1024', 'with': "flow = add name by ('应用总流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=155
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[155]原语 if 0 <= $aa_num < 1024  with flow = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': 'flow.flow = lambda flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=156
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[156]原语 if 1024 <= $aa_num < 1048576  with flow.flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': "flow = add name by ('应用总流量(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=157
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[157]原语 if 1024 <= $aa_num < 1048576  with flow = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': 'flow.flow = lambda flow by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=158
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[158]原语 if 1048576 <= $aa_num < 1073741824  with flow.flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': "flow = add name by ('应用总流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=159
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[159]原语 if 1048576 <= $aa_num < 1073741824  with flow = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=160
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[160]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow = add name by ('应用总流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=161
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[161]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=162
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[162]原语 if $aa_num > 10995116277760 with flow.flow = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow = add name by ('应用总流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=163
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[163]原语 if $aa_num > 10995116277760 with flow = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[164]原语 rename flow as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'icon', 'by': "'F352'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[165]原语 flow = add icon by ("F352") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'details', 'by': "'自$tt1至$tt2以来的总访问流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[166]原语 flow = add details by ("自$tt1至$tt2以来的总访问流量(HTTP协议)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'flow', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[168]原语 flow = loc flow by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'max_visit1 = @udf max_visit1 by udf0.df_append with (,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=170
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[170]原语 if max_visit1.index.size == 0 with max_visit1 = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'alter max_visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=171
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[171]原语 if max_visit1.index.size == 0 with alter max_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'visit_count', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[172]原语 visit_m = order max_visit1 by visit_count with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[173]原语 dd = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[174]原语 visit_m = loc visit_m by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_m', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[175]原语 rename visit_m as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[176]原语 aa_num = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_m = add name by ('日最大访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=177
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[177]原语 if $aa_num < 100000 with visit_m = add name by ("日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=178
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[178]原语 if 100000 <= $aa_num < 1000000000 with visit_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_m = add name by ('日最大访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=179
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[179]原语 if 100000 <= $aa_num < 1000000000 with visit_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=180
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[180]原语 if $aa_num >= 1000000000 with visit_m.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_m = add name by ('日最大访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=181
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[181]原语 if $aa_num >= 1000000000 with visit_m = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[182]原语 visit_m = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大访问量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[183]原语 visit_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'flow', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[185]原语 flow_m = order max_visit1 by flow with desc limit ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[186]原语 dd = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_m', 'Action': 'loc', 'loc': 'flow_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[187]原语 flow_m = loc flow_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_m', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[188]原语 rename flow_m as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[189]原语 aa_num = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_m = add name by ('日最大流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=190
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[190]原语 if $aa_num <= 1024 with flow_m = add name by ("日最大... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_m.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=191
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[191]原语 if 1024 < $aa_num <= 1048576 with flow_m.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_m = add name by ('日最大流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=192
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[192]原语 if 1024 < $aa_num <= 1048576 with flow_m = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_m.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=193
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[193]原语 if 1048576 < $aa_num <= 1073741824 with flow_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_m = add name by ('日最大流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=194
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[194]原语 if 1048576 < $aa_num <= 1073741824 with flow_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=195
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[195]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_m = add name by ('日最大流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=196
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[196]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=197
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[197]原语 if $aa_num > 10995116277760 with flow_m.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_m = add name by ('日最大流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=198
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[198]原语 if $aa_num > 10995116277760 with flow_m = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'icon', 'by': "'F159'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[199]原语 flow_m = add icon by ("F159") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[200]原语 flow_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大流量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tj', 'Action': 'union', 'union': 'visit_1,flow,visit_m,flow_m,visit_t,flow_t'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[202]原语 tj = union visit_1,flow,visit_m,flow_m,visit_t,flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tj', 'Action': 'loc', 'loc': 'tj', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[203]原语 tj = loc tj by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tj', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days:tj_zdy_周'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[204]原语 store tj to ssdb by ssdb0 with visit_days:tj_zdy_周... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1 month'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[207]原语 month = @sdf sys_now with -1 month 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[208]原语 month = @sdf format_now with ($month,"%Y-%m-%d 00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),10) as min_time,left(toString(max(time)),10) as max_time from api_visit_hour where time >= toDateTime('$month')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[210]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=211
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[211]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit1', 'by': 'visit_count:int,flow:int,min_time:str,max_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[212]原语 alter visit1 by visit_count:int,flow:int,min_time:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'max_visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select left(toString(time),10) as day,sum(visit_num) visit_count,sum(visit_flow) as flow from api_visit_hour where time >= toDateTime('$month') group by day"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[213]原语 max_visit1 = load ckh by ckh with select left(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'max_visit1', 'by': 'visit_count:int,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[214]原语 alter max_visit1 by visit_count:int,flow:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[217]原语 visit_1 = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_1', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[218]原语 rename visit_1 as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[219]原语 aa_num = eval visit_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_1 = add name by ('总访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=220
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[220]原语 if $aa_num < 100000 with visit_1 = add name by ("总... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=221
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[221]原语 if 100000 <= $aa_num < 1000000000 with visit_1.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_1 = add name by ('总访问量(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=222
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[222]原语 if 100000 <= $aa_num < 1000000000 with visit_1 = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=223
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[223]原语 if $aa_num >= 1000000000 with visit_1.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_1 = add name by ('总访问量(亿次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=224
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[224]原语 if $aa_num >= 1000000000 with visit_1 = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[225]原语 visit_1 = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[226]原语 tt1 = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt2', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[227]原语 tt2 = eval visit1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'details', 'by': '"自$tt1至$tt2以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[228]原语 visit_1 = add details by ("自$tt1至$tt2以来的总访问次数(HTTP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit_1', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[229]原语 visit_1 = loc visit_1 by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[232]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[233]原语 aa_num = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $aa_num < 1024', 'with': "flow = add name by ('应用总流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=234
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[234]原语 if 0 <= $aa_num < 1024  with flow = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': 'flow.flow = lambda flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=235
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[235]原语 if 1024 <= $aa_num < 1048576  with flow.flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': "flow = add name by ('应用总流量(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=236
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[236]原语 if 1024 <= $aa_num < 1048576  with flow = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': 'flow.flow = lambda flow by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=237
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[237]原语 if 1048576 <= $aa_num < 1073741824  with flow.flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': "flow = add name by ('应用总流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=238
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[238]原语 if 1048576 <= $aa_num < 1073741824  with flow = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=239
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[239]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow = add name by ('应用总流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=240
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[240]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=241
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[241]原语 if $aa_num > 10995116277760 with flow.flow = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow = add name by ('应用总流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=242
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[242]原语 if $aa_num > 10995116277760 with flow = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[243]原语 rename flow as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'icon', 'by': "'F352'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[244]原语 flow = add icon by ("F352") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'details', 'by': "'自$tt1至$tt2以来的总访问流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[245]原语 flow = add details by ("自$tt1至$tt2以来的总访问流量(HTTP协议)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'flow', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[247]原语 flow = loc flow by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'max_visit1 = @udf max_visit1 by udf0.df_append with (,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=249
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[249]原语 if max_visit1.index.size == 0 with max_visit1 = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'alter max_visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=250
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[250]原语 if max_visit1.index.size == 0 with alter max_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'visit_count', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[251]原语 visit_m = order max_visit1 by visit_count with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[252]原语 dd = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[253]原语 visit_m = loc visit_m by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_m', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[254]原语 rename visit_m as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[255]原语 aa_num = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_m = add name by ('日最大访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=256
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[256]原语 if $aa_num < 100000 with visit_m = add name by ("日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=257
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[257]原语 if 100000 <= $aa_num < 1000000000 with visit_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_m = add name by ('日最大访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=258
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[258]原语 if 100000 <= $aa_num < 1000000000 with visit_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=259
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[259]原语 if $aa_num >= 1000000000 with visit_m.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_m = add name by ('日最大访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=260
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[260]原语 if $aa_num >= 1000000000 with visit_m = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[261]原语 visit_m = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大访问量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[262]原语 visit_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'flow', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[264]原语 flow_m = order max_visit1 by flow with desc limit ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[265]原语 dd = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_m', 'Action': 'loc', 'loc': 'flow_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[266]原语 flow_m = loc flow_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_m', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[267]原语 rename flow_m as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[268]原语 aa_num = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_m = add name by ('日最大流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=269
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[269]原语 if $aa_num <= 1024 with flow_m = add name by ("日最大... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_m.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=270
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[270]原语 if 1024 < $aa_num <= 1048576 with flow_m.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_m = add name by ('日最大流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=271
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[271]原语 if 1024 < $aa_num <= 1048576 with flow_m = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_m.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=272
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[272]原语 if 1048576 < $aa_num <= 1073741824 with flow_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_m = add name by ('日最大流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=273
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[273]原语 if 1048576 < $aa_num <= 1073741824 with flow_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=274
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[274]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_m = add name by ('日最大流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=275
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[275]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=276
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[276]原语 if $aa_num > 10995116277760 with flow_m.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_m = add name by ('日最大流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=277
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[277]原语 if $aa_num > 10995116277760 with flow_m = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'icon', 'by': "'F159'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[278]原语 flow_m = add icon by ("F159") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[279]原语 flow_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大流量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tj', 'Action': 'union', 'union': 'visit_1,flow,visit_m,flow_m,visit_t,flow_t'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[281]原语 tj = union visit_1,flow,visit_m,flow_m,visit_t,flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tj', 'Action': 'loc', 'loc': 'tj', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[282]原语 tj = loc tj by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tj', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days:tj_zdy_月'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[283]原语 store tj to ssdb by ssdb0 with visit_days:tj_zdy_月... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'year', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-0 year'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[286]原语 year = @sdf sys_now with -0 year 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'year', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$year,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[287]原语 year = @sdf format_now with ($year,"%Y-%m-%d 00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),10) as min_time,left(toString(max(time)),10) as max_time from api_visit_hour where time >= toDateTime('$year')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[289]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=290
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[290]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit1', 'by': 'visit_count:int,flow:int,min_time:str,max_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[291]原语 alter visit1 by visit_count:int,flow:int,min_time:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'max_visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select left(toString(time),10) as day,sum(visit_num) as visit_count,sum(visit_flow) as flow from api_visit_hour where time >= toDateTime('$year') group by day"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[292]原语 max_visit1 = load ckh by ckh with select left(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'max_visit1', 'by': 'visit_count:int,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[293]原语 alter max_visit1 by visit_count:int,flow:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[296]原语 visit_1 = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_1', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[297]原语 rename visit_1 as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[298]原语 aa_num = eval visit_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_1 = add name by ('总访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=299
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[299]原语 if $aa_num < 100000 with visit_1 = add name by ("总... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=300
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[300]原语 if 100000 <= $aa_num < 1000000000 with visit_1.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_1 = add name by ('总访问量(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=301
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[301]原语 if 100000 <= $aa_num < 1000000000 with visit_1 = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=302
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[302]原语 if $aa_num >= 1000000000 with visit_1.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_1 = add name by ('总访问量(亿次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=303
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[303]原语 if $aa_num >= 1000000000 with visit_1 = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[304]原语 visit_1 = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[305]原语 tt1 = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt2', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[306]原语 tt2 = eval visit1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'details', 'by': '"自$tt1至$tt2以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[307]原语 visit_1 = add details by ("自$tt1至$tt2以来的总访问次数(HTTP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit_1', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[308]原语 visit_1 = loc visit_1 by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[311]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[312]原语 aa_num = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $aa_num < 1024', 'with': "flow = add name by ('应用总流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=313
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[313]原语 if 0 <= $aa_num < 1024  with flow = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': 'flow.flow = lambda flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=314
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[314]原语 if 1024 <= $aa_num < 1048576  with flow.flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': "flow = add name by ('应用总流量(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=315
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[315]原语 if 1024 <= $aa_num < 1048576  with flow = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': 'flow.flow = lambda flow by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=316
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[316]原语 if 1048576 <= $aa_num < 1073741824  with flow.flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': "flow = add name by ('应用总流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=317
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[317]原语 if 1048576 <= $aa_num < 1073741824  with flow = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=318
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[318]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow = add name by ('应用总流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=319
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[319]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=320
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[320]原语 if $aa_num > 10995116277760 with flow.flow = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow = add name by ('应用总流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=321
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[321]原语 if $aa_num > 10995116277760 with flow = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[322]原语 rename flow as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'icon', 'by': "'F352'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[323]原语 flow = add icon by ("F352") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'details', 'by': "'自$tt1至$tt2以来的总访问流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[324]原语 flow = add details by ("自$tt1至$tt2以来的总访问流量(HTTP协议)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'flow', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[326]原语 flow = loc flow by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'max_visit1 = @udf max_visit1 by udf0.df_append with (,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=328
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[328]原语 if max_visit1.index.size == 0 with max_visit1 = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'alter max_visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=329
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[329]原语 if max_visit1.index.size == 0 with alter max_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'visit_count', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[330]原语 visit_m = order max_visit1 by visit_count with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[331]原语 dd = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[332]原语 visit_m = loc visit_m by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_m', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[333]原语 rename visit_m as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[334]原语 aa_num = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_m = add name by ('日最大访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=335
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[335]原语 if $aa_num < 100000 with visit_m = add name by ("日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=336
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[336]原语 if 100000 <= $aa_num < 1000000000 with visit_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_m = add name by ('日最大访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=337
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[337]原语 if 100000 <= $aa_num < 1000000000 with visit_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=338
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[338]原语 if $aa_num >= 1000000000 with visit_m.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_m = add name by ('日最大访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=339
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[339]原语 if $aa_num >= 1000000000 with visit_m = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[340]原语 visit_m = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大访问量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[341]原语 visit_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'flow', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[343]原语 flow_m = order max_visit1 by flow with desc limit ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[344]原语 dd = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_m', 'Action': 'loc', 'loc': 'flow_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[345]原语 flow_m = loc flow_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_m', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[346]原语 rename flow_m as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[347]原语 aa_num = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_m = add name by ('日最大流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=348
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[348]原语 if $aa_num <= 1024 with flow_m = add name by ("日最大... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_m.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=349
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[349]原语 if 1024 < $aa_num <= 1048576 with flow_m.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_m = add name by ('日最大流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=350
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[350]原语 if 1024 < $aa_num <= 1048576 with flow_m = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_m.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=351
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[351]原语 if 1048576 < $aa_num <= 1073741824 with flow_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_m = add name by ('日最大流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=352
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[352]原语 if 1048576 < $aa_num <= 1073741824 with flow_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=353
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[353]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_m = add name by ('日最大流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=354
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[354]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=355
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[355]原语 if $aa_num > 10995116277760 with flow_m.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_m = add name by ('日最大流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=356
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[356]原语 if $aa_num > 10995116277760 with flow_m = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'icon', 'by': "'F159'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[357]原语 flow_m = add icon by ("F159") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[358]原语 flow_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大流量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tj', 'Action': 'union', 'union': 'visit_1,flow,visit_m,flow_m,visit_t,flow_t'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[360]原语 tj = union visit_1,flow,visit_m,flow_m,visit_t,flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tj', 'Action': 'loc', 'loc': 'tj', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[361]原语 tj = loc tj by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tj', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days:tj_zdy_年'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[362]原语 store tj to ssdb by ssdb0 with visit_days:tj_zdy_年... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_shouye.fbi]执行第[365]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],365

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



