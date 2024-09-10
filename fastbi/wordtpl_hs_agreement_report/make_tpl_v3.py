#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_hs_agreement_report/make_tpl
#datetime: 2024-08-30T16:10:58.583699
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
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[29]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[33]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'fsffdsfd'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[35]原语 store a to ssdb with fsffdsfd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[38]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[39]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=42
		ptree['funs']=block_if_42
		ptree['funs2']=block_if_else_42
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[42]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[48]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[52]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[53]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'start_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'start_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[69]原语 start_time = eval a by loc[0,"start_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'end_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'end_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[70]原语 end_time = eval a by loc[0,"end_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$start_time".strip() in ["","undefined"]', 'with': '""\nstart_time = @sdf sys_now with -1m\nstart_time = @sdf format_now with ($start_time,"%Y-%m-%d")\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=74
		ptree['funs']=block_if_74
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[74]原语 if "$start_time".strip() in ["","undefined"] with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"$end_time".strip() in ["","undefined"]', 'with': '""\nend_time = @sdf sys_now with +1d\nend_time = @sdf format_now with ($end_time,"%Y-%m-%d")\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=78
		ptree['funs']=block_if_78
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[78]原语 if "$end_time".strip() in ["","undefined"] with "e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now_time', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[83]原语 now_time = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[84]原语 now_time = @sdf format_now with ($now_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'protocal_time', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'start_time,end_time,now_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[86]原语 protocal_time = @udf udf0.new_df with (start_time,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'protocal_time', 'Action': '@udf', '@udf': 'protocal_time', 'by': 'udf0.df_append', 'with': '$start_time,$end_time,$now_time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[87]原语 protocal_time = @udf protocal_time by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'protocal_time', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'protocal_time'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[88]原语 store protocal_time to ssdb by ssdb0 with protocal... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'protocol', 'Action': 'loc', 'loc': 'a', 'by': 'protocol'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[90]原语 protocol = loc a by (protocol) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'protocol', 'Action': 'eval', 'eval': 'protocol', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[91]原语 protocol = eval protocol by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'protocol', 'Action': '@udf', '@udf': 'protocol', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[92]原语 protocol = @udf protocol by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '协议名,审计记录数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[95]原语 df1 = @udf udf0.new_df with (协议名,审计记录数) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'api_smtp,api_dns,api_pop3,api_imap,api_smb,api_ftp,api_tftp,api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[98]原语 df2 = @udf udf0.new_df with (api_smtp,api_dns,api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_append', 'with': 'smtp邮件协议,dns协议,pop3邮件协议,imap邮件协议,Windows共享,FTP文件传输,TFTP文件传输,HTTP协议'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[99]原语 df2 = @udf df2 by udf0.df_append with (smtp邮件协议,dn... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'protocol', 'with': '@prot=$1', 'run': '""\nprot_count = load ckh by ckh with select count(*) as `审计记录数` from @prot where left(toString(timestamp),10) <= \'$end_time\' and left(toString(timestamp),10) > \'$start_time\'\nprot_count = eval prot_count by (iloc[0,0])\nprot_name = loc df2 by (@prot)\nprot_name = eval prot_name by (iloc[0,0])\ndf1 = @udf df1 by udf0.df_append with ($prot_name,$prot_count)\n""'}
	try:
		ptree['lineno']=102
		ptree['funs']=block_foreach_102
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[102]原语 foreach protocol run "prot_count = load ckh by ckh... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'protocal_list_tab'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[110]原语 store df1 to ssdb by ssdb0 with protocal_list_tab 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df1', 'Action': 'loc', 'loc': 'df1', 'by': '协议名', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[112]原语 df1 = loc df1 by 协议名 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df1.审计记录数', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[113]原语 alter df1.审计记录数 as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'protocal_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[114]原语 store df1 to ssdb by ssdb0 with protocal_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[164]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[166]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[168]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[171]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[173]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[176]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[177]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[178]原语 assert t by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[180]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_agreement_report/make_tpl.fbi]执行第[183]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],183

#主函数结束,开始块函数

def block_if_42(ptree):

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
		add_the_error('[第42行if语句中]执行第[43]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_42

def block_if_else_42(ptree):

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
		add_the_error('[第42行if_else语句中]执行第[42]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_42

def block_if_74(ptree):

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
		add_the_error('[第74行if语句中]执行第[75]原语 start_time = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第74行if语句中]执行第[76]原语 start_time = @sdf format_now with ($start_time,"%Y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_74

def block_if_78(ptree):

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
		add_the_error('[第78行if语句中]执行第[79]原语 end_time = @sdf sys_now with +1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第78行if语句中]执行第[80]原语 end_time = @sdf format_now with ($end_time,"%Y-%m-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_78

def block_foreach_102(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'prot_count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as `审计记录数` from @prot where left(toString(timestamp),10) <= '$end_time' and left(toString(timestamp),10) > '$start_time'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[103]原语 prot_count = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'prot_count', 'Action': 'eval', 'eval': 'prot_count', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[104]原语 prot_count = eval prot_count by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'prot_name', 'Action': 'loc', 'loc': 'df2', 'by': '@prot'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[105]原语 prot_name = loc df2 by (@prot) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'prot_name', 'Action': 'eval', 'eval': 'prot_name', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[106]原语 prot_name = eval prot_name by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$prot_name,$prot_count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[107]原语 df1 = @udf df1 by udf0.df_append with ($prot_name,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_102

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



