#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: zts_Audit_overview
#datetime: 2024-08-30T16:10:54.072323
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
		add_the_error('[zts_Audit_overview.fbi]执行第[18]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_audit_overview', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT substring(toString(time),6,5) as time1,uniqCombined(app) as tp,uniqCombined(url) as tu,uniqCombined(account) as ta,uniqCombined(srcip) as ts from api_monitor_hour where time >= toDate(today()-6) group by time1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[22]原语 zts_audit_overview = load ckh by ckh with SELECT s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_audit_overview', 'by': 'time1:str,tp:int,tu:int,ta:int,ts:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[23]原语 alter zts_audit_overview by time1:str,tp:int,tu:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts_audit_overview', 'Action': 'order', 'order': 'zts_audit_overview', 'by': 'time1', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[24]原语 zts_audit_overview = order zts_audit_overview by t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_audit_overview', 'Action': '@udf', '@udf': 'zts_audit_overview', 'by': 'udf0.df_fillna_cols', 'with': 'tp:0,tu:0,ta:0,ts:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[25]原语 zts_audit_overview = @udf zts_audit_overview by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_audit_overview', 'by': '"tp":"应用数量","tu":"接口数量","ta":"账户数量","ts":"终端数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[26]原语 rename zts_audit_overview by ("tp":"应用数量","tu":"接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_audit_overview', 'Action': 'loc', 'loc': 'zts_audit_overview', 'by': 'time1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[27]原语 zts_audit_overview = loc zts_audit_overview by tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_audit_overview', 'to': 'ssdb', 'with': 'Audit:zts_audit_overview'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[28]原语 store zts_audit_overview to ssdb with Audit:zts_au... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_app_top', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT app,sum(visit_num) as cp from api_monitor_hour where time >= toDate(today()-30) and app != 'sum1' group by app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[34]原语 zts_app_top = load ckh by ckh with SELECT app,sum(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_app_top', 'by': 'app:str,cp:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[35]原语 alter zts_app_top by app:str,cp:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts_app_top', 'Action': 'order', 'order': 'zts_app_top', 'by': 'cp', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[36]原语 zts_app_top = order zts_app_top by cp with desc li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_app_top', 'by': '"cp":"应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[37]原语 rename zts_app_top by ("cp":"应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_app_top', 'to': 'ssdb', 'with': 'Audit:zts_app_top'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[38]原语 store zts_app_top to ssdb with Audit:zts_app_top 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_url_top', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT url,sum(visit_num) as n_url from api_monitor_hour where time >= toDate(today()-30) and url != 'sum1' group by url"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[53]原语 zts_url_top = load ckh by ckh with SELECT url,sum(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_url_top', 'by': 'url:str,n_url:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[54]原语 alter zts_url_top by url:str,n_url:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts_url_top', 'Action': 'order', 'order': 'zts_url_top', 'by': 'n_url', 'with': 'desc LIMIT 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[55]原语 zts_url_top = order zts_url_top by n_url with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_url_top', 'by': '"n_url":"接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[56]原语 rename zts_url_top by ("n_url":"接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_url_top', 'to': 'ssdb', 'with': 'Audit:zts_url_top'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[57]原语 store zts_url_top to ssdb with Audit:zts_url_top 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_srcip_top', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT srcip,sum(visit_num) as n_sc from api_monitor_hour WHERE time >= toDate(today()-30) and srcip != 'sum1' group by srcip"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[60]原语 zts_srcip_top = load ckh by ckh with SELECT srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_srcip_top', 'by': 'srcip:str,n_sc:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[61]原语 alter zts_srcip_top by srcip:str,n_sc:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts_srcip_top', 'Action': 'order', 'order': 'zts_srcip_top', 'by': 'n_sc', 'with': 'desc LIMIT 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[62]原语 zts_srcip_top = order zts_srcip_top by n_sc with d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_srcip_top', 'by': '"n_sc":"终端数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[63]原语 rename zts_srcip_top by ("n_sc":"终端数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_srcip_top', 'to': 'ssdb', 'with': 'Audit:zts_srcip_top'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[64]原语 store zts_srcip_top to ssdb with Audit:zts_srcip_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_month_contrast', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT substring(toString(time),6,2) as time1,uniqCombined(app) as n_ap,uniqCombined(url) as n_ur,count() as n_cc,uniqCombined(account) as n_ac,uniqCombined(srcip) as n_sr from api_monitor_hour WHERE time >= toDate(today()-60) GROUP BY time1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[68]原语 zts_month_contrast = load ckh by ckh with SELECT s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_month_contrast', 'by': 'time1:str,n_ap:int,n_ur:int,n_cc:int,n_ac:int,n_sr:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[69]原语 alter zts_month_contrast by time1:str,n_ap:int,n_u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'zts_month_contrast.time1', 'Action': 'lambda', 'lambda': 'time1', 'by': "x:x+'月'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[70]原语 zts_month_contrast.time1 = lambda time1 by (x:x+"月... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_month_contrast', 'Action': 'loc', 'loc': 'zts_month_contrast', 'by': 'time1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[71]原语 zts_month_contrast = loc zts_month_contrast by tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_month_contrast', 'by': '"n_ap":"应用数量","n_ur":"接口数量","n_ac":"账户数量","n_sr":"终端数量","n_cc":"事件数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[72]原语 rename zts_month_contrast by ("n_ap":"应用数量","n_ur"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_month_contrast2', 'Action': '@udf', '@udf': 'zts_month_contrast', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[73]原语 zts_month_contrast2 = @udf zts_month_contrast by u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts_month_contrast2', 'to': 'ssdb', 'with': 'Audit:zts_month_contrast2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[74]原语 store zts_month_contrast2 to ssdb with Audit:zts_m... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select COUNT(*) AS num from api_dns'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[78]原语 dns1 = load ckh by ckh with select COUNT(*) AS num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dns1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[79]原语 alter dns1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dns', 'Action': 'loc', 'loc': 'dns1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[80]原语 dns = loc dns1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dns', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[81]原语 rename dns by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'dns', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[82]原语 aa_num = eval dns by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'dns.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=83
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[83]原语 if $aa_num > 100000 with dns.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "dns = add name by ('DNS协议总数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=84
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[84]原语 if $aa_num > 100000 with dns = add name by ("DNS协议... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "dns = add name by ('DNS协议总数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=85
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[85]原语 if $aa_num <= 100000 with dns = add name by ("DNS协... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns', 'Action': 'add', 'add': 'icon', 'by': "'F137'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[86]原语 dns = add icon by ("F137") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[87]原语 dns = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_dns'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[88]原语 dns = add pageid by ("qes:api_dns") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select COUNT(*) AS num from api_fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[90]原语 fileinfo1 = load ckh by ckh with select COUNT(*) A... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'fileinfo1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[91]原语 alter fileinfo1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'fileinfo', 'Action': 'loc', 'loc': 'fileinfo1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[92]原语 fileinfo = loc fileinfo1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fileinfo', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[93]原语 rename fileinfo by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'fileinfo', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[94]原语 aa_num = eval fileinfo by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'fileinfo.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=95
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[95]原语 if $aa_num > 100000 with fileinfo.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "fileinfo = add name by ('文件信息总数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=96
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[96]原语 if $aa_num > 100000 with fileinfo = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "fileinfo = add name by ('文件信息总数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=97
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[97]原语 if $aa_num <= 100000 with fileinfo = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'icon', 'by': "'F362'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[98]原语 fileinfo = add icon by ("F362") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[99]原语 fileinfo = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_fileinfo'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[100]原语 fileinfo = add pageid by ("qes:api_fileinfo") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_pop31', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_pop3'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[102]原语 api_pop31 = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_pop31', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[103]原语 alter api_pop31 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_pop3', 'Action': 'loc', 'loc': 'api_pop31', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[104]原语 api_pop3 = loc api_pop31 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_pop3', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[105]原语 rename api_pop3 by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_pop3', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[106]原语 aa_num = eval api_pop3 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_pop3.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=107
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[107]原语 if $aa_num > 100000 with api_pop3.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_pop3 = add name by ('Pop3邮件协议(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=108
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[108]原语 if $aa_num > 100000 with api_pop3 = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_pop3 = add name by ('Pop3邮件协议')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=109
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[109]原语 if $aa_num <= 100000 with api_pop3 = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_pop3', 'Action': 'add', 'add': 'icon', 'by': "'F139'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[110]原语 api_pop3 = add icon by ("F139") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_pop3', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[111]原语 api_pop3 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_pop3', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_pop3'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[112]原语 api_pop3 = add pageid by ("qes:api_pop3") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_imap1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_imap'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[114]原语 api_imap1 = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_imap1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[115]原语 alter api_imap1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_imap', 'Action': 'loc', 'loc': 'api_imap1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[116]原语 api_imap = loc api_imap1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_imap', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[117]原语 rename api_imap by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_imap', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[118]原语 aa_num = eval api_imap by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_imap.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=119
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[119]原语 if $aa_num > 100000 with api_imap.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_imap = add name by ('Imap邮件协议(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=120
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[120]原语 if $aa_num > 100000 with api_imap = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_imap = add name by ('Imap邮件协议')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=121
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[121]原语 if $aa_num <= 100000 with api_imap = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_imap', 'Action': 'add', 'add': 'icon', 'by': "'F161'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[122]原语 api_imap = add icon by ("F161") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_imap', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[123]原语 api_imap = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_imap', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_imap'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[124]原语 api_imap = add pageid by ("qes:api_imap") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_smtp1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smtp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[126]原语 api_smtp1 = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_smtp1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[127]原语 alter api_smtp1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_smtp', 'Action': 'loc', 'loc': 'api_smtp1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[128]原语 api_smtp = loc api_smtp1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_smtp', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[129]原语 rename api_smtp by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_smtp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[130]原语 aa_num = eval api_smtp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_smtp.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=131
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[131]原语 if $aa_num > 100000 with api_smtp.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_smtp = add name by ('Smtp邮件协议(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=132
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[132]原语 if $aa_num > 100000 with api_smtp = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_smtp = add name by ('Smtp邮件协议')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=133
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[133]原语 if $aa_num <= 100000 with api_smtp = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smtp', 'Action': 'add', 'add': 'icon', 'by': "'F160'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[134]原语 api_smtp = add icon by ("F160") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smtp', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[135]原语 api_smtp = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smtp', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_smtp'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[136]原语 api_smtp = add pageid by ("qes:api_smtp") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_smb1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smb'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[138]原语 api_smb1 = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_smb1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[139]原语 alter api_smb1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_smb', 'Action': 'loc', 'loc': 'api_smb1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[140]原语 api_smb = loc api_smb1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_smb', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[141]原语 rename api_smb by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_smb', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[142]原语 aa_num = eval api_smb by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_smb.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=143
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[143]原语 if $aa_num > 100000 with api_smb.value = lambda va... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_smb = add name by ('Windows共享(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=144
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[144]原语 if $aa_num > 100000 with api_smb = add name by ("W... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_smb = add name by ('Windows共享')"}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[145]原语 if $aa_num <= 100000 with api_smb = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smb', 'Action': 'add', 'add': 'icon', 'by': "'F141'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[146]原语 api_smb = add icon by ("F141") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smb', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[147]原语 api_smb = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_smb', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_smb'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[148]原语 api_smb = add pageid by ("qes:api_smb") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_ftp1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_ftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[150]原语 api_ftp1 = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_ftp1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[151]原语 alter api_ftp1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_ftp', 'Action': 'loc', 'loc': 'api_ftp1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[152]原语 api_ftp = loc api_ftp1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_ftp', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[153]原语 rename api_ftp by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_ftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[154]原语 aa_num = eval api_ftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_ftp.value = lambda value by (x:round(x/10000,2))'}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[155]原语 if $aa_num > 100000 with api_ftp.value = lambda va... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_ftp = add name by ('FTP文件传输(万)')"}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[156]原语 if $aa_num > 100000 with api_ftp = add name by ("F... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_ftp = add name by ('FTP文件传输')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=157
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[157]原语 if $aa_num <= 100000 with api_ftp = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_ftp', 'Action': 'add', 'add': 'icon', 'by': "'F184'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[158]原语 api_ftp = add icon by ("F184") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_ftp', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[159]原语 api_ftp = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_ftp', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_ftp'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[160]原语 api_ftp = add pageid by ("qes:api_ftp") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_tftp1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_tftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[162]原语 api_tftp1 = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_tftp1', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[163]原语 alter api_tftp1 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_tftp', 'Action': 'loc', 'loc': 'api_tftp1', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[164]原语 api_tftp = loc api_tftp1 by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_tftp', 'by': '"num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[165]原语 rename api_tftp by ("num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'api_tftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[166]原语 aa_num = eval api_tftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'api_tftp.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=167
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[167]原语 if $aa_num > 100000 with api_tftp.value = lambda v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "api_tftp = add name by ('Tftp文件传输(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=168
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[168]原语 if $aa_num > 100000 with api_tftp = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "api_tftp = add name by ('Tftp文件传输')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=169
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[169]原语 if $aa_num <= 100000 with api_tftp = add name by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_tftp', 'Action': 'add', 'add': 'icon', 'by': "'F181'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[170]原语 api_tftp = add icon by ("F181") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_tftp', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[171]原语 api_tftp = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_tftp', 'Action': 'add', 'add': 'pageid', 'by': "'qes:api_tftp'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[172]原语 api_tftp = add pageid by ("qes:api_tftp") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'xy', 'Action': 'union', 'union': 'dns,fileinfo,api_pop3,api_imap,api_smtp,api_smb,api_ftp,api_tftp'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[174]原语 xy = union dns,fileinfo,api_pop3,api_imap,api_smtp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'xy', 'Action': 'loc', 'loc': 'xy', 'by': 'name,value,icon,details,pageid'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[175]原语 xy = loc xy by name,value,icon,details,pageid 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'xy', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'Audit:Audit'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[176]原语 store xy to ssdb by ssdb0 with Audit:Audit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_dns where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[180]原语 dns = load ckh by ckh with select count(*) as num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dns', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[181]原语 alter dns by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dns', 'Action': 'add', 'add': 'name', 'by': "'DNS协议'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[182]原语 dns = add name by ("DNS协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_pop3 where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[183]原语 pop3 = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'pop3', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[184]原语 alter pop3 by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'pop3', 'Action': 'add', 'add': 'name', 'by': "'Pop3邮件协议'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[185]原语 pop3 = add name by ("Pop3邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_imap where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[186]原语 imap = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'imap', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[187]原语 alter imap by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'imap', 'Action': 'add', 'add': 'name', 'by': "'Imap邮件协议'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[188]原语 imap = add name by ("Imap邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smtp where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[189]原语 smtp = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smtp', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[190]原语 alter smtp by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smtp', 'Action': 'add', 'add': 'name', 'by': "'Smtp邮件协议'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[191]原语 smtp = add name by ("Smtp邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smb where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[192]原语 smb = load ckh by ckh with select count(*) as num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smb', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[193]原语 alter smb by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'smb', 'Action': 'add', 'add': 'name', 'by': "'Windows共享'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[194]原语 smb = add name by ("Windows共享") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_ftp where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[195]原语 ftp = load ckh by ckh with select count(*) as num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ftp', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[196]原语 alter ftp by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ftp', 'Action': 'add', 'add': 'name', 'by': "'Ftp文件传输'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[197]原语 ftp = add name by ("Ftp文件传输") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_tftp where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[198]原语 tftp = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tftp', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[199]原语 alter tftp by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tftp', 'Action': 'add', 'add': 'name', 'by': "'Tftp文件传输'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[200]原语 tftp = add name by ("Tftp文件传输") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_fileinfo where timestamp >= toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[201]原语 fileinfo = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'fileinfo', 'by': 'num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[202]原语 alter fileinfo by num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'name', 'by': "'文件信息'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[203]原语 fileinfo = add name by ("文件信息") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'j_xyxx', 'Action': 'union', 'union': 'dns,ppop3,imap,smtp,smb,ftp,tftp,fileinfo'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[204]原语 j_xyxx = union dns,ppop3,imap,smtp,smb,ftp,tftp,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_xyxx', 'Action': 'loc', 'loc': 'j_xyxx', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[205]原语 j_xyxx = loc j_xyxx by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'j_xyxx', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'xieyi:j_data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[206]原语 store j_xyxx to ssdb by ssdb0 with xieyi:j_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[209]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[210]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[211]原语 day = @sdf format_now with ($day,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[212]原语 now = @sdf format_now with ($now,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day,$now,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[213]原语 j_hour = @udf udf0.new_df_timerange with ($day,$no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[214]原语 j_hour.hour = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[215]原语 j_hour = loc j_hour by hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_dns where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[216]原语 dns = load ckh by ckh with select substring(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dns', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[217]原语 alter dns by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dns', 'as': "'num':'DNS协议'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[218]原语 rename dns as ("num":"DNS协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_pop3 where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[219]原语 pop3 = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'pop3', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[220]原语 alter pop3 by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'pop3', 'as': "'num':'Pop3邮件协议'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[221]原语 rename pop3 as ("num":"Pop3邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_imap where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[222]原语 imap = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'imap', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[223]原语 alter imap by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'imap', 'as': "'num':'Imap邮件协议'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[224]原语 rename imap as ("num":"Imap邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_smtp where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[225]原语 smtp = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smtp', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[226]原语 alter smtp by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'smtp', 'as': "'num':'Smtp邮件协议'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[227]原语 rename smtp as ("num":"Smtp邮件协议") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_smb where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[228]原语 smb = load ckh by ckh with select substring(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'smb', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[229]原语 alter smb by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'smb', 'as': "'num':'Windows共享'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[230]原语 rename smb as ("num":"Windows共享") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_ftp where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[231]原语 ftp = load ckh by ckh with select substring(toStri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ftp', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[232]原语 alter ftp by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ftp', 'as': "'num':'Ftp文件传输'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[233]原语 rename ftp as ("num":"Ftp文件传输") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_tftp where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[234]原语 tftp = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tftp', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[235]原语 alter tftp by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tftp', 'as': "'num':'Tftp文件传输'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[236]原语 rename tftp as ("num":"Tftp文件传输") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,count(*) as num from api_fileinfo where timestamp >= toDate(today()) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[237]原语 fileinfo = load ckh by ckh with select substring(t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'fileinfo', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[238]原语 alter fileinfo by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fileinfo', 'as': "'num':'文件信息'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[239]原语 rename fileinfo as ("num":"文件信息") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'j_hour,dns', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[240]原语 xyxx = join j_hour,dns by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,pop3', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[241]原语 xyxx = join xyxx,pop3 by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,imap', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[242]原语 xyxx = join xyxx,imap by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,smtp', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[243]原语 xyxx = join xyxx,smtp by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,smb', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[244]原语 xyxx = join xyxx,smb by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,ftp', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[245]原语 xyxx = join xyxx,ftp by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,tftp', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[246]原语 xyxx = join xyxx,tftp by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'xyxx,fileinfo', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[247]原语 xyxx = join xyxx,fileinfo by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xyxx', 'Action': '@udf', '@udf': 'xyxx', 'by': 'udf0.df_fillna_cols', 'with': 'DNS协议:0,Pop3邮件协议:0,Imap邮件协议:0,Smtp邮件协议:0,Windows共享:0,Ftp文件传输:0,Tftp文件传输:0,文件信息:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[248]原语 xyxx = @udf xyxx by udf0.df_fillna_cols with DNS协议... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'xyxx', 'by': 'hour:str,DNS协议:int,Pop3邮件协议:int,Imap邮件协议:int,Smtp邮件协议:int,Windows共享:int,Ftp文件传输:int,Tftp文件传输:int,文件信息:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[249]原语 alter xyxx by hour:str,DNS协议:int,Pop3邮件协议:int,Imap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'xyxx.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[250]原语 xyxx.hour = lambda hour by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'xyxx', 'Action': 'loc', 'loc': 'xyxx', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[251]原语 xyxx = loc xyxx by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'xyxx', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'xieyi:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[252]原语 store xyxx to ssdb by ssdb0 with xieyi:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select rrname,count(*) as num from api_dns where timestamp >= toDate(today()) and rrname != '' group by rrname"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[255]原语 t_dns = load ckh by ckh with select rrname,count(*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 't_dns', 'by': 'rrname:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[256]原语 alter t_dns by rrname:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 't_dns', 'Action': 'order', 'order': 't_dns', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[257]原语 t_dns = order t_dns by num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 't_dns.详情', 'Action': 'lambda', 'lambda': 'rrname', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[258]原语 t_dns.详情 = lambda rrname by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't_dns', 'Action': 'loc', 'loc': 't_dns', 'by': 'rrname', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[259]原语 t_dns = loc t_dns by rrname to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 't_dns', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dns:t_dns'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[260]原语 store t_dns to ssdb by ssdb0 with dns:t_dns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select srcip,count(*) as num from api_ftp where timestamp >= toDate(today()) group by srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[263]原语 t_ftp = load ckh by ckh with select srcip,count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 't_ftp', 'by': 'srcip:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[264]原语 alter t_ftp by srcip:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 't_ftp', 'Action': 'order', 'order': 't_ftp', 'by': 'num', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[265]原语 t_ftp = order t_ftp by num with desc limit 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 't_ftp.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[266]原语 t_ftp.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't_ftp', 'Action': 'loc', 'loc': 't_ftp', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[267]原语 t_ftp = loc t_ftp by srcip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 't_ftp', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ftp:t_ftp'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[268]原语 store t_ftp to ssdb by ssdb0 with ftp:t_ftp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_file', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app_proto as name,count(*) as num from api_fileinfo where timestamp >= toDate(today()) group by name'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[271]原语 t_file = load ckh by ckh with select app_proto as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 't_file', 'by': 'name:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[272]原语 alter t_file by name:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 't_file', 'Action': 'order', 'order': 't_file', 'by': 'num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[273]原语 t_file = order t_file by num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 't_file', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'file:t_file'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[274]原语 store t_file to ssdb by ssdb0 with file:t_file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(name) as app_num,sum(ysjjk) as url_num,sum(sjfw) as sj_num,sum(xsjjk) as app1_num from audit_statistics'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[279]原语 zts_num = load db by mysql1 with select count(name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_num', 'Action': '@udf', '@udf': 'zts_num', 'by': 'udf0.df_fillna_cols', 'with': 'app_num:0,url_num:0,sj_num:0,app1_num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[280]原语 zts_num = @udf zts_num by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zts_num', 'by': 'app_num:int,url_num:int,sj_num:int,app1_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[281]原语 alter zts_num by app_num:int,url_num:int,sj_num:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_app_num', 'Action': 'loc', 'loc': 'zts_num', 'by': 'app_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[285]原语 zts_app_num = loc zts_num by app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_app_num', 'Action': 'add', 'add': 'details', 'by': "'审计应用的总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[286]原语 zts_app_num = add details by ("审计应用的总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_app_num', 'by': '"app_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[287]原语 rename zts_app_num by ("app_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_app_num', 'Action': 'add', 'add': 'name', 'by': "'审计应用数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[288]原语 zts_app_num = add name by ("审计应用数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_app_num', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[289]原语 zts_app_num = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_url_num', 'Action': 'loc', 'loc': 'zts_num', 'by': 'url_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[294]原语 zts_url_num = loc zts_num by url_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_url_num', 'by': '"url_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[295]原语 rename zts_url_num by ("url_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'zts_url_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[296]原语 aa_num = eval zts_url_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'zts_url_num.value = lambda value by (x:round(x/10000,2))'}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[297]原语 if $aa_num > 100000 with zts_url_num.value = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "zts_url_num = add name by ('已审计接口数(万)')"}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[298]原语 if $aa_num > 100000 with zts_url_num = add name by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "zts_url_num = add name by ('已审计接口数')"}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[299]原语 if $aa_num <= 100000 with zts_url_num = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_url_num', 'Action': 'add', 'add': 'details', 'by': "'应用审计的已审计接口总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[300]原语 zts_url_num = add details by ("应用审计的已审计接口总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_url_num', 'Action': 'add', 'add': 'icon', 'by': "'F307'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[301]原语 zts_url_num = add icon by ("F307") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_account_num', 'Action': 'loc', 'loc': 'zts_num', 'by': 'sj_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[306]原语 zts_account_num = loc zts_num by sj_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_account_num', 'by': '"sj_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[307]原语 rename zts_account_num by ("sj_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'zts_account_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[308]原语 aa_num = eval zts_account_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'zts_account_num.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=309
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[309]原语 if $aa_num > 100000 with zts_account_num.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "zts_account_num = add name by ('审计事件数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=310
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[310]原语 if $aa_num > 100000 with zts_account_num = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "zts_account_num = add name by ('审计事件数')"}
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
		add_the_error('[zts_Audit_overview.fbi]执行第[311]原语 if $aa_num <= 100000 with zts_account_num = add na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_account_num', 'Action': 'add', 'add': 'details', 'by': "'所有接口审计产生的事件总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[312]原语 zts_account_num = add details by ("所有接口审计产生的事件总数")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zts_account_num', 'Action': 'add', 'add': 'icon', 'by': "'F441'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[313]原语 zts_account_num = add icon by ("F441") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'jks', 'Action': 'loc', 'loc': 'zts_num', 'by': 'app1_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[318]原语 jks = loc zts_num by app1_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'jks', 'by': '"app1_num":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[319]原语 rename jks by ("app1_num":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'jks', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[320]原语 aa_num = eval jks by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'jks.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=321
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[321]原语 if $aa_num > 100000 with jks.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "jks = add name by ('审计接口数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=322
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[322]原语 if $aa_num > 100000 with jks = add name by ("审计接口数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "jks = add name by ('审计接口数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=323
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[323]原语 if $aa_num <= 100000 with jks = add name by ("审计接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'jks', 'Action': 'add', 'add': 'details', 'by': "'审计应用包含的接口总数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[324]原语 jks = add details by ("审计应用包含的接口总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'jks', 'Action': 'add', 'add': 'icon', 'by': "'F306'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[325]原语 jks = add icon by ("F306") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'j_jks', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select sum(visit_num) as value from api_monitor_hour where time > toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[328]原语 j_jks = load ckh by ckh with select sum(visit_num)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'j_jks', 'by': 'value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[329]原语 alter j_jks by value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'j_jks', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[331]原语 aa_num = eval j_jks by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'j_jks.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=332
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[332]原语 if $aa_num > 100000 with j_jks.value = lambda valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "j_jks = add name by ('今日审计事件数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=333
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[333]原语 if $aa_num > 100000 with j_jks = add name by ("今日审... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "j_jks = add name by ('今日审计事件数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=334
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[334]原语 if $aa_num <= 100000 with j_jks = add name by ("今日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'j_jks', 'Action': 'add', 'add': 'details', 'by': "'今日接口审计产生的事件数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[335]原语 j_jks = add details by ("今日接口审计产生的事件数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'j_jks', 'Action': 'add', 'add': 'icon', 'by': "'F010'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[336]原语 j_jks = add icon by ("F010") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'xy1', 'Action': 'union', 'union': 'dns1,fileinfo1,api_pop31,api_imap1,api_smtp1,api_smb1,api_ftp1,api_tftp1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[339]原语 xy1 = union dns1,fileinfo1,api_pop31,api_imap1,api... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'xy1', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[340]原语 xy1 = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'xy1', 'Action': 'group', 'group': 'xy1', 'by': 'aa', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[341]原语 xy1 = group xy1 by aa agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'xy1', 'as': "'num_sum':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[342]原语 rename xy1 as ("num_sum":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'xy1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[343]原语 aa_num = eval xy1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'xy1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=344
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[344]原语 if $aa_num > 100000 with xy1.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "xy1 = add name by ('其他协议事件数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=345
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[345]原语 if $aa_num > 100000 with xy1 = add name by ("其他协议事... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "xy1 = add name by ('其他协议事件数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=346
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[346]原语 if $aa_num <= 100000 with xy1 = add name by ("其他协议... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'xy1', 'Action': 'add', 'add': 'details', 'by': "'包含DNS协议、文件信息、Pop3邮件协议、Imap邮件协议、Smtp邮件协议、Windows共享、FTP文件传输、Tftp文件传输的协议事件数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[347]原语 xy1 = add details by ("包含DNS协议、文件信息、Pop3邮件协议、Imap邮... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'xy1', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[348]原语 xy1 = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'Audit', 'Action': 'union', 'union': 'zts_app_num,jks,zts_url_num,zts_account_num,j_jks,xy1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[351]原语 Audit = union zts_app_num,jks,zts_url_num,zts_acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'Audit', 'Action': 'loc', 'loc': 'Audit', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[352]原语 Audit = loc Audit by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'Audit', 'Action': 'add', 'add': 'pageid', 'by': "'modeling:zts_audit_statistics','','modeling:api_new','','','dashboard7:ATmH9OW'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[353]原语 Audit = add pageid by ("modeling:zts_audit_statist... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'Audit', 'Action': 'add', 'add': '参数', 'by': "'','','@api_status=1','','',''"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[354]原语 Audit = add 参数 by ("","","@api_status=1","","","")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'Audit', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'Audit:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[355]原语 store Audit to ssdb by ssdb0 with Audit:trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[359]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[360]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[361]原语 day = @sdf format_now with ($day,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[362]原语 now = @sdf format_now with ($now,"%Y-%m-%d %H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day,$now,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[363]原语 j_hour = @udf udf0.new_df_timerange with ($day,$no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[364]原语 j_hour.hour = lambda end_time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[365]原语 j_hour = loc j_hour by hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'moni', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(time),1,13) as hour,sum(visit_num) as num from api_monitor_hour where time >= toDate(today()-1) group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[366]原语 moni = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'moni', 'by': 'hour:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[367]原语 alter moni by hour:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'moni', 'Action': 'group', 'group': 'moni', 'by': 'hour', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[368]原语 moni = group moni by hour agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'moni', 'Action': 'loc', 'loc': 'moni', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[369]原语 moni = loc moni by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'xyxx', 'Action': 'join', 'join': 'j_hour,moni', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[370]原语 xyxx = join j_hour,moni by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xyxx', 'Action': '@udf', '@udf': 'xyxx', 'by': 'udf0.df_fillna_cols', 'with': 'num_sum:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[371]原语 xyxx = @udf xyxx by udf0.df_fillna_cols with num_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'xyxx.num_sum', 'Action': 'lambda', 'lambda': 'num_sum', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[372]原语 xyxx.num_sum = lambda num_sum by (x:round(x/10000,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'xyxx', 'as': "'num_sum':'接口审计(万)'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[373]原语 rename xyxx as ("num_sum":"接口审计(万)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'xyxx.hour', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x[11:]+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[374]原语 xyxx.hour = lambda hour by (x:x[11:]+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'xyxx', 'Action': 'loc', 'loc': 'xyxx', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[375]原语 xyxx = loc xyxx by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'xyxx', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'jk:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[376]原语 store xyxx to ssdb by ssdb0 with jk:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-30d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[380]原语 day1 = @sdf sys_now with -30d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day1,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[381]原语 day1 = @sdf format_now with ($day1,"%Y-%m-%d 00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[382]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[383]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%d 00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'day', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day1,$day2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[384]原语 day = @udf udf0.new_df_timerange with ($day1,$day2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'day.day', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[385]原语 day.day = lambda end_time by (x:x[5:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'day', 'Action': 'loc', 'loc': 'day', 'by': 'day'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[386]原语 day = loc day by day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_moni', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(time),6,5) as day,sum(visit_num) as sj from api_monitor_hour where time >= toDate(today()-30) group by day'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[388]原语 api_moni = load ckh by ckh with select substring(t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_moni', 'by': 'day:str,sj:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[389]原语 alter api_moni by day:str,sj:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_moni', 'Action': 'join', 'join': 'day,api_moni', 'by': 'day,day', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[390]原语 api_moni = join day,api_moni by day,day with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_moni', 'Action': 'loc', 'loc': 'api_moni', 'by': 'day,sj'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[391]原语 api_moni = loc api_moni by day,sj 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_moni', 'Action': 'loc', 'loc': 'api_moni', 'by': 'day', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[392]原语 api_moni = loc api_moni by day to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_moni', 'Action': '@udf', '@udf': 'api_moni', 'by': 'udf0.df_fillna_cols', 'with': 'sj:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[393]原语 api_moni = @udf api_moni by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_moni.sj', 'Action': 'lambda', 'lambda': 'sj', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[394]原语 api_moni.sj = lambda sj by (x:round(x/10000,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_moni', 'by': "'sj':'接口审计事件数(万)'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[395]原语 rename api_moni by ("sj":"接口审计事件数(万)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_moni', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'shijian:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[396]原语 store api_moni to ssdb by ssdb0 with shijian:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[zts_Audit_overview.fbi]执行第[399]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],399

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



