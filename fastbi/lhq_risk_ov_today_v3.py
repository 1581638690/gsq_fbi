#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_risk_ov_today
#datetime: 2024-08-30T16:10:55.340410
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
		add_the_error('[lhq_risk_ov_today.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[15]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[lhq_risk_ov_today.fbi]执行第[16]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[16]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[18]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[19]原语 day = @sdf format_now with ($now,"%Y-%m-%dT00:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'yday1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[20]原语 yday1 = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'yday', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$yday1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[21]原语 yday = @sdf format_now with ($yday1,"%Y-%m-%dT00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ne_ev', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(risk_label) as r_num from api_risk where first_time >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[26]原语 ne_ev = load ckh by ckh with select count(risk_lab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ne_ev', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[27]原语 alter ne_ev by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_delay where time >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[29]原语 delay = load ckh by ckh with select count(*) as r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'delay', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[30]原语 alter delay by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'r_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from r_req_alm where timestamp >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[32]原语 r_req = load ckh by ckh with select count(*) as r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'r_req', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[33]原语 alter r_req by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from stat_req_alm where timestamp >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[35]原语 stat = load ckh by ckh with select count(*) as r_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[36]原语 alter stat by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from sensitive_data_alarm where time >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[38]原语 sensitive = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[39]原语 alter sensitive by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_abroad where timestamp >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[41]原语 abroad = load ckh by ckh with select count(*) as r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'abroad', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[42]原语 alter abroad by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from datafilter_alarm where timestamp >= '$day'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[44]原语 datafilter = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[45]原语 alter datafilter by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'temp', 'Action': 'union', 'union': 'ne_ev,delay,r_req,stat,sensitive,abroad,datafilter'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[47]原语 temp = union (ne_ev,delay,r_req,stat,sensitive,abr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ne_ev', 'Action': 'group', 'group': 'temp', 'by': 'index', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[48]原语 ne_ev = group temp by index agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ne_ev', 'by': '"r_num_sum":"r_num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[49]原语 rename ne_ev by ("r_num_sum":"r_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ne_ev1', 'Action': 'loc', 'loc': 'ne_ev', 'by': 'r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[52]原语 ne_ev1 = loc ne_ev by r_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'ne_ev1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[53]原语 aa_num = eval ne_ev1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'ne_ev1.r_num = lambda r_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=54
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[54]原语 if $aa_num > 100000 with ne_ev1.r_num = lambda r_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'rename ne_ev1 by ("r_num":"今日告警事件数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=55
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[55]原语 if $aa_num > 100000 with rename ne_ev1 by ("r_num"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': 'rename ne_ev1 by ("r_num":"今日告警事件数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=56
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[56]原语 if $aa_num <= 100000 with rename ne_ev1 by ("r_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ne_ev1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ne:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[57]原语 store ne_ev1 to ssdb by ssdb0 with ne:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yne_ev', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(risk_label) as r_num from api_risk where first_time >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[61]原语 yne_ev = load ckh by ckh with select count(risk_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'yne_ev', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[62]原语 alter yne_ev by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ydelay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_delay where time >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[64]原语 ydelay = load ckh by ckh with select count(*) as r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ydelay', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[65]原语 alter ydelay by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yr_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from r_req_alm where timestamp >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[67]原语 yr_req = load ckh by ckh with select count(*) as r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'yr_req', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[68]原语 alter yr_req by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ystat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from stat_req_alm where timestamp >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[70]原语 ystat = load ckh by ckh with select count(*) as r_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ystat', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[71]原语 alter ystat by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ysensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from sensitive_data_alarm where time >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[73]原语 ysensitive = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ysensitive', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[74]原语 alter ysensitive by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yabroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from api_abroad where timestamp >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[76]原语 yabroad = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'yabroad', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[77]原语 alter yabroad by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ydatafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as r_num from datafilter_alarm where timestamp >= '$yday'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[79]原语 ydatafilter = load ckh by ckh with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ydatafilter', 'by': 'r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[80]原语 alter ydatafilter by r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'temp', 'Action': 'union', 'union': 'yne_ev,ydelay,yr_req,ystat,ysensitive,yabroad,ydatafilter'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[82]原语 temp = union (yne_ev,ydelay,yr_req,ystat,ysensitiv... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'yne_ev', 'Action': 'group', 'group': 'temp', 'by': 'index', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[83]原语 yne_ev = group temp by index agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'yne_ev', 'by': '"r_num_sum":"r_num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[84]原语 rename yne_ev by ("r_num_sum":"r_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'en', 'Action': 'eval', 'eval': 'ne_ev', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[87]原语 en= eval ne_ev by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yen', 'Action': 'eval', 'eval': 'yne_ev', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[88]原语 yen = eval yne_ev by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$en-$yen'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[89]原语 ice = @sdf sys_eval with ($en-$yen) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yen != 0', 'with': '""\nicre = @sdf sys_eval with (round($ice/$yen*100,2))\ner = @udf udf0.new_df with (value)\ner = @udf er by udf0.df_append with ( + )\ner = @udf er by udf0.df_append with ($icre%)\ner = @udf er by udf0.df_append with ($yen)\nstore er to ssdb by ssdb0 with er_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=91
		ptree['funs']=block_if_91
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[91]原语 if $ice > 0 and $yen != 0  with "icre = @sdf sys_e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yen == 0', 'with': '""\ner = @udf udf0.new_df with (value)\ner = @udf er by udf0.df_append with ( + )\ner = @udf er by udf0.df_append with (100.0%)\ner = @udf er by udf0.df_append with ($yen)\nstore er to ssdb by ssdb0 with er_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=100
		ptree['funs']=block_if_100
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[100]原语 if $ice > 0 and $yen == 0 with "er = @udf udf0.new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice == 0', 'with': '""\ner = @udf udf0.new_df with (value)\ner = @udf er by udf0.df_append with ( + )\ner = @udf er by udf0.df_append with (0.0%)\ner = @udf er by udf0.df_append with ($yen)\nstore er to ssdb by ssdb0 with er_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=107
		ptree['funs']=block_if_107
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[107]原语 if $ice == 0 with "er = @udf udf0.new_df with (val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice < 0', 'with': '""\nice = @sdf sys_eval with ($yen-$en)\nicre = @sdf sys_eval with (round($ice/$yen*100,2))\ner = @udf udf0.new_df with (value)\ner = @udf er by udf0.df_append with (-)\ner = @udf er by udf0.df_append with ($icre%)\ner = @udf er by udf0.df_append with ($yen)\nstore er to ssdb by ssdb0 with er_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=114
		ptree['funs']=block_if_114
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[114]原语 if $ice < 0 with "ice = @sdf sys_eval with ($yen-$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'de', 'Action': 'eval', 'eval': 'delay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[129]原语 de = eval delay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yde', 'Action': 'eval', 'eval': 'ydelay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[130]原语 yde = eval ydelay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$de-$yde'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[131]原语 ice = @sdf sys_eval with ($de-$yde) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yde != 0', 'with': '""\nicre = @sdf sys_eval with (round($ice/$yde*100,2))\naa = @udf udf0.new_df with (value)\naa = @udf aa by udf0.df_append with ( + )\naa = @udf aa by udf0.df_append with ($icre%)\naa = @udf aa by udf0.df_append with ($yde)\nstore aa to ssdb by ssdb0 with aa_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=133
		ptree['funs']=block_if_133
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[133]原语 if $ice > 0 and $yde != 0 with "icre = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yde == 0', 'with': '""\naa = @udf udf0.new_df with (value)\naa = @udf aa by udf0.df_append with ( + )\naa = @udf aa by udf0.df_append with (100.0%)\naa = @udf aa by udf0.df_append with ($yde)\nstore aa to ssdb by ssdb0 with aa_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=142
		ptree['funs']=block_if_142
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[142]原语 if $ice > 0 and $yde == 0 with "aa = @udf udf0.new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice == 0', 'with': '""\naa = @udf udf0.new_df with (value)\naa = @udf aa by udf0.df_append with ( + )\naa = @udf aa by udf0.df_append with (0.0%)\naa = @udf aa by udf0.df_append with ($yde)\nstore aa to ssdb by ssdb0 with aa_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=149
		ptree['funs']=block_if_149
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[149]原语 if $ice == 0 with "aa = @udf udf0.new_df with (val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice < 0', 'with': '""\nice = @sdf sys_eval with ($yde-$de)\nicre = @sdf sys_eval with (round($ice/$yde*100,2))\naa = @udf udf0.new_df with (value)\naa = @udf aa by udf0.df_append with (-)\naa = @udf aa by udf0.df_append with ($icre%)\naa = @udf aa by udf0.df_append with ($yde)\nstore aa to ssdb by ssdb0 with aa_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=156
		ptree['funs']=block_if_156
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[156]原语 if $ice < 0 with "ice = @sdf sys_eval with ($yde-$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ab', 'Action': 'eval', 'eval': 'abroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[170]原语 ab = eval abroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yab', 'Action': 'eval', 'eval': 'yabroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[171]原语 yab = eval yabroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$ab-$yab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[172]原语 ice = @sdf sys_eval with ($ab-$yab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yab != 0', 'with': '""\nicre = @sdf sys_eval with (round($ice/$yab*100,2))\nbb = @udf udf0.new_df with (value)\nbb = @udf bb by udf0.df_append with ( + )\nbb = @udf bb by udf0.df_append with ($icre%)\nbb = @udf bb by udf0.df_append with ($yab)\nstore bb to ssdb by ssdb0 with bb_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=174
		ptree['funs']=block_if_174
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[174]原语 if $ice > 0 and $yab != 0 with "icre = @sdf sys_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $yab == 0', 'with': '""\nbb = @udf udf0.new_df with (value)\nbb = @udf bb by udf0.df_append with ( + )\nbb = @udf bb by udf0.df_append with (100.0%)\nbb = @udf bb by udf0.df_append with ($yab)\nstore bb to ssdb by ssdb0 with bb_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=183
		ptree['funs']=block_if_183
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[183]原语 if $ice > 0 and $yab == 0 with "bb = @udf udf0.new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice == 0', 'with': '""\nbb = @udf udf0.new_df with (value)\nbb = @udf bb by udf0.df_append with ( + )\nbb = @udf bb by udf0.df_append with (0.0%)\nbb = @udf bb by udf0.df_append with ($yab)\nstore bb to ssdb by ssdb0 with bb_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=190
		ptree['funs']=block_if_190
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[190]原语 if $ice == 0 with "bb = @udf udf0.new_df with (val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice < 0', 'with': '""\nice = @sdf sys_eval with ($yab-$ab)\nicre = @sdf sys_eval with (round($ice/$yab*100,2))\nbb = @udf udf0.new_df with (value)\nbb = @udf bb by udf0.df_append with (-)\nbb = @udf bb by udf0.df_append with ($icre%)\nbb = @udf bb by udf0.df_append with ($yab)\nstore bb to ssdb by ssdb0 with bb_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=197
		ptree['funs']=block_if_197
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[197]原语 if $ice < 0 with "ice = @sdf sys_eval with ($yab-$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'eval', 'eval': 'sensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[211]原语 sens = eval sensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ysens', 'Action': 'eval', 'eval': 'ysensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[212]原语 ysens = eval ysensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$sens-$ysens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[213]原语 ice = @sdf sys_eval with ($sens-$ysens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $ysens != 0', 'with': '""\nicre = @sdf sys_eval with (round($ice/$ysens*100,2))\ncc = @udf udf0.new_df with (value)\ncc = @udf cc by udf0.df_append with ( + )\ncc = @udf cc by udf0.df_append with ($icre%)\ncc = @udf cc by udf0.df_append with ($ysens)\nstore cc to ssdb by ssdb0 with cc_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=215
		ptree['funs']=block_if_215
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[215]原语 if $ice > 0 and $ysens != 0 with "icre = @sdf sys_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $ysens == 0', 'with': '""\ncc = @udf udf0.new_df with (value)\ncc = @udf cc by udf0.df_append with ( + )\ncc = @udf cc by udf0.df_append with (100.0%)\ncc = @udf cc by udf0.df_append with ($ysens)\nstore cc to ssdb by ssdb0 with cc_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=224
		ptree['funs']=block_if_224
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[224]原语 if $ice > 0 and $ysens == 0 with "cc = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice == 0', 'with': '""\ncc = @udf udf0.new_df with (value)\ncc = @udf cc by udf0.df_append with ( + )\ncc = @udf cc by udf0.df_append with (0.0%)\ncc = @udf cc by udf0.df_append with ($ysens)\nstore cc to ssdb by ssdb0 with cc_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=232
		ptree['funs']=block_if_232
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[232]原语 if $ice == 0 with "cc = @udf udf0.new_df with (val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice < 0', 'with': '""\ncc = @sdf sys_eval with ($ysens-$sens)\ncc = @sdf sys_eval with (round($ice/$ysens*100,2))\ncc = @udf udf0.new_df with (value)\ncc = @udf cc by udf0.df_append with (-)\ncc = @udf cc by udf0.df_append with ($icre%)\ncc = @udf cc by udf0.df_append with ($ysens)\nstore cc to ssdb by ssdb0 with cc_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=239
		ptree['funs']=block_if_239
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[239]原语 if $ice < 0 with "cc = @sdf sys_eval with ($ysens-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_d', 'Action': 'eval', 'eval': 'datafilter', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[253]原语 sens_d = eval datafilter by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ysens_d', 'Action': 'eval', 'eval': 'ydatafilter', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[254]原语 ysens_d = eval ydatafilter by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$sens_d-$ysens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[255]原语 ice = @sdf sys_eval with ($sens_d-$ysens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $ysens_d != 0', 'with': '""\nicre = @sdf sys_eval with (round($ice/$ysens_d*100,2))\ndd = @udf udf0.new_df with (value)\ndd = @udf dd by udf0.df_append with ( + )\ndd = @udf dd by udf0.df_append with ($icre%)\ndd = @udf dd by udf0.df_append with ($ysens_d)\nstore dd to ssdb by ssdb0 with dd_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=257
		ptree['funs']=block_if_257
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[257]原语 if $ice > 0 and $ysens_d != 0 with "icre = @sdf sy... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice > 0 and $ysens_d == 0', 'with': '""\ndd = @udf udf0.new_df with (value)\ndd = @udf dd by udf0.df_append with ( + )\ndd = @udf dd by udf0.df_append with (100.0%)\ndd = @udf dd by udf0.df_append with ($ysens_d)\nstore dd to ssdb by ssdb0 with dd_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=266
		ptree['funs']=block_if_266
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[266]原语 if $ice > 0 and $ysens_d == 0 with "dd = @udf udf0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice == 0', 'with': '""\ndd = @udf udf0.new_df with (value)\ndd = @udf dd by udf0.df_append with ( + )\ndd = @udf dd by udf0.df_append with (0.0%)\ndd = @udf dd by udf0.df_append with ($ysens_d)\nstore dd to ssdb by ssdb0 with dd_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=274
		ptree['funs']=block_if_274
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[274]原语 if $ice == 0 with "dd = @udf udf0.new_df with (val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ice < 0', 'with': '""\ndd = @sdf sys_eval with ($ysens_d-$sens_d)\ndd = @sdf sys_eval with (round($ice/$ysens_d*100,2))\ndd = @udf udf0.new_df with (value)\ndd = @udf dd by udf0.df_append with (-)\ndd = @udf dd by udf0.df_append with ($icre%)\ndd = @udf dd by udf0.df_append with ($ysens_d)\nstore dd to ssdb by ssdb0 with dd_rate\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=281
		ptree['funs']=block_if_281
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[281]原语 if $ice < 0 with "dd = @sdf sys_eval with ($ysens_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ne_ev', 'by': '"r_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[295]原语 rename ne_ev by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'ne_ev', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[296]原语 aa_num = eval ne_ev by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'ne_ev.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=297
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[297]原语 if $aa_num > 100000 with ne_ev.value = lambda valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "ne_ev = add name by ('告警事件数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=298
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[298]原语 if $aa_num > 100000 with ne_ev = add name by ("告警事... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "ne_ev = add name by ('告警事件数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=299
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[299]原语 if $aa_num <= 100000 with ne_ev = add name by ("告警... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ne_ev', 'Action': 'add', 'add': 'icon', 'by': "'F186'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[300]原语 ne_ev = add icon by ("F186") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive', 'by': '"r_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[302]原语 rename sensitive by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'sensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[303]原语 aa_num = eval sensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'sensitive.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=304
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[304]原语 if $aa_num > 100000 with sensitive.value = lambda ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "sensitive = add name by ('敏感数据告警数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=305
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[305]原语 if $aa_num > 100000 with sensitive = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "sensitive = add name by ('敏感数据告警数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=306
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[306]原语 if $aa_num <= 100000 with sensitive = add name by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sensitive', 'Action': 'add', 'add': 'icon', 'by': "'F143'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[307]原语 sensitive = add icon by ("F143") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datafilter', 'by': '"r_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[309]原语 rename datafilter by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'datafilter', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[310]原语 aa_num = eval datafilter by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'datafilter.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=311
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[311]原语 if $aa_num > 100000 with datafilter.value = lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "datafilter = add name by ('文件敏感信息告警数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=312
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[312]原语 if $aa_num > 100000 with datafilter = add name by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "datafilter = add name by ('文件敏感信息告警数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=313
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[313]原语 if $aa_num <= 100000 with datafilter = add name by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'datafilter', 'Action': 'add', 'add': 'icon', 'by': "'F182'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[314]原语 datafilter = add icon by ("F182") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'abroad', 'by': '"r_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[316]原语 rename abroad by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'abroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[317]原语 aa_num = eval abroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'abroad.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=318
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[318]原语 if $aa_num > 100000 with abroad.value = lambda val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "abroad = add name by ('境外访问告警数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=319
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[319]原语 if $aa_num > 100000 with abroad = add name by ("境外... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "abroad = add name by ('境外访问告警数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=320
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[320]原语 if $aa_num <= 100000 with abroad = add name by ("境... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'abroad', 'Action': 'add', 'add': 'icon', 'by': "'F148'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[321]原语 abroad = add icon by ("F148") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'delay', 'by': '"r_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[323]原语 rename delay by ("r_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'delay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[324]原语 aa_num = eval delay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'delay.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=325
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[325]原语 if $aa_num > 100000 with delay.value = lambda valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "delay = add name by ('耗时告警数量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=326
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[326]原语 if $aa_num > 100000 with delay = add name by ("耗时告... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "delay = add name by ('耗时告警数量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=327
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[327]原语 if $aa_num <= 100000 with delay = add name by ("耗时... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'delay', 'Action': 'add', 'add': 'icon', 'by': "'F140'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[328]原语 delay = add icon by ("F140") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ttt', 'Action': 'union', 'union': 'ne_ev,sensitive,datafilter,abroad,delay'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[330]原语 ttt = union ne_ev,sensitive,datafilter,abroad,dela... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ttt', 'Action': 'loc', 'loc': 'ttt', 'by': 'name,value,icon'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[331]原语 ttt = loc ttt by name,value,icon 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ttt', 'Action': 'add', 'add': 'pageid', 'by': "'','qes:sensitive_data_alarm','qes:datafilter_alarm','qes:api_abroad','qes:ACu2dJW'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[332]原语 ttt = add pageid by ("","qes:sensitive_data_alarm"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ttt', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'today:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[333]原语 store ttt to ssdb by ssdb0 with today:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'n_en', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(first_time),1,13) as htime ,count(risk_label) as r_num from api_risk where first_time >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[339]原语 n_en = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'n_en', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[340]原语 alter n_en by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'n_en', 'Action': 'add', 'add': 'hour', 'with': 'n_en["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[341]原语 n_en = add hour with n_en["htime"].str[11:13] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'n_en', 'Action': 'loc', 'loc': 'n_en', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[342]原语 n_en = loc n_en by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'n_eg', 'Action': 'group', 'group': 'n_en', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[343]原语 n_eg = group n_en by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,13) as htime ,count(*) as r_num from api_delay where time >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[347]原语 delay = load ckh by ckh with select substring(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'delay', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[348]原语 alter delay by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'delay', 'Action': 'add', 'add': 'hour', 'with': 'delay["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[349]原语 delay = add hour with delay["htime"].str[11:13] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'delay', 'Action': 'loc', 'loc': 'delay', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[350]原语 delay = loc delay by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'delay', 'Action': 'group', 'group': 'delay', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[351]原语 delay = group delay by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'r_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),1,13) as htime,count(*) as r_num from r_req_alm where timestamp >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[355]原语 r_req = load ckh by ckh with select substring(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'r_req', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[356]原语 alter r_req by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'r_req', 'Action': 'add', 'add': 'hour', 'with': 'r_req["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[357]原语 r_req = add hour with r_req["htime"].str[11:13] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'r_req', 'Action': 'loc', 'loc': 'r_req', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[358]原语 r_req = loc r_req by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'r_req', 'Action': 'group', 'group': 'r_req', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[359]原语 r_req = group r_req by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),1,13) as htime ,count(*) as r_num from stat_req_alm where timestamp >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[363]原语 stat = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'stat', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[364]原语 alter stat by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'stat', 'Action': 'add', 'add': 'hour', 'with': 'stat["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[365]原语 stat = add hour with stat["htime"].str[11:13] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'stat', 'Action': 'loc', 'loc': 'stat', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[366]原语 stat = loc stat by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'stat', 'Action': 'group', 'group': 'stat', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[367]原语 stat = group stat by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(time),1,13) as htime ,count(*) as r_num from sensitive_data_alarm where time >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[371]原语 sensitive = load ckh by ckh with select substring(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[372]原语 alter sensitive by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sensitive', 'Action': 'add', 'add': 'hour', 'with': 'sensitive["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[373]原语 sensitive = add hour with sensitive["htime"].str[1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive', 'Action': 'loc', 'loc': 'sensitive', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[374]原语 sensitive = loc sensitive by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sensitive', 'Action': 'group', 'group': 'sensitive', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[375]原语 sensitive = group sensitive by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),1,13) as htime ,count(*) as r_num from api_abroad where timestamp >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[379]原语 abroad = load ckh by ckh with select substring(toS... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'abroad', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[380]原语 alter abroad by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'abroad', 'Action': 'add', 'add': 'hour', 'with': 'abroad["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[381]原语 abroad = add hour with abroad["htime"].str[11:13] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'abroad', 'Action': 'loc', 'loc': 'abroad', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[382]原语 abroad = loc abroad by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'abroad', 'Action': 'group', 'group': 'abroad', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[383]原语 abroad = group abroad by hour agg r_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select substring(toString(timestamp),1,13) as htime ,count(*) as r_num from datafilter_alarm where timestamp >= '$day' group by htime"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[387]原语 datafilter = load ckh by ckh with select substring... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter', 'by': 'htime:str,r_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[388]原语 alter datafilter by htime:str,r_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'datafilter', 'Action': 'add', 'add': 'hour', 'with': 'datafilter["htime"].str[11:13]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[389]原语 datafilter = add hour with datafilter["htime"].str... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datafilter', 'Action': 'loc', 'loc': 'datafilter', 'by': 'hour,r_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[390]原语 datafilter = loc datafilter by (hour,r_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'datafilter', 'Action': 'group', 'group': 'datafilter', 'by': 'hour', 'agg': 'r_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[391]原语 datafilter = group datafilter by hour agg r_num:su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'n_eg', 'by': '"r_num_sum":"阈值告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[473]原语 rename n_eg by ("r_num_sum":"阈值告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'delay', 'by': '"r_num_sum":"访问耗时告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[474]原语 rename delay by ("r_num_sum":"访问耗时告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'r_req', 'by': '"r_num_sum":"异地访问告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[475]原语 rename r_req by ("r_num_sum":"异地访问告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'stat', 'by': '"r_num_sum":"请求异常告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[476]原语 rename stat by ("r_num_sum":"请求异常告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive', 'by': '"r_num_sum":"敏感数据告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[477]原语 rename sensitive by ("r_num_sum":"敏感数据告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'abroad', 'by': '"r_num_sum":"境外访问告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[478]原语 rename abroad by ("r_num_sum":"境外访问告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datafilter', 'by': '"r_num_sum":"文件敏感信息告警"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[479]原语 rename datafilter by ("r_num_sum":"文件敏感信息告警") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_trend', 'Action': 'join', 'join': 'n_eg,delay', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[483]原语 api_trend = join n_eg,delay by index,index with ou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_trend', 'Action': 'join', 'join': 'api_trend,r_req', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[484]原语 api_trend = join api_trend,r_req by index,index wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_trend', 'Action': 'join', 'join': 'api_trend,stat', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[485]原语 api_trend = join api_trend,stat by index,index wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_trend', 'Action': 'join', 'join': 'api_trend,sensitive', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[486]原语 api_trend = join api_trend,sensitive by index,inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_trend', 'Action': 'join', 'join': 'api_trend,abroad', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[487]原语 api_trend = join api_trend,abroad by index,index w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'alm_mh', 'Action': 'join', 'join': 'api_trend,datafilter', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[488]原语 alm_mh = join api_trend,datafilter by index,index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%d 23:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[492]原语 hour1 = @sdf format_now with ($now,"%Y-%m-%d 23:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$yday1,"%Y-%m-%d 23:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[493]原语 hour2 = @sdf format_now with ($yday1,"%Y-%m-%d 23:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$hour2,$hour1,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[494]原语 hour = @udf udf0.new_df_timerange with ($hour2,$ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour', 'Action': 'loc', 'loc': 'hour', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[495]原语 hour = loc hour by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.end_time', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[496]原语 hour.end_time = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'hour', 'as': "'end_time':'hour'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[497]原语 rename hour as ("end_time":"hour") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'n_rml', 'Action': 'loc', 'loc': 'alm_mh', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[500]原语 n_rml = loc alm_mh by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'n_rml', 'Action': 'join', 'join': 'hour,n_rml', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[501]原语 n_rml = join hour,n_rml by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'n_rml', 'Action': '@udf', '@udf': 'n_rml', 'by': 'udf0.df_fillna_cols', 'with': '阈值告警:0,访问耗时告警:0,异地访问告警:0,请求异常告警:0,敏感数据告警:0,境外访问告警:0,文件敏感信息告警:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[502]原语 n_rml = @udf n_rml by udf0.df_fillna_cols with 阈值告... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'n_rml', 'Action': 'loc', 'loc': 'n_rml', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[503]原语 n_rml = loc n_rml by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'n_rml.aa', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[504]原语 alter n_rml.aa as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'n_rml.aa', 'Action': 'lambda', 'lambda': 'aa', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[505]原语 n_rml.aa = lambda aa by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'n_rml', 'Action': 'loc', 'loc': 'n_rml', 'by': 'aa', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[506]原语 n_rml = loc n_rml by aa to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'n_rml', 'Action': 'loc', 'loc': 'n_rml', 'by': 'drop', 'drop': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[507]原语 n_rml = loc n_rml by drop hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'n_rml', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'nrh:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[508]原语 store n_rml to ssdb by ssdb0 with nrh:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 're', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,count(*) as num from stat_req_alm where timestamp >= '$day' group by app order by num desc limit 5"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[594]原语 re = load ckh by ckh with select app,count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 're', 'by': 'app:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[595]原语 alter re by app:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 're.详情', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[596]原语 re.详情 = lambda app by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 're', 'Action': 'loc', 'loc': 're', 'by': 'app', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[597]原语 re = loc re by app to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 're', 'as': "'num':'分布数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[598]原语 rename re as ("num":"分布数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 're', 'to': 'ssdb', 'by': 'ssdb0', 'with': 're:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[599]原语 store re to ssdb by ssdb0 with re:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select key,count(*) as num from sensitive_data_alarm where time >= '$day' group by key order by num desc limit 5"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[602]原语 sensitive = load ckh by ckh with select key,count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[603]原语 alter sensitive by key:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sensitive', 'Action': 'order', 'order': 'sensitive', 'by': 'num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[604]原语 sensitive = order sensitive by num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sensitive.详情', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[605]原语 sensitive.详情 = lambda key by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sensitive.key', 'Action': 'str', 'str': 'key', 'by': 'slice(0,4)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[606]原语 sensitive.key = str key by (slice(0,4)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive', 'Action': 'loc', 'loc': 'sensitive', 'by': 'key', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[607]原语 sensitive = loc sensitive by key to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive', 'as': "'num':'分布数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[608]原语 rename sensitive as ("num":"分布数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sensitive', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_gj:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[609]原语 store sensitive to ssdb by ssdb0 with sens_gj:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select type,warn_level,count(*) as num from api_delay where time >= '$day' group by type,warn_level order by num desc limit 5"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[612]原语 api_delay = load ckh by ckh with select type,warn_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_delay', 'by': 'type:str,warn_level:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[613]原语 alter api_delay by type:str,warn_level:str,num:int... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay_time', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:delay_time'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[614]原语 delay_time = load ssdb by ssdb0 with dd:delay_time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'delay_time', 'Action': 'loc', 'loc': 'delay_time', 'by': 'index', 'to': 'warn_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[615]原语 delay_time = loc delay_time by index to warn_level... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_delay', 'Action': 'join', 'join': 'api_delay,delay_time', 'by': 'warn_level,warn_level'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[616]原语 api_delay = join api_delay,delay_time by warn_leve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_delay.type.value', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[617]原语 alter api_delay.type.value as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_delay', 'Action': 'add', 'add': 'type1', 'by': "api_delay['type']+':'+ api_delay['value']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[618]原语 api_delay = add type1 by api_delay["type"]+":"+ ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_delay', 'Action': 'loc', 'loc': 'api_delay', 'by': 'type1,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[619]原语 api_delay = loc api_delay by type1,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_delay', 'as': "'type1':'请求类型:告警级别','num':'分布数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[620]原语 rename api_delay as ("type1":"请求类型:告警级别","num":"分布... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_delay', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'delay:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[621]原语 store api_delay to ssdb by ssdb0 with delay:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_risk_ov_today.fbi]执行第[628]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],629

#主函数结束,开始块函数

def block_if_91(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yen*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[92]原语 icre = @sdf sys_eval with (round($ice/$yen*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[93]原语 er = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[94]原语 er = @udf er by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[95]原语 er = @udf er by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$yen'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[96]原语 er = @udf er by udf0.df_append with ($yen) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'er', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'er_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第91行if语句中]执行第[97]原语 store er to ssdb by ssdb0 with er_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_91

def block_if_100(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第100行if语句中]执行第[101]原语 er = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第100行if语句中]执行第[102]原语 er = @udf er by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '100.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第100行if语句中]执行第[103]原语 er = @udf er by udf0.df_append with (100.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$yen'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第100行if语句中]执行第[104]原语 er = @udf er by udf0.df_append with ($yen) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'er', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'er_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第100行if语句中]执行第[105]原语 store er to ssdb by ssdb0 with er_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_100

def block_if_107(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第107行if语句中]执行第[108]原语 er = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第107行if语句中]执行第[109]原语 er = @udf er by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '0.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第107行if语句中]执行第[110]原语 er = @udf er by udf0.df_append with (0.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$yen'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第107行if语句中]执行第[111]原语 er = @udf er by udf0.df_append with ($yen) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'er', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'er_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第107行if语句中]执行第[112]原语 store er to ssdb by ssdb0 with er_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_107

def block_if_114(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yen-$en'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[115]原语 ice = @sdf sys_eval with ($yen-$en) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yen*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[116]原语 icre = @sdf sys_eval with (round($ice/$yen*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[117]原语 er = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '-'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[118]原语 er = @udf er by udf0.df_append with (-) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[119]原语 er = @udf er by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'er', 'Action': '@udf', '@udf': 'er', 'by': 'udf0.df_append', 'with': '$yen'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[120]原语 er = @udf er by udf0.df_append with ($yen) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'er', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'er_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第114行if语句中]执行第[121]原语 store er to ssdb by ssdb0 with er_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_114

def block_if_133(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yde*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[134]原语 icre = @sdf sys_eval with (round($ice/$yde*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[135]原语 aa = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[136]原语 aa = @udf aa by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[137]原语 aa = @udf aa by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$yde'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[138]原语 aa = @udf aa by udf0.df_append with ($yde) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'aa_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第133行if语句中]执行第[139]原语 store aa to ssdb by ssdb0 with aa_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_133

def block_if_142(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[143]原语 aa = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[144]原语 aa = @udf aa by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '100.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[145]原语 aa = @udf aa by udf0.df_append with (100.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$yde'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[146]原语 aa = @udf aa by udf0.df_append with ($yde) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'aa_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第142行if语句中]执行第[147]原语 store aa to ssdb by ssdb0 with aa_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_142

def block_if_149(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第149行if语句中]执行第[150]原语 aa = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第149行if语句中]执行第[151]原语 aa = @udf aa by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '0.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第149行if语句中]执行第[152]原语 aa = @udf aa by udf0.df_append with (0.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$yde'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第149行if语句中]执行第[153]原语 aa = @udf aa by udf0.df_append with ($yde) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'aa_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第149行if语句中]执行第[154]原语 store aa to ssdb by ssdb0 with aa_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_149

def block_if_156(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yde-$de'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[157]原语 ice = @sdf sys_eval with ($yde-$de) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yde*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[158]原语 icre = @sdf sys_eval with (round($ice/$yde*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[159]原语 aa = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '-'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[160]原语 aa = @udf aa by udf0.df_append with (-) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[161]原语 aa = @udf aa by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '$yde'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[162]原语 aa = @udf aa by udf0.df_append with ($yde) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'aa_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第156行if语句中]执行第[163]原语 store aa to ssdb by ssdb0 with aa_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_156

def block_if_174(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yab*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[175]原语 icre = @sdf sys_eval with (round($ice/$yab*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[176]原语 bb = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[177]原语 bb = @udf bb by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[178]原语 bb = @udf bb by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$yab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[179]原语 bb = @udf bb by udf0.df_append with ($yab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'bb_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第174行if语句中]执行第[180]原语 store bb to ssdb by ssdb0 with bb_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_174

def block_if_183(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第183行if语句中]执行第[184]原语 bb = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第183行if语句中]执行第[185]原语 bb = @udf bb by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '100.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第183行if语句中]执行第[186]原语 bb = @udf bb by udf0.df_append with (100.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$yab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第183行if语句中]执行第[187]原语 bb = @udf bb by udf0.df_append with ($yab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'bb_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第183行if语句中]执行第[188]原语 store bb to ssdb by ssdb0 with bb_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_183

def block_if_190(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第190行if语句中]执行第[191]原语 bb = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第190行if语句中]执行第[192]原语 bb = @udf bb by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '0.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第190行if语句中]执行第[193]原语 bb = @udf bb by udf0.df_append with (0.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$yab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第190行if语句中]执行第[194]原语 bb = @udf bb by udf0.df_append with ($yab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'bb_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第190行if语句中]执行第[195]原语 store bb to ssdb by ssdb0 with bb_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_190

def block_if_197(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ice', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yab-$ab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[198]原语 ice = @sdf sys_eval with ($yab-$ab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$yab*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[199]原语 icre = @sdf sys_eval with (round($ice/$yab*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[200]原语 bb = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '-'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[201]原语 bb = @udf bb by udf0.df_append with (-) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[202]原语 bb = @udf bb by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '$yab'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[203]原语 bb = @udf bb by udf0.df_append with ($yab) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'bb_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第197行if语句中]执行第[204]原语 store bb to ssdb by ssdb0 with bb_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_197

def block_if_215(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$ysens*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[216]原语 icre = @sdf sys_eval with (round($ice/$ysens*100,2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[217]原语 cc = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[218]原语 cc = @udf cc by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[219]原语 cc = @udf cc by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$ysens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[220]原语 cc = @udf cc by udf0.df_append with ($ysens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'cc', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'cc_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第215行if语句中]执行第[221]原语 store cc to ssdb by ssdb0 with cc_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_215

def block_if_224(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第224行if语句中]执行第[225]原语 cc = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第224行if语句中]执行第[226]原语 cc = @udf cc by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '100.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第224行if语句中]执行第[227]原语 cc = @udf cc by udf0.df_append with (100.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$ysens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第224行if语句中]执行第[228]原语 cc = @udf cc by udf0.df_append with ($ysens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'cc', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'cc_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第224行if语句中]执行第[229]原语 store cc to ssdb by ssdb0 with cc_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_224

def block_if_232(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第232行if语句中]执行第[233]原语 cc = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第232行if语句中]执行第[234]原语 cc = @udf cc by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '0.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第232行if语句中]执行第[235]原语 cc = @udf cc by udf0.df_append with (0.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$ysens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第232行if语句中]执行第[236]原语 cc = @udf cc by udf0.df_append with ($ysens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'cc', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'cc_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第232行if语句中]执行第[237]原语 store cc to ssdb by ssdb0 with cc_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_232

def block_if_239(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$ysens-$sens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[240]原语 cc = @sdf sys_eval with ($ysens-$sens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$ysens*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[241]原语 cc = @sdf sys_eval with (round($ice/$ysens*100,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[242]原语 cc = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '-'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[243]原语 cc = @udf cc by udf0.df_append with (-) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[244]原语 cc = @udf cc by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cc', 'Action': '@udf', '@udf': 'cc', 'by': 'udf0.df_append', 'with': '$ysens'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[245]原语 cc = @udf cc by udf0.df_append with ($ysens) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'cc', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'cc_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第239行if语句中]执行第[246]原语 store cc to ssdb by ssdb0 with cc_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_239

def block_if_257(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'icre', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$ysens_d*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[258]原语 icre = @sdf sys_eval with (round($ice/$ysens_d*100... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[259]原语 dd = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[260]原语 dd = @udf dd by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[261]原语 dd = @udf dd by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$ysens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[262]原语 dd = @udf dd by udf0.df_append with ($ysens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第257行if语句中]执行第[263]原语 store dd to ssdb by ssdb0 with dd_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_257

def block_if_266(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第266行if语句中]执行第[267]原语 dd = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第266行if语句中]执行第[268]原语 dd = @udf dd by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '100.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第266行if语句中]执行第[269]原语 dd = @udf dd by udf0.df_append with (100.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$ysens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第266行if语句中]执行第[270]原语 dd = @udf dd by udf0.df_append with ($ysens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第266行if语句中]执行第[271]原语 store dd to ssdb by ssdb0 with dd_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_266

def block_if_274(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第274行if语句中]执行第[275]原语 dd = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': ' + '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第274行if语句中]执行第[276]原语 dd = @udf dd by udf0.df_append with ( + ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '0.0%'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第274行if语句中]执行第[277]原语 dd = @udf dd by udf0.df_append with (0.0%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$ysens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第274行if语句中]执行第[278]原语 dd = @udf dd by udf0.df_append with ($ysens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第274行if语句中]执行第[279]原语 store dd to ssdb by ssdb0 with dd_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_274

def block_if_281(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$ysens_d-$sens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[282]原语 dd = @sdf sys_eval with ($ysens_d-$sens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'round($ice/$ysens_d*100,2)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[283]原语 dd = @sdf sys_eval with (round($ice/$ysens_d*100,2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[284]原语 dd = @udf udf0.new_df with (value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '-'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[285]原语 dd = @udf dd by udf0.df_append with (-) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$icre%'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[286]原语 dd = @udf dd by udf0.df_append with ($icre%) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '$ysens_d'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[287]原语 dd = @udf dd by udf0.df_append with ($ysens_d) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd_rate'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第281行if语句中]执行第[288]原语 store dd to ssdb by ssdb0 with dd_rate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_281

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



