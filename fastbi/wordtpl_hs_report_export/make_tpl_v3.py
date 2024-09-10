#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_hs_report_export/make_tpl
#datetime: 2024-08-30T16:10:58.729386
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
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[25]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[27]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[30]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[31]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=34
		ptree['funs']=block_if_34
		ptree['funs2']=block_if_else_34
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[34]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[40]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[44]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[45]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count() as count FROM api_monitor WHERE toDate(time) > toDate(now())-30 and toDate(time) < toDate(now())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[49]原语 zts_1 = load ckh by ckh with SELECT count() as cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT LEFT(toString(now()),10) as time,uniqCombined(app) as yy,uniqCombined(url) as jk,count() as sj FROM api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[50]原语 zts = load ckh by ckh with SELECT LEFT(toString(no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[53]原语 store zts to ssdb by ssdb0 with zts 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[54]原语 store zts_1 to ssdb by ssdb0 with zts_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num,name1,name2,name3,name4,name5,name6,name7'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[57]原语 df1 = @udf udf0.new_df with (num,name1,name2,name3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '8,dns协议,ftp协议,tftp协议,smb协议,imap协议,smtp协议,pop3协议'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[58]原语 df1 = @udf df1 by udf0.df_append with (8,dns协议,ftp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'protocal'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[59]原语 store df1 to ssdb by ssdb0 with protocal 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_dns'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[78]原语 dns_sum = load ckh by ckh with SELECT count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns_sum', 'Action': 'add', 'add': 'a', 'with': "dns_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[79]原语 dns_sum  = add a with (dns_sum["count"] >= 10000) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'dns_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[80]原语 a1 = eval dns_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter dns_sum by count:str\ndns_sum.count = str count by ([:-4])\ndns_sum = add counts with dns_sum[\'count\'] + \'万余\'\n"', 'else': '"\ndns_sum = add counts with dns_sum[\'count\']\n""'}
	try:
		ptree['lineno']=81
		ptree['funs']=block_if_81
		ptree['funs2']=block_if_else_81
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[81]原语 if a1 == "True" with "alter dns_sum by count:strdn... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dns_sum', 'Action': 'loc', 'loc': 'dns_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[88]原语 dns_sum = loc dns_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dns_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[89]原语 rename dns_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dns_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dns_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[90]原语 store dns_sum to ssdb by ssdb0 with dns_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_ftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[93]原语 ftp_sum = load ckh by ckh with SELECT count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ftp_sum', 'Action': 'add', 'add': 'a', 'with': "ftp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[94]原语 ftp_sum  = add a with (ftp_sum["count"] >= 10000) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'ftp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[95]原语 a1 = eval ftp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter ftp_sum by count:str\nftp_sum.count = str count by ([:-4])\nftp_sum = add counts with ftp_sum[\'count\'] + \'万余\'\n"', 'else': '"\nftp_sum = add counts with ftp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=96
		ptree['funs']=block_if_96
		ptree['funs2']=block_if_else_96
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[96]原语 if a1 == "True" with "alter ftp_sum by count:strft... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ftp_sum', 'Action': 'loc', 'loc': 'ftp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[103]原语 ftp_sum = loc ftp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ftp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[104]原语 rename ftp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ftp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ftp_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[105]原语 store ftp_sum to ssdb by ssdb0 with ftp_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_tftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[108]原语 tftp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tftp_sum', 'Action': 'add', 'add': 'a', 'with': "tftp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[109]原语 tftp_sum  = add a with (tftp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'tftp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[110]原语 a1 = eval tftp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter tftp_sum by count:str\ntftp_sum.count = str count by ([:-4])\ntftp_sum = add counts with tftp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntftp_sum = add counts with tftp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=111
		ptree['funs']=block_if_111
		ptree['funs2']=block_if_else_111
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[111]原语 if a1 == "True" with "alter tftp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tftp_sum', 'Action': 'loc', 'loc': 'tftp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[118]原语 tftp_sum = loc tftp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tftp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[119]原语 rename tftp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tftp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tftp_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[120]原语 store tftp_sum to ssdb by ssdb0 with tftp_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_smb'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[123]原语 smb_sum = load ckh by ckh with SELECT count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smb_sum', 'Action': 'add', 'add': 'a', 'with': "smb_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[124]原语 smb_sum  = add a with (smb_sum["count"] >= 10000) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'smb_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[125]原语 a1 = eval smb_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter smb_sum by count:str\nsmb_sum.count = str count by ([:-4])\nsmb_sum = add counts with smb_sum[\'count\'] + \'万余\'\n"', 'else': '"\nsmb_sum = add counts with smb_sum[\'count\']\n""'}
	try:
		ptree['lineno']=126
		ptree['funs']=block_if_126
		ptree['funs2']=block_if_else_126
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[126]原语 if a1 == "True" with "alter smb_sum by count:strsm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'smb_sum', 'Action': 'loc', 'loc': 'smb_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[133]原语 smb_sum = loc smb_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'smb_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[134]原语 rename smb_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'smb_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'smb_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[135]原语 store smb_sum to ssdb by ssdb0 with smb_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'imap_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_imap'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[138]原语 imap_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'imap_sum', 'Action': 'add', 'add': 'a', 'with': "imap_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[139]原语 imap_sum  = add a with (imap_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'imap_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[140]原语 a1 = eval imap_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter imap_sum by count:str\nimap_sum.count = str count by ([:-4])\nimap_sum = add counts with imap_sum[\'count\'] + \'万余\'\n"', 'else': '"\nimap_sum = add counts with imap_sum[\'count\']\n""'}
	try:
		ptree['lineno']=141
		ptree['funs']=block_if_141
		ptree['funs2']=block_if_else_141
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[141]原语 if a1 == "True" with "alter imap_sum by count:stri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'imap_sum', 'Action': 'loc', 'loc': 'imap_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[148]原语 imap_sum = loc imap_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'imap_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[149]原语 rename imap_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'imap_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'imap_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[150]原语 store imap_sum to ssdb by ssdb0 with imap_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smtp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_smtp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[153]原语 smtp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smtp_sum', 'Action': 'add', 'add': 'a', 'with': "smtp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[154]原语 smtp_sum  = add a with (smtp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'smtp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[155]原语 a1 = eval smtp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter smtp_sum by count:str\nsmtp_sum.count = str count by ([:-4])\nsmtp_sum = add counts with smtp_sum[\'count\'] + \'万余\'\n"', 'else': '"\nsmtp_sum = add counts with smtp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=156
		ptree['funs']=block_if_156
		ptree['funs2']=block_if_else_156
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[156]原语 if a1 == "True" with "alter smtp_sum by count:strs... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'smtp_sum', 'Action': 'loc', 'loc': 'smtp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[163]原语 smtp_sum = loc smtp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'smtp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[164]原语 rename smtp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'smtp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'smtp_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[165]原语 store smtp_sum to ssdb by ssdb0 with smtp_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pop3_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_pop3'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[168]原语 pop3_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'pop3_sum', 'Action': 'add', 'add': 'a', 'with': "pop3_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[169]原语 pop3_sum  = add a with (pop3_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'pop3_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[170]原语 a1 = eval pop3_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter pop3_sum by count:str\npop3_sum.count = str count by ([:-4])\npop3_sum = add counts with pop3_sum[\'count\'] + \'万余\'\n"', 'else': '"\npop3_sum = add counts with pop3_sum[\'count\']\n""'}
	try:
		ptree['lineno']=171
		ptree['funs']=block_if_171
		ptree['funs2']=block_if_else_171
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[171]原语 if a1 == "True" with "alter pop3_sum by count:strp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pop3_sum', 'Action': 'loc', 'loc': 'pop3_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[178]原语 pop3_sum = loc pop3_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'pop3_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[179]原语 rename pop3_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'pop3_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pop3_sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[180]原语 store pop3_sum to ssdb by ssdb0 with pop3_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num,name1,name2,name3,name4,name5,name6'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[185]原语 df1 = @udf udf0.new_df with (num,name1,name2,name3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '6,阈值告警,耗时告警,异地访问告警,请求异常告警,API风险告警,敏感信息告警'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[186]原语 df1 = @udf df1 by udf0.df_append with (6,阈值告警,耗时告警... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'alm'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[187]原语 store df1 to ssdb by ssdb0 with alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[190]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[191]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[192]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=193
		ptree['funs']=block_if_193
		ptree['funs2']=block_if_else_193
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[193]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[200]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[201]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[202]原语 store temp_sum to ssdb by ssdb0 with risk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM r_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[206]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[207]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[208]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=209
		ptree['funs']=block_if_209
		ptree['funs2']=block_if_else_209
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[209]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[216]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[217]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'r_req'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[218]原语 store temp_sum to ssdb by ssdb0 with r_req 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM api_delay'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[223]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[224]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[225]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\n\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=226
		ptree['funs']=block_if_226
		ptree['funs2']=block_if_else_226
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[226]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[234]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[235]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'delay'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[236]原语 store temp_sum to ssdb by ssdb0 with delay 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM stat_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[239]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[240]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[241]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=242
		ptree['funs']=block_if_242
		ptree['funs2']=block_if_else_242
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[242]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[249]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[250]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'stat_req'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[251]原语 store temp_sum to ssdb by ssdb0 with stat_req 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM risk_api'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[254]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[255]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[256]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=257
		ptree['funs']=block_if_257
		ptree['funs2']=block_if_else_257
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[257]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[264]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[265]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_api'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[266]原语 store temp_sum to ssdb by ssdb0 with risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp_sum', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*) as count FROM sensitive_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[269]原语 temp_sum = load ckh by ckh with SELECT count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'a', 'with': "temp_sum['count'] >= 10000"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[270]原语 temp_sum  = add a with (temp_sum["count"] >= 10000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a1', 'Action': 'eval', 'eval': 'temp_sum', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[271]原语 a1 = eval temp_sum by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a1 == "True"', 'with': '""\nalter temp_sum by count:str\ntemp_sum.count = str count by ([:-4])\ntemp_sum = add counts with temp_sum[\'count\'] + \'万余\'\n"', 'else': '"\ntemp_sum = add counts with temp_sum[\'count\']\n""'}
	try:
		ptree['lineno']=272
		ptree['funs']=block_if_272
		ptree['funs2']=block_if_else_272
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[272]原语 if a1 == "True" with "alter temp_sum by count:strt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_sum', 'Action': 'loc', 'loc': 'temp_sum', 'by': 'counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[279]原语 temp_sum = loc temp_sum by (counts) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'temp_sum', 'by': '"counts":"count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[280]原语 rename temp_sum by ("counts":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_sum', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive_data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[281]原语 store temp_sum to ssdb by ssdb0 with sensitive_dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_url', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT url,count() as a from api_monitor WHERE toDate(time) > toDate(now())-30 and toDate(time) < toDate(now()) group by url ORDER by a desc LIMIT 5'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[287]原语 zts_url = load ckh by ckh with SELECT url,count() ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_url', 'as': '"a":"接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[288]原语 rename zts_url as ("a":"接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_url', 'by': '接口数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[289]原语 alter zts_url by 接口数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_url', 'Action': '@udf', '@udf': 'zts_url', 'by': 'udf0.df_set_index', 'with': 'url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[290]原语 zts_url = @udf zts_url by udf0.df_set_index with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_url', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_url'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[291]原语 store zts_url to ssdb by ssdb0 with zts_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT app,count() as a from api_monitor group by app ORDER BY a DESC LIMIT 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[294]原语 zts_app = load ckh by ckh with SELECT app,count() ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_app', 'as': '"a":"应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[295]原语 rename zts_app as ("a":"应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_app', 'by': '应用数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[296]原语 alter zts_app by 应用数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_app', 'Action': '@udf', '@udf': 'zts_app', 'by': 'udf0.df_set_index', 'with': 'app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[297]原语 zts_app = @udf zts_app by udf0.df_set_index with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_app'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[298]原语 store zts_app to ssdb by ssdb0 with zts_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_type_count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT api_type,COUNT(*) as a FROM api_monitor md WHERE api_type is NOT NULL group by api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[301]原语 zts_type_count = load ckh by ckh with SELECT api_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_type_count', 'as': '"a":"事件类型数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[302]原语 rename zts_type_count as ("a":"事件类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_type_count', 'by': 'api_type:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[303]原语 alter zts_type_count by api_type:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '0,普通'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[304]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '1,登录'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[305]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '2,敏感数据'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[306]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '3,文件上传'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[307]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '4,文件下载'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[308]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '5,服务接口'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[309]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '6,数据库操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[310]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_replace', 'with': '7,命令操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[311]原语 zts_type_count = @udf zts_type_count by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_type_count', 'by': '事件类型数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[312]原语 alter zts_type_count by 事件类型数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_count', 'Action': '@udf', '@udf': 'zts_type_count', 'by': 'udf0.df_set_index', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[313]原语 zts_type_count = @udf zts_type_count by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_type_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_type_count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[314]原语 store zts_type_count to ssdb by ssdb0 with zts_typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_type_distribution', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT api_type,COUNT(*) as a FROM api_monitor WHERE toDate(time) > toDate(now())-30 and toDate(time) < toDate(now()) and api_type is not null GROUP BY api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[317]原语 zts_type_distribution = load ckh by ckh with SELEC... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_type_distribution', 'as': '"a":"接口类型数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[318]原语 rename zts_type_distribution as ("a":"接口类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_type_distribution', 'by': 'api_type:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[319]原语 alter zts_type_distribution by api_type:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '0,普通'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[320]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '1,登录'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[321]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '2,敏感数据'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[322]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '3,文件上传'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[323]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '4,文件下载'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[324]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '5,服务接口'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[325]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '6,数据库操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[326]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_replace', 'with': '7,命令操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[327]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_type_distribution', 'by': '接口类型数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[328]原语 alter zts_type_distribution by 接口类型数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_distribution', 'Action': '@udf', '@udf': 'zts_type_distribution', 'by': 'udf0.df_set_index', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[329]原语 zts_type_distribution = @udf zts_type_distribution... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_type_distribution', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_type_distribution'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[330]原语 store zts_type_distribution to ssdb by ssdb0 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_month_contrast', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT toMonth(time) as time1,uniqCombined(app) as yy,uniqCombined(url) as jk,count() as shijian,uniqCombined(account) as zh,uniqCombined(srcip) as zd from api_monitor WHERE toDate(time) > toDate(now())-30 and toDate(time) < toDate(now()) GROUP BY time1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[334]原语 zts_month_contrast = load ckh by ckh with SELECT t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'zts_month_contrast.index.size <= 1', 'with': '""\nzts_month_contrast2 = load ckh by ckh with SELECT toMonth(time) as time1,uniqCombined(app) as yy ,uniqCombined(url) as jk ,count() as shijian,uniqCombined(account) as zh ,uniqCombined(srcip) as zd from api_monitor WHERE toDate(time) > toDate(now())-60 and toDate(time) < toDate(now())-30 GROUP BY time1\nzts_month_contrast = union (zts_month_contrast,zts_month_contrast2)\n""'}
	try:
		ptree['lineno']=335
		ptree['funs']=block_if_335
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[335]原语 if zts_month_contrast.index.size <= 1 with "zts_mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'zts_month_contrast.index.size == 1', 'with': '""\nzts_month_contrast = @udf zts_month_contrast by udf0.df_append with (0,0,0,0,0,0)\nzts_month_contrast = loc zts_month_contrast by (time1,yy,jk,zh,zd,shijian)\nzts_month_contrast = @udf zts_month_contrast by udf0.df_set with (iloc[0,0]="本月")\nzts_month_contrast = @udf zts_month_contrast by udf0.df_set with (iloc[1,0]="上月")\n"', 'else': '"\nzts_month_contrast = loc zts_month_contrast by (time1,yy,jk,zh,zd,shijian)\nzts_month_contrast = @udf zts_month_contrast by udf0.df_set with (iloc[0,0]="上月")\nzts_month_contrast = @udf zts_month_contrast by udf0.df_set with (iloc[1,0]="本月")\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=339
		ptree['funs']=block_if_339
		ptree['funs2']=block_if_else_339
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[339]原语 if zts_month_contrast.index.size == 1 with "zts_mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_month_contrast', 'as': '"yy":"应用","jk":"接口","shijian":"事件","zh":"账号","zd":"终端"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[349]原语 rename zts_month_contrast as ("yy":"应用","jk":"接口",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_contrast', 'Action': 'loc', 'loc': 'zts_month_contrast', 'by': 'time1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[350]原语 zts_month_contrast = loc zts_month_contrast by tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[351]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_contrast', 'Action': 'loc', 'loc': 'zts_month_contrast', 'by': 'index', 'to': '类型'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[352]原语 zts_month_contrast = loc zts_month_contrast by ind... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_fillna_cols', 'with': '类型:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[354]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_fillna_cols', 'with': '类型:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[355]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_month_contrast', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_contrast2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[356]原语 store zts_month_contrast to ssdb by ssdb0 with zts... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_application', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT app as yy,uniqCombined(url) as jk,MIN(`time`) as ks,count() as jl FROM api_monitor md group by app ORDER by jk DESC limit 20'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[359]原语 zts_application = load ckh by ckh with SELECT app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_application', 'as': '"yy":"应用名","jk":"接口数量","ks":"开始审计时间","jl":"审计记录数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[360]原语 rename zts_application as ("yy":"应用名","jk":"接口数量",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_application', 'Action': 'loc', 'loc': 'zts_application', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[361]原语 zts_application = loc zts_application by index to ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_application', 'Action': 'add', 'add': '序号', 'by': ' zts_application["序号"]+1 '}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[362]原语 zts_application = add 序号 by ( zts_application["序号"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_application', 'Action': '@udf', '@udf': 'zts_application', 'by': 'udf0.df_fillna_cols', 'with': '审计记录数量:0 ,接口数量:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[363]原语 zts_application = @udf zts_application by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_application', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_application'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[364]原语 store zts_application to ssdb by ssdb0 with zts_ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_type_report', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT content_type as sj,COUNT(*) as jl,uniqCombined(app) as yy FROM api_monitor md WHERE content_type is NOT NULL group by content_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[369]原语 zts_type_report = load ckh by ckh with SELECT cont... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_type_report', 'as': '"sj":"事件类型","jl":"审计记录数量","yy":"应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[370]原语 rename zts_type_report as ("sj":"事件类型","jl":"审计记录数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_type_report', 'Action': 'loc', 'loc': 'zts_type_report', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[371]原语 zts_type_report = loc zts_type_report by index to ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_type_report', 'Action': 'add', 'add': '序号', 'by': ' zts_type_report["序号"]+1 '}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[372]原语 zts_type_report = add 序号 by ( zts_type_report["序号"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_type_report', 'Action': '@udf', '@udf': 'zts_type_report', 'by': 'udf0.df_fillna_cols', 'with': '审计记录数量:0 ,应用数量:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[373]原语 zts_type_report = @udf zts_type_report by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_type_report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_type_report'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[374]原语 store zts_type_report to ssdb by ssdb0 with zts_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_url_report', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT app as yy,url as jk,count() as jl FROM api_monitor md WHERE url is not NULL AND toDate(md.time) > toDate(now())-30 and toDate(md.time) < toDate(now()) group by app,url ORDER by jl DESC limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[379]原语 zts_url_report = load ckh by ckh with SELECT app a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_url_report', 'as': '"yy":"应用","jk":"接口","jl":"审计记录数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[380]原语 rename zts_url_report as ("yy":"应用","jk":"接口","jl"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_url_report', 'Action': 'loc', 'loc': 'zts_url_report', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[381]原语 zts_url_report = loc zts_url_report by index to 序号... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_url_report', 'Action': 'add', 'add': '序号', 'by': ' zts_url_report["序号"]+1 '}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[382]原语 zts_url_report = add 序号 by ( zts_url_report["序号"]+... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_url_report', 'Action': '@udf', '@udf': 'zts_url_report', 'by': 'udf0.df_fillna_cols', 'with': '审计记录数量:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[383]原语 zts_url_report = @udf zts_url_report by udf0.df_fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_url_report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_url_report'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[384]原语 store zts_url_report to ssdb by ssdb0 with zts_url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_ip_top', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select srcip as zd,uniqCombined(app) as yy,uniqCombined(url) as jk from api_visit_hour where LEFT(toString(time),7)=left(toString(now()),7) group by srcip order by yy desc limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[388]原语 zts_ip_top = load ckh by ckh with select srcip as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_ip_top', 'as': '"zd":"终端","yy":"访问应用数","jk":"访问接口数"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[389]原语 rename zts_ip_top as ("zd":"终端","yy":"访问应用数","jk":... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_srcip_top', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT srcip,count() as jl FROM api_monitor md WHERE srcip is not NULL AND toDate(md.time) > toDate(now())-30 and toDate(md.time) < toDate(now()) group by srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[390]原语 zts_srcip_top = load ckh by ckh with SELECT srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_srcip_top', 'as': '"jl":"审计记录数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[391]原语 rename zts_srcip_top as ("jl":"审计记录数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_month_top', 'Action': 'join', 'join': 'zts_ip_top,zts_srcip_top', 'by': '终端,srcip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[393]原语 zts_month_top = join zts_ip_top,zts_srcip_top by 终... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_top', 'Action': 'loc', 'loc': 'zts_month_top', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[394]原语 zts_month_top = loc zts_month_top by index to 序号 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_month_top', 'Action': 'add', 'add': '序号', 'by': ' zts_month_top["序号"]+1 '}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[395]原语 zts_month_top = add 序号 by ( zts_month_top["序号"]+1 ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_top', 'Action': 'loc', 'loc': 'zts_month_top', 'by': '序号,终端,访问应用数,访问接口数,审计记录数量'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[396]原语 zts_month_top = loc zts_month_top by 序号,终端,访问应用数,访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_top', 'Action': '@udf', '@udf': 'zts_month_top', 'by': 'udf0.df_fillna_cols', 'with': '审计记录数量:0 ,访问应用数:0,访问接口数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[397]原语 zts_month_top = @udf zts_month_top by udf0.df_fill... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_month_top', 'by': '审计记录数量:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[398]原语 alter zts_month_top by 审计记录数量:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_month_top', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_month_top'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[399]原语 store zts_month_top to ssdb by ssdb0 with zts_mont... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),srcip,app FROM api_risk group by srcip,app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[404]原语 temp = load ckh by ckh with SELECT count(*),srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[407]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"srcip":"风险来源",\'app\':\'告警应用\',\'count()\':\'告警次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[408]原语 temp_table= rename temp_table as ("srcip":"风险来源","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[409]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[410]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[411]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '告警次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[412]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[413]原语 store temp_table to ssdb by ssdb0 with risk_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),url,type FROM api_delay group by url,type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[419]原语 temp = load ckh by ckh with SELECT count(*),url,ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[422]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"url":"告警接口",\'type\':\'请求类型\',\'count()\':\'告警次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[423]原语 temp_table= rename temp_table as ("url":"告警接口","ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[424]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[425]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[426]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '告警次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[427]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'delay_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[428]原语 store temp_table to ssdb by ssdb0 with delay_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),src_ip,url FROM r_req_alm group by src_ip,url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[433]原语 temp = load ckh by ckh with SELECT count(*),src_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[436]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"src_ip":"异地访问IP",\'url\':\'告警接口\',\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[437]原语 temp_table= rename temp_table as ("src_ip":"异地访问IP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[438]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[439]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[440]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[441]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'r_req_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[442]原语 store temp_table to ssdb by ssdb0 with r_req_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),src_ip,url,status FROM stat_req_alm group by src_ip,url,status'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[446]原语 temp = load ckh by ckh with SELECT count(*),src_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[449]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"src_ip":"源IP",\'url\':\'告警接口\',\'count()\':\'访问次数\',\'status\':\'告警状态\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[450]原语 temp_table= rename temp_table as ("src_ip":"源IP","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[451]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[452]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[453]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[454]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'stat_req_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[455]原语 store temp_table to ssdb by ssdb0 with stat_req_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),url,app FROM risk_api group by url,app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[459]原语 temp = load ckh by ckh with SELECT count(*),url,ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[462]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"app":"告警应用",\'url\':\'告警接口\',\'count()\':\'告警次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[463]原语 temp_table= rename temp_table as ("app":"告警应用","ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[464]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[465]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[466]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '告警次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[467]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_api_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[468]原语 store temp_table to ssdb by ssdb0 with risk_api_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),srcip,app,url_c FROM sensitive_data group by srcip,app,url_c'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[472]原语 temp = load ckh by ckh with SELECT count(*),srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'temp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[475]原语 temp_table= order temp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '"app":"告警应用",\'url_c\':\'告警接口\',\'count()\':\'告警次数\',\'srcip\':\'源IP\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[476]原语 temp_table= rename temp_table as ("app":"告警应用","ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[477]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[478]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[479]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '告警次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[480]原语 temp_table = @udf temp_table by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[481]原语 store temp_table to ssdb by ssdb0 with sensitive_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_dns group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[486]原语 dns = load ckh by ckh with SELECT count(*),dstip,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'dns', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[489]原语 temp_table = order dns by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[490]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[491]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[492]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[493]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[494]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dns_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[495]原语 store temp_table to ssdb by ssdb0 with dns_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_ftp group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[500]原语 ftp = load ckh by ckh with SELECT count(*),dstip,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'ftp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[503]原语 temp_table = order ftp by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[504]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[505]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[506]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[507]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[508]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ftp_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[509]原语 store temp_table to ssdb by ssdb0 with ftp_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_tftp group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[515]原语 tftp = load ckh by ckh with SELECT count(*),dstip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'tftp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[518]原语 temp_table = order tftp by "count()" with desc lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[519]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[520]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[521]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[522]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[523]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tftp_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[524]原语 store temp_table to ssdb by ssdb0 with tftp_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_smb group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[528]原语 smb = load ckh by ckh with SELECT count(*),dstip,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'smb', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[531]原语 temp_table = order smb by "count()" with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[532]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[533]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[534]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[535]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[536]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'smb_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[537]原语 store temp_table to ssdb by ssdb0 with smb_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_imap group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[541]原语 api_imap = load ckh by ckh with SELECT count(*),ds... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'api_imap', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[544]原语 temp_table = order api_imap by "count()" with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[545]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[546]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[547]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[548]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[549]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_imap_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[550]原语 store temp_table to ssdb by ssdb0 with api_imap_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_smtp group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[554]原语 api_smtp = load ckh by ckh with SELECT count(*),ds... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'api_smtp', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[557]原语 temp_table = order api_smtp by "count()" with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[558]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[559]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[560]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[561]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[562]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_smtp_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[563]原语 store temp_table to ssdb by ssdb0 with api_smtp_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT count(*),dstip,srcip FROM api_pop3 group by dstip,srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[568]原语 api_pop3 = load ckh by ckh with SELECT count(*),ds... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'temp_table', 'Action': 'order', 'order': 'api_pop3', 'by': 'count()', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[571]原语 temp_table = order api_pop3 by "count()" with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'temp_table', 'Action': 'rename', 'rename': 'temp_table', 'as': '\'dstip\':\'目的IP\',"srcip":"源IP",\'count()\':\'访问次数\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[572]原语 temp_table = rename temp_table as ("dstip":"目的IP",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'by': 'index', 'to': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[573]原语 temp_table = loc temp_table by index to kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp_table', 'Action': 'loc', 'loc': 'temp_table', 'drop': 'kong'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[574]原语 temp_table = loc temp_table drop kong 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_table', 'Action': 'add', 'add': '序号', 'by': 'temp_table.index+1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[575]原语 temp_table = add 序号 by (temp_table.index+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp_table', 'Action': '@udf', '@udf': 'temp_table', 'by': 'udf0.df_fillna_cols', 'with': '访问次数:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[576]原语 temp_table = @udf temp_table by  udf0.df_fillna_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp_table', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_pop3_list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[577]原语 store temp_table to ssdb by ssdb0 with api_pop3_li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'today', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[581]原语 today = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'today', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$today,[0:10]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[582]原语 today = @sdf sys_str with ($today,[0:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'report0', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'zts_audit_report'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[583]原语 report0 = load ssdb by ssdb0 with zts_audit_report... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,time,type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[584]原语 report=@udf udf0.new_df with name,time,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report', 'Action': '@udf', '@udf': 'report', 'by': 'udf0.df_append', 'with': '@report_name,$today,审计报告'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[585]原语 report = @udf report by udf0.df_append with (@repo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'report', 'Action': 'union', 'union': 'report0,report'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[586]原语 report = union report0,report 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_audit_report'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[587]原语 store report to ssdb by ssdb0 with zts_audit_repor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[592]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[594]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[596]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'result', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts:result'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[598]原语 store result to ssdb by ssdb0 with zts:result 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[601]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[605]原语 b = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[606]原语 b = @udf b by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'b', 'by': 'df.index[0] >0', 'as': 'notice', 'to': '@report_name 报告生成完毕!', 'with': '@report_name 报告生成发现错误!'}
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
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[607]原语 assert b by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'b', 'by': 'df.index[0] >0', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[609]原语 assert b by df.index[0] >0  as notice as alert to ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[610]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_hs_report_export/make_tpl.fea]执行第[613]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],613

#主函数结束,开始块函数

def block_if_34(ptree):

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
		add_the_error('[第34行if语句中]执行第[35]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_34

def block_if_else_34(ptree):

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
		add_the_error('[第34行if_else语句中]执行第[34]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_34

def block_if_81(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dns_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第81行if语句中]执行第[82]原语 alter dns_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'dns_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第81行if语句中]执行第[83]原语 dns_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns_sum', 'Action': 'add', 'add': 'counts', 'with': "dns_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第81行if语句中]执行第[84]原语 dns_sum = add counts with dns_sum["count"] + "万余" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_81

def block_if_else_81(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns_sum', 'Action': 'add', 'add': 'counts', 'with': "dns_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第81行if_else语句中]执行第[81]原语 dns_sum = add counts with dns_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_81

def block_if_96(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ftp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第96行if语句中]执行第[97]原语 alter ftp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'ftp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第96行if语句中]执行第[98]原语 ftp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ftp_sum', 'Action': 'add', 'add': 'counts', 'with': "ftp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第96行if语句中]执行第[99]原语 ftp_sum = add counts with ftp_sum["count"] + "万余" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_96

def block_if_else_96(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'ftp_sum', 'Action': 'add', 'add': 'counts', 'with': "ftp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第96行if_else语句中]执行第[96]原语 ftp_sum = add counts with ftp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_96

def block_if_111(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tftp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第111行if语句中]执行第[112]原语 alter tftp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'tftp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第111行if语句中]执行第[113]原语 tftp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tftp_sum', 'Action': 'add', 'add': 'counts', 'with': "tftp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第111行if语句中]执行第[114]原语 tftp_sum = add counts with tftp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_111

def block_if_else_111(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'tftp_sum', 'Action': 'add', 'add': 'counts', 'with': "tftp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第111行if_else语句中]执行第[111]原语 tftp_sum = add counts with tftp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_111

def block_if_126(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smb_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第126行if语句中]执行第[127]原语 alter smb_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'smb_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第126行if语句中]执行第[128]原语 smb_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smb_sum', 'Action': 'add', 'add': 'counts', 'with': "smb_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第126行if语句中]执行第[129]原语 smb_sum = add counts with smb_sum["count"] + "万余" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_126

def block_if_else_126(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'smb_sum', 'Action': 'add', 'add': 'counts', 'with': "smb_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第126行if_else语句中]执行第[126]原语 smb_sum = add counts with smb_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_126

def block_if_141(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'imap_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第141行if语句中]执行第[142]原语 alter imap_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'imap_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第141行if语句中]执行第[143]原语 imap_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'imap_sum', 'Action': 'add', 'add': 'counts', 'with': "imap_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第141行if语句中]执行第[144]原语 imap_sum = add counts with imap_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_141

def block_if_else_141(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'imap_sum', 'Action': 'add', 'add': 'counts', 'with': "imap_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第141行if_else语句中]执行第[141]原语 imap_sum = add counts with imap_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_141

def block_if_156(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smtp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[157]原语 alter smtp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'smtp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[158]原语 smtp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smtp_sum', 'Action': 'add', 'add': 'counts', 'with': "smtp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[159]原语 smtp_sum = add counts with smtp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_156

def block_if_else_156(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'smtp_sum', 'Action': 'add', 'add': 'counts', 'with': "smtp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第156行if_else语句中]执行第[156]原语 smtp_sum = add counts with smtp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_156

def block_if_171(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'pop3_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[172]原语 alter pop3_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'pop3_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[173]原语 pop3_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'pop3_sum', 'Action': 'add', 'add': 'counts', 'with': "pop3_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[174]原语 pop3_sum = add counts with pop3_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_171

def block_if_else_171(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'pop3_sum', 'Action': 'add', 'add': 'counts', 'with': "pop3_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第171行if_else语句中]执行第[171]原语 pop3_sum = add counts with pop3_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_171

def block_if_193(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第193行if语句中]执行第[194]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第193行if语句中]执行第[195]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第193行if语句中]执行第[196]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_193

def block_if_else_193(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第193行if_else语句中]执行第[193]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_193

def block_if_209(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[210]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[211]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[212]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_209

def block_if_else_209(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第209行if_else语句中]执行第[209]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_209

def block_if_226(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第226行if语句中]执行第[228]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第226行if语句中]执行第[229]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第226行if语句中]执行第[230]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_226

def block_if_else_226(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第226行if_else语句中]执行第[226]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_226

def block_if_242(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第242行if语句中]执行第[243]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第242行if语句中]执行第[244]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第242行if语句中]执行第[245]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_242

def block_if_else_242(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第242行if_else语句中]执行第[242]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_242

def block_if_257(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[258]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[259]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[260]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_257

def block_if_else_257(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第257行if_else语句中]执行第[257]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_257

def block_if_272(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'temp_sum', 'by': 'count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第272行if语句中]执行第[273]原语 alter temp_sum by count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'temp_sum.count', 'Action': 'str', 'str': 'count', 'by': '[:-4]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第272行if语句中]执行第[274]原语 temp_sum.count = str count by ([:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count'] + '万余'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第272行if语句中]执行第[275]原语 temp_sum = add counts with temp_sum["count"] + "万余... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_272

def block_if_else_272(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'temp_sum', 'Action': 'add', 'add': 'counts', 'with': "temp_sum['count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第272行if_else语句中]执行第[272]原语 temp_sum = add counts with temp_sum["count"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_272

def block_if_335(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_month_contrast2', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT toMonth(time) as time1,uniqCombined(app) as yy ,uniqCombined(url) as jk ,count() as shijian,uniqCombined(account) as zh ,uniqCombined(srcip) as zd from api_monitor WHERE toDate(time) > toDate(now())-60 and toDate(time) < toDate(now())-30 GROUP BY time1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第335行if语句中]执行第[336]原语 zts_month_contrast2 = load ckh by ckh with SELECT ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'zts_month_contrast', 'Action': 'union', 'union': 'zts_month_contrast,zts_month_contrast2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第335行if语句中]执行第[337]原语 zts_month_contrast = union (zts_month_contrast,zts... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_335

def block_if_339(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_append', 'with': '0,0,0,0,0,0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第339行if语句中]执行第[340]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_contrast', 'Action': 'loc', 'loc': 'zts_month_contrast', 'by': 'time1,yy,jk,zh,zd,shijian'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第339行if语句中]执行第[341]原语 zts_month_contrast = loc zts_month_contrast by (ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_set', 'with': 'iloc[0,0]="本月"'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第339行if语句中]执行第[342]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_set', 'with': 'iloc[1,0]="上月"'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第339行if语句中]执行第[343]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_339

def block_if_else_339(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_contrast', 'Action': 'loc', 'loc': 'zts_month_contrast', 'by': 'time1,yy,jk,zh,zd,shijian'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第339行if_else语句中]执行第[339]原语 zts_month_contrast = loc zts_month_contrast by (ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_set', 'with': 'iloc[0,0]="上月"'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第339行if_else语句中]执行第[340]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_set', 'with': 'iloc[1,0]="本月"'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第339行if_else语句中]执行第[341]原语 zts_month_contrast = @udf zts_month_contrast by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_339

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



