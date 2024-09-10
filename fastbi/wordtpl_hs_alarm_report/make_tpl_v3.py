#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_hs_alarm_report/make_tpl
#datetime: 2024-08-30T16:10:57.554663
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
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[23]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[27]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[31]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%dT%H:%M:%S"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[32]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=35
		ptree['funs']=block_if_35
		ptree['funs2']=block_if_else_35
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[35]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[41]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[44]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'True', 'as': 'notice', 'to': '@report_name 报告开始生成!', 'with': '报告生成发现错误!'}
	ptree['to'] = replace_ps(ptree['to'],runtime)
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[45]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'start_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'start_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[52]原语 start_time = eval a by loc[0,"start_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'end_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'end_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[53]原语 end_time = eval a by loc[0,"end_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$start_time".strip() in ["","undefined"]', 'with': '""\nstart_time = @sdf sys_now with -1m\nstart_time = @sdf format_now with ($start_time,"%Y-%m-%d")\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=57
		ptree['funs']=block_if_57
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[57]原语 if "$start_time".strip() in ["","undefined"] with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$end_time".strip() in ["","undefined"]', 'with': '""\nend_time = @sdf sys_now with +1d\nend_time = @sdf format_now with ($end_time,"%Y-%m-%d")\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=61
		ptree['funs']=block_if_61
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[61]原语 if "$end_time".strip() in ["","undefined"] with "e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now_time', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[66]原语 now_time = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[67]原语 now_time = @sdf format_now with ($now_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alarm_time', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'start_time,end_time,now_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[69]原语 alarm_time = @udf udf0.new_df with (start_time,end... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alarm_time', 'Action': '@udf', '@udf': 'alarm_time', 'by': 'udf0.df_append', 'with': '$start_time,$end_time,$now_time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[70]原语 alarm_time = @udf alarm_time by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'alarm_time', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'alarm_time'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[71]原语 store alarm_time to ssdb by ssdb0 with alarm_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'alarm', 'Action': 'loc', 'loc': 'a', 'by': 'alarm'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[73]原语 alarm = loc a by (alarm) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'alarm', 'Action': 'eval', 'eval': 'alarm', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[74]原语 alarm = eval alarm by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alarm', 'Action': '@udf', '@udf': 'alarm', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[75]原语 alarm = @udf alarm by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alm_report', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '告警类型,告警记录数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[78]原语 alm_report = @udf udf0.new_df with (告警类型,告警记录数) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'risk_api,api_risk,api_delay,r_req_alm,stat_req_alm,api_abroad,sensitive_data_alarm,datafilter_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[81]原语 df2 = @udf udf0.new_df with (risk_api,api_risk,api... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_append', 'with': 'OWASP-API,访问阈值告警,访问耗时告警,异地访问告警,请求异常告警,境外访问告警,敏感数据告警,文件敏感信息告警'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[82]原语 df2 = @udf df2 by udf0.df_append with (OWASP-API,访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'risk_api,api_risk,api_delay,r_req_alm,stat_req_alm,api_abroad,sensitive_data_alarm,datafilter_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[84]原语 df3 = @udf udf0.new_df with (risk_api,api_risk,api... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_append', 'with': 'first_time,first_time,time,timestamp,timestamp,timestamp,time,timestamp'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[85]原语 df3 = @udf df3 by udf0.df_append with (first_time,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'alarm', 'with': '@prot=$1', 'run': '""\ntime_name = loc df3 by (@prot)\ntime_name = eval time_name by (iloc[0,0])\nalm_count = load ckh by ckh with select count(*) as `告警记录数` from @prot where left(toString($time_name),10) <= \'$end_time\' and left(toString($time_name),10) > \'$start_time\'\nalm_count = eval alm_count by (iloc[0,0])\nalm_name = loc df2 by (@prot)\nalm_name = eval alm_name by (iloc[0,0])\nalm_report = @udf alm_report by udf0.df_append with ($alm_name,$alm_count)\n""'}
	try:
		ptree['lineno']=88
		ptree['funs']=block_foreach_88
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[88]原语 foreach alarm run "time_name = loc df3 by (@prot)t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'alm_report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'alarm_list_tab'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[98]原语 store alm_report to ssdb by ssdb0 with alarm_list_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'alm_report', 'Action': 'loc', 'loc': 'alm_report', 'by': '告警类型', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[100]原语 alm_report = loc alm_report by 告警类型 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'alm_report', 'by': '告警记录数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[101]原语 alter alm_report by 告警记录数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'alm_report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'alarm_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[102]原语 store alm_report to ssdb by ssdb0 with alarm_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[108]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[110]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[112]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[115]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[117]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[120]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[121]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 't', 'by': 'df.index[0] >0', 'as': 'notice', 'to': '@report_name 报告生成完毕!', 'with': '@report_name 报告生成发现错误!'}
	ptree['to'] = replace_ps(ptree['to'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[122]原语 assert t by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[124]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_alarm_report/make_tpl.fbi]执行第[127]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],127

#主函数结束,开始块函数

def block_if_35(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'set', 'set': 'param', 'by': 'define', 'as': 'report_name', 'with': '@zh-$now'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[第35行if语句中]执行第[36]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_35

def block_if_else_35(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'set', 'set': 'param', 'by': 'define', 'as': 'report_name', 'with': '@report_name-$now'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[第35行if_else语句中]执行第[35]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_35

def block_if_57(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'start_time', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第57行if语句中]执行第[58]原语 start_time = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'start_time', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$start_time,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第57行if语句中]执行第[59]原语 start_time = @sdf format_now with ($start_time,"%Y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_57

def block_if_61(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'end_time', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '+1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第61行if语句中]执行第[62]原语 end_time = @sdf sys_now with +1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'end_time', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$end_time,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第61行if语句中]执行第[63]原语 end_time = @sdf format_now with ($end_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_61

def block_foreach_88(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_name', 'Action': 'loc', 'loc': 'df3', 'by': '@prot'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[89]原语 time_name = loc df3 by (@prot) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time_name', 'Action': 'eval', 'eval': 'time_name', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[90]原语 time_name = eval time_name by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'alm_count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as `告警记录数` from @prot where left(toString($time_name),10) <= '$end_time' and left(toString($time_name),10) > '$start_time'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[91]原语 alm_count = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'alm_count', 'Action': 'eval', 'eval': 'alm_count', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[92]原语 alm_count = eval alm_count by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'alm_name', 'Action': 'loc', 'loc': 'df2', 'by': '@prot'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[93]原语 alm_name = loc df2 by (@prot) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'alm_name', 'Action': 'eval', 'eval': 'alm_name', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[94]原语 alm_name = eval alm_name by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alm_report', 'Action': '@udf', '@udf': 'alm_report', 'by': 'udf0.df_append', 'with': '$alm_name,$alm_count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第88行foreach语句中]执行第[95]原语 alm_report = @udf alm_report by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_88

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



