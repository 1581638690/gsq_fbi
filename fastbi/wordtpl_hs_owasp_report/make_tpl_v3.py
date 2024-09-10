#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_hs_owasp_report/make_tpl
#datetime: 2024-08-30T16:10:56.803377
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[27]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[31]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[32]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[35]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[41]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[45]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[46]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'start_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'start_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[55]原语 start_time = eval a by loc[0,"start_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'end_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'end_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[56]原语 end_time = eval a by loc[0,"end_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$start_time".strip() in ["","undefined"]', 'with': '""\nstart_time = @sdf sys_now with -1m\nstart_time = @sdf format_now with ($start_time,"%Y-%m-%d")\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=60
		ptree['funs']=block_if_60
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[60]原语 if "$start_time".strip() in ["","undefined"] with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$end_time".strip() in ["","undefined"]', 'with': '""\nend_time = @sdf sys_now with +1d\nend_time = @sdf format_now with ($end_time,"%Y-%m-%d")\n""'}
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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[64]原语 if "$end_time".strip() in ["","undefined"] with "e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now_time', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[69]原语 now_time = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[70]原语 now_time = @sdf format_now with ($now_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_time', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'start_time,end_time,now_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[72]原语 owasp_time = @udf udf0.new_df with (start_time,end... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_time', 'Action': '@udf', '@udf': 'owasp_time', 'by': 'udf0.df_append', 'with': '$start_time,$end_time,$now_time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[73]原语 owasp_time = @udf owasp_time by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'owasp_time', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'owasp_time'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[74]原语 store owasp_time to ssdb by ssdb0 with owasp_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'owasp', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'owasp']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[76]原语 owasp = eval a by loc[0,"owasp"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp', 'Action': '@udf', '@udf': 'owasp', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[77]原语 owasp = @udf owasp by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'API19-1,API19-2,API19-3,API19-4,API19-7,API19-8'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[82]原语 df3 = @udf udf0.new_df with (API19-1,API19-2,API19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_append', 'with': '失效的对象认证,失效的用户认证,过渡的数据暴露,资源缺乏或速率限制,安全配置不当,注入'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[83]原语 df3 = @udf df3 by udf0.df_append with (失效的对象认证,失效的... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_risk', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api19_risk_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[85]原语 api_risk = load ssdb by ssdb0 with dd:api19_risk_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk', 'Action': 'loc', 'loc': 'api_risk', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[86]原语 api_risk = loc api_risk by index to type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_type_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[87]原语 api_type = load ssdb by ssdb0 with dd:api_type_ris... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_type', 'Action': 'loc', 'loc': 'api_type', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[88]原语 api_type = loc api_type by index to type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_report', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '弱点类型,弱点记录数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[90]原语 owasp_report = @udf udf0.new_df with (弱点类型,弱点记录数) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_report1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'type,弱点记录数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[91]原语 owasp_report1 = @udf udf0.new_df with (type,弱点记录数)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'owasp', 'with': 'prot=$1', 'run': '""\n##弱点大类分布\nowasp_count = @udf RS.load_mysql_sql with (mysql1,select count(*) as `弱点记录数` from api19_risk where type like "@prot%" and left(gmt_create,10) <= "$now_time" and left(gmt_create,10) > "$start_time" )\nowasp_count = eval owasp_count by (iloc[0,0])\nowasp_name = eval df3 by loc[0,\'@prot\']\nowasp_report = @udf owasp_report by udf0.df_append with ($owasp_name,$owasp_count)\n##弱点小类分布\nowasp_group = @udf RS.load_mysql_sql with (mysql1,select type,count(*) as 弱点记录数 from api19_risk where type like "@prot%" and left(gmt_create,10) <= "$now_time" and left(gmt_create,10) > "$start_time" group by type )\nowasp_report1 = union owasp_report1,owasp_group\n""'}
	try:
		ptree['lineno']=94
		ptree['funs']=block_foreach_94
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[94]原语 foreach owasp run "##弱点大类分布owasp_count = @udf RS.l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'owasp_report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'owasp_list_tab'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[107]原语 store owasp_report to ssdb by ssdb0 with owasp_lis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'owasp_report1', 'Action': 'join', 'join': 'owasp_report1,api_risk', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[110]原语 owasp_report1 = join owasp_report1,api_risk by typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'owasp_report1', 'Action': 'loc', 'loc': 'owasp_report1', 'by': 'value', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[111]原语 owasp_report1 = loc owasp_report1 by value to inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'owasp_report1', 'Action': 'loc', 'loc': 'owasp_report1', 'by': '弱点记录数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[112]原语 owasp_report1 = loc owasp_report1 by 弱点记录数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'owasp_report1', 'by': '弱点记录数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[113]原语 alter owasp_report1 by 弱点记录数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'owasp_report1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'owasp_list_group'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[114]原语 store owasp_report1 to ssdb by ssdb0 with owasp_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'owasp_report2', 'Action': 'loc', 'loc': 'owasp_report', 'by': '弱点类型', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[117]原语 owasp_report2 = loc owasp_report by 弱点类型 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'owasp_report2', 'by': '弱点记录数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[118]原语 alter owasp_report2 by 弱点记录数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'owasp_report2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'owasp_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[119]原语 store owasp_report2 to ssdb by ssdb0 with owasp_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'owasp_report3', 'Action': 'join', 'join': 'owasp_report,api_type', 'by': '弱点类型,value', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[122]原语 owasp_report3 = join owasp_report,api_type by 弱点类型... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'owasp_report3', 'Action': 'loc', 'loc': 'owasp_report3', 'by': 'type,弱点记录数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[123]原语 owasp_report3 = loc owasp_report3 by type,弱点记录数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'owasp_report3', 'Action': 'loc', 'loc': 'owasp_report3', 'by': 'type', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[124]原语 owasp_report3 = loc owasp_report3 by type to index... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_report3', 'Action': '@udf', '@udf': 'owasp_report3', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[125]原语 owasp_report3 = @udf owasp_report3 by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'owasp_report', 'Action': 'add', 'add': 'aaa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[126]原语 owasp_report = add aaa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'owasp_report', 'by': '弱点记录数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[127]原语 alter owasp_report by 弱点记录数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'tt', 'Action': 'group', 'group': 'owasp_report', 'by': 'aaa', 'agg': '弱点记录数:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[128]原语 tt = group owasp_report by aaa agg 弱点记录数:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt', 'Action': 'eval', 'eval': 'tt', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[129]原语 tt = eval tt by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'owasp_report3', 'Action': 'add', 'add': 'count', 'by': "'$tt'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[130]原语 owasp_report3 = add count by ("$tt") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'owasp_report3', 'as': "'API19-1':'api_1','API19-2':'api_2','API19-3':'api_3','API19-4':'api_4','API19-7':'api_7','API19-8':'api_8'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[131]原语 rename owasp_report3 as ("API19-1":"api_1","API19-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'owasp_report3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'owasp_count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[132]原语 store owasp_report3 to ssdb by ssdb0 with owasp_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[136]原语 data = load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[138]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[140]原语 result = @udf data by doc.modifiy_doc with (@id,@b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[143]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[145]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[148]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[149]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 't', 'by': 'df.index[0] > 0', 'as': 'notice', 'to': '@report_name 报告生成完毕!', 'with': '@report_name 报告生成发现错误!'}
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
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[150]原语 assert t by df.index[0] > 0  as notice to @report_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_owasp_report/make_tpl.fbi]执行第[152]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],155

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

def block_if_60(ptree):

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
		add_the_error('[第60行if语句中]执行第[61]原语 start_time = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第60行if语句中]执行第[62]原语 start_time = @sdf format_now with ($start_time,"%Y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_60

def block_if_64(ptree):

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
		add_the_error('[第64行if语句中]执行第[65]原语 end_time = @sdf sys_now with +1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第64行if语句中]执行第[66]原语 end_time = @sdf format_now with ($end_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_64

def block_foreach_94(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_count', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select count(*) as `弱点记录数` from api19_risk where type like "@prot%" and left(gmt_create,10) <= "$now_time" and left(gmt_create,10) > "$start_time" '}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[96]原语 owasp_count = @udf RS.load_mysql_sql with (mysql1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'owasp_count', 'Action': 'eval', 'eval': 'owasp_count', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[97]原语 owasp_count = eval owasp_count by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'owasp_name', 'Action': 'eval', 'eval': 'df3', 'by': "loc[0,'@prot']"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[98]原语 owasp_name = eval df3 by loc[0,"@prot"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_report', 'Action': '@udf', '@udf': 'owasp_report', 'by': 'udf0.df_append', 'with': '$owasp_name,$owasp_count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[99]原语 owasp_report = @udf owasp_report by udf0.df_append... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'owasp_group', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select type,count(*) as 弱点记录数 from api19_risk where type like "@prot%" and left(gmt_create,10) <= "$now_time" and left(gmt_create,10) > "$start_time" group by type '}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[101]原语 owasp_group = @udf RS.load_mysql_sql with (mysql1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'owasp_report1', 'Action': 'union', 'union': 'owasp_report1,owasp_group'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[102]原语 owasp_report1 = union owasp_report1,owasp_group 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_94

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



