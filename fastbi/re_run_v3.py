#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: re_run
#datetime: 2024-08-30T16:10:54.037902
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'csr_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[9]原语 a = @udf FBI.x_finder3_stop2 with csr_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_main_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[10]原语 a = @udf FBI.x_finder3_stop2 with api_main_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_apps_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[11]原语 a = @udf FBI.x_finder3_stop2 with api_apps_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_urls_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[12]原语 a = @udf FBI.x_finder3_stop2 with api_urls_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_ips_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[13]原语 a = @udf FBI.x_finder3_stop2 with api_ips_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_users_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[14]原语 a = @udf FBI.x_finder3_stop2 with api_users_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[15]原语 a = @udf FBI.x_finder3_stop2 with api_visit_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_alerts_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[16]原语 a = @udf FBI.x_finder3_stop2 with api_alerts_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_monitor_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[17]原语 a = @udf FBI.x_finder3_stop2 with api_monitor_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[18]原语 a = @udf FBI.x_finder3_stop2 with api_owasp1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_sensite_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[20]原语 a = @udf FBI.x_finder3_stop2 with api_sensite_json... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[21]原语 a = @udf FBI.x_finder3_stop2 with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[22]原语 a = @udf FBI.x_finder3_stop2 with api_risk_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'clear_distinct'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[23]原语 a = @udf FBI.x_finder3_start with clear_distinct 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'clear_distinct'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[24]原语 a = @udf FBI.x_finder3_stop2 with clear_distinct 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[28]原语 ip = @udf RS.exec_mysql_sql with (mysql1,truncate ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[29]原语 app = @udf RS.exec_mysql_sql with (mysql1,truncate... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[30]原语 api = @udf RS.exec_mysql_sql with (mysql1,truncate... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_account_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[31]原语 account = @udf RS.exec_mysql_sql with (mysql1,trun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sensitive_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[32]原语 sen = @udf RS.exec_mysql_sql with (mysql1,truncate... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'manage', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table Report_management'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[34]原语 manage = @udf RS.exec_mysql_sql with (mysql1,trunc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate data_risk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[35]原语 data = @udf RS.exec_mysql_sql with (mysql1,truncat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate table api_visit'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[36]原语 visit = load ckh by ckh with truncate table api_vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate table api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[37]原语 visit = load ckh by ckh with truncate table api_mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate table api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[38]原语 visit = load ckh by ckh with truncate table api_ri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate table risk_api'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[39]原语 visit = load ckh by ckh with truncate table risk_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'kfk', 'as': '192.168.1.190:9092'}
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[41]原语 define kfk as 192.168.1.190:9092 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'k', 'Action': '@udf', '@udf': 'KFK.df_link', 'with': 'kfk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[42]原语 k = @udf KFK.df_link with kfk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'topic', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_topics'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[45]原语 topic = @udf k by KFK.show_topics 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'o', 'Action': '@udf', '@udf': 'k,topic', 'by': 'KFK.show_muli_offset'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[46]原语 o = @udf k,topic by KFK.show_muli_offset 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'p', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_offset', 'with': 'risk_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[48]原语 p = @udf k by KFK.show_offset with risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.describe', 'with': 'risk_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[50]原语 d = @udf k by KFK.describe with risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_partitions', 'with': 'risk_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[51]原语 d = @udf k by KFK.show_partitions with risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'risk_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[54]原语 d = @udf k by KFK.delete_topics with risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[55]原语 d = @udf k by KFK.delete_topics with api_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_sen'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[56]原语 d = @udf k by KFK.delete_topics with api_sen 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[57]原语 d = @udf k by KFK.delete_topics with api_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_alert'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[58]原语 d = @udf k by KFK.delete_topics with api_alert 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[59]原语 d = @udf k by KFK.delete_topics with api_visit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[60]原语 d = @udf k by KFK.delete_topics with api_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[61]原语 d = @udf k by KFK.delete_topics with api_user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_monitor'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[62]原语 d = @udf k by KFK.delete_topics with api_monitor 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.fast_load', 'with': 'zichan,x1,30,30, False'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[65]原语 a = @udf k by KFK.fast_load with zichan,x1,30,30, ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'q', 'by': 'KFK.fast_store', 'with': 'kfk2,zichan_3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[re_run.fbi]执行第[68]原语 a=@udf q by  by KFK.fast_store with kfk2,zichan_3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],73

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



