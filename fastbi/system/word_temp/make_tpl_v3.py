#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: system/word_temp/make_tpl
#datetime: 2024-08-30T16:10:56.712487
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
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[20]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[23]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[24]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=27
		ptree['funs']=block_if_27
		ptree['funs2']=block_if_else_27
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[27]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[33]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[37]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[38]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'sys_name,dns,vuln_type,level,des,url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[50]原语 b = @udf udf0.new_df with (sys_name,dns,vuln_type,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_append', 'with': '漏洞修复中心,www.baidu.com,5,12,木马漏洞,www.google.com'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[51]原语 b = @udf b by udf0.df_append with (漏洞修复中心,www.baid... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'exam_t1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[52]原语 store b to ssdb by ssdb0 with exam_t1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'fix_comm,org_name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[54]原语 c = @udf udf0.new_df with (fix_comm,org_name) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '定时修复,商务部组织'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[55]原语 c = @udf c by udf0.df_append with (定时修复,商务部组织) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'c', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'exam_t2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[56]原语 store c to ssdb by ssdb0 with exam_t2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'length,width'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[59]原语 scatter= @udf udf0.new_df with (length,width) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'scatter', 'by': 'udf0.df_append', 'with': '5.1,3.5'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[60]原语 scatter= @udf scatter by udf0.df_append with (5.1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'scatter', 'by': 'udf0.df_append', 'with': '4.9,3.0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[61]原语 scatter= @udf scatter by udf0.df_append with (4.9,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'scatter', 'by': 'udf0.df_append', 'with': '7.0,3.2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[62]原语 scatter= @udf scatter by udf0.df_append with (7.0,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'scatter', 'by': 'udf0.df_append', 'with': '6.4,3.2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[63]原语 scatter= @udf scatter by udf0.df_append with (6.4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'scatter', 'Action': '@udf', '@udf': 'scatter', 'by': 'udf0.df_append', 'with': '5.9,3.0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[64]原语 scatter= @udf scatter by udf0.df_append with (5.9,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'scatter.length', 'as': 'float'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[65]原语 alter scatter.length as float 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'scatter.width', 'as': 'float'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[66]原语 alter scatter.width as float 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'scatter', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'scatter_key'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[67]原语 store scatter to ssdb by ssdb0 with scatter_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'other', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'lab,val'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[69]原语 other= @udf udf0.new_df with (lab,val) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'other', 'Action': '@udf', '@udf': 'other', 'by': 'udf0.df_append', 'with': '厨师,10'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[70]原语 other= @udf other by udf0.df_append with (厨师,10) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'other', 'Action': '@udf', '@udf': 'other', 'by': 'udf0.df_append', 'with': '店主,30'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[71]原语 other= @udf other by udf0.df_append with (店主,30) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'other', 'Action': '@udf', '@udf': 'other', 'by': 'udf0.df_append', 'with': '学生,20'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[72]原语 other= @udf other by udf0.df_append with (学生,20) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'other.val', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[73]原语 alter other.val as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'other', 'Action': '@udf', '@udf': 'other', 'by': 'udf0.df_set_index', 'with': 'lab'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[74]原语 other = @udf other by udf0.df_set_index with (lab)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'other', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'other_key'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[75]原语 store other to ssdb by ssdb0 with other_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'date,type,desc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[80]原语 c = @udf udf0.new_df with (date,type,desc) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '2013-02-31,tt,例子1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[81]原语 c = @udf c by udf0.df_append with (2013-02-31,tt,例... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '2004-02-24,vv,例子2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[82]原语 c = @udf c by udf0.df_append with (2004-02-24,vv,例... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '2034-02-09,uu,例子3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[83]原语 c = @udf c by udf0.df_append with (2034-02-09,uu,例... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'c', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'table_exam'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[84]原语 store c to ssdb by ssdb0 with table_exam 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'title1,type1,instro1,method1,pop1,sys1,inco1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[86]原语 d = @udf udf0.new_df with (title1,type1,instro1,me... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'd', 'by': 'udf0.df_append', 'with': 'HTTP_SQL注入攻击,CGI攻击,SQL注入攻击源于英文attack,使用安全的代码定期查看WEB服务日志,流行,Web 服务器,多种操作系统'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[87]原语 d = @udf d by udf0.df_append with (HTTP_SQL注入攻击,CG... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'd', 'by': 'udf0.df_append', 'with': 'HTTP_XSS攻击,CGI攻击,XSCross-Site Scripting跨站脚本攻击,如无需要请在WEB浏览器上禁用javascript脚本,流行,Web 服务器,单一操作系统'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[88]原语 d = @udf d by udf0.df_append with (HTTP_XSS攻击,CGI攻... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'reg_table_exam'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[89]原语 store d to ssdb by ssdb0 with reg_table_exam 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[93]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[95]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[97]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[100]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[102]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[105]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[106]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[107]原语 assert t by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[109]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[system/word_temp/make_tpl.fbi]执行第[112]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],112

#主函数结束,开始块函数

def block_if_27(ptree):

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
		add_the_error('[第27行if语句中]执行第[28]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_27

def block_if_else_27(ptree):

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
		add_the_error('[第27行if_else语句中]执行第[27]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_27

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



