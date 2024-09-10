#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_visit_flow
#datetime: 2024-08-30T16:10:55.134625
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
		add_the_error('[lhq_visit_flow.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[17]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[lhq_visit_flow.fbi]执行第[18]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[18]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[22]原语 app = load db by mysql1 with select count(*) as va... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[23]原语 alter app by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'name', 'by': "'应用总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[24]原语 app = add name by ("应用总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'icon', 'by': "'F298'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[25]原语 app = add icon by ("F298") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[26]原语 app = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_0', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_app_new where app_type = 0 and merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[28]原语 app_0 = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_0', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[29]原语 alter app_0 by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_0', 'Action': 'add', 'add': 'name', 'by': "'外部应用总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[30]原语 app_0 = add name by ("外部应用总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_0', 'Action': 'add', 'add': 'icon', 'by': "'F076'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[31]原语 app_0 = add icon by ("F076") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_0', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[32]原语 app_0 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_app_new where app_type = 1 and merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[34]原语 app_1 = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_1', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[35]原语 alter app_1 by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'name', 'by': "'内部应用总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[36]原语 app_1 = add name by ("内部应用总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'icon', 'by': "'F077'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[37]原语 app_1 = add icon by ("F077") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[38]原语 app_1 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_api_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[40]原语 api = load db by mysql1 with select count(*) as va... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[41]原语 alter api by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'name', 'by': "'接口总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[42]原语 api = add name by ("接口总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'icon', 'by': "'F138'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[43]原语 api = add icon by ("F138") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[44]原语 api = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_ip_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[46]原语 ip = load db by mysql1 with select count(*) as val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ip', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[47]原语 alter ip by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ip', 'Action': 'add', 'add': 'name', 'by': "'终端总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[48]原语 ip = add name by ("终端总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ip', 'Action': 'add', 'add': 'icon', 'by': "'F146'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[49]原语 ip = add icon by ("F146") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ip', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[50]原语 ip = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as value from data_account_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[52]原语 account = load db by mysql1 with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[53]原语 alter account by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account', 'Action': 'add', 'add': 'name', 'by': "'账号总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[54]原语 account = add name by ("账号总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account', 'Action': 'add', 'add': 'icon', 'by': "'F019'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[55]原语 account = add icon by ("F019") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[56]原语 account = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'visit_days', 'Action': 'union', 'union': 'app,app_0,app_1,api,ip,account'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[58]原语 visit_days = union app,app_0,app_1,api,ip,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_days', 'Action': 'loc', 'loc': 'visit_days', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[59]原语 visit_days = loc visit_days by name,value,icon,det... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_days', 'Action': 'add', 'add': 'pageid', 'by': "'modeling:app_new','modeling:app_new_0','modeling:app_new_1','modeling:api_new','modeling:ip_new','modeling:account_new'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[60]原语 visit_days = add pageid by ("modeling:app_new","mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_days', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days:aa'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[61]原语 store visit_days to ssdb by ssdb0 with visit_days:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[71]原语 hour1 = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour1,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[72]原语 hour1 = @sdf format_now with ($hour1,"%Y-%m-%d 00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[73]原语 hour2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour2,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[74]原语 hour2 = @sdf format_now with ($hour2,"%Y-%m-%d 00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$hour1,$hour2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[75]原语 hour = @udf udf0.new_df_timerange with ($hour1,$ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.hour', 'Action': 'lambda', 'lambda': 'start_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[76]原语 hour.hour = lambda start_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour', 'Action': 'loc', 'loc': 'hour', 'by': 'index', 'to': 'hour1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[77]原语 hour = loc hour by index to hour1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour.hour1', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[78]原语 alter hour.hour1 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.hour1', 'Action': 'lambda', 'lambda': 'hour1', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[79]原语 hour.hour1 = lambda hour1 by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour', 'Action': 'loc', 'loc': 'hour', 'by': 'hour1,hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[80]原语 hour = loc hour by hour1,hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_trend1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(time),1,13) as timestamps,sum(visit_flow) as flow from api_visit_hour group by timestamps'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[83]原语 visit_trend1 = load ckh by ckh with select substri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_trend1', 'by': 'timestamps:str,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[84]原语 alter visit_trend1 by timestamps:str,flow:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_trend', 'Action': 'loc', 'loc': 'visit_trend1', 'by': 'timestamps,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[85]原语 visit_trend = loc visit_trend1 by timestamps,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_trend', 'Action': 'add', 'add': 'hour', 'with': 'visit_trend["timestamps"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[86]原语 visit_trend = add hour with visit_trend["timestamp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'visit_hour', 'Action': 'group', 'group': 'visit_trend', 'by': 'hour', 'agg': 'flow:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[87]原语 visit_hour = group visit_trend by hour agg flow:me... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_trend', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[89]原语 visit_trend = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'visit_min', 'Action': 'group', 'group': 'visit_trend', 'by': 'aa', 'agg': 'flow:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[90]原语 visit_min = group visit_trend by aa agg flow:mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit_min.index.size == 0', 'with': 'visit_min = @udf visit_min by udf0.df_append with 0'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=91
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[91]原语 if visit_min.index.size == 0 with visit_min = @udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_min', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[92]原语 aa_num = eval visit_min by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': 'visit_hour.流量 = lambda flow_mean by (x:x)'}
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
		add_the_error('[lhq_visit_flow.fbi]执行第[93]原语 if $aa_num <= 1024 with visit_hour.流量 = lambda flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'visit_hour.流量 = lambda flow_mean by (x:round(x/1024,1))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=94
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[94]原语 if 1024 < $aa_num <= 1048576  with visit_hour.流量 =... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'visit_hour.流量 = lambda flow_mean by (x:round(x/1048576,1))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=95
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[95]原语 if 1048576 < $aa_num <= 1073741824 with visit_hour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num', 'with': 'visit_hour.流量 = lambda flow_mean by (x:round(x/1073741824,1))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=96
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[96]原语 if 1073741824 < $aa_num with visit_hour.流量 = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_hour', 'Action': 'loc', 'loc': 'visit_hour', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[97]原语 visit_hour = loc visit_hour by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'visit_hour', 'Action': 'join', 'join': 'hour,visit_hour', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[98]原语 visit_hour = join hour,visit_hour by hour,hour wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_hour', 'Action': 'loc', 'loc': 'visit_hour', 'by': 'hour1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[99]原语 visit_hour = loc visit_hour by hour1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_hour', 'Action': '@udf', '@udf': 'visit_hour', 'by': 'udf0.df_fillna_cols', 'with': 'flow_mean:0,流量:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[100]原语 visit_hour = @udf visit_hour by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_hour1', 'Action': 'loc', 'loc': 'visit_hour', 'by': 'flow_mean'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[101]原语 visit_hour1 = loc visit_hour by flow_mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_hour', 'Action': 'loc', 'loc': 'visit_hour', 'by': '流量'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[102]原语 visit_hour = loc visit_hour by 流量 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_hour', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_flow_hour:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[103]原语 store visit_hour to ssdb by ssdb0 with visit_flow_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'title'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[105]原语 aa = @udf udf0.new_df with title 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': 'aa = @udf aa by udf0.df_append with 流量(B)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=106
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[106]原语 if $aa_num <= 1024 with aa = @udf aa by udf0.df_ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'aa = @udf aa by udf0.df_append with 流量(k)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=107
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[107]原语 if 1024 < $aa_num <= 1048576  with aa = @udf aa by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'aa = @udf aa by udf0.df_append with 流量(M)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=108
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[108]原语 if 1048576 < $aa_num <= 1073741824 with aa = @udf ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num', 'with': 'aa = @udf aa by udf0.df_append with 流量(G)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=109
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[109]原语 if 1073741824 < $aa_num with aa = @udf aa by udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'title:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[110]原语 store aa to ssdb by ssdb0 with title:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'visit_hour1.流量(M)', 'Action': 'lambda', 'lambda': 'flow_mean', 'by': 'x:round(x/1048576,1)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[112]原语 visit_hour1.流量(M) = lambda flow_mean by (x:round(x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_hour1', 'Action': 'loc', 'loc': 'visit_hour1', 'by': '流量(M)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[113]原语 visit_hour1 = loc visit_hour1 by 流量(M) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_hour1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'day:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[114]原语 store visit_hour1 to ssdb by ssdb0 with day:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[120]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[121]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[122]原语 day1 = @sdf format_now with ($day,"%Y-%m-%d %H:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[123]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%d %H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day1,$day2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[124]原语 j_hour = @udf udf0.new_df_timerange with ($day1,$d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[125]原语 j_hour.hour = lambda end_time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[126]原语 j_hour = loc j_hour by hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'j_visit', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,13) as hour,sum(visit_flow) as flow,sum(visit_num) as flow1 from api_visit_hour where time > '$day1' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[127]原语 j_visit = load ckh by ckh with select substring(to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'j_visit', 'by': 'hour:str,flow:int,flow1:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[128]原语 alter j_visit by hour:str,flow:int,flow1:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'xlink/hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[131]原语 a = @udf ZFile.list_dir with xlink/hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour_2', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[135]原语 hour_2 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'name=$1', 'run': '""\n##取出已处理的数据\nhour_1 = load pq by @name\nhour_2 = union hour_2,hour_1\n""'}
	try:
		ptree['lineno']=136
		ptree['funs']=block_foreach_136
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[136]原语 foreach a run "##取出已处理的数据hour_1 = load pq by @name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'hour_1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[141]原语 drop hour_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'hour_2.index.size > 0', 'with': '""\nalter hour_2.time as str\nhour_2.hour = lambda time by (x:x[0:13])\nhour_2.hour = str hour by ( replace(\'T\',\' \' ) )\nhour_2 = group hour_2 by hour agg visit_num:sum,visit_flow:sum\nhour_2 = loc hour_2 by index to hour\nrename hour_2 as (\'visit_flow_sum\':\'flow\',\'visit_num_sum\':\'flow1\')\n""'}
	try:
		ptree['lineno']=142
		ptree['funs']=block_if_142
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[142]原语 if hour_2.index.size > 0 with "alter hour_2.time a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'j_visit', 'Action': 'union', 'union': 'j_visit,hour_2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[151]原语 j_visit = union j_visit,hour_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'j_visit', 'Action': 'group', 'group': 'j_visit', 'by': 'hour', 'agg': 'flow:sum,flow1:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[152]原语 j_visit = group j_visit by hour agg flow:sum,flow1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit', 'Action': 'loc', 'loc': 'j_visit', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[153]原语 j_visit = loc j_visit by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'j_visit', 'as': "'flow1_sum':'flow1','flow_sum':'flow'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[154]原语 rename j_visit as ("flow1_sum":"flow1","flow_sum":... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit1', 'Action': 'loc', 'loc': 'j_visit', 'by': 'hour,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[155]原语 j_visit1 = loc j_visit by hour,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'j_visit1', 'Action': 'join', 'join': 'j_hour,j_visit1', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[156]原语 j_visit1 = join j_hour,j_visit1 by hour,hour with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'j_visit1', 'Action': 'add', 'add': 'hour1', 'with': 'j_visit1["hour"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[157]原语 j_visit1 = add hour1 with j_visit1["hour"].str[11:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'j_visit1.hour1', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[158]原语 alter j_visit1.hour1 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_visit1.hour1', 'Action': 'lambda', 'lambda': 'hour1', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[159]原语 j_visit1.hour1 = lambda hour1 by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit1', 'Action': 'loc', 'loc': 'j_visit1', 'by': 'hour1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[160]原语 j_visit1 = loc j_visit1 by hour1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_visit1', 'Action': '@udf', '@udf': 'j_visit1', 'by': 'udf0.df_fillna_cols', 'with': 'flow:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[161]原语 j_visit1 = @udf j_visit1 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_visit1.流量', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1048576,1)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[162]原语 j_visit1.流量 = lambda flow by (x:round(x/1048576,1)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit1', 'Action': 'loc', 'loc': 'j_visit1', 'by': '流量'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[163]原语 j_visit1 = loc j_visit1 by 流量 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'j_visit1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'j_visit:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[164]原语 store j_visit1 to ssdb by ssdb0 with j_visit:trend... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit2', 'Action': 'loc', 'loc': 'j_visit', 'by': 'hour,flow1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[167]原语 j_visit2 = loc j_visit by hour,flow1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'j_visit2', 'Action': 'join', 'join': 'j_hour,j_visit2', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[168]原语 j_visit2 = join j_hour,j_visit2 by hour,hour with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'j_visit2', 'Action': 'add', 'add': 'hour1', 'with': 'j_visit2["hour"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[169]原语 j_visit2 = add hour1 with j_visit2["hour"].str[11:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'j_visit2.hour1', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[170]原语 alter j_visit2.hour1 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_visit2.hour1', 'Action': 'lambda', 'lambda': 'hour1', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[171]原语 j_visit2.hour1 = lambda hour1 by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit2', 'Action': 'loc', 'loc': 'j_visit2', 'by': 'hour1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[172]原语 j_visit2 = loc j_visit2 by hour1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_visit2', 'Action': '@udf', '@udf': 'j_visit2', 'by': 'udf0.df_fillna_cols', 'with': 'flow1:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[173]原语 j_visit2 = @udf j_visit2 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_visit2.访问次数', 'Action': 'lambda', 'lambda': 'flow1', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[174]原语 j_visit2.访问次数 = lambda flow1 by (x:round(x/10000,2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_visit2', 'Action': 'loc', 'loc': 'j_visit2', 'by': '访问次数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[175]原语 j_visit2 = loc j_visit2 by 访问次数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'j_visit2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'j_visit:trend1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[176]原语 store j_visit2 to ssdb by ssdb0 with j_visit:trend... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[179]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[180]原语 month1 = @sdf format_now with ($month1,"%Y-%m-%dT0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[181]原语 month2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month2,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[182]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'month', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$month1,$month2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[183]原语 month = @udf udf0.new_df_timerange with ($month1,$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'month', 'Action': 'loc', 'loc': 'month', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[184]原语 month = loc month by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'month', 'as': '"end_time":"timestamps"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[185]原语 rename month as ("end_time":"timestamps") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'month.timestamps', 'Action': 'lambda', 'lambda': 'timestamps', 'by': 'x:x[0:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[186]原语 month.timestamps = lambda timestamps by (x:x[0:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_mm', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,10) as timestamps,sum(visit_flow) as flow,sum(visit_num) as flow1 from api_visit_hour where time >= '$month1' group by timestamps order by timestamps asc"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[188]原语 visit_mm = load ckh by ckh with select substring(t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_mm', 'by': 'timestamps:str,flow:int,flow1:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[189]原语 alter visit_mm by timestamps:str,flow:int,flow1:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_mm', 'by': 'timestamps,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[190]原语 visit_m = loc visit_mm by timestamps,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'visit_m.timestamps', 'Action': 'str', 'str': 'timestamps', 'by': 'slice(0,10)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[191]原语 visit_m.timestamps = str timestamps by (slice(0,10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[193]原语 visit_m = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'visit_min', 'Action': 'group', 'group': 'visit_m', 'by': 'aa', 'agg': 'flow:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[194]原语 visit_min = group visit_m by aa agg flow:mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit_min.index.size == 0', 'with': 'visit_min = @udf visit_min by udf0.df_append with 0'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=195
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[195]原语 if visit_min.index.size == 0 with visit_min = @udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_min', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[196]原语 aa_num = eval visit_min by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 1073741824', 'with': 'visit_m.流量 = lambda flow by (x:round(x/1048576,1))'}
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
		add_the_error('[lhq_visit_flow.fbi]执行第[197]原语 if $aa_num < 1073741824 with visit_m.流量 = lambda f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1073741824', 'with': 'visit_m.流量 = lambda flow by (x:round(x/1073741824,1))'}
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
		add_the_error('[lhq_visit_flow.fbi]执行第[198]原语 if $aa_num >= 1073741824 with visit_m.流量 = lambda ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'visit_m', 'Action': 'join', 'join': 'month,visit_m', 'by': 'timestamps,timestamps', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[199]原语 visit_m = join month,visit_m by timestamps,timesta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'visit_m.timestamps', 'Action': 'str', 'str': 'timestamps', 'by': 'slice(5,10)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[200]原语 visit_m.timestamps = str timestamps by (slice(5,10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_m', 'Action': '@udf', '@udf': 'visit_m', 'by': 'udf0.df_fillna_cols', 'with': 'flow:0,流量:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[201]原语 visit_m = @udf visit_m by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'timestamps', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[202]原语 visit_m = loc visit_m by timestamps to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m1', 'Action': 'loc', 'loc': 'visit_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[203]原语 visit_m1 = loc visit_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': '流量'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[204]原语 visit_m = loc visit_m by 流量 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_m', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_flow_day:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[205]原语 store visit_m to ssdb by ssdb0 with visit_flow_day... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'title'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[207]原语 aa = @udf udf0.new_df with title 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 1073741824', 'with': 'aa = @udf aa by udf0.df_append with 流量(M)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=208
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[208]原语 if $aa_num < 1073741824 with aa = @udf aa by udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1073741824', 'with': 'aa = @udf aa by udf0.df_append with 流量(G)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=209
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[209]原语 if $aa_num >= 1073741824 with aa = @udf aa by udf0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'title1:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[210]原语 store aa to ssdb by ssdb0 with title1:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'visit_m1.流量(M)', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1048576,1)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[212]原语 visit_m1.流量(M) = lambda flow by (x:round(x/1048576... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m1', 'Action': 'loc', 'loc': 'visit_m1', 'by': '流量(M)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[213]原语 visit_m1 = loc visit_m1 by 流量(M) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_m1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'month:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[214]原语 store visit_m1 to ssdb by ssdb0 with month:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_mm', 'by': 'timestamps,flow1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[218]原语 visit_m = loc visit_mm by timestamps,flow1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'visit_m.访问次数', 'Action': 'lambda', 'lambda': 'flow1', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[219]原语 visit_m.访问次数 = lambda flow1 by (x:round(x/10000,2)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'visit_m', 'Action': 'join', 'join': 'month,visit_m', 'by': 'timestamps,timestamps', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[220]原语 visit_m = join month,visit_m by timestamps,timesta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'visit_m.timestamps', 'Action': 'str', 'str': 'timestamps', 'by': 'slice(5,10)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[221]原语 visit_m.timestamps = str timestamps by (slice(5,10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_m', 'Action': '@udf', '@udf': 'visit_m', 'by': 'udf0.df_fillna_cols', 'with': 'flow1:0,访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[222]原语 visit_m = @udf visit_m by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'timestamps', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[223]原语 visit_m = loc visit_m by timestamps to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': '访问次数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[224]原语 visit_m = loc visit_m by 访问次数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_m', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_flow1_day:tr'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[225]原语 store visit_m to ssdb by ssdb0 with visit_flow1_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-6d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[229]原语 week = @sdf sys_now with -6d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$week,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[230]原语 week = @sdf format_now with ($week,"%Y-%m-%dT00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_w', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,10) as timestamps,toDayOfWeek(toDateTime(time)) as week,sum(visit_flow) as flow from api_visit_hour where time >= '$week' group by timestamps,week order by timestamps"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[231]原语 visit_w = load ckh by ckh with select substring(to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_w', 'by': 'timestamps:str,week:str,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[232]原语 alter visit_w by timestamps:str,week:str,flow:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_w', 'Action': 'loc', 'loc': 'visit_w', 'by': 'week,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[233]原语 visit_w = loc visit_w by week,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '1,周一'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[235]原语 visit_w = @udf visit_w by udf0.df_replace with (1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '2,周二'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[236]原语 visit_w = @udf visit_w by udf0.df_replace with (2,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '3,周三'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[237]原语 visit_w = @udf visit_w by udf0.df_replace with (3,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '4,周四'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[238]原语 visit_w = @udf visit_w by udf0.df_replace with (4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '5,周五'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[239]原语 visit_w = @udf visit_w by udf0.df_replace with (5,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '6,周六'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[240]原语 visit_w = @udf visit_w by udf0.df_replace with (6,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_w', 'Action': '@udf', '@udf': 'visit_w', 'by': 'udf0.df_replace', 'with': '7,周日'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[241]原语 visit_w = @udf visit_w by udf0.df_replace with (7,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'visit_w.flow', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1048576,1)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[242]原语 visit_w.flow = lambda flow by (x:round(x/1048576,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_w', 'Action': 'loc', 'loc': 'visit_w', 'by': 'week', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[244]原语 visit_w = loc visit_w by week to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_w', 'by': '"flow":"流量(M)"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[245]原语 rename visit_w by ("flow":"流量(M)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_w', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'week:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[246]原语 store visit_w to ssdb by ssdb0 with week:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_visit_flow.fbi]执行第[250]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],253

#主函数结束,开始块函数

def block_foreach_136(ptree):

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
		add_the_error('[第136行foreach语句中]执行第[138]原语 hour_1 = load pq by @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'hour_2', 'Action': 'union', 'union': 'hour_2,hour_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第136行foreach语句中]执行第[139]原语 hour_2 = union hour_2,hour_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_136

def block_if_142(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour_2.time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[143]原语 alter hour_2.time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour_2.hour', 'Action': 'lambda', 'lambda': 'time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[144]原语 hour_2.hour = lambda time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'hour_2.hour', 'Action': 'str', 'str': 'hour', 'by': " replace('T',' ' ) "}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[145]原语 hour_2.hour = str hour by ( replace("T"," " ) ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'hour_2', 'Action': 'group', 'group': 'hour_2', 'by': 'hour', 'agg': 'visit_num:sum,visit_flow:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[146]原语 hour_2 = group hour_2 by hour agg visit_num:sum,vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour_2', 'Action': 'loc', 'loc': 'hour_2', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[147]原语 hour_2 = loc hour_2 by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'hour_2', 'as': "'visit_flow_sum':'flow','visit_num_sum':'flow1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[148]原语 rename hour_2 as ("visit_flow_sum":"flow","visit_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_142

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



