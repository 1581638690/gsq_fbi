#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: begin
#datetime: 2024-08-30T16:10:54.858638
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_list'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[9]原语 a = @udf FBI.x_finder3_list 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'csr_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[11]原语 a = @udf FBI.x_finder3_start with csr_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'csr_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[12]原语 a = @udf FBI.x_finder3_stop2 with csr_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_test'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[14]原语 a = @udf FBI.x_finder3_start with api_test 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_test'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[15]原语 a = @udf FBI.x_finder3_stop2 with api_test 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_monitor_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[17]原语 a = @udf FBI.x_finder3_start with api_monitor_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_monitor_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[18]原语 a = @udf FBI.x_finder3_stop2 with api_monitor_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'clear_distinct'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[20]原语 a = @udf FBI.x_finder3_start with clear_distinct 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'clear_distinct'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[21]原语 a = @udf FBI.x_finder3_stop2 with clear_distinct 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'csr_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[23]原语 a = @udf FBI.x_finder3_start with csr_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'csr_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[24]原语 a = @udf FBI.x_finder3_stop2 with csr_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_main_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[26]原语 a = @udf FBI.x_finder3_start with api_main_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_main_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[27]原语 a = @udf FBI.x_finder3_stop2 with api_main_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_apps_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[29]原语 a = @udf FBI.x_finder3_start with api_apps_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_apps_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[30]原语 a = @udf FBI.x_finder3_stop2 with api_apps_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_urls_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[32]原语 a = @udf FBI.x_finder3_start with api_urls_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_urls_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[33]原语 a = @udf FBI.x_finder3_stop2 with api_urls_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_ips_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[35]原语 a = @udf FBI.x_finder3_start with api_ips_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_ips_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[36]原语 a = @udf FBI.x_finder3_stop2 with api_ips_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_users_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[38]原语 a = @udf FBI.x_finder3_start with api_users_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_users_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[39]原语 a = @udf FBI.x_finder3_stop2 with api_users_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_visit_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[41]原语 a = @udf FBI.x_finder3_start with api_visit_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[42]原语 a = @udf FBI.x_finder3_stop2 with api_visit_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_alerts_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[44]原语 a = @udf FBI.x_finder3_start with api_alerts_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_alerts_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[45]原语 a = @udf FBI.x_finder3_stop2 with api_alerts_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_delay_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[47]原语 a = @udf FBI.x_finder3_start with api_delay_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_delay_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[48]原语 a = @udf FBI.x_finder3_stop2 with api_delay_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[50]原语 a = @udf FBI.x_finder3_stop2 with api_owasp1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_owasp1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[51]原语 a = @udf FBI.x_finder3_start with api_owasp1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_sensite_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[53]原语 a = @udf FBI.x_finder3_stop2 with api_sensite_json... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_sensite_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[54]原语 a = @udf FBI.x_finder3_start with api_sensite_json... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[56]原语 a = @udf FBI.x_finder3_stop2 with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[57]原语 a = @udf FBI.x_finder3_start with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[59]原语 a = @udf FBI.x_finder3_stop2 with api_risk_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_risk_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[60]原语 a = @udf FBI.x_finder3_start with api_risk_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'dsaw_file_rule'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[62]原语 a = @udf FBI.x_finder3_stop2 with dsaw_file_rule 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'dsaw_file_rule'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[63]原语 a = @udf FBI.x_finder3_start with dsaw_file_rule 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[65]原语 a = @udf FBI.x_finder3_stop2 with api_proto 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[66]原语 a = @udf FBI.x_finder3_start with api_proto 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'req_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[68]原语 a = @udf FBI.x_finder3_stop2 with req_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'req_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[69]原语 a = @udf FBI.x_finder3_start with req_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'date_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[71]原语 a = @udf FBI.x_finder3_stop2 with date_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'date_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[72]原语 a = @udf FBI.x_finder3_start with date_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log_2022-05-24,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[75]原语 a = load ssdb by ssdb0 query qrange,X_log_2022-05-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_main_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[78]原语 a = load ssdb by ssdb0 query qrange,X_log:api_main... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_main_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[79]原语 a = load ssdb by ssdb0 query qclear,X_log:api_main... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_monitor_ckh,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[81]原语 a = load ssdb by ssdb0 query qrange,X_log:api_moni... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_monitor_ckh,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[82]原语 a = load ssdb by ssdb0 query qclear,X_log:api_moni... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_urls_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[84]原语 a = load ssdb by ssdb0 query qrange,X_log:api_urls... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_urls_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[85]原语 a = load ssdb by ssdb0 query qclear,X_log:api_urls... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_ips_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[87]原语 a = load ssdb by ssdb0 query qrange,X_log:api_ips_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_ips_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[88]原语 a = load ssdb by ssdb0 query qclear,X_log:api_ips_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_users_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[90]原语 a = load ssdb by ssdb0 query qrange,X_log:api_user... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_users_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[91]原语 a = load ssdb by ssdb0 query qclear,X_log:api_user... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_visit_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[93]原语 a = load ssdb by ssdb0 query qrange,X_log:api_visi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_visit_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[94]原语 a = load ssdb by ssdb0 query qclear,X_log:api_visi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_monitor_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[96]原语 a = load ssdb by ssdb0 query qrange,X_log:api_moni... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_monitor_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[97]原语 a = load ssdb by ssdb0 query qclear,X_log:api_moni... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_owasp1,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[99]原语 a = load ssdb by ssdb0 query qrange,X_log:api_owas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_owasp1,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[100]原语 a = load ssdb by ssdb0 query qclear,X_log:api_owas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_sensite_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[102]原语 a = load ssdb by ssdb0 query qrange,X_log:api_sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_sensite_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[103]原语 a = load ssdb by ssdb0 query qclear,X_log:api_sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_risk_event,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[105]原语 a = load ssdb by ssdb0 query qrange,X_log:api_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_risk_event,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[106]原语 a = load ssdb by ssdb0 query qclear,X_log:api_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_risk_json,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[108]原语 a = load ssdb by ssdb0 query qrange,X_log:api_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_risk_json,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[109]原语 a = load ssdb by ssdb0 query qclear,X_log:api_risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:dsaw_file_rule,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[111]原语 a = load ssdb by ssdb0 query qrange,X_log:dsaw_fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:dsaw_file_rule,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[112]原语 a = load ssdb by ssdb0 query qclear,X_log:dsaw_fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,X_log:api_proto,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[114]原语 a = load ssdb by ssdb0 query qrange,X_log:api_prot... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log:api_proto,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[115]原语 a = load ssdb by ssdb0 query qclear,X_log:api_prot... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,X_log_2022-05-24,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[117]原语 a = load ssdb by ssdb0 query qclear,X_log_2022-05-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange, ST_log_2022-05-24,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[119]原语 a = load ssdb by ssdb0 query qrange, ST_log_2022-0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear, ST_log_2022-05-24,0,1000'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[121]原语 a = load ssdb by ssdb0 query qclear, ST_log_2022-0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'name=>*'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[126]原语 df = load ssdb by ssdb0 with name=>* 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'name', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[begin.fbi]执行第[128]原语 store df to ssdb by ssdb0 with name as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],129

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



