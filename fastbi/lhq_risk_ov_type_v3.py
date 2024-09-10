#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_risk_ov_type
#datetime: 2024-08-30T16:10:53.955200
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
		add_the_error('[lhq_risk_ov_type.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[15]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[lhq_risk_ov_type.fbi]执行第[16]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[16]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,type,state from api19_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[19]原语 api19_risk = load db by mysql1 with select app,typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk', 'by': 'app:str,type:str,state:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[20]原语 alter api19_risk by app:str,type:str,state:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'api19_risk', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[21]原语 a_num = eval api19_risk by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_num', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'r_num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[22]原语 api_num = @udf udf0.new_df with r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_num', 'Action': '@udf', '@udf': 'api_num', 'by': 'udf0.df_append', 'with': '$a_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[23]原语 api_num = @udf api_num by udf0.df_append with $a_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_num.r_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[24]原语 alter api_num.r_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_risk', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'访问阈值告警' as aa from api_risk"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[26]原语 api_risk = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_risk', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[27]原语 alter api_risk by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'访问耗时告警' as aa from api_delay"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[29]原语 api_delay = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_delay', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[30]原语 alter api_delay by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'r_req_alm', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'异地访问告警' as aa from r_req_alm"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[32]原语 r_req_alm = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'r_req_alm', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[33]原语 alter r_req_alm by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat_req_alm', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'请求异常告警' as aa from stat_req_alm"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[35]原语 stat_req_alm = load ckh by ckh with select count(*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat_req_alm', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[36]原语 alter stat_req_alm by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'境外访问告警' as aa from api_abroad"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[38]原语 api_abroad = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_abroad', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[39]原语 alter api_abroad by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive_data_alarm', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'敏感数据告警' as aa from sensitive_data_alarm"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[41]原语 sensitive_data_alarm = load ckh by ckh with select... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive_data_alarm', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[42]原语 alter sensitive_data_alarm by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter_alarm', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num,'文件敏感信息告警' as aa from datafilter_alarm"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[44]原语 datafilter_alarm = load ckh by ckh with select cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter_alarm', 'by': 'r_num:int,aa:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[45]原语 alter datafilter_alarm by r_num:int,aa:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'event_num', 'Action': 'union', 'union': 'api_risk,api_delay,r_req_alm,stat_req_alm,api_abroad,sensitive_data_alarm,datafilter_alarm'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[47]原语 event_num = union (api_risk,api_delay,r_req_alm,st... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'event_num', 'Action': 'group', 'group': 'event_num', 'by': 'index', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[48]原语 event_num = group event_num by index agg r_num:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'event_num', 'by': "'r_num_sum':'r_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[49]原语 rename event_num by ("r_num_sum":"r_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'state', 'Action': 'group', 'group': 'api19_risk', 'by': 'state', 'agg': 'state:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[54]原语 state = group api19_risk by state agg state:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'state', 'as': "'state_count':'状态数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[55]原语 rename state as ("state_count":"状态数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'state', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'state:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[56]原语 store state to ssdb by ssdb0 with state:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tal_num', 'Action': 'union', 'union': 'api_num,event_num'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[60]原语 tal_num = union (api_num,event_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'tal_num', 'Action': 'group', 'group': 'tal_num', 'by': 'index', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[61]原语 tal_num = group tal_num by index agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tal_num1', 'Action': 'loc', 'loc': 'tal_num', 'by': 'r_num_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[62]原语 tal_num1 = loc tal_num by r_num_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'tal_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[63]原语 aa_num = eval tal_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'tal_num.r_num_sum = lambda r_num_sum by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=64
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[64]原语 if $aa_num > 100000 with tal_num.r_num_sum = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'rename tal_num by ("r_num_sum":"总风险数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=65
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[65]原语 if $aa_num > 100000 with rename tal_num by ("r_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': 'rename tal_num by ("r_num_sum":"总风险数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=66
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[66]原语 if $aa_num <= 100000 with rename tal_num by ("r_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tal_num', 'Action': 'add', 'add': 'tips', 'by': '"弱点事件总数和告警事件总数之和"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[67]原语 tal_num = add tips by ("弱点事件总数和告警事件总数之和") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tal_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tl:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[68]原语 store tal_num to ssdb by ssdb0 with tl:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_num1', 'Action': 'loc', 'loc': 'api_num', 'by': 'r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[70]原语 api_num1 = loc api_num by r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[71]原语 aa_num = eval api_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_num.r_num = lambda r_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=72
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[72]原语 if $aa_num > 100000 with api_num.r_num = lambda r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'rename api_num by ("r_num":"弱点接口数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=73
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[73]原语 if $aa_num > 100000 with rename api_num by ("r_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': 'rename api_num by ("r_num":"弱点接口数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=74
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[74]原语 if $aa_num <= 100000 with rename api_num by ("r_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_num', 'Action': 'add', 'add': '参数', 'by': "'参数可遍历'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[75]原语 api_num = add 参数 by ("参数可遍历") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ru:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[76]原语 store api_num to ssdb by ssdb0 with ru:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'event_num1', 'Action': 'loc', 'loc': 'event_num', 'by': 'r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[78]原语 event_num1 = loc event_num by r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'event_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[79]原语 aa_num = eval event_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'event_num.r_num = lambda r_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=80
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[80]原语 if $aa_num > 100000 with event_num.r_num = lambda ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'rename event_num by ("r_num":"告警事件数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=81
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[81]原语 if $aa_num > 100000 with rename event_num by ("r_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': 'rename event_num by ("r_num":"告警事件数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=82
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[82]原语 if $aa_num <= 100000 with rename event_num by ("r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'event_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 're:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[83]原语 store event_num to ssdb by ssdb0 with re:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_num', 'Action': 'group', 'group': 'api19_risk', 'by': 'app', 'agg': 'app:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[85]原语 app_num = group api19_risk by app agg app:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'app_num', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[86]原语 a_num = eval app_num by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_num', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'r_num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[87]原语 app_num = @udf udf0.new_df with r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_num', 'Action': '@udf', '@udf': 'app_num', 'by': 'udf0.df_append', 'with': '$a_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[88]原语 app_num = @udf app_num by udf0.df_append with $a_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_num', 'by': '"r_num":"弱点应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[89]原语 rename app_num by ("r_num":"弱点应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_num', 'Action': '@udf', '@udf': 'app_num', 'by': 'udf0.df_append', 'with': '存在弱点的应用数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[90]原语 app_num = @udf app_num by udf0.df_append with 存在弱点... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'rp:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[91]原语 store app_num to ssdb by ssdb0 with rp:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[94]原语 day = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[95]原语 day = @sdf format_now with ($day,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'risk_t', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as 今日弱点接口数量 from api19_risk where left(last_time,10) = '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[96]原语 risk_t = load db by mysql1 with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risk_t', 'by': '今日弱点接口数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[97]原语 alter risk_t by 今日弱点接口数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk_t', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tr:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[98]原语 store risk_t to ssdb by ssdb0 with tr:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type', 'Action': 'union', 'union': 'api_risk,api_delay,r_req_alm,stat_req_alm,api_abroad,sensitive_data_alarm,datafilter_alarm'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[101]原语 type = union (api_risk,api_delay,r_req_alm,stat_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'type', 'Action': 'filter', 'filter': 'type', 'by': 'r_num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[102]原语 type = filter type by r_num != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'type', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[103]原语 num = eval type by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'u_tp', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 't_num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[104]原语 u_tp = @udf udf0.new_df with (t_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'u_tp', 'Action': '@udf', '@udf': 'u_tp', 'by': 'udf0.df_append', 'with': '$num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[105]原语 u_tp = @udf u_tp by udf0.df_append with ($num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'u_tp', 'by': '"t_num":"告警类型数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[106]原语 rename u_tp by ("t_num":"告警类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'u_tp', 'Action': '@udf', '@udf': 'u_tp', 'by': 'udf0.df_append', 'with': '告警模型存在事件的类型数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[107]原语 u_tp = @udf u_tp by udf0.df_append with 告警模型存在事件的类... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'u_tp', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'rt:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[108]原语 store u_tp to ssdb by ssdb0 with rt:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tal_num1', 'as': "'r_num_sum':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[112]原语 rename tal_num1 as ("r_num_sum":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'tal_num1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[113]原语 aa_num = eval tal_num1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'tal_num1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=114
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[114]原语 if $aa_num > 100000 with tal_num1.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "tal_num1 = add name by ('总风险数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=115
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[115]原语 if $aa_num > 100000 with tal_num1 = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "tal_num1 = add name by ('总风险数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=116
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[116]原语 if $aa_num <= 100000 with tal_num1 = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tal_num1', 'Action': 'add', 'add': 'icon', 'by': "'F206'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[117]原语 tal_num1 = add icon by ("F206") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tal_num1', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[118]原语 tal_num1 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_num1', 'as': "'r_num':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[120]原语 rename api_num1 as ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_num1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[121]原语 aa_num = eval api_num1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_num1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=122
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[122]原语 if $aa_num > 100000 with api_num1.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_num1 = add name by ('弱点接口数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=123
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[123]原语 if $aa_num > 100000 with api_num1 = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_num1 = add name by ('弱点接口数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=124
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[124]原语 if $aa_num <= 100000 with api_num1 = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_num1', 'Action': 'add', 'add': 'icon', 'by': "'F309'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[125]原语 api_num1 = add icon by ("F309") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_num1', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[126]原语 api_num1 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_num', 'Action': 'filter', 'filter': 'app_num', 'by': 'index == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[128]原语 app_num = filter app_num by index == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_num', 'as': "'弱点应用数量':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[129]原语 rename app_num as ("弱点应用数量":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_num', 'Action': 'add', 'add': 'name', 'by': "'弱点应用数量'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[130]原语 app_num = add name by ("弱点应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_num', 'Action': 'add', 'add': 'icon', 'by': "'F145'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[131]原语 app_num = add icon by ("F145") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_num', 'Action': 'add', 'add': 'details', 'by': "'存在弱点的应用数量'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[132]原语 app_num = add details by ("存在弱点的应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'event_num1', 'by': "'r_num':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[134]原语 rename event_num1 by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'event_num1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[135]原语 aa_num = eval event_num1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'event_num1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=136
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[136]原语 if $aa_num > 100000 with event_num1.value = lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "event_num1 = add name by ('告警事件数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=137
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[137]原语 if $aa_num > 100000 with event_num1 = add name by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "event_num1 = add name by ('告警事件数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=138
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[138]原语 if $aa_num <= 100000 with event_num1 = add name by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'event_num1', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[139]原语 event_num1 = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'event_num1', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[140]原语 event_num1 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ttt', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as value from api_modsecurity'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[142]原语 ttt = load ckh by ckh with select count(*) as valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ttt', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[143]原语 alter ttt by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'ttt', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[144]原语 aa_num = eval ttt by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'ttt.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=145
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[145]原语 if $aa_num > 100000 with ttt.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "ttt = add name by ('安全事件数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=146
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[146]原语 if $aa_num > 100000 with ttt = add name by ("安全事件数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "ttt = add name by ('安全事件数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=147
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[147]原语 if $aa_num <= 100000 with ttt = add name by ("安全事件... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ttt', 'Action': 'add', 'add': 'icon', 'by': "'F291'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[148]原语 ttt = add icon by ("F291") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ttt', 'Action': 'add', 'add': 'details', 'by': "'http访问监测到的攻击行为'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[149]原语 ttt = add details by ("http访问监测到的攻击行为") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as value from api_model'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[151]原语 api_model = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_model', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[152]原语 alter api_model by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_model', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[153]原语 aa_num = eval api_model by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_model.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=154
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[154]原语 if $aa_num > 100000 with api_model.value = lambda ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_model = add name by ('数据泄露场景(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=155
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[155]原语 if $aa_num > 100000 with api_model = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_model = add name by ('数据泄露场景分析')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=156
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[156]原语 if $aa_num <= 100000 with api_model = add name by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_model', 'Action': 'add', 'add': 'icon', 'by': "'F306'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[157]原语 api_model = add icon by ("F306") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_model', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[158]原语 api_model = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'hb', 'Action': 'union', 'union': 'tal_num1,api_num1,app_num,event_num1,ttt,api_model'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[160]原语 hb = union tal_num1,api_num1,app_num,event_num1,tt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hb', 'Action': 'loc', 'loc': 'hb', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[161]原语 hb = loc hb by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'hb', 'Action': 'add', 'add': 'pageid', 'by': "'dashboard7:lhq_view_risk_one','dashboard7:A7L6vpWaa','dashboard7:A7L6vpWaa','','qes:api_modsecurity','qes:api_model'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[162]原语 hb = add pageid by ("dashboard7:lhq_view_risk_one"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'hb', 'Action': 'add', 'add': '参数', 'by': "'','@type=参数可遍历','@type=参数可遍历','','',''"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[163]原语 hb = add 参数 by ("","@type=参数可遍历","@type=参数可遍历","",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'hb', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'hb:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[164]原语 store hb to ssdb by ssdb0 with hb:num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'fxmx', 'Action': 'union', 'union': 'api_risk,api_delay,r_req_alm,stat_req_alm,api_abroad,sensitive_data_alarm,datafilter_alarm'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[168]原语 fxmx = union (api_risk,api_delay,r_req_alm,stat_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'fxmx', 'Action': 'order', 'order': 'fxmx', 'by': 'r_num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[169]原语 fxmx = order fxmx by r_num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'fxmx.详情', 'Action': 'lambda', 'lambda': 'aa', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[170]原语 fxmx.详情 = lambda aa by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fxmx', 'by': '"r_num":"风险模型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[172]原语 rename fxmx by ("r_num":"风险模型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'fxmx', 'Action': 'loc', 'loc': 'fxmx', 'by': 'aa', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[173]原语 fxmx = loc fxmx by aa to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'fxmx', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'fx:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[174]原语 store fxmx to ssdb by ssdb0 with fx:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_tt', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select b.type2,count(api) as num from api19_risk a left join api19_type b on a.type = b.type group by b.type2 order by num'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[180]原语 api19_tt = load db by mysql1 with select b.type2,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_tt', 'by': 'type2:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[181]原语 alter api19_tt by type2:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_tt', 'Action': 'filter', 'filter': 'api19_tt', 'by': 'num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[182]原语 api19_tt = filter api19_tt by num != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_tt.详情', 'Action': 'lambda', 'lambda': 'type2', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[183]原语 api19_tt.详情 = lambda type2 by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_tt', 'Action': 'loc', 'loc': 'api19_tt', 'by': 'type2', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[184]原语 api19_tt = loc api19_tt by type2 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_tt', 'as': "'num':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[185]原语 rename api19_tt as ("num":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_tt', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tt:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[186]原语 store api19_tt to ssdb by ssdb0 with tt:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'risk', 'Action': 'group', 'group': 'api19_risk', 'by': 'type', 'agg': 'type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[192]原语 risk = group api19_risk by type agg type:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api19_risk_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[193]原语 api19_type = load ssdb by ssdb0 with dd:api19_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,api19_type', 'by': 'index,index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[194]原语 risk = join risk,api19_type by index,index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[195]原语 risk = loc risk by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk', 'Action': 'add', 'add': 'bb', 'by': 'risk["aa"]+\':\'+risk["value"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[196]原语 risk = add bb by risk["aa"]+":"+risk["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': 'bb,type_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[199]原语 risk = loc risk by bb,type_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'risk', 'Action': 'order', 'order': 'risk', 'by': 'type_count', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[200]原语 risk = order risk by type_count with desc limit 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk', 'as': "'bb':'弱点类型','type_count':'弱点类型数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[202]原语 rename risk as ("bb":"弱点类型","type_count":"弱点类型数量")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ai:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[203]原语 store risk to ssdb by ssdb0 with ai:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[206]原语 hour1 = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[207]原语 hour2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour1,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[208]原语 hour1 = @sdf format_now with ($hour1,"%Y-%m-%d %H:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour2,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[209]原语 hour2 = @sdf format_now with ($hour2,"%Y-%m-%d %H:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$hour1,$hour2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[210]原语 hour = @udf udf0.new_df_timerange with ($hour1,$ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour', 'Action': 'loc', 'loc': 'hour', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[211]原语 hour = loc hour by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.end_time', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[212]原语 hour.end_time = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'hour', 'as': "'end_time':'hour'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[213]原语 rename hour as ("end_time":"hour") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour3', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-23h'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[214]原语 hour3 = @sdf sys_now with -23h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour3', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour3,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[215]原语 hour3 = @sdf format_now with ($hour3,"%Y-%m-%d %H:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'n_en', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(first_time),12,2) as hour ,count(risk_label) as r_num1 from api_risk where first_time >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[217]原语 n_en = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'n_en', 'by': 'hour:str,r_num1:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[218]原语 alter n_en by hour:str,r_num1:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),12,2) as hour ,count(*) as r_num2 from api_delay where time >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[220]原语 delay = load ckh by ckh with select substring(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'delay', 'by': 'hour:str,r_num2:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[221]原语 alter delay by hour:str,r_num2:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'r_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),12,2) as hour ,count(*) as r_num3 from r_req_alm where timestamp >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[223]原语 r_req = load ckh by ckh with select substring(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'r_req', 'by': 'hour:str,r_num3:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[224]原语 alter r_req by hour:str,r_num3:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),12,2) as hour ,count(*) as r_num4 from stat_req_alm where timestamp >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[226]原语 stat = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat', 'by': 'hour:str,r_num4:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[227]原语 alter stat by hour:str,r_num4:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),12,2) as hour ,count(*) as r_num5 from sensitive_data_alarm where time >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[229]原语 sensitive = load ckh by ckh with select substring(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'hour:str,r_num5:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[230]原语 alter sensitive by hour:str,r_num5:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),12,2) as hour ,count(*) as r_num6 from api_abroad where timestamp >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[232]原语 abroad = load ckh by ckh with select substring(toS... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'abroad', 'by': 'hour:str,r_num6:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[233]原语 alter abroad by hour:str,r_num6:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),12,2) as hour ,count(*) as r_num7 from datafilter_alarm where timestamp >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[235]原语 datafilter = load ckh by ckh with select substring... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter', 'by': 'hour:str,r_num7:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[236]原语 alter datafilter by hour:str,r_num7:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'hour,n_en', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[237]原语 risk_24 = join hour,n_en by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,delay', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[238]原语 risk_24 = join risk_24,delay by hour,hour with lef... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,r_req', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[239]原语 risk_24 = join risk_24,r_req by hour,hour with lef... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,stat', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[240]原语 risk_24 = join risk_24,stat by hour,hour with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,sensitive', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[241]原语 risk_24 = join risk_24,sensitive by hour,hour with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,abroad', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[242]原语 risk_24 = join risk_24,abroad by hour,hour with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk_24', 'Action': 'join', 'join': 'risk_24,datafilter', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[243]原语 risk_24 = join risk_24,datafilter by hour,hour wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk_24', 'Action': '@udf', '@udf': 'risk_24', 'by': 'udf0.df_fillna_cols', 'with': 'r_num1:0,r_num2:0,r_num3:0,r_num4:0,r_num5:0,r_num6:0,r_num7:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[244]原语 risk_24 = @udf risk_24 by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'risk_24.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[245]原语 risk_24.hour = lambda hour by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk_24', 'Action': 'add', 'add': '总风险', 'by': "risk_24['r_num1']+risk_24['r_num2']+risk_24['r_num3']+risk_24['r_num4']+risk_24['r_num5']+risk_24['r_num6']+risk_24['r_num7']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[246]原语 risk_24 = add 总风险 by risk_24["r_num1"]+risk_24["r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk_24', 'Action': 'loc', 'loc': 'risk_24', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[247]原语 risk_24 = loc risk_24 by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk_24', 'as': "'r_num1':'访问阈值告警','r_num2':'访问耗时告警','r_num3':'异地访问告警','r_num4':'请求异常告警','r_num5':'敏感数据告警','r_num6':'境外访问告警','r_num7':'文件敏感信息告警'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[248]原语 rename risk_24 as ("r_num1":"访问阈值告警","r_num2":"访问耗... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk_24', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'r_24:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[249]原语 store risk_24 to ssdb by ssdb0 with r_24:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select left(last_time,13) as hour,count(*) as num from api19_risk where last_time >= '$hour3' group by hour"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[252]原语 api19_risk = load db by mysql1 with select left(la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[253]原语 alter api19_risk by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[254]原语 api19_risk.hour = lambda hour by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api19_risk', 'Action': 'join', 'join': 'hour,api19_risk', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[255]原语 api19_risk = join hour,api19_risk by hour,hour wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_risk', 'Action': '@udf', '@udf': 'api19_risk', 'by': 'udf0.df_fillna_cols', 'with': 'num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[256]原语 api19_risk = @udf api19_risk by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[257]原语 api19_risk.hour = lambda hour by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[258]原语 api19_risk = loc api19_risk by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk', 'as': "'num':'发现接口数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[259]原语 rename api19_risk as ("num":"发现接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'r_24:risk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[260]原语 store api19_risk to ssdb by ssdb0 with r_24:risk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_mod', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select class,count(*) as num from api_modsecurity where class != '' group by class"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[263]原语 api_mod = load ckh by ckh with select class,count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_mod', 'by': 'class:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[264]原语 alter api_mod by class:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api_mod', 'Action': 'order', 'order': 'api_mod', 'by': 'num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[265]原语 api_mod = order api_mod by num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_mod', 'as': "'num':'安全事件数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[266]原语 rename api_mod as ("num":"安全事件数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_mod.详情', 'Action': 'lambda', 'lambda': 'class', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[267]原语 api_mod.详情 = lambda class by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_mod', 'Action': 'loc', 'loc': 'api_mod', 'by': 'class', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[268]原语 api_mod = loc api_mod by class to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_mod', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api:api_mod'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[269]原语 store api_mod to ssdb by ssdb0 with api:api_mod 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select type,count(*) as num from api_model group by type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[272]原语 api_model = load ckh by ckh with select type,count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_model', 'by': 'type:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[273]原语 alter api_model by type:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:model_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[274]原语 type = load ssdb by ssdb0 with dd:model_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type', 'Action': 'loc', 'loc': 'type', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[275]原语 type = loc type by index to type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_model', 'Action': 'join', 'join': 'type,api_model', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[276]原语 api_model = join type,api_model by type,type with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_model', 'Action': '@udf', '@udf': 'api_model', 'by': 'udf0.df_fillna_cols', 'with': 'num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[277]原语 api_model = @udf api_model by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api_model', 'Action': 'order', 'order': 'api_model', 'by': 'num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[278]原语 api_model = order api_model by num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_model', 'as': "'type':'详情','num':'事件数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[279]原语 rename api_model as ("type":"详情","num":"事件数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_model', 'Action': 'loc', 'loc': 'api_model', 'by': 'value', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[280]原语 api_model = loc api_model by value to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_model', 'Action': 'loc', 'loc': 'api_model', 'by': '事件数,详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[281]原语 api_model = loc api_model by 事件数,详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_model', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api:api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[282]原语 store api_model to ssdb by ssdb0 with api:api_mode... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_type.fbi]执行第[297]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],297

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



