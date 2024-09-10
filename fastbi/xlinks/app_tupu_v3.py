#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: xlinks/app_tupu
#datetime: 2024-08-30T16:10:58.185946
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
		add_the_error('[xlinks/app_tupu.fbi]执行第[18]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'app_agent'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[24]原语 aa = load ssdb by ssdb0 with app_agent 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[26]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load db by mysql1 with select min(gmt_modified) as time from app_datalink'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=27
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[27]原语 if $a_num == 0 with aa = load db by mysql1 with se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[29]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select max(gmt_modified) as time from app_datalink'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[31]原语 aa = load db by mysql1 with select max(gmt_modifie... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[32]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app from app_datalink where gmt_modified >= '$time1' and gmt_modified < '$time2' limit 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[35]原语 ccc = load db by mysql1 with select app from app_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[xlinks/app_tupu.fbi]执行第[36]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[36]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_agent'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[38]原语 store aa to ssdb by ssdb0 with app_agent 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_datalink', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct src_ip,app,url from app_datalink where gmt_modified >= '$time1' and gmt_modified < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[43]原语 app_datalink = load db by mysql1 with select disti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'yy_jj', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'src_ip,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[45]原语 yy_jj = loc app_datalink by src_ip,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'yy_jj', 'Action': 'distinct', 'distinct': 'yy_jj', 'by': 'src_ip,url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[46]原语 yy_jj = distinct yy_jj by src_ip,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'yy_jj', 'as': "'src_ip':'A','url':'B'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[47]原语 rename yy_jj as ("src_ip":"A","url":"B") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'yy_jj', 'Action': 'add', 'add': 'C', 'by': "'visit'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[48]原语 yy_jj = add C by ("visit") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'jj_md', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'app,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[51]原语 jj_md = loc app_datalink by app,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'jj_md', 'Action': 'distinct', 'distinct': 'jj_md', 'by': 'app,url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[52]原语 jj_md = distinct jj_md by app,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'jj_md', 'as': "'url':'A','app':'B'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[53]原语 rename jj_md as ("url":"A","app":"B") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'jj_md', 'Action': 'add', 'add': 'C', 'by': "'belong'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[54]原语 jj_md = add C by ("belong") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ff', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_sum from data_app_new where merge_state = 2'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[57]原语 ff = load db by mysql1 with select app,app_sum fro... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aaa', 'Action': 'loc', 'loc': 'ff', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[58]原语 aaa = loc ff by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'father', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'A,B'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[59]原语 father = @udf udf0.new_df with A,B 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'aaa', 'with': 'app=$1', 'run': '""\napp_1 = filter ff by app == \'@app\'\napp_1.app_sum = lambda app_sum by (x:x.split(","))\napp_1 = @udf app_1 by udf0.df_l2cs with app_sum\napp_1 = @udf app_1 by udf0.df_reset_index\napp_1 = loc app_1 drop index,app,app_sum\napp_1 = @udf app_1 by udf0.df_T\nrename app_1 as (0:\'B\')\napp_1 = filter app_1 by B != \'@app\'\napp_1 = add A by (\'@app\')\nfather = union father,app_1\n""'}
	try:
		ptree['lineno']=60
		ptree['funs']=block_foreach_60
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[60]原语 foreach aaa run "app_1 = filter ff by app == "@app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'father', 'Action': 'loc', 'loc': 'father', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[72]原语 father = loc father by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'father', 'Action': 'loc', 'loc': 'father', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[73]原语 father = loc father drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'father', 'Action': 'add', 'add': 'C', 'by': "'father'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[74]原语 father = add C by ("father") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'father', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'father_data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[75]原语 store father to ssdb by ssdb0 with father_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app_link', 'Action': 'union', 'union': 'yy_jj,jj_md,father'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[78]原语 app_link = union yy_jj,jj_md,father 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_ll', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct A,B,C from api_link'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[79]原语 app_ll = load ckh by ckh with select distinct A,B,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_ll', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[80]原语 app_ll = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_link', 'Action': 'join', 'join': 'app_link,app_ll', 'by': '[A,B,C],[A,B,C]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[81]原语 app_link = join app_link,app_ll by [A,B,C],[A,B,C]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_link', 'Action': '@udf', '@udf': 'app_link', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[82]原语 app_link = @udf app_link by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_link', 'Action': 'filter', 'filter': 'app_link', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[83]原语 app_link = filter app_link by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_link', 'Action': 'loc', 'loc': 'app_link', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[84]原语 app_link = loc app_link drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_link', 'as': "'A':'S','B':'O','C':'P'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[85]原语 rename app_link as ("A":"S","B":"O","C":"P") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_count', 'Action': 'eval', 'eval': 'app_link', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[88]原语 new_count = eval app_link by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'add_count', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($new_count/5000) + 2'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[89]原语 add_count = @sdf sys_eval with (int($new_count/500... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new_pd', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[91]原语 new_pd = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'new_pd', 'Action': 'add', 'add': 'num', 'by': 'range(1,$add_count)'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[92]原语 new_pd = add num by (range(1,$add_count)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'new_pd', 'with': 'num = $1', 'run': '""\nadd1 = filter app_link by index >= 5000 * (@num -1) and index < 5000 * @num\nret = @udf add1 by GL.add_http_mkd\nret_pd = @sdf sys_lambda with ($ret,x: \'Successfully\' in x )\nif $ret_pd == True with rename app_link as (\'S\':\'A\',\'O\':\'B\',\'P\':\'C\')\nif $ret_pd == True with store add1 to ckh by ckh with api_link\n""'}
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
		add_the_error('[xlinks/app_tupu.fbi]执行第[94]原语 foreach new_pd run "add1 = filter app_link by inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app11', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'src_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[106]原语 app11 = loc app_datalink by src_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app11', 'as': "'src_ip':'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[107]原语 rename app11 as ("src_ip":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app22', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[108]原语 app22 = loc app_datalink by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app33', 'Action': 'loc', 'loc': 'father', 'by': 'B'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[109]原语 app33 = loc father by B 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app33', 'as': "'B':'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[110]原语 rename app33 as ("B":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app', 'Action': 'union', 'union': 'app11,app22,aaa,app33'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[111]原语 app = union app11,app22,aaa,app33 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[112]原语 app = distinct app by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct app as S,app_type as O from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[115]原语 app_1 = load db by mysql1 with select distinct app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_1.O', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[116]原语 alter app_1.O as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:APP-app_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[117]原语 app_type = load ssdb by ssdb0 with dd:APP-app_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1,app_type', 'by': 'SP.tag2dict', 'with': 'O'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[118]原语 app_1 = @udf app_1,app_type by SP.tag2dict with O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'P', 'by': "'type'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[119]原语 app_1 = add P by ("type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_1', 'Action': 'join', 'join': 'app_1,app', 'by': 'S,app', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[120]原语 app_1 = join app_1,app by S,app with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_1', 'Action': 'loc', 'loc': 'app_1', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[121]原语 app_1 = loc app_1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[122]原语 app_1 = @udf app_1 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_1', 'Action': 'filter', 'filter': 'app_1', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[123]原语 app_1 = filter app_1 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[126]原语 api = loc app_datalink by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api', 'as': "'url':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[127]原语 rename api as ("url":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'O', 'by': "'接口'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[128]原语 api = add O by ("接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'P', 'by': "'type'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[129]原语 api = add P by ("type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app_un', 'Action': 'union', 'union': 'app_1,api'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[132]原语 app_un = union app_1,api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct S,O,P from api_link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[133]原语 app_data = load ckh by ckh with select distinct S,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_data', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[134]原语 app_data = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_un', 'Action': 'join', 'join': 'app_un,app_data', 'by': '[S,O,P],[S,O,P]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[135]原语 app_un = join app_un,app_data by [S,O,P],[S,O,P] w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_un', 'Action': '@udf', '@udf': 'app_un', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[136]原语 app_un = @udf app_un by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_un', 'Action': 'filter', 'filter': 'app_un', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[137]原语 app_un = filter app_un by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_un', 'Action': 'loc', 'loc': 'app_un', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[138]原语 app_un = loc app_un by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_count', 'Action': 'eval', 'eval': 'app_un', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[141]原语 new_count = eval app_un by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'add_count', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($new_count/5000) + 2'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[142]原语 add_count = @sdf sys_eval with (int($new_count/500... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new_pd', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[144]原语 new_pd = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'new_pd', 'Action': 'add', 'add': 'num', 'by': 'range(1,$add_count)'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[145]原语 new_pd = add num by (range(1,$add_count)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'new_pd', 'with': 'num = $1', 'run': '""\nadd1 = filter app_un by index >= 5000 * (@num -1) and index < 5000 * @num\nret = @udf add1 by GL.add_http_mkd\nret_pd = @sdf sys_lambda with ($ret,x: \'Successfully\' in x )\nif $ret_pd == True with store add1 to ckh by ckh with api_link_data\n""'}
	try:
		ptree['lineno']=147
		ptree['funs']=block_foreach_147
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[147]原语 foreach new_pd run "add1 = filter app_un by index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_node1', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'src_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[156]原语 app_node1 = loc app_datalink by src_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_node1', 'as': "'src_ip':'id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[157]原语 rename app_node1 as ("src_ip":"id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_node2', 'Action': 'loc', 'loc': 'app_datalink', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[158]原语 app_node2 = loc app_datalink by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_node2', 'as': "'app':'id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[159]原语 rename app_node2 as ("app":"id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app_node', 'Action': 'union', 'union': 'app_node1,app_node2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[160]原语 app_node = union (app_node1,app_node2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app_node', 'Action': 'distinct', 'distinct': 'app_node', 'by': 'id'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[161]原语 app_node = distinct app_node by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_data', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,sensitive_label,app_type,active from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[163]原语 app_data = load db by mysql1 with select app,sensi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[164]原语 app_active = load ssdb by ssdb0 with dd:api_active... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_data.active.app_type.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[165]原语 alter app_data.active.app_type.sensitive_label as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_data', 'Action': '@udf', '@udf': 'app_data,app_active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[166]原语 app_data = @udf app_data,app_active by SP.tag2dict... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_data', 'Action': '@udf', '@udf': 'app_data,app_type', 'by': 'SP.tag2dict', 'with': 'app_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[168]原语 app_data = @udf app_data,app_type by SP.tag2dict w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:sensitive_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[169]原语 sens = load ssdb by ssdb0 with dd:sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_data', 'Action': '@udf', '@udf': 'app_data,sens', 'by': 'SP.tag2dict', 'with': 'sensitive_label'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[170]原语 app_data = @udf app_data,sens by SP.tag2dict with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_data', 'as': "'sensitive_label':'敏感类型','app_type':'应用类型','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[171]原语 rename app_data as ("sensitive_label":"敏感类型","app_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app_node', 'with': 'app=$1', 'run': '""\napp_node1 = filter app_data by app == \'@app\'\nrename app_node1 as (\'app\':\'应用IP/域名\')\nstore app_node1 to ssdb by ssdb0 with app_node:@app\n""'}
	try:
		ptree['lineno']=173
		ptree['funs']=block_foreach_173
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[173]原语 foreach app_node run "app_node1 = filter app_data ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[xlinks/app_tupu.fbi]执行第[180]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],180

#主函数结束,开始块函数

def block_foreach_60(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_1', 'Action': 'filter', 'filter': 'ff', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[61]原语 app_1 = filter ff by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_1.app_sum', 'Action': 'lambda', 'lambda': 'app_sum', 'by': 'x:x.split(",")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[62]原语 app_1.app_sum = lambda app_sum by (x:x.split(","))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_l2cs', 'with': 'app_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[63]原语 app_1 = @udf app_1 by udf0.df_l2cs with app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[64]原语 app_1 = @udf app_1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_1', 'Action': 'loc', 'loc': 'app_1', 'drop': 'index,app,app_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[65]原语 app_1 = loc app_1 drop index,app,app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[66]原语 app_1 = @udf app_1 by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_1', 'as': "0:'B'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[67]原语 rename app_1 as (0:"B") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_1', 'Action': 'filter', 'filter': 'app_1', 'by': "B != '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[68]原语 app_1 = filter app_1 by B != "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'A', 'by': "'@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[69]原语 app_1 = add A by ("@app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'father', 'Action': 'union', 'union': 'father,app_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第60行foreach语句中]执行第[70]原语 father = union father,app_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_60

def block_foreach_94(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'add1', 'Action': 'filter', 'filter': 'app_link', 'by': 'index >= 5000 * (@num -1) and index < 5000 * @num'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[95]原语 add1 = filter app_link by index >= 5000 * (@num -1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'add1', 'by': 'GL.add_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[96]原语 ret = @udf add1 by GL.add_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ret_pd', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$ret,x: 'Successfully' in x "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[97]原语 ret_pd = @sdf sys_lambda with ($ret,x: "Successful... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ret_pd == True', 'with': "rename app_link as ('S':'A','O':'B','P':'C')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=98
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[98]原语 if $ret_pd == True with rename app_link as ("S":"A... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ret_pd == True', 'with': 'store add1 to ckh by ckh with api_link'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=99
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[99]原语 if $ret_pd == True with store add1 to ckh by ckh w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_94

def block_foreach_147(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'add1', 'Action': 'filter', 'filter': 'app_un', 'by': 'index >= 5000 * (@num -1) and index < 5000 * @num'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第147行foreach语句中]执行第[148]原语 add1 = filter app_un by index >= 5000 * (@num -1) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'add1', 'by': 'GL.add_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第147行foreach语句中]执行第[149]原语 ret = @udf add1 by GL.add_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ret_pd', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$ret,x: 'Successfully' in x "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第147行foreach语句中]执行第[150]原语 ret_pd = @sdf sys_lambda with ($ret,x: "Successful... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ret_pd == True', 'with': 'store add1 to ckh by ckh with api_link_data'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=151
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第147行foreach语句中]执行第[151]原语 if $ret_pd == True with store add1 to ckh by ckh w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_147

def block_foreach_173(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_node1', 'Action': 'filter', 'filter': 'app_data', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第173行foreach语句中]执行第[174]原语 app_node1 = filter app_data by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_node1', 'as': "'app':'应用IP/域名'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第173行foreach语句中]执行第[175]原语 rename app_node1 as ("app":"应用IP/域名") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_node1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_node:@app'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第173行foreach语句中]执行第[176]原语 store app_node1 to ssdb by ssdb0 with app_node:@ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_173

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



