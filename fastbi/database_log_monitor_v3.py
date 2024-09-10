#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: database_log_monitor
#datetime: 2024-08-30T16:10:55.449531
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
		add_the_error('[database_log_monitor.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select account from event_monitor_oper group by account order by count(*) desc'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[13]原语 user = load ckh by ckh with select account from ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user.account', 'Action': 'lambda', 'lambda': 'account', 'by': "x: '未知' if x == '' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[14]原语 user.account = lambda account by (x: "未知" if x == ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'user', 'Action': 'add', 'add': 'account1', 'by': 'user.account'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[15]原语 user = add account1 by user.account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'user', 'Action': 'loc', 'loc': 'user', 'by': 'account1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[16]原语 user = loc user by account1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'account,account1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[17]原语 a = @udf udf0.new_df with account,account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '全部,全部'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[18]原语 a = @udf a by udf0.df_append with (全部,全部) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'account1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[19]原语 a = loc a by account1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tab1', 'Action': 'union', 'union': 'a,user'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[20]原语 tab1 = union a,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tab1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:logList_user'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[21]原语 store tab1 to ssdb by ssdb0 with dd:logList_user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app_name from event_monitor_oper where app_name != '' group by app_name order by count(*) desc"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[25]原语 app = load ckh by ckh with select app_name from ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_name1', 'by': 'app.app_name'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[26]原语 app = add app_name1 by app.app_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'app_name1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[27]原语 app = loc app by app_name1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'app_name,app_name1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[28]原语 b = @udf udf0.new_df with app_name,app_name1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_append', 'with': '全部,全部'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[29]原语 b = @udf b by udf0.df_append with (全部,全部) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'b', 'Action': 'loc', 'loc': 'b', 'by': 'app_name1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[30]原语 b = loc b by app_name1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tab2', 'Action': 'union', 'union': 'b,app'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[31]原语 tab2 = union b,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tab2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:logList_app'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[32]原语 store tab2 to ssdb by ssdb0 with dd:logList_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'action', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select action from event_monitor_oper where action != '' group by action order by count(*) desc"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[36]原语 action = load ckh by ckh with select action from e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'action', 'Action': 'add', 'add': 'action1', 'by': 'action.action'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[37]原语 action = add action1 by action.action 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'action', 'Action': 'loc', 'loc': 'action', 'by': 'action1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[38]原语 action = loc action by action1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'action,action1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[39]原语 c = @udf udf0.new_df with action,action1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '全部,全部'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[40]原语 c = @udf c by udf0.df_append with (全部,全部) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c', 'Action': 'loc', 'loc': 'c', 'by': 'action1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[41]原语 c = loc c by action1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tab3', 'Action': 'union', 'union': 'c,action'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[42]原语 tab3 = union c,action 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tab3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:logList_action'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[43]原语 store tab3 to ssdb by ssdb0 with dd:logList_action... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'users', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(distinct account) as users_count from event_monitor_oper where account != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[49]原语 users = load ckh by ckh with select count(distinct... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'users', 'as': '{"users_count":"累计用户数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[50]原语 rename users as {"users_count":"累计用户数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'users', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'userCount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[51]原语 store users to ssdb by ssdb0 with userCount 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apps', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(distinct app_name) as apps_count from event_monitor_oper where app_name != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[54]原语 apps = load ckh by ckh with select count(distinct ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'apps', 'as': '{"apps_count":"累计应用数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[55]原语 rename apps as {"apps_count":"累计应用数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'apps', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'appCount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[56]原语 store apps to ssdb by ssdb0 with appCount 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'logs', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) from event_monitor_oper'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[59]原语 logs = load ckh by ckh with select count(*) from e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'logs', 'as': '{"count()":"累计日志总数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[60]原语 rename logs as {"count()":"累计日志总数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'logs', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'logCount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[61]原语 store logs to ssdb by ssdb0 with logCount 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now_time', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[64]原语 now_time = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now_time', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now_time,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[65]原语 now_time = @sdf format_now with ($now_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'intraday_logs', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) from event_monitor_oper where time > '$now_time'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[66]原语 intraday_logs = load ckh by ckh with select count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'intraday_logs', 'as': '{"count()":"当天新增日志"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[67]原语 rename intraday_logs as {"count()":"当天新增日志"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'intraday_logs', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'IntradayLogCount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[68]原语 store intraday_logs to ssdb by ssdb0 with Intraday... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user_log_top5', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select account,count(*) from event_monitor_oper group by account order by count(*) desc limit 5'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[73]原语 user_log_top5 = load ckh by ckh with select accoun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user_log_top5.account', 'Action': 'lambda', 'lambda': 'account', 'by': "x: '未知' if x == '' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[74]原语 user_log_top5.account = lambda account by (x: "未知"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'user_log_top5', 'as': '{"count()":"总量"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[75]原语 rename user_log_top5 as {"count()":"总量"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'user_log_top5', 'Action': 'loc', 'loc': 'user_log_top5', 'by': 'account', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[76]原语 user_log_top5 = loc user_log_top5 by account to in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'user_log_top5', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'userLogTop5'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[77]原语 store user_log_top5 to ssdb by ssdb0 with userLogT... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_log_top5', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app_name,count(*) from event_monitor_oper where app_name != '' group by app_name order by count(*) desc limit 5"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[80]原语 app_log_top5 = load ckh by ckh with select app_nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_log_top5', 'as': '{"count()":"总量"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[81]原语 rename app_log_top5 as {"count()":"总量"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_log_top5', 'Action': 'loc', 'loc': 'app_log_top5', 'by': 'app_name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[82]原语 app_log_top5 = loc app_log_top5 by app_name to ind... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_log_top5', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'appLogTop5_ces'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[83]原语 store app_log_top5 to ssdb by ssdb0 with appLogTop... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'log_list_all', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select time,account,app_name,name,action,event from event_monitor_oper'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[87]原语 log_list_all = load ckh by ckh with select time,ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list_all.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("{","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[88]原语 log_list_all.event = lambda event by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list_all.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("}","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[89]原语 log_list_all.event = lambda event by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list_all.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("[","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[90]原语 log_list_all.event = lambda event by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list_all.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("]","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[91]原语 log_list_all.event = lambda event by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list_all.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace(\'"\',\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[92]原语 log_list_all.event = lambda event by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'log_list_all', 'as': '{"time":"时间","account":"用户","app_name":"应用名","name":"接口事件","action":"动作行为","event":"操作参数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[93]原语 rename log_list_all as {"time":"时间","account":"用户"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'log_list_all', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'logList_all'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[94]原语 store log_list_all to ssdb by ssdb0 with logList_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'log_list', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select time,account,app_name,name,action,event from event_monitor_oper order by time desc limit 100'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[96]原语 log_list = load ckh by ckh with select time,accoun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'log_list.time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[98]原语 alter log_list.time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.time', 'Action': 'lambda', 'lambda': 'time', 'by': 'x:x[0:16]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[99]原语 log_list.time = lambda time by (x:x[0:16]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("{","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[102]原语 log_list.event = lambda event by x:x.replace("{","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("}","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[103]原语 log_list.event = lambda event by x:x.replace("}","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("[","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[104]原语 log_list.event = lambda event by x:x.replace("[","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace("]","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[105]原语 log_list.event = lambda event by x:x.replace("]","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'log_list.event', 'Action': 'lambda', 'lambda': 'event', 'by': 'x:x.replace(\'"\',\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[106]原语 log_list.event = lambda event by x:x.replace(","")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'log_list', 'as': '{"time":"时间","account":"用户","app_name":"应用名","name":"接口事件","action":"动作行为","event":"操作参数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[107]原语 rename log_list as {"time":"时间","account":"用户","ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '时间,用户,应用名,接口事件,动作行为,操作参数,width'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[110]原语 new = @udf udf0.new_df with (时间,用户,应用名,接口事件,动作行为,操... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new', 'Action': '@udf', '@udf': 'new', 'by': 'udf0.df_append', 'with': '170,150,150,200,150,460,td_width'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[111]原语 new = @udf new by udf0.df_append with (170,150,150... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'new', 'Action': 'loc', 'loc': 'new', 'by': 'width', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[112]原语 new = loc new by width to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'log_list', 'Action': 'union', 'union': 'new,log_list'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[113]原语 log_list = union new,log_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'log_list', 'Action': 'loc', 'loc': 'log_list', 'by': '时间,用户,应用名,接口事件,动作行为,操作参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[114]原语 log_list = loc log_list by 时间,用户,应用名,接口事件,动作行为,操作参... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'log_list', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'logList_ces'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[115]原语 store log_list to ssdb by ssdb0 with logList_ces 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[118]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[119]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[120]原语 day = @sdf format_now with ($day,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[121]原语 now = @sdf format_now with ($now,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day,$now,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[122]原语 j_hour = @udf udf0.new_df_timerange with ($day,$no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[123]原语 j_hour.hour = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[124]原语 j_hour = loc j_hour by hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'emo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),12,2) as hour,count(*) as num from event_monitor_oper where time >= '$day' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[125]原语 emo = load ckh by ckh with select substring(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'emo', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[126]原语 alter emo by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'res', 'Action': 'join', 'join': 'j_hour,emo', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[127]原语 res = join j_hour,emo by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'res', 'Action': '@udf', '@udf': 'res', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[128]原语 res = @udf res by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'res.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[129]原语 res.hour = lambda hour by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'res', 'Action': 'loc', 'loc': 'res', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[130]原语 res = loc res by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'res', 'as': '{"num":"访问次数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[131]原语 rename res as {"num":"访问次数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'res', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data:log_visit_24h'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[132]原语 store res to ssdb by ssdb0 with data:log_visit_24h... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-30d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[135]原语 day = @sdf sys_now with -30d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[136]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[database_log_monitor.fbi]执行第[137]原语 day = @sdf format_now with ($day,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[138]原语 now = @sdf format_now with ($now,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_day', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day,$now,1d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[139]原语 j_day = @udf udf0.new_df_timerange with ($day,$now... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_day.day', 'Action': 'lambda', 'lambda': 'start_time', 'by': 'x:x[0:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[140]原语 j_day.day = lambda start_time by (x:x[0:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_day', 'Action': 'loc', 'loc': 'j_day', 'by': 'day'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[141]原语 j_day = loc j_day by day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'emo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,10) as day,count(*) as num from event_monitor_oper where time >= '$day' group by day"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[142]原语 emo = load ckh by ckh with select substring(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'emo', 'by': 'day:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[143]原语 alter emo by day:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'res', 'Action': 'join', 'join': 'j_day,emo', 'by': 'day,day', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[144]原语 res = join j_day,emo by day,day with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'res', 'Action': '@udf', '@udf': 'res', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[145]原语 res = @udf res by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'res', 'Action': 'loc', 'loc': 'res', 'by': 'day', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[146]原语 res = loc res by day to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'res', 'as': '{"num":"访问次数"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[147]原语 rename res as {"num":"访问次数"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'res', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data:log_visit_30d'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[148]原语 store res to ssdb by ssdb0 with data:log_visit_30d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[database_log_monitor.fbi]执行第[151]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],151

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



