#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: hour_visit
#datetime: 2024-08-30T16:10:54.394967
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
	
	
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'k', 'Action': '@sdf', '@sdf': 'sys_timestamp'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[10]原语 k = @sdf sys_timestamp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[12]原语 hour = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'b', 'with': 'name=$1', 'run': '""\n##取出已处理的数据\nhour_1 = load pq by @name\nhour = union hour,hour_1\n##删除已经处理过的数据\nbb = @udf ZFile.rm_file with @name\n""'}
	try:
		ptree['lineno']=13
		ptree['funs']=block_foreach_13
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[13]原语 foreach b run "##取出已处理的数据hour_1 = load pq by @name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'hour', 'Action': 'group', 'group': 'hour', 'by': 'app,url,srcip,dstip,account', 'agg': 'visit_num:sum,visit_flow:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[22]原语 hour = group hour by app,url,srcip,dstip,account a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'hour', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[23]原语 hour = @udf hour by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'hour', 'as': "'visit_num_sum':'visit_num','visit_flow_sum':'visit_flow','time_max':'time'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[24]原语 rename hour as ("visit_num_sum":"visit_num","visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'hour', 'Action': 'order', 'order': 'hour', 'by': 'visit_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[25]原语 hour = order hour by visit_num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct app from data_app_new where portrait_status = 1 and app_type = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[28]原语 app = load db by mysql1 with select distinct app f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct url from data_api_new where portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[29]原语 api = load db by mysql1 with select distinct url f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct srcip from data_ip_new where portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[30]原语 ip = load db by mysql1 with select distinct srcip ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct account from data_account_new where portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[31]原语 account = load db by mysql1 with select distinct a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'hx1', 'Action': 'join', 'join': 'app,hour', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[32]原语 hx1 = join app,hour by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'hx2', 'Action': 'join', 'join': 'api,hour', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[33]原语 hx2 = join api,hour by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'hx3', 'Action': 'join', 'join': 'ip,hour', 'by': 'srcip,srcip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[34]原语 hx3 = join ip,hour by srcip,srcip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'hx4', 'Action': 'join', 'join': 'account,hour', 'by': 'account,account', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[35]原语 hx4 = join account,hour by account,account with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'hx', 'Action': 'union', 'union': 'hx1,hx2,hx3,hx4'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[36]原语 hx = union hx1,hx2,hx3,hx4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'hx', 'Action': 'distinct', 'distinct': 'hx', 'by': 'app,url,srcip,dstip,account,visit_num,visit_flow,time'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[37]原语 hx = distinct hx by app,url,srcip,dstip,account,vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hx.time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[38]原语 alter hx.time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hx', 'Action': '@udf', '@udf': 'hx', 'by': 'udf0.df_fillna_cols', 'with': "app:'',url:'',srcip:'',dstip:'',account:'',visit_num:0,visit_flow:0,time:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[39]原语 hx = @udf hx by udf0.df_fillna_cols with app:"",ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'hx', 'Action': 'filter', 'filter': 'hx', 'by': "time != '' and app != '' and url != '' and srcip != '' and dstip != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[40]原语 hx = filter hx by time != "" and app != "" and url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hx', 'by': 'visit_num:int,visit_flow:int,time:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[41]原语 alter hx by visit_num:int,visit_flow:int,time:date... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'hx.index.size != 0', 'with': 'store hx to ckh by ckh with api_hx'}
	try:
		ptree['lineno']=42
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[42]原语 if hx.index.size != 0 with store hx to ckh by ckh ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'hour', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[45]原语 num = eval hour by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '50000 <= $num <= 100000', 'with': 'num1 = @sdf sys_eval with (($num-50000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[47]原语 if 50000 <= $num <= 100000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '50000 <= $num <= 100000', 'with': 'hour1 = limit hour by 50000'}
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
		add_the_error('[hour_visit.fbi]执行第[48]原语 if 50000 <= $num <= 100000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $num <= 200000', 'with': 'num1 = @sdf sys_eval with (($num-100000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=49
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[49]原语 if 100000 < $num <= 200000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 < $num <= 200000', 'with': 'hour1 = limit hour by 100000'}
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
		add_the_error('[hour_visit.fbi]执行第[50]原语 if 100000 < $num <= 200000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '200000 < $num <= 300000', 'with': 'num1 = @sdf sys_eval with (($num-150000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=51
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[51]原语 if 200000 < $num <= 300000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '200000 < $num <= 300000', 'with': 'hour1 = limit hour by 150000'}
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
		add_the_error('[hour_visit.fbi]执行第[52]原语 if 200000 < $num <= 300000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '300000 < $num <= 400000', 'with': 'num1 = @sdf sys_eval with (($num-200000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=53
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[53]原语 if 300000 < $num <= 400000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '300000 < $num <= 400000', 'with': 'hour1 = limit hour by 200000'}
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
		add_the_error('[hour_visit.fbi]执行第[54]原语 if 300000 < $num <= 400000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '400000 < $num <= 500000', 'with': 'num1 = @sdf sys_eval with (($num-250000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=55
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[55]原语 if 400000 < $num <= 500000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '400000 < $num <= 500000', 'with': 'hour1 = limit hour by 250000'}
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
		add_the_error('[hour_visit.fbi]执行第[56]原语 if 400000 < $num <= 500000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '500000 < $num <= 600000', 'with': 'num1 = @sdf sys_eval with (($num-300000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=57
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[57]原语 if 500000 < $num <= 600000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '500000 < $num <= 600000', 'with': 'hour1 = limit hour by 300000'}
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
		add_the_error('[hour_visit.fbi]执行第[58]原语 if 500000 < $num <= 600000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '600000 < $num <= 700000', 'with': 'num1 = @sdf sys_eval with (($num-350000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=59
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[59]原语 if 600000 < $num <= 700000 with num1 = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '600000 < $num <= 700000', 'with': 'hour1 = limit hour by 350000'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=60
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[60]原语 if 600000 < $num <= 700000 with hour1 = limit hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num > 700000', 'with': 'num1 = @sdf sys_eval with (($num-400000)*-1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=61
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[61]原语 if $num > 700000 with num1 = @sdf sys_eval with ((... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num > 700000', 'with': 'hour1 = limit hour by 400000'}
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
		add_the_error('[hour_visit.fbi]执行第[62]原语 if $num > 700000 with hour1 = limit hour by 400000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num > 50000', 'with': '""\nhour2 = limit hour by $num1\nhour2 = add hh by 1\nhour2 = group hour2 by hh agg visit_num:sum,visit_flow:sum,time:max\nalter hour2 by visit_num_sum:int,visit_flow_sum:int,time_max:datetime64\nvisit_num = eval hour2 by iloc[0,0]\nvisit_flow = eval hour2 by iloc[0,1]\ntime = eval hour2 by iloc[0,2]\nhour = @udf hour1 by udf0.df_append with (sum1,sum1,sum1,sum1,sum1,$visit_num,$visit_flow,$time)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=64
		ptree['funs']=block_if_64
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[64]原语 if $num > 50000 with "hour2 = limit hour by $num1h... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour', 'by': 'visit_num:int,visit_flow:int,time:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[75]原语 alter hour by visit_num:int,visit_flow:int,time:da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ss', 'Action': 'if', 'if': 'hour.index.size != 0', 'with': 'store hour to ckh by ckh with api_visit_hour'}
	try:
		ptree['lineno']=77
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[77]原语 ss = if hour.index.size != 0 with store hour to ck... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ss != True', 'with': 'store hour to pq by xlink/hx/@file/hx_hour_$k.pq'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=79
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[79]原语 if $ss != True with store hour to pq by xlink/hx/@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'hour.index.size != 0', 'with': 'store hour to pq by xlink/api_visit_hx_day/hx_day_$k.pq'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=81
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hour_visit.fbi]执行第[81]原语 if hour.index.size != 0 with store hour to pq by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],83

#主函数结束,开始块函数

def block_foreach_13(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'hour_1', 'Action': 'load', 'load': 'pq', 'by': '@name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第13行foreach语句中]执行第[15]原语 hour_1 = load pq by @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'hour', 'Action': 'union', 'union': 'hour,hour_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第13行foreach语句中]执行第[16]原语 hour = union hour,hour_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': '@name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第13行foreach语句中]执行第[18]原语 bb = @udf ZFile.rm_file with @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_13

def block_if_64(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'hour2', 'Action': 'limit', 'limit': 'hour', 'by': '$num1'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[65]原语 hour2 = limit hour by $num1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'hour2', 'Action': 'add', 'add': 'hh', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[66]原语 hour2 = add hh by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'hour2', 'Action': 'group', 'group': 'hour2', 'by': 'hh', 'agg': 'visit_num:sum,visit_flow:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[67]原语 hour2 = group hour2 by hh agg visit_num:sum,visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour2', 'by': 'visit_num_sum:int,visit_flow_sum:int,time_max:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[68]原语 alter hour2 by visit_num_sum:int,visit_flow_sum:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_num', 'Action': 'eval', 'eval': 'hour2', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[69]原语 visit_num = eval hour2 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_flow', 'Action': 'eval', 'eval': 'hour2', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[70]原语 visit_flow = eval hour2 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time', 'Action': 'eval', 'eval': 'hour2', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[71]原语 time = eval hour2 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'hour1', 'by': 'udf0.df_append', 'with': 'sum1,sum1,sum1,sum1,sum1,$visit_num,$visit_flow,$time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第64行if语句中]执行第[72]原语 hour = @udf hour1 by udf0.df_append with (sum1,sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_64

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



