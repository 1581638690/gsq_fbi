#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_ArYGedl/make_tpl
#datetime: 2024-08-30T16:10:56.909615
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
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[27]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[31]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'a', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[33]原语 a_num = eval a by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'a = @udf udf0.new_df with name,status'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=34
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[34]原语 if $a_num == 0 with a = @udf udf0.new_df with name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'a = @udf a by udf0.df_append with (,正在生成报告)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=35
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[35]原语 if $a_num == 0 with a = @udf a by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[37]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[38]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=41
		ptree['funs']=block_if_41
		ptree['funs2']=block_if_else_41
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[41]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[47]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[51]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[52]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[57]原语 tt = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$tt,"%Y-%m-%d %H"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[58]原语 tt = @sdf format_now with ($tt,"%Y-%m-%d %H") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[59]原语 date = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date', 'Action': '@udf', '@udf': 'date', 'by': 'udf0.df_append', 'with': '$tt'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[60]原语 date = @udf date by udf0.df_append with ($tt) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'date', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'date_t'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[61]原语 store date to ssdb by ssdb0 with date_t 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_app_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_type,sx,sensitive_label,merge_state from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[64]原语 data_app_new = load db by mysql1 with select app,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[65]原语 app = @udf udf0.new_df with num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'data_app_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[66]原语 num = eval data_app_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_append', 'with': '$num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[67]原语 app = @udf app by udf0.df_append with ($num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[68]原语 store app to ssdb by ssdb0 with app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'type_0,type_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[70]原语 type = @udf udf0.new_df with type_0,type_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'type0', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'app_type == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[71]原语 type0 = filter data_app_new by app_type == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type0', 'Action': 'eval', 'eval': 'type0', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[72]原语 type0 = eval type0 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'type1', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'app_type == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[73]原语 type1 = filter data_app_new by app_type == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type1', 'Action': 'eval', 'eval': 'type1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[74]原语 type1 = eval type1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type', 'Action': '@udf', '@udf': 'type', 'by': 'udf0.df_append', 'with': '$type0,$type1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[75]原语 type = @udf type by udf0.df_append with ($type0,$t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'type_app'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[76]原语 store type to ssdb by ssdb0 with type_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ng', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'y,w'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[78]原语 ng = @udf udf0.new_df with y,w 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'yng', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'sx != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[79]原语 yng = filter data_app_new by sx != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yng', 'Action': 'eval', 'eval': 'yng', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[80]原语 yng = eval yng by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'wng', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'sx == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[81]原语 wng = filter data_app_new by sx == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'wng', 'Action': 'eval', 'eval': 'wng', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[82]原语 wng = eval wng by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ng', 'Action': '@udf', '@udf': 'ng', 'by': 'udf0.df_append', 'with': '$yng,$wng'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[83]原语 ng = @udf ng by udf0.df_append with ($yng,$wng) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ng', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_ng'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[84]原语 store ng to ssdb by ssdb0 with app_ng 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'mg,fmg'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[86]原语 sens = @udf udf0.new_df with mg,fmg 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'mg', 'Action': 'filter', 'filter': 'data_app_new', 'by': "sensitive_label == '1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[87]原语 mg = filter data_app_new by sensitive_label == "1"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mg', 'Action': 'eval', 'eval': 'mg', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[88]原语 mg = eval mg by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'fmg', 'Action': 'filter', 'filter': 'data_app_new', 'by': "sensitive_label == '0'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[89]原语 fmg = filter data_app_new by sensitive_label == "0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fmg', 'Action': 'eval', 'eval': 'fmg', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[90]原语 fmg = eval fmg by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_append', 'with': '$mg,$fmg'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[91]原语 sens = @udf sens by udf0.df_append with ($mg,$fmg)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_mg'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[92]原语 store sens to ssdb by ssdb0 with app_mg 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'hb,whb'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[94]原语 app = @udf udf0.new_df with hb,whb 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'hb', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'merge_state == 2'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[95]原语 hb = filter data_app_new by merge_state == 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'hb', 'Action': 'eval', 'eval': 'hb', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[96]原语 hb = eval hb by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'whb', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'merge_state == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[97]原语 whb = filter data_app_new by merge_state == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'whb', 'Action': 'eval', 'eval': 'whb', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[98]原语 whb = eval whb by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_append', 'with': '$hb,$whb'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[99]原语 app = @udf app by udf0.df_append with ($hb,$whb) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_hb'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[100]原语 store app to ssdb by ssdb0 with app_hb 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_risk', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_risk.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[102]原语 app_risk = load pq by dt_table/app_risk.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risks', 'by': 'app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[103]原语 alter risks by app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'app_risk', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[104]原语 risk = loc app_risk by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[105]原语 risk = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'risk', 'Action': 'group', 'group': 'risk', 'by': 'aa', 'agg': 'app:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[106]原语 risk = group risk by aa agg app:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_risk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[107]原语 store risk to ssdb by ssdb0 with app_risk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'modsecurity', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct app from api_modsecurity'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[109]原语 modsecurity = load ckh by ckh with select distinct... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'modsecurity', 'by': 'app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[110]原语 alter modsecurity by app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'modsecurity', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[111]原语 modsecurity = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'modsecurity', 'Action': 'group', 'group': 'modsecurity', 'by': 'aa', 'agg': 'app:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[112]原语 modsecurity = group modsecurity by aa agg app:coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'modsecurity', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_modsecurity'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[113]原语 store modsecurity to ssdb by ssdb0 with app_modsec... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datas', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/data_app_new.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[117]原语 datas = load pq by dt_table/data_app_new.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_dest', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[121]原语 app_dest = loc datas by app_type,app,name,dstip_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_dest', 'Action': 'order', 'order': 'app_dest', 'by': 'dstip_num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[122]原语 app_dest = order app_dest by dstip_num with desc l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_dest', 'by': 'dstip_num:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[124]原语 alter app_dest by dstip_num:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_dest', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','dstip_num':'部署服务器数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[125]原语 rename app_dest as ("app_type":"应用类型","app":"应用","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_dest', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_dest'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[126]原语 store app_dest to ssdb by ssdb0 with app_dest 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_visit', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,visits_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[130]原语 app_visit = loc datas by app_type,app,name,visits_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_visit', 'Action': 'order', 'order': 'app_visit', 'by': 'visits_num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[131]原语 app_visit = order app_visit by visits_num with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_visit', 'by': 'visits_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[133]原语 alter app_visit by visits_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_visit', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','visits_num':'访问数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[134]原语 rename app_visit as ("app_type":"应用类型","app":"应用",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_visit', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_visit'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[135]原语 store app_visit to ssdb by ssdb0 with app_visit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[138]原语 app_flow = loc datas by app_type,app,name,visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_flow', 'Action': 'order', 'order': 'app_flow', 'by': 'visits_flow', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[139]原语 app_flow = order app_flow by visits_flow with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_flow', 'by': 'visits_flow:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[141]原语 alter app_flow by visits_flow:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_flow.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': "x:x+'(M)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[142]原语 app_flow.visits_flow = lambda visits_flow by (x:x+... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_flow', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','visits_flow':'访问流量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[143]原语 rename app_flow as ("app_type":"应用类型","app":"应用","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_flow', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_flow'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[144]原语 store app_flow to ssdb by ssdb0 with app_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_u', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,api_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[147]原语 app_u = loc datas by app_type,app,name,api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_u', 'Action': 'order', 'order': 'app_u', 'by': 'api_num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[148]原语 app_u = order app_u by api_num with desc limit 20 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_u', 'by': 'api_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[149]原语 alter app_u by api_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_u', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','api_num':'接口数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[150]原语 rename app_u as ("app_type":"应用类型","app":"应用","nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_u', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_api'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[151]原语 store app_u to ssdb by ssdb0 with app_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_srcip', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,srcip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[154]原语 app_srcip = loc datas by app_type,app,name,srcip_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_srcip', 'Action': 'order', 'order': 'app_srcip', 'by': 'srcip_num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[155]原语 app_srcip = order app_srcip by srcip_num with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_srcip', 'by': 'srcip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[156]原语 alter app_srcip by srcip_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_srcip', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','srcip_num':'访问IP数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[157]原语 rename app_srcip as ("app_type":"应用类型","app":"应用",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_srcip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_srcip'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[158]原语 store app_srcip to ssdb by ssdb0 with app_srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_account', 'Action': 'loc', 'loc': 'datas', 'by': 'app_type,app,name,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[161]原语 app_account = loc datas by app_type,app,name,accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_account', 'Action': 'order', 'order': 'app_account', 'by': 'account_num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[162]原语 app_account = order app_account by account_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_account', 'by': 'account_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[163]原语 alter app_account by account_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_account', 'as': "'app_type':'应用类型','app':'应用','name':'应用名称','account_num':'访问账号数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[164]原语 rename app_account as ("app_type":"应用类型","app":"应用... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_account', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_account'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[165]原语 store app_account to ssdb by ssdb0 with app_accoun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_app.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[168]原语 sens = load pq by sensitive/sensitive_app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'app:str,url_count:int,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[169]原语 alter sens by app:str,url_count:int,srcip_count:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sens1', 'Action': 'loc', 'loc': 'sens', 'by': 'app,url_count,srcip_count,account_count,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[171]原语 app_sens1 = loc sens by app,url_count,srcip_count,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_sens1', 'Action': 'order', 'order': 'app_sens1', 'by': 'sensitive_count', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[172]原语 app_sens1 = order app_sens1 by sensitive_count wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_sens1', 'by': 'url_count:int,srcip_count:int,account_count:int,sensitive_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[174]原语 alter app_sens1 by url_count:int,srcip_count:int,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_sens1', 'as': "'app':'应用','url_count':'接口数量','srcip_count':'终端数量','account_count':'账号数量','sensitive_count':'敏感数据数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[175]原语 rename app_sens1 as ("app":"应用","url_count":"接口数量"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_sens1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_sens1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[176]原语 store app_sens1 to ssdb by ssdb0 with app_sens1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sens2', 'Action': 'loc', 'loc': 'sens', 'by': 'app,s_num_sum,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[179]原语 app_sens2 = loc sens by app,s_num_sum,sensitive_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[180]原语 sens = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'app:str,url:str,src_ip:str,account:str,key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[181]原语 alter sens by app:str,url:str,src_ip:str,account:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'app,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[182]原语 sens = loc sens by app,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens', 'Action': 'distinct', 'distinct': 'sens', 'by': 'app,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[183]原语 sens = distinct sens by app,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens', 'by': 'app', 'agg': 'key:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[184]原语 sens = group sens by app agg key:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'index', 'to': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[185]原语 sens = loc sens by index to app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_sens2', 'Action': 'join', 'join': 'app_sens2,sens', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[186]原语 app_sens2 = join app_sens2,sens by app,app with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_sens2', 'Action': 'order', 'order': 'app_sens2', 'by': 'key_count', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[187]原语 app_sens2 = order app_sens2 by key_count with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sens2', 'Action': 'loc', 'loc': 'app_sens2', 'by': 'app,key_count,s_num_sum,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[188]原语 app_sens2 = loc app_sens2 by app,key_count,s_num_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_sens2.key_count.sensitive_count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[189]原语 alter app_sens2.key_count.sensitive_count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_sens2', 'as': "'app':'应用','key_count':'敏感类型数量','s_num_sum':'敏感数据类型访问分布','sensitive_count':'敏感数据数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[190]原语 rename app_sens2 as ("app":"应用","key_count":"敏感类型数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_sens2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_sens2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[191]原语 store app_sens2 to ssdb by ssdb0 with app_sens2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'risks', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_risk.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[194]原语 risks = load pq by dt_table/app_risk.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risks', 'by': 'app:str,api_num:int,api_count:int,type_num:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[195]原语 alter risks by app:str,api_num:int,api_count:int,t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_risk1', 'Action': 'loc', 'loc': 'risks', 'by': 'app,api_num,api_count,type_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[197]原语 app_risk1 = loc risks by app,api_num,api_count,typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_risk1', 'Action': 'order', 'order': 'app_risk1', 'by': 'api_count', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[198]原语 app_risk1 = order app_risk1 by api_count with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_risk1.api_num.api_count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[199]原语 alter app_risk1.api_num.api_count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_risk1', 'as': "'app':'应用','api_num':'接口总数','api_count':'接口弱点量','type_num':'弱点类型分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[200]原语 rename app_risk1 as ("app":"应用","api_num":"接口总数","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_risk1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_risk1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[201]原语 store app_risk1 to ssdb by ssdb0 with app_risk1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select a.app,b.level,count(*) as num from api19_risk a join api19_type b on a.type = b.type group by a.app,b.level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[204]原语 api19_risk = load db by mysql1 with select a.app,b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_risk', 'Action': 'filter', 'filter': 'api19_risk', 'by': "level == '高'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[205]原语 api19_risk = filter api19_risk by level == "高" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_risk2', 'Action': 'loc', 'loc': 'risks', 'by': 'app,api_count,type_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[206]原语 app_risk2 = loc risks by app,api_count,type_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_risk2', 'Action': 'join', 'join': 'app_risk2,api19_risk', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[207]原语 app_risk2 = join app_risk2,api19_risk by app,app w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_risk2', 'Action': 'order', 'order': 'app_risk2', 'by': 'num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[208]原语 app_risk2 = order app_risk2 by num with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_risk2', 'Action': 'loc', 'loc': 'app_risk2', 'by': 'app,num,api_count,type_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[209]原语 app_risk2 = loc app_risk2 by app,num,api_count,typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_risk2', 'Action': '@udf', '@udf': 'app_risk2', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[210]原语 app_risk2 = @udf app_risk2 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_risk2.num', 'Action': 'lambda', 'lambda': 'num', 'by': "x:0 if x == '' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[211]原语 app_risk2.num = lambda num by (x:0 if x == "" else... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_risk2', 'by': 'num:int,api_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[212]原语 alter app_risk2 by num:int,api_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_risk2', 'as': "'app':'应用','num':'弱点高风险数量','api_count':'接口弱点量','type_num':'弱点类型分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[213]原语 rename app_risk2 as ("app":"应用","num":"弱点高风险数量","a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_risk2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_risk2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[214]原语 store app_risk2 to ssdb by ssdb0 with app_risk2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_mod1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,class,count(*) as num from api_modsecurity where class != '' group by app,class"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[218]原语 app_mod1 = load ckh by ckh with select app,class,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app', 'Action': 'group', 'group': 'app_mod1', 'by': 'app', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[219]原语 app = group app_mod1 by app agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[220]原语 app = @udf app by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_mod1', 'by': 'num:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[221]原语 alter app_mod1 by num:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_mod1', 'Action': 'add', 'add': 's_num', 'by': 'df[\'class\'] +"("+ df[\'num\'] + ")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[222]原语 app_mod1 = add s_num by  df["class"] +"("+ df["num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_mod1.s_num', 'Action': 'lambda', 'lambda': 's_num', 'by': "x: x+'，'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[223]原语 app_mod1.s_num = lambda s_num by x: x+"，" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_mod1', 'Action': 'group', 'group': 'app_mod1', 'by': 'app', 'agg': 's_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[224]原语 app_mod1 = group app_mod1 by app agg s_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_mod1', 'Action': '@udf', '@udf': 'app_mod1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[225]原语 app_mod1 = @udf app_mod1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_mod1.s_num_sum', 'Action': 'lambda', 'lambda': 's_num_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[226]原语 app_mod1.s_num_sum = lambda s_num_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_mod1', 'Action': 'join', 'join': 'app,app_mod1', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[227]原语 app_mod1 = join app,app_mod1 by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_mod1', 'Action': 'order', 'order': 'app_mod1', 'by': 'num_sum', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[228]原语 app_mod1 = order app_mod1 by num_sum with desc lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_mod1', 'Action': '@udf', '@udf': 'app_mod1', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[229]原语 app_mod1 = @udf app_mod1 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_mod1', 'by': 'num_sum:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[230]原语 alter app_mod1 by num_sum:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_mod1', 'as': "'app':'应用','num_sum':'安全事件数','s_num_sum':'安全事件类型分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[231]原语 rename app_mod1 as ("app":"应用","num_sum":"安全事件数","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_mod1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_mod1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[232]原语 store app_mod1 to ssdb by ssdb0 with app_mod1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_mod2', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,level,count(*) as num from api_modsecurity where level = '高级' or level = '中级' or level = '低级' or level = '信息' group by app,level"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[235]原语 app_mod2 = load ckh by ckh with select app,level,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'lel', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:modsecurity_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[236]原语 lel = load ssdb by ssdb0 with dd:modsecurity_level... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'dd1', 'Action': 'group', 'group': 'app_mod2', 'by': 'app', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[237]原语 dd1 = group app_mod2 by app agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd1', 'Action': '@udf', '@udf': 'dd1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[238]原语 dd1 = @udf dd1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app', 'Action': 'filter', 'filter': 'app_mod2', 'by': "level == '高级'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[239]原语 app = filter app_mod2 by level == "高级" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_mod2', 'Action': 'order', 'order': 'app_mod2', 'by': 'num'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[240]原语 app_mod2 = order app_mod2 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_mod2', 'by': 'num:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[241]原语 alter app_mod2 by num:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_mod2', 'Action': 'add', 'add': 's_num', 'by': 'df[\'level\'] +"("+ df[\'num\'] + ")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[242]原语 app_mod2 = add s_num by  df["level"] +"("+ df["num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_mod2.s_num', 'Action': 'lambda', 'lambda': 's_num', 'by': "x: x+'，'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[243]原语 app_mod2.s_num = lambda s_num by x: x+"，" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_mod2', 'Action': 'group', 'group': 'app_mod2', 'by': 'app', 'agg': 's_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[244]原语 app_mod2 = group app_mod2 by app agg s_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_mod2', 'Action': '@udf', '@udf': 'app_mod2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[245]原语 app_mod2 = @udf app_mod2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_mod2.s_num_sum', 'Action': 'lambda', 'lambda': 's_num_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[246]原语 app_mod2.s_num_sum = lambda s_num_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_mod2', 'Action': 'join', 'join': 'app_mod2,dd1', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[247]原语 app_mod2 = join app_mod2,dd1 by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_mod2', 'Action': 'join', 'join': 'app_mod2,app', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[248]原语 app_mod2 = join app_mod2,app by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_mod2', 'Action': 'order', 'order': 'app_mod2', 'by': 'num', 'with': 'desc limit 20'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[249]原语 app_mod2 = order app_mod2 by num with desc limit 2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_mod2', 'Action': '@udf', '@udf': 'app_mod2', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[250]原语 app_mod2 = @udf app_mod2 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_mod2.num', 'Action': 'lambda', 'lambda': 'num', 'by': "x:0 if x == '' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[251]原语 app_mod2.num = lambda num by (x:0 if x == "" else ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_mod2', 'Action': 'filter', 'filter': 'app_mod2', 'by': "num != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[252]原语 app_mod2 = filter app_mod2 by num != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_mod2', 'Action': 'loc', 'loc': 'app_mod2', 'by': 'app,num,num_sum,s_num_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[253]原语 app_mod2 = loc app_mod2 by app,num,num_sum,s_num_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_mod2', 'by': 'num:int,num_sum:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[254]原语 alter app_mod2 by num:int,num_sum:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_mod2', 'as': "'app':'应用','num':'安全事件高级风险数','num_sum':'应用总风险数','s_num_sum':'安全事件等级分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[255]原语 rename app_mod2 as ("app":"应用","num":"安全事件高级风险数","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_mod2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_mod2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[256]原语 store app_mod2 to ssdb by ssdb0 with app_mod2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[260]原语 data = load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[262]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[264]原语 result = @udf data by doc.modifiy_doc with (@id,@b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[267]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[269]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[272]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[273]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[274]原语 assert t by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[276]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_ArYGedl/make_tpl.fbi]执行第[279]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],279

#主函数结束,开始块函数

def block_if_41(ptree):

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
		add_the_error('[第41行if语句中]执行第[42]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_41

def block_if_else_41(ptree):

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
		add_the_error('[第41行if_else语句中]执行第[41]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_41

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



