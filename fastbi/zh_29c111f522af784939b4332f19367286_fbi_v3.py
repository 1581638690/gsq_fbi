#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: zh_29c111f522af784939b4332f19367286_fbi
#datetime: 2024-08-30T16:10:56.415050
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
		add_the_error('[appdst_tab/确认.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[10]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'a', 'by': 'len(df.iloc[0,1].split(","))>=2', 'as': 'break', 'with': '请选中对应应用再进行修改!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[appdst_tab/确认.fbi]执行第[11]原语 assert a by len(df.iloc[0... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[11]原语 assert a by len(df.iloc[0,1].split(","))>=2 as bre... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apps_sum', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[12]原语 apps_sum = eval a by (iloc[0,2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '\'$apps_sum\' != ""', 'as': 'break', 'with': '应用不能为空！'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[appdst_tab/确认.fbi]执行第[13]原语 assert "$apps_sum" != "" ... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[13]原语 assert "$apps_sum" != "" as break with 应用不能为空！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'qq', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app from data_app_new where app='$apps_sum'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[14]原语 qq = load db by mysql1 with select app from data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'qq', 'by': 'df.index.size <=0', 'as': 'break', 'with': '应用已存在！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[appdst_tab/确认.fbi]执行第[15]原语 assert qq by df.index.siz... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[15]原语 assert qq by df.index.size <=0 as break with 应用已存在... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_n', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[16]原语 app_n = eval a by (iloc[0,1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': "'$app_n'.split(',')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[17]原语 apps = @sdf sys_eval with ("$app_n".split(",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'str($apps)[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[18]原语 apps = @sdf sys_eval with (str($apps)[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_all', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,merge_state,visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active from data_app_new where app in ($apps)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[20]原语 app_all = load db by mysql1 with select id,merge_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq', 'Action': 'filter', 'filter': 'app_all', 'by': 'merge_state != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[21]原语 qq = filter app_all by merge_state != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq', 'Action': 'filter', 'filter': 'qq', 'by': 'merge_state != 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[22]原语 qq = filter qq by merge_state != 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'qq', 'by': 'df.index.size <= 0', 'as': 'break', 'with': '存在已合并的应用！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[appdst_tab/确认.fbi]执行第[23]原语 assert qq by df.index.siz... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[23]原语 assert qq by df.index.size <= 0 as break with 存在已合... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_ap', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,app app_merges from data_api_new where app in ($apps)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[25]原语 api_ap = load db by mysql1 with select id,app app_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_ap', 'Action': 'add', 'add': 'app', 'by': "'$apps_sum'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[26]原语 api_ap = add app by ("$apps_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_ap', 'Action': '@udf', '@udf': 'api_ap', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[27]原语 api_ap = @udf api_ap by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'api_ap', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[28]原语 @udf api_ap by CRUD.save_table with (mysql1,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_all', 'Action': 'loc', 'loc': 'app_all', 'by': 'id,merge_state,visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[30]原语 app_all = loc app_all by id,merge_state,visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app_all', 'by': 'id,merge_state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[31]原语 app = loc app_all by id,merge_state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'merge_state', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[32]原语 app = add merge_state by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_merges', 'by': "'$apps_sum'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[33]原语 app = add app_merges by ("$apps_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[34]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[35]原语 @udf app by CRUD.save_table with (mysql1,data_app_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app2', 'Action': 'loc', 'loc': 'app_all', 'by': 'visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[36]原语 app2 = loc app_all by visits_num,visits_flow,sj_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app_merges', 'by': "'$apps_sum'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[37]原语 app2 = add app_merges by ("$apps_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[39]原语 alter app2.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.app_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[40]原语 alter app2.app_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.app_status', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[41]原语 alter app2.app_status as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[42]原语 alter app2.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[43]原语 app2 = @udf app2 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': "x: 0 if x =='' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[44]原语 app2.visits_flow = lambda visits_flow by x: 0 if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sj_num', 'Action': 'lambda', 'lambda': 'sj_num', 'by': "x: 0 if x =='' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[45]原语 app2.sj_num = lambda sj_num by x: 0 if x =="" else... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.monitor_flow', 'Action': 'lambda', 'lambda': 'monitor_flow', 'by': "x: 0 if x =='' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[46]原语 app2.monitor_flow = lambda monitor_flow by x: 0 if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.imp_api_num', 'Action': 'lambda', 'lambda': 'imp_api_num', 'by': "x: 0 if x =='' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[47]原语 app2.imp_api_num = lambda imp_api_num by x: 0 if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.dstip_num', 'Action': 'lambda', 'lambda': 'dstip_num', 'by': "x: 0 if x =='' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[48]原语 app2.dstip_num = lambda dstip_num by x: 0 if x =="... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.visits_flow', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[49]原语 alter app2.visits_flow as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.sj_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[50]原语 alter app2.sj_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.monitor_flow', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[51]原语 alter app2.monitor_flow as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.imp_api_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[52]原语 alter app2.imp_api_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.dstip_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[53]原语 alter app2.dstip_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app2', 'Action': 'group', 'group': 'app2', 'by': 'app_merges', 'agg': 'visits_num:sum,visits_flow:sum,sj_num:sum,monitor_flow:sum,api_num:sum,imp_api_num:sum,srcip_num:sum,account_num:sum,dstip_num:sum,sensitive_label:sum,app_type:sum,app_status:sum,active:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[54]原语 app2 = group app2 by app_merges agg visits_num:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[55]原语 app2 = @udf app2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app2', 'by': '"visits_num_sum":"visits_num","visits_flow_sum":"visits_flow","sj_num_sum":"sj_num","monitor_flow_sum":"monitor_flow","api_num_sum":"api_num","imp_api_num_sum":"imp_api_num","srcip_num_sum":"srcip_num","account_num_sum":"account_num","dstip_num_sum":"dstip_num","sensitive_label_sum":"sensitive_label","app_type_sum":"app_type","app_status_sum":"app_status","active_sum":"active"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[56]原语 rename app2 by ("visits_num_sum":"visits_num","vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'merge_state', 'by': '2'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[57]原语 app2 = add merge_state by 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:\'3\' if "3" in x else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[58]原语 app2.sensitive_label = lambda sensitive_label by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:\'2\' if "2" in x else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[59]原语 app2.sensitive_label = lambda sensitive_label by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:\'1\' if "1" in x else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[60]原语 app2.sensitive_label = lambda sensitive_label by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:\'0\' if "0" in x else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[61]原语 app2.sensitive_label = lambda sensitive_label by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:1 if "1" in x else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[62]原语 app2.app_type = lambda app_type by x:1 if "1" in x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app_status', 'by': '"0"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[63]原语 app2 = add app_status by ("0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.active', 'Action': 'lambda', 'lambda': 'active', 'by': "x:'3'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[64]原语 app2.active = lambda active by x:"3" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.active', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[65]原语 alter app2.active as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.app_status', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[66]原语 alter app2.app_status as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[67]原语 alter app2.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app_sum', 'by': "'$app_n'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[68]原语 app2 = add app_sum by ("$app_n") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'first_time', 'by': 'str(datetime.now())'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[69]原语 app2 = add first_time by str(datetime.now()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'last_time', 'by': 'str(datetime.now())'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[70]原语 app2 = add last_time by str(datetime.now()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app', 'by': "'$apps_sum'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[71]原语 app2 = add app by ("$apps_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_merges', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,app from data_app_new where app = '$apps_sum' and merge_state = 2"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[72]原语 app_merges = load db by mysql1 with select id,app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app2', 'Action': 'join', 'join': 'app2,app_merges', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[73]原语 app2 = join app2,app_merges by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[74]原语 app2 = @udf app2 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[75]原语 app2 = @udf app2 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'app2', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[76]原语 @udf app2 by CRUD.save_table with (mysql1,data_app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,app_sum from data_app_new where merge_state = 2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[78]原语 app =  @udf RS.load_mysql_sql with (mysql1,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[79]原语 app = @udf app by udf0.df_set_index with app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app', 'by': 'app.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[80]原语 app = add app by (app.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'app_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[81]原语 a=@udf SSDB.hclear with app_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_merge', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[82]原语 store app to ssdb by ssdb0 with app_merge as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'app2', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[84]原语 push app2 as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[appdst_tab/确认.fbi]执行第[86]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],86

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



