#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: FBI_autorun
#datetime: 2024-08-30T16:10:54.643932
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
		add_the_error('[FBI_autorun.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '1 > 2', 'as': 'log', 'with': '系统启动'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[17]原语 assert 1 > 2 as log with 系统启动 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= show', 'Ta': 'pk', 'Action': 'show', 'show': 'defines'}
	try:
		show_fun(ptree)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[19]原语 pk = show defines 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_key', 'Action': 'filter', 'filter': 'pk', 'by': 'key=="data_key"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[20]原语 data_key = filter pk by (key=="data_key") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'bb', 'Action': 'eval', 'eval': 'data_key', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[21]原语 bb = eval data_key by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'act_key', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$bb,"run data_gov_init.fea"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[22]原语 act_key = @sdf sys_unif_run with ($bb,"run data_go... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'main_process'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[33]原语 a = @udf FBI.x_finder3_stop2 with main_process 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'main_process'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[34]原语 a = @udf FBI.x_finder3_start2 with main_process 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'csr_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[35]原语 a = @udf FBI.x_finder3_stop2 with csr_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'csr_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[36]原语 a = @udf FBI.x_finder3_start2 with csr_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'csr_main_process'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[37]原语 a = @udf FBI.x_finder3_stop2 with csr_main_process... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'csr_main_process'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[38]原语 a = @udf FBI.x_finder3_start2 with csr_main_proces... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'yuans_http'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[40]原语 a = @udf FBI.x_finder3_stop2 with yuans_http 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'yuans_http'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[41]原语 a = @udf FBI.x_finder3_start2 with yuans_http 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[43]原语 a = @udf FBI.x_finder3_stop2 with api_proto 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[44]原语 a = @udf FBI.x_finder3_start2 with api_proto 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'dbms'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[46]原语 a = @udf FBI.x_finder3_stop2 with dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'dbms'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[47]原语 a = @udf FBI.x_finder3_start2 with dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'sen_dbms'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[48]原语 a = @udf FBI.x_finder3_stop2 with sen_dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'sen_dbms'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[49]原语 a = @udf FBI.x_finder3_start2 with sen_dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[50]原语 a = @udf FBI.x_finder3_stop2 with dbms_obj 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[51]原语 a = @udf FBI.x_finder3_start2 with dbms_obj 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_mege'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[53]原语 a = @udf FBI.x_finder3_stop2 with api_mege 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_mege'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[54]原语 a = @udf FBI.x_finder3_start2 with api_mege 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'req_alm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[56]原语 a = @udf FBI.x_finder3_stop2 with req_alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'req_alm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[57]原语 a = @udf FBI.x_finder3_start2 with req_alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'dns'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[58]原语 a = @udf FBI.x_finder3_stop2 with dns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'dns'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[59]原语 a = @udf FBI.x_finder3_start2 with dns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[60]原语 a = @udf FBI.x_finder3_stop2 with api_visit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[61]原语 a = @udf FBI.x_finder3_start2 with api_visit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_2_3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[68]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_2_3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp_2_3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[69]原语 a = @udf FBI.x_finder3_start2 with api_owasp_2_3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_sen_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[70]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_sen_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp_sen_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[71]原语 a = @udf FBI.x_finder3_start2 with api_owasp_sen_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_aaai_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[73]原语 a = @udf FBI.x_finder3_stop2 with api_aaai_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_aaai_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[74]原语 a = @udf FBI.x_finder3_start2 with api_aaai_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[80]原语 a = @udf FBI.x_finder3_stop2 with api_owasp2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[81]原语 a = @udf FBI.x_finder3_start2 with api_owasp2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp4'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[83]原语 a = @udf FBI.x_finder3_stop2 with api_owasp4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp4'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[84]原语 a = @udf FBI.x_finder3_start2 with api_owasp4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[86]原语 a = @udf FBI.x_finder3_stop2 with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[87]原语 a = @udf FBI.x_finder3_start2 with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_monitor'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[92]原语 a = @udf FBI.x_finder3_stop2 with api_monitor 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_monitor'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[93]原语 a = @udf FBI.x_finder3_start2 with api_monitor 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_delay_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[98]原语 a = @udf FBI.x_finder3_stop2 with api_delay_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_delay_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[99]原语 a = @udf FBI.x_finder3_start2 with api_delay_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit_hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[101]原语 a = @udf FBI.x_finder3_stop2 with api_visit_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_visit_hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[102]原语 a = @udf FBI.x_finder3_start2 with api_visit_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'data_filter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[109]原语 a = @udf FBI.x_finder3_stop2 with data_filter 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'data_filter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[110]原语 a = @udf FBI.x_finder3_start2 with data_filter 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'req_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[118]原语 a = @udf FBI.x_finder3_stop2 with req_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'req_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[119]原语 a = @udf FBI.x_finder3_start2 with req_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'ip_datalink_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[124]原语 a = @udf FBI.x_finder3_stop2 with ip_datalink_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'ip_datalink_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[125]原语 a = @udf FBI.x_finder3_start2 with ip_datalink_ckh... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'object_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[128]原语 a = @udf FBI.x_finder3_stop2 with object_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'object_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[129]原语 a = @udf FBI.x_finder3_start2 with object_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_main_json2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[131]原语 a = @udf FBI.x_finder3_stop2 with api_main_json2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_main_json2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[132]原语 a = @udf FBI.x_finder3_start2 with api_main_json2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_1_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[139]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_1_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp_1_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[140]原语 a = @udf FBI.x_finder3_start2 with api_owasp_1_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp1_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[141]原语 a = @udf FBI.x_finder3_stop2 with api_owasp1_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp1_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[142]原语 a = @udf FBI.x_finder3_start2 with api_owasp1_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'http_datafilter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[144]原语 a=@udf FBI.x_finder3_stop2 with http_datafilter 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'http_datafilter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[145]原语 a = @udf FBI.x_finder3_start2 with http_datafilter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[148]原语 a=@udf FBI.x_finder3_stop2 with api_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[149]原语 a = @udf FBI.x_finder3_start2 with api_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_model_file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[150]原语 a=@udf FBI.x_finder3_stop2 with api_model_file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_model_file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[151]原语 a = @udf FBI.x_finder3_start2 with api_model_file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_business'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[152]原语 a=@udf FBI.x_finder3_stop2 with api_business 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_business'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[153]原语 a = @udf FBI.x_finder3_start2 with api_business 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp4_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[154]原语 a=@udf FBI.x_finder3_stop2 with api_owasp4_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_owasp4_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[155]原语 a = @udf FBI.x_finder3_start2 with api_owasp4_mode... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'modsecurity'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[160]原语 a = @udf FBI.x_finder3_stop2 with modsecurity 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'modsecurity'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[161]原语 a = @udf FBI.x_finder3_start2 with modsecurity 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_operation_event_oper'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[164]原语 a = @udf FBI.x_finder3_stop2 with api_operation_ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start2', 'with': 'api_operation_event_oper'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[165]原语 a = @udf FBI.x_finder3_start2 with api_operation_e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'data_gov_clear_dd.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[170]原语 run data_gov_clear_dd.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'api_ruodian.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[172]原语 run api_ruodian.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'api_mon_visit.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[174]原语 run api_mon_visit.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'sensitive_table.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[176]原语 run sensitive_table.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'dsaw_overview.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[178]原语 run dsaw_overview.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[FBI_autorun.fbi]执行第[180]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],180

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



