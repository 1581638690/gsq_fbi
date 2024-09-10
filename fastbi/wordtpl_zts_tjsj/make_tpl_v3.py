#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_zts_tjsj/make_tpl
#datetime: 2024-08-30T16:10:56.975319
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
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[23]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[26]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[31]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[32]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[35]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[41]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[45]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[46]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'IP']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[56]原语 app = eval a by loc[0,"IP"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj1', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,SELECT '$app' as 'name' ,count(*) as 'jk' from data_api_new where app = '$app'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[59]原语 zts_sj1 = @udf RS.load_mysql_sql with (mysql1,SELE... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj2', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,SELECT '$app' as 'name' ,count(*) as 'xsjjk' from data_api_new where app = '$app' and api_status=1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[60]原语 zts_sj2 = @udf RS.load_mysql_sql with (mysql1,SELE... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_sj3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT '$app' as name,count(distinct url) as ysjjk,count(*) as sjfw,count(distinct api_type) as sjlx from api_monitor where app = '$app'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[65]原语 zts_sj3 = load ckh by ckh with SELECT "$app" as na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_sj4', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT '$app' as name,max(time) as time_max,min(time) as time_min,formatDateTime(now(),'%Y-%m-%d') as time from api_monitor where app = '$app'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[66]原语 zts_sj4 = load ckh by ckh with SELECT "$app" as na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj0', 'Action': 'join', 'join': 'zts_sj1,zts_sj2', 'by': 'name,name'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[68]原语 zts_sj0 = join zts_sj1,zts_sj2 by name,name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj0', 'Action': 'join', 'join': 'zts_sj0,zts_sj3', 'by': 'name,name'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[69]原语 zts_sj0 = join zts_sj0,zts_sj3 by name,name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj0', 'Action': 'join', 'join': 'zts_sj0,zts_sj4', 'by': 'name,name'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[70]原语 zts_sj0 = join zts_sj0,zts_sj4 by name,name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj0', 'Action': '@udf', '@udf': 'zts_sj0', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[71]原语 zts_sj0 = @udf zts_sj0 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_sj0', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_sj0'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[72]原语 store zts_sj0 to ssdb by ssdb0 with zts_sj0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_s1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT api_type as sjlx,count(distinct url) as sjjk,count(*) as sjfw from api_monitor where app = '$app' group by api_type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[77]原语 zts_s1 =load ckh by ckh with SELECT api_type as sj... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_s1', 'by': 'sjlx:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[78]原语 alter zts_s1 by sjlx:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '0,普通'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[79]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (0,普通... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '1,登录'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[80]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (1,登录... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '2,敏感数据'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[81]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (2,敏感... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '3,文件上传'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[82]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (3,文件... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '4,文件下载'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[83]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (4,文件... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '5,服务接口'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[84]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (5,服务... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '6,数据库操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[85]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (6,数据... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '7,命令操作'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[86]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (7,命令... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s1', 'Action': '@udf', '@udf': 'zts_s1', 'by': 'udf0.df_replace', 'with': '8,注销'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[87]原语 zts_s1 = @udf zts_s1 by udf0.df_replace with (8,注销... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'zts_s1', 'Action': 'rename', 'rename': 'zts_s1', 'by': '"sjlx":"事件类型","sjjk":"已审计接口","sjfw":"审计记录"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[88]原语 zts_s1 = rename zts_s1 by ("sjlx":"事件类型","sjjk":"已... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_s1', 'Action': 'loc', 'loc': 'zts_s1', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[89]原语 zts_s1 = loc zts_s1 by index to 序号 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_s1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_s1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[90]原语 store zts_s1 to ssdb by ssdb0 with zts_s1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_s2', 'Action': 'loc', 'loc': 'zts_s1', 'by': '事件类型,审计记录'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[91]原语 zts_s2 = loc zts_s1 by 事件类型,审计记录 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_s2', 'Action': '@udf', '@udf': 'zts_s2', 'by': 'udf0.df_set_index', 'with': '事件类型'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[92]原语 zts_s2 = @udf zts_s2 by udf0.df_set_index with (事件... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_s2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_s2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[93]原语 store zts_s2 to ssdb by ssdb0 with zts_s2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_s3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,count(*) as mun,sum(case when risk_level = '2' then 1 else 0 end) as risk_num from api_monitor where app = '$app' group by url order by mun limit 10"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[97]原语 zts_s3 = load ckh by ckh with select url,count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'zts_s3', 'Action': 'rename', 'rename': 'zts_s3', 'by': '"url":"接口名","mun":"审计记录","risk_num":"高风险记录"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[99]原语 zts_s3 = rename zts_s3 by ("url":"接口名","mun":"审计记录... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_s3', 'Action': 'loc', 'loc': 'zts_s3', 'by': 'index', 'to': '序号'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[100]原语 zts_s3 = loc zts_s3 by index to 序号 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_s3', 'by': '高风险记录:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[102]原语 alter zts_s3 by 高风险记录:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_s3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_s3'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[103]原语 store zts_s3 to ssdb by ssdb0 with zts_s3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'today', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[105]原语 today = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[106]原语 today = @sdf sys_str with ($today,[0:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'report0', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'zts_audit_report'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[107]原语 report0 = load ssdb by ssdb0 with zts_audit_report... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,time,type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[108]原语 report=@udf udf0.new_df with name,time,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report', 'Action': '@udf', '@udf': 'report', 'by': 'udf0.df_append', 'with': '@report_name,$today,应用审计报告'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[109]原语 report = @udf report by udf0.df_append with (@repo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'report', 'Action': 'union', 'union': 'report0,report'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[110]原语 report = union report0,report 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'report', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts_audit_report'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[111]原语 store report to ssdb by ssdb0 with zts_audit_repor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[116]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[118]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[120]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'result', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts:result'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[122]原语 store result to ssdb by ssdb0 with zts:result 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[126]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= assert', 'Ta': 'ret', 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[128]原语 ret = assert not_have_error() as alert to 报告生成完成! ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ret', 'with': '""\n#保存\nb = add status with (\'报告生成完毕\')\nb = @udf b by CRUD.save_table with (@link,@table)\nassert b by df.index[0] >0 as notice to @report_name 报告生成完毕! with @report_name 报告生成发现错误!\nassert b by df.index[0] >0 as alert to 报告生成完成! with 报告生成发现错误!\n"', 'else': '"\nb = add status with (\'报告生成出错\')\nb = @udf b by CRUD.save_table with (@link,@table)\nassert True as notice to @report_name 报告生成出错! with @report_name 报告生成发现错误!\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=130
		ptree['funs']=block_if_130
		ptree['funs2']=block_if_else_130
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[130]原语 if $ret with "#保存b = add status with ("报告生成完毕")b =... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[142]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_zts_tjsj/make_tpl.fbi]执行第[145]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],146

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

def block_if_130(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第130行if语句中]执行第[132]原语 b = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第130行if语句中]执行第[133]原语 b = @udf b by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第130行if语句中]执行第[134]原语 assert b by df.index[0] >0 as notice to @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'b', 'by': 'df.index[0] >0', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第130行if语句中]执行第[135]原语 assert b by df.index[0] >0 as alert to 报告生成完成! wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_130

def block_if_else_130(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= add', 'Ta': 'b', 'Action': 'add', 'add': 'status', 'with': "'报告生成出错'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第130行if_else语句中]执行第[130]原语 b = add status with ("报告生成出错") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第130行if_else语句中]执行第[131]原语 b = @udf b by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'True', 'as': 'notice', 'to': '@report_name 报告生成出错!', 'with': '@report_name 报告生成发现错误!'}
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
		add_the_error('[第130行if_else语句中]执行第[132]原语 assert True as notice to @report_name 报告生成出错! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_130

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



