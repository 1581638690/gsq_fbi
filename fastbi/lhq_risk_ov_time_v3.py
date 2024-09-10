#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_risk_ov_time
#datetime: 2024-08-30T16:10:55.576169
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
		add_the_error('[lhq_risk_ov_time.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[15]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[lhq_risk_ov_time.fbi]执行第[16]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[16]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[19]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month1,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[20]原语 month = @sdf format_now with ($month1,"%Y-%m-%d 00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select type,count(*) as r_num from api19_risk where last_time > '$month' group by type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[22]原语 api = load db by mysql1 with select type,count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api', 'by': 'type:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[23]原语 alter api by type:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_n', 'Action': 'loc', 'loc': 'api', 'by': 'r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[24]原语 api_n = loc api by r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_n', 'Action': 'add', 'add': 'ss', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[25]原语 api_n = add ss by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_n', 'Action': 'group', 'group': 'api_n', 'by': 'ss', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[26]原语 api_n = group api_n by ss agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_n', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[27]原语 aa_num = eval api_n by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num == 0', 'with': 'api_n = @udf api_n by udf0.df_append with 0'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=28
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[28]原语 if $aa_num == 0 with api_n = @udf api_n by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_n', 'as': "'r_num_sum':'弱点接口数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[29]原语 rename api_n as ("r_num_sum":"弱点接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_n', 'Action': 'loc', 'loc': 'api_n', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[30]原语 api_n = loc api_n by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_n', 'Action': 'loc', 'loc': 'api_n', 'by': 'drop', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[31]原语 api_n = loc api_n by drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_n', 'Action': '@udf', '@udf': 'api_n', 'by': 'udf0.df_append', 'with': '近一个月'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[32]原语 api_n = @udf api_n by udf0.df_append with 近一个月 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_n', 'Action': 'add', 'add': '参数', 'by': "'参数可遍历'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[33]原语 api_n = add 参数 by ("参数可遍历") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_n', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_n:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[34]原语 store api_n to ssdb by ssdb0 with api_n:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api19_risk_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[36]原语 api19_type = load ssdb by ssdb0 with dd:api19_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_type', 'Action': 'loc', 'loc': 'api19_type', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[37]原语 api19_type = loc api19_type by index to type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api', 'Action': 'join', 'join': 'api,api19_type', 'by': 'type,type', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[38]原语 api = join api,api19_type by type,type with outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_fillna_cols', 'with': 'r_num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[39]原语 api = @udf api by udf0.df_fillna_cols with r_num:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api', 'Action': 'order', 'order': 'api', 'by': 'r_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[40]原语 api = order api by r_num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api', 'Action': 'loc', 'loc': 'api', 'by': 'value,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[41]原语 api = loc api by value,r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'name1', 'Action': 'eval', 'eval': 'api', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[43]原语 name1 = eval api by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api_1', 'Action': 'filter', 'filter': 'api', 'by': "value == '$name1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[44]原语 api_1 = filter api by value == "$name1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_1', 'Action': 'loc', 'loc': 'api_1', 'by': 'value', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[45]原语 api_1 = loc api_1 by value to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_1', 'as': "'r_num':'$name1'"}
	ptree['as'] = deal_sdf(workspace,ptree['as'])
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[46]原语 rename api_1 as ("r_num":"$name1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_1', 'Action': '@udf', '@udf': 'api_1', 'by': 'udf0.df_append', 'with': '近一个月弱点接口数排名第一的弱点类型的接口数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[47]原语 api_1 = @udf api_1 by udf0.df_append with 近一个月弱点接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_1', 'Action': 'add', 'add': '参数', 'by': "'$name1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[48]原语 api_1 = add 参数 by ("$name1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_1:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[49]原语 store api_1 to ssdb by ssdb0 with api_1:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'name2', 'Action': 'eval', 'eval': 'api', 'by': 'iloc[2,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[51]原语 name2 = eval api by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api_2', 'Action': 'filter', 'filter': 'api', 'by': "value == '$name2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[52]原语 api_2 = filter api by value == "$name2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_2', 'Action': 'loc', 'loc': 'api_2', 'by': 'value', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[53]原语 api_2 = loc api_2 by value to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_2', 'as': "'r_num':'$name2'"}
	ptree['as'] = deal_sdf(workspace,ptree['as'])
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[54]原语 rename api_2 as ("r_num":"$name2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_2', 'Action': '@udf', '@udf': 'api_2', 'by': 'udf0.df_append', 'with': '近一个月弱点接口数排名第二的弱点类型的接口数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[55]原语 api_2 = @udf api_2 by udf0.df_append with 近一个月弱点接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_2', 'Action': 'add', 'add': '参数', 'by': "'$name2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[56]原语 api_2 = add 参数 by ("$name2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_2:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[57]原语 store api_2 to ssdb by ssdb0 with api_2:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'event_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(risk_label) as r_num from api_risk where first_time > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[61]原语 event_n = load ckh by ckh with select count(risk_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'event_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[62]原语 alter event_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'event_n', 'Action': 'add', 'add': 'aa', 'by': "'访问阈值告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[63]原语 event_n = add aa by ("访问阈值告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_delay where time > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[65]原语 delay_n = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'delay_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[66]原语 alter delay_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'delay_n', 'Action': 'add', 'add': 'aa', 'by': "'访问耗时告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[67]原语 delay_n = add aa by ("访问耗时告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'req_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from r_req_alm where timestamp > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[69]原语 req_n = load ckh by ckh with select count(*) as r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'req_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[70]原语 alter req_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'req_n', 'Action': 'add', 'add': 'aa', 'by': "'异地访问告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[71]原语 req_n = add aa by ("异地访问告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from stat_req_alm where timestamp > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[73]原语 stat_n = load ckh by ckh with select count(*) as r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[74]原语 alter stat_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'stat_n', 'Action': 'add', 'add': 'aa', 'by': "'请求异常告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[75]原语 stat_n = add aa by ("请求异常告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from sensitive_data_alarm where time > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[77]原语 sens_n = load ckh by ckh with select count(*) as r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[78]原语 alter sens_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_n', 'Action': 'add', 'add': 'aa', 'by': "'敏感数据告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[79]原语 sens_n = add aa by ("敏感数据告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_abroad where timestamp > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[81]原语 abroad_n = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'abroad_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[82]原语 alter abroad_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'abroad_n', 'Action': 'add', 'add': 'aa', 'by': "'境外访问告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[83]原语 abroad_n = add aa by ("境外访问告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'filter_n', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from datafilter_alarm where timestamp > '$month'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[85]原语 filter_n = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'filter_n', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[86]原语 alter filter_n by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'filter_n', 'Action': 'add', 'add': 'aa', 'by': "'文件敏感信息告警'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[87]原语 filter_n = add aa by ("文件敏感信息告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'alm_num1', 'Action': 'union', 'union': 'event_n,delay_n,req_n,stat_n,abroad_n,sens_n,filter_n'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[90]原语 alm_num1 = union (event_n,delay_n,req_n,stat_n,abr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'alm_num', 'Action': 'group', 'group': 'alm_num1', 'by': 'index', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[91]原语 alm_num = group alm_num1 by index agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'alm_num', 'by': '"r_num_sum":"告警事件数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[92]原语 rename alm_num by ("r_num_sum":"告警事件数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alm_num', 'Action': '@udf', '@udf': 'alm_num', 'by': 'udf0.df_append', 'with': '近一个月'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[93]原语 alm_num = @udf alm_num by udf0.df_append with 近一个月... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'alm_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'alm_num:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[94]原语 store alm_num to ssdb by ssdb0 with alm_num:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ggg', 'Action': 'order', 'order': 'alm_num1', 'by': 'r_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[96]原语 ggg = order alm_num1 by r_num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ggg', 'Action': 'loc', 'loc': 'ggg', 'by': 'aa,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[97]原语 ggg = loc ggg by aa,r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'name1', 'Action': 'eval', 'eval': 'ggg', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[98]原语 name1 = eval ggg by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'gg', 'Action': 'filter', 'filter': 'ggg', 'by': "aa == '$name1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[99]原语 gg = filter ggg by aa == "$name1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'gg', 'Action': 'loc', 'loc': 'gg', 'by': 'aa', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[100]原语 gg = loc gg by aa to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'gg', 'as': "'r_num':'$name1'"}
	ptree['as'] = deal_sdf(workspace,ptree['as'])
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[101]原语 rename gg as ("r_num":"$name1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'gg', 'Action': '@udf', '@udf': 'gg', 'by': 'udf0.df_append', 'with': '近一个月告警事件排名第一的告警类型的事件数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[102]原语 gg = @udf gg by udf0.df_append with 近一个月告警事件排名第一的告... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'gg', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gg:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[103]原语 store gg to ssdb by ssdb0 with gg:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'name2', 'Action': 'eval', 'eval': 'ggg', 'by': 'iloc[1,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[105]原语 name2 = eval ggg by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'gg1', 'Action': 'filter', 'filter': 'ggg', 'by': "aa == '$name2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[106]原语 gg1 = filter ggg by aa == "$name2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'gg1', 'Action': 'loc', 'loc': 'gg1', 'by': 'aa', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[107]原语 gg1 = loc gg1 by aa to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'gg1', 'as': "'r_num':'$name2'"}
	ptree['as'] = deal_sdf(workspace,ptree['as'])
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[108]原语 rename gg1 as ("r_num":"$name2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'gg1', 'Action': '@udf', '@udf': 'gg1', 'by': 'udf0.df_append', 'with': '近一个月告警事件排名第二的告警类型的事件数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[109]原语 gg1 = @udf gg1 by udf0.df_append with 近一个月告警事件排名第二... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'gg1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gg1:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[110]原语 store gg1 to ssdb by ssdb0 with gg1:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-2 month'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[114]原语 date = @sdf sys_now with (-2 month) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$date,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[115]原语 date = @sdf format_now with ($date,"%Y-%m-%d 00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_mod', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from api_modsecurity where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[117]原语 api_mod = load ckh by ckh with select SUBSTRING(to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_mod', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[118]原语 alter api_mod by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_mod', 'by': '"r_num":"安全事件告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[120]原语 rename api_mod by ("r_num":"安全事件告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from api_model where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[122]原语 api_model = load ckh by ckh with select SUBSTRING(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_model', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[123]原语 alter api_model by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_model', 'by': '"r_num":"数据泄露场景分析"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[125]原语 rename api_model by ("r_num":"数据泄露场景分析") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'emh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(first_time),1,7) as mtime,count(risk_label) as r_num from api_risk where first_time >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[127]原语 emh = load ckh by ckh with select SUBSTRING(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'emh', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[128]原语 alter emh by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(time),1,7) as mtime,count(*) as r_num from api_delay where time >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[131]原语 delay = load ckh by ckh with select SUBSTRING(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'delay', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[132]原语 alter delay by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'r_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from r_req_alm where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[135]原语 r_req = load ckh by ckh with select SUBSTRING(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'r_req', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[136]原语 alter r_req by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from stat_req_alm where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[139]原语 stat = load ckh by ckh with select SUBSTRING(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[140]原语 alter stat by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(time),1,7) as mtime,count(*) as r_num from sensitive_data_alarm where time >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[143]原语 sensitive = load ckh by ckh with select SUBSTRING(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[144]原语 alter sensitive by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from api_abroad where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[147]原语 abroad = load ckh by ckh with select SUBSTRING(toS... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'abroad', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[148]原语 alter abroad by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,7) as mtime,count(*) as r_num from datafilter_alarm where timestamp >= '$date' group by mtime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[151]原语 datafilter = load ckh by ckh with select SUBSTRING... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter', 'by': 'mtime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[152]原语 alter datafilter by mtime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'alm_mh', 'Action': 'union', 'union': 'emh,delay,r_req,stat,sensitive,abroad,datafilter'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[156]原语 alm_mh = union (emh,delay,r_req,stat,sensitive,abr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'alm_mh', 'Action': 'group', 'group': 'alm_mh', 'by': 'mtime', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[157]原语 alm_mh = group alm_mh by mtime agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'alm_mh', 'Action': 'loc', 'loc': 'alm_mh', 'by': 'index', 'to': 'mtime'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[158]原语 alm_mh = loc alm_mh by index to mtime 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'alm_mh', 'by': '"r_num_sum":"告警事件"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[159]原语 rename alm_mh by ("r_num_sum":"告警事件") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'alm_mh', 'Action': 'join', 'join': 'alm_mh,api_mod', 'by': 'mtime,mtime', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[161]原语 alm_mh = join alm_mh,api_mod by mtime,mtime with l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'alm_mh', 'Action': 'join', 'join': 'alm_mh,api_model', 'by': 'mtime,mtime', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[162]原语 alm_mh = join alm_mh,api_model by mtime,mtime with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'alm_mh', 'Action': 'order', 'order': 'alm_mh', 'by': 'mtime'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[163]原语 alm_mh = order alm_mh by mtime 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'alm_mh', 'Action': 'loc', 'loc': 'alm_mh', 'by': 'mtime', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[164]原语 alm_mh = loc alm_mh by mtime to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'alm_mh', 'Action': '@udf', '@udf': 'alm_mh', 'by': 'udf0.df_fillna_cols', 'with': '告警事件:0,安全事件告警:0,数据泄露场景分析:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[165]原语 alm_mh = @udf alm_mh by udf0.df_fillna_cols with 告... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'alm_mh', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'mtotal:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[166]原语 store alm_mh to ssdb by ssdb0 with mtotal:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-0 week'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[171]原语 week1 = @sdf sys_now with -0 week 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week2', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1 week'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[173]原语 week2 = @sdf sys_now with -1 week 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$week1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[175]原语 week1 = @sdf format_now with ($week1,"%Y-%m-%dT00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$week2,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[176]原语 week2 = @sdf format_now with ($week2,"%Y-%m-%dT00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_w1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type where last_time >= '$week1' group by b.type2"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[179]原语 api19_w1 = load db by mysql1 with select b.type2,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_w1', 'by': 'type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[180]原语 alter api19_w1 by type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_w1', 'Action': 'loc', 'loc': 'api19_w1', 'by': 'type2', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[181]原语 api19_w1 = loc api19_w1 by type2 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_w1', 'as': "'num':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[182]原语 rename api19_w1 as ("num":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_w1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'this:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[183]原语 store api19_w1 to ssdb by ssdb0 with this:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_w2', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type where last_time >= '$week2' and last_time < '$week1' group by b.type2"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[186]原语 api19_w2 = load db by mysql1 with select b.type2,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_w2', 'by': 'type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[187]原语 alter api19_w2 by type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_w2', 'Action': 'loc', 'loc': 'api19_w2', 'by': 'type2', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[188]原语 api19_w2 = loc api19_w2 by type2 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_w2', 'as': "'num':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[189]原语 rename api19_w2 as ("num":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_w2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'last:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[190]原语 store api19_w2 to ssdb by ssdb0 with last:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1 month'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[196]原语 month2 = @sdf sys_now with -1 month 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month2,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[197]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%dT0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month3', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-2 month'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[198]原语 month3 = @sdf sys_now with -2 month 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month3', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month3,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[199]原语 month3 = @sdf format_now with ($month3,"%Y-%m-%dT0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_m1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type where last_time >= '$month2' group by b.type2"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[202]原语 api19_m1 = load db by mysql1 with select b.type2,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_m1', 'by': 'type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[203]原语 alter api19_m1 by type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_m1', 'Action': 'loc', 'loc': 'api19_m1', 'by': 'type2', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[204]原语 api19_m1 = loc api19_m1 by type2 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_m1', 'as': "'num':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[205]原语 rename api19_m1 as ("num":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_m1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'thism:mpie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[206]原语 store api19_m1 to ssdb by ssdb0 with thism:mpie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_m2', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type where last_time >= '$month3' and last_time < '$month2' group by b.type2"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[209]原语 api19_m2 = load db by mysql1 with select b.type2,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_m2', 'by': 'type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[210]原语 alter api19_m2 by type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_m2', 'Action': 'loc', 'loc': 'api19_m2', 'by': 'type2', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[211]原语 api19_m2 = loc api19_m2 by type2 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_m2', 'as': "'num':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[212]原语 rename api19_m2 as ("num":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_m2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'lastm:mpie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[213]原语 store api19_m2 to ssdb by ssdb0 with lastm:mpie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk_w', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select state,count(*) as state_count from api19_risk where last_time >= '$week1' group by state"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[223]原语 api19_risk_w = load db by mysql1 with select state... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk_w', 'by': 'state:str,state_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[224]原语 alter api19_risk_w by state:str,state_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk_w', 'Action': 'loc', 'loc': 'api19_risk_w', 'by': 'state', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[225]原语 api19_risk_w = loc api19_risk_w by state to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk_w', 'as': "'state_count':'弱点状态数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[226]原语 rename api19_risk_w as ("state_count":"弱点状态数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_risk_w', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'week:list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[227]原语 store api19_risk_w to ssdb by ssdb0 with week:list... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk_m', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select state,count(*) as state_count from api19_risk where last_time >= '$month2' group by state"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[228]原语 api19_risk_m = load db by mysql1 with select state... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk_m', 'by': 'state:str,state_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[229]原语 alter api19_risk_m by state:str,state_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk_m', 'Action': 'loc', 'loc': 'api19_risk_m', 'by': 'state', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[230]原语 api19_risk_m = loc api19_risk_m by state to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk_m', 'as': "'state_count':'弱点状态数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[231]原语 rename api19_risk_m as ("state_count":"弱点状态数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_risk_m', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'month:list'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[232]原语 store api19_risk_m to ssdb by ssdb0 with month:lis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[236]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[lhq_risk_ov_time.fbi]执行第[237]原语 month1 = @sdf format_now with ($month1,"%Y-%m-%dT0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[238]原语 month2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[lhq_risk_ov_time.fbi]执行第[239]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'month', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$month1,$month2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[240]原语 month = @udf udf0.new_df_timerange with ($month1,$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'month', 'Action': 'loc', 'loc': 'month', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[241]原语 month = loc month by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'month', 'as': '"end_time":"times"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[242]原语 rename month as ("end_time":"times") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'month.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[243]原语 month.times = lambda times by (x:x[:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_mod', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,10) as times,count(*) as r_num from api_modsecurity where timestamp >= '$month1' group by times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[246]原语 api_mod = load ckh by ckh with select SUBSTRING(to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_mod', 'by': 'times:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[247]原语 alter api_mod by times:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_mod', 'by': '"r_num":"安全事件告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[248]原语 rename api_mod by ("r_num":"安全事件告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select SUBSTRING(toString(timestamp),1,10) as times,count(*) as r_num from api_model where timestamp >= '$month1' group by times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[250]原语 api_model = load ckh by ckh with select SUBSTRING(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_model', 'by': 'times:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[251]原语 alter api_model by times:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_model', 'by': '"r_num":"数据泄露场景分析"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[252]原语 rename api_model by ("r_num":"数据泄露场景分析") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'tl_trend', 'Action': 'join', 'join': 'month,api_mod', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[253]原语 tl_trend = join month,api_mod by times,times with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'tl_trend', 'Action': 'join', 'join': 'tl_trend,api_model', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[254]原语 tl_trend = join tl_trend,api_model by times,times ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tl_trend', 'Action': '@udf', '@udf': 'tl_trend', 'by': 'udf0.df_fillna_cols', 'with': '安全事件告警:0,数据泄露场景分析:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[255]原语 tl_trend = @udf tl_trend by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'tl_trend.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[256]原语 tl_trend.times = lambda times by (x:x[5:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tl_trend', 'Action': 'loc', 'loc': 'tl_trend', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[257]原语 tl_trend = loc tl_trend by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tl_trend', 'Action': 'loc', 'loc': 'tl_trend', 'by': '安全事件告警,数据泄露场景分析'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[258]原语 tl_trend = loc tl_trend by 安全事件告警,数据泄露场景分析 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tl_trend', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'total:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[259]原语 store tl_trend to ssdb by ssdb0 with total:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select left(last_time,10) as times,b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type where last_time >= '$month1' group by b.type2,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[263]原语 api_risk = load db by mysql1 with select left(last... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_risk', 'by': 'times:str,type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[264]原语 alter api_risk by times:str,type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_risk', 'Action': 'group', 'group': 'api_risk', 'by': 'times,type2', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[265]原语 api_risk = group api_risk by times,type2 agg num:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk', 'Action': '@udf', '@udf': 'api_risk', 'by': 'udf0.df_unstack', 'with': 'num_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[266]原语 api_risk = @udf api_risk by udf0.df_unstack with n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk', 'Action': 'loc', 'loc': 'api_risk', 'by': 'index', 'to': 'times'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[267]原语 api_risk = loc api_risk by index to times 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_risk', 'Action': 'join', 'join': 'month,api_risk', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[268]原语 api_risk = join month,api_risk by times,times with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk', 'Action': '@udf', '@udf': 'api_risk', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[269]原语 api_risk = @udf api_risk by udf0.df_fillna with (0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_risk.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[271]原语 api_risk.times = lambda times by (x:x[5:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk', 'Action': 'loc', 'loc': 'api_risk', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[272]原语 api_risk = loc api_risk by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'total:api_risk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[273]原语 store api_risk to ssdb by ssdb0 with total:api_ris... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_time.fbi]执行第[276]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],276

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



