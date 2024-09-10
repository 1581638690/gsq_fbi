#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: factory_reset
#datetime: 2024-08-30T16:10:53.864634
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
		add_the_error('[factory_reset.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'reset', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'factory_reset as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[17]原语 reset = load ssdb by ssdb0 with factory_reset as j... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'date_num', 'Action': 'jaas', 'jaas': 'reset', 'by': "reset['reset']", 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[18]原语 date_num = jaas reset by reset["reset"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'factory_reset as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[19]原语 d = load ssdb by ssdb0 with factory_reset as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'd', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$d, x:{"reset": ""}'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[20]原语 d = @sdf sys_lambda with ($d, x:{"reset": ""}) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'factory_reset'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[21]原语 store d to ssdb by ssdb0 with factory_reset 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$date_num == "ABC@2020"', 'as': 'altert', 'to': '密码正确,正在重置', 'with': '密码错误！'}
	ptree['assert'] = replace_ps(ptree['assert'],runtime)
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[22]原语 assert  $date_num == "ABC@2020" as altert to 密码正确,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': '$date_num == "ABC@2020"', 'as': 'log', 'to': '重置密码正确，一键清除执行', 'with': '输入重置密码错误'}
	ptree['assert'] = replace_ps(ptree['assert'],runtime)
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[23]原语 assert  $date_num == "ABC@2020" as log to 重置密码正确，一... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$date_num == "ABC@2020"', 'with': '""\na = @udf FBI.x_finder3_stop2 with /opt/openfbi/fbi-bin/stop-fst.sh\n#停止xlink\na = @udf FBI.x_finder3_stop2 with api_aaai_json\na = @udf FBI.x_finder3_stop2 with req_alm\na = @udf FBI.x_finder3_stop2 with dns\na = @udf FBI.x_finder3_stop2 with api_visit\na = @udf FBI.x_finder3_stop2 with api_owasp_2_3\na = @udf FBI.x_finder3_stop2 with api_owasp_sen_data\na = @udf FBI.x_finder3_stop2 with api_aaai_jso\na = @udf FBI.x_finder3_stop2 with api_mege\na = @udf FBI.x_finder3_stop2 with api_owasp2\na = @udf FBI.x_finder3_stop2 with api_owasp4\na = @udf FBI.x_finder3_stop2 with api_risk_event\na = @udf FBI.x_finder3_stop2 with api_monitor_ckh\na = @udf FBI.x_finder3_stop2 with api_delay_json\na = @udf FBI.x_finder3_stop2 with api_proto\na = @udf FBI.x_finder3_stop2 with api_visit_hx\na = @udf FBI.x_finder3_stop2 with data_filter\na = @udf FBI.x_finder3_stop2 with req_alarm\na = @udf FBI.x_finder3_stop2 with ip_datalink_ckh\na = @udf FBI.x_finder3_stop2 with yuan_http\na = @udf FBI.x_finder3_stop2 with object_active\na = @udf FBI.x_finder3_stop2 with api_main_json2\na = @udf FBI.x_finder3_stop2 with main_process\na = @udf FBI.x_finder3_stop2 with api_owasp_1_1\na = @udf FBI.x_finder3_stop2 with api_owasp1_2\na = @udf FBI.x_finder3_stop2 with http_datafilter\na = @udf FBI.x_finder3_stop2 with api_model\na = @udf FBI.x_finder3_stop2 with modsecurity\na = @udf FBI.x_finder3_stop2 with api_owasp4_model\na = @udf FBI.x_finder3_stop2 with api_owasp4_2\na = @udf FBI.x_finder3_stop2 with api_business\n# 清空 hashmap\na= @udf SSDB.hclear with FF:urldis\na= @udf SSDB.hclear with FF:url2\na= @udf SSDB.hclear with FF:url3\na= @udf SSDB.hclear with FF:ip2\na= @udf SSDB.hclear with FF:app2\na= @udf SSDB.hclear with FF:user3\na= @udf SSDB.hclear with FF:alert2\na= @udf SSDB.hclear with FF:urll\na= @udf SSDB.hclear with FF:urll2\na= @udf SSDB.hclear with FF:app_js\na= @udf SSDB.hclear with FF:api_js\na= @udf SSDB.hclear with FF:rule_file\na= @udf SSDB.hclear with api_merge\na= @udf SSDB.hclear with api_merge1\na= @udf SSDB.hclear with app_merge\na= @udf SSDB.hclear with FF:y_url\na= @udf SSDB.hclear with FF:app_datalink\na= @udf SSDB.hclear with FF:ip_datalink\na= @udf SSDB.hclear with FF:acc_ip\na= @udf SSDB.hclear with FF:url_ip\na= @udf SSDB.hclear with FF:url_acc\na= @udf SSDB.hclear with FF:acc_url\na= @udf SSDB.hclear with FF:ip_url\na= @udf SSDB.hclear with FF:app_time\na= @udf SSDB.hclear with FF:app_active\na= @udf SSDB.hclear with FF:app_active2\na= @udf SSDB.hclear with FF:api_time\na= @udf SSDB.hclear with FF:api_active\na= @udf SSDB.hclear with FF:api_active2\na= @udf SSDB.hclear with FF:ip_time\na= @udf SSDB.hclear with FF:ip_active\na= @udf SSDB.hclear with FF:ip_active2\na= @udf SSDB.hclear with FF:account_time\na= @udf SSDB.hclear with FF:account_active\na= @udf SSDB.hclear with FF:account_active2\n#删除文件数据和数据库\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/FF_url2.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/FF_ip2.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/FF_app2.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/FF_user3.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/merge.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/parm_iter.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/urlimit.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/dic.pkl\ns= @udf FBI.local_cmd with sudo rm -rf /data/xlink/api_mon.pkl\ns= @udf FBI.local_cmd with sudo rm -rf /data/xlink/app_mon.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /data/xlink/object_guess.pkl\ns = @udf FBI.local_cmd with sudo rm -rf /opt/openfbi/workspace/xlink\ns = @udf FBI.local_cmd with sudo rm -rf /opt/openfbi/workspace/dt_table\ns = @udf FBI.local_cmd with sudo rm -rf /opt/openfbi/workspace/hx\ns = @udf FBI.local_cmd with sudo rm -rf /opt/openfbi/workspace/sensitive\ns = load ckh by ckh with TRUNCATE TABLE agent_datalink\ns = load ckh by ckh with TRUNCATE TABLE api_abroad\ns = load ckh by ckh with TRUNCATE TABLE api_delay\ns = load ckh by ckh with TRUNCATE TABLE api_dns\ns = load ckh by ckh with TRUNCATE TABLE api_fileinfo\ns = load ckh by ckh with TRUNCATE TABLE api_ftp\ns = load ckh by ckh with TRUNCATE TABLE api_httpdata\ns = load ckh by ckh with TRUNCATE TABLE api_hx\ns = load ckh by ckh with TRUNCATE TABLE api_imap\ns = load ckh by ckh with TRUNCATE TABLE api_link\ns = load ckh by ckh with TRUNCATE TABLE api_link_data\ns = load ckh by ckh with TRUNCATE TABLE api_model\ns = load ckh by ckh with TRUNCATE TABLE api_modsecurity\ns = load ckh by ckh with TRUNCATE TABLE api_monitor\ns = load ckh by ckh with TRUNCATE TABLE api_pop3\ns = load ckh by ckh with TRUNCATE TABLE api_risk\ns = load ckh by ckh with TRUNCATE TABLE api_smb\ns = load ckh by ckh with TRUNCATE TABLE api_smtp\ns = load ckh by ckh with TRUNCATE TABLE api_tftp\ns = load ckh by ckh with TRUNCATE TABLE api_visit_day\ns = load ckh by ckh with TRUNCATE TABLE api_visit_hour\ns = load ckh by ckh with TRUNCATE TABLE datafilter\ns = load ckh by ckh with TRUNCATE TABLE compress\ns = load ckh by ckh with TRUNCATE TABLE datafilter_alarm\ns = load ckh by ckh with TRUNCATE TABLE date_alm\ns = load ckh by ckh with TRUNCATE TABLE filter_count\ns = load ckh by ckh with TRUNCATE TABLE ip_link\ns = load ckh by ckh with TRUNCATE TABLE ip_link_data\ns = load ckh by ckh with TRUNCATE TABLE merge_urls\ns = load ckh by ckh with TRUNCATE TABLE r_req_alm\ns = load ckh by ckh with TRUNCATE TABLE risk_api\ns = load ckh by ckh with TRUNCATE TABLE sen_http_count\ns = load ckh by ckh with TRUNCATE TABLE sensitive_data\ns = load ckh by ckh with TRUNCATE TABLE sensitive_data_alarm\ns = load ckh by ckh with TRUNCATE TABLE stat_req_alm\ns = load ckh by ckh with TRUNCATE TABLE api_business\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table user)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_app_new)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table aaa)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table sensitive_data)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_account_new)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table middle_biao)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table ip_label_library)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table account_label_library)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table report_app)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table risk_api)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table disk_resource)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table app_label_library)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table app_sx)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table owasp_report)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table monitor_data)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_ip_new)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table ip_datalink)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table Report_management)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_api_new)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table SNMP_test)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table api_daily)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table report_test)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_risk)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table rule_file)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table alarm_report)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table dgydelme)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table data_fbiuser)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table audit_statistics)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table app_datalink)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table api_label_library)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table agreement_report)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table api19_risk)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table hx_account)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table hx_api)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table hx_app)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table hx_ip)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table app_word)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table report)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table dbms_obj)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table dbms_user)\ns = @udf RS.exec_mysql_sql with (mysql1,truncate table fileinfo)\nrun sensitive_table.fbi\nrun zts_Audit_overview.fbi\nrun dsaw_overview.fbi\ns = @udf FBI.local_cmd with sleep 60s\ns = @udf FBI.local_cmd with init 6\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=25
		ptree['funs']=block_if_25
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[25]原语 if $date_num == "ABC@2020" with "a = @udf FBI.x_fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[factory_reset.fbi]执行第[236]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],236

#主函数结束,开始块函数

def block_if_25(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': '/opt/openfbi/fbi-bin/stop-fst.sh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[26]原语 a = @udf FBI.x_finder3_stop2 with /opt/openfbi/fbi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_aaai_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[28]原语 a = @udf FBI.x_finder3_stop2 with api_aaai_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'req_alm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[29]原语 a = @udf FBI.x_finder3_stop2 with req_alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'dns'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[30]原语 a = @udf FBI.x_finder3_stop2 with dns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[31]原语 a = @udf FBI.x_finder3_stop2 with api_visit 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_2_3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[32]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_2_3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_sen_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[33]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_sen_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_aaai_jso'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[34]原语 a = @udf FBI.x_finder3_stop2 with api_aaai_jso 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_mege'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[35]原语 a = @udf FBI.x_finder3_stop2 with api_mege 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[36]原语 a = @udf FBI.x_finder3_stop2 with api_owasp2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp4'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[37]原语 a = @udf FBI.x_finder3_stop2 with api_owasp4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_risk_event'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[38]原语 a = @udf FBI.x_finder3_stop2 with api_risk_event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_monitor_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[39]原语 a = @udf FBI.x_finder3_stop2 with api_monitor_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_delay_json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[40]原语 a = @udf FBI.x_finder3_stop2 with api_delay_json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[41]原语 a = @udf FBI.x_finder3_stop2 with api_proto 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_visit_hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[42]原语 a = @udf FBI.x_finder3_stop2 with api_visit_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'data_filter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[43]原语 a = @udf FBI.x_finder3_stop2 with data_filter 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'req_alarm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[44]原语 a = @udf FBI.x_finder3_stop2 with req_alarm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'ip_datalink_ckh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[45]原语 a = @udf FBI.x_finder3_stop2 with ip_datalink_ckh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'yuan_http'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[46]原语 a = @udf FBI.x_finder3_stop2 with yuan_http 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'object_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[47]原语 a = @udf FBI.x_finder3_stop2 with object_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_main_json2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[48]原语 a = @udf FBI.x_finder3_stop2 with api_main_json2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'main_process'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[49]原语 a = @udf FBI.x_finder3_stop2 with main_process 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp_1_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[50]原语 a = @udf FBI.x_finder3_stop2 with api_owasp_1_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp1_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[51]原语 a = @udf FBI.x_finder3_stop2 with api_owasp1_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'http_datafilter'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[52]原语 a = @udf FBI.x_finder3_stop2 with http_datafilter 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[53]原语 a = @udf FBI.x_finder3_stop2 with api_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'modsecurity'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[54]原语 a = @udf FBI.x_finder3_stop2 with modsecurity 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp4_model'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[55]原语 a = @udf FBI.x_finder3_stop2 with api_owasp4_model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_owasp4_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[56]原语 a = @udf FBI.x_finder3_stop2 with api_owasp4_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_business'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[57]原语 a = @udf FBI.x_finder3_stop2 with api_business 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:urldis'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[59]原语 a= @udf SSDB.hclear with FF:urldis 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:url2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[60]原语 a= @udf SSDB.hclear with FF:url2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:url3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[61]原语 a= @udf SSDB.hclear with FF:url3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[62]原语 a= @udf SSDB.hclear with FF:ip2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[63]原语 a= @udf SSDB.hclear with FF:app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:user3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[64]原语 a= @udf SSDB.hclear with FF:user3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:alert2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[65]原语 a= @udf SSDB.hclear with FF:alert2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:urll'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[66]原语 a= @udf SSDB.hclear with FF:urll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:urll2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[67]原语 a= @udf SSDB.hclear with FF:urll2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app_js'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[68]原语 a= @udf SSDB.hclear with FF:app_js 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:api_js'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[69]原语 a= @udf SSDB.hclear with FF:api_js 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:rule_file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[70]原语 a= @udf SSDB.hclear with FF:rule_file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'api_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[71]原语 a= @udf SSDB.hclear with api_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'api_merge1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[72]原语 a= @udf SSDB.hclear with api_merge1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'app_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[73]原语 a= @udf SSDB.hclear with app_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:y_url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[74]原语 a= @udf SSDB.hclear with FF:y_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app_datalink'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[75]原语 a= @udf SSDB.hclear with FF:app_datalink 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip_datalink'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[76]原语 a= @udf SSDB.hclear with FF:ip_datalink 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:acc_ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[77]原语 a= @udf SSDB.hclear with FF:acc_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:url_ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[78]原语 a= @udf SSDB.hclear with FF:url_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:url_acc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[79]原语 a= @udf SSDB.hclear with FF:url_acc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:acc_url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[80]原语 a= @udf SSDB.hclear with FF:acc_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip_url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[81]原语 a= @udf SSDB.hclear with FF:ip_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[82]原语 a= @udf SSDB.hclear with FF:app_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[83]原语 a= @udf SSDB.hclear with FF:app_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:app_active2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[84]原语 a= @udf SSDB.hclear with FF:app_active2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:api_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[85]原语 a= @udf SSDB.hclear with FF:api_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:api_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[86]原语 a= @udf SSDB.hclear with FF:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:api_active2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[87]原语 a= @udf SSDB.hclear with FF:api_active2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[88]原语 a= @udf SSDB.hclear with FF:ip_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[89]原语 a= @udf SSDB.hclear with FF:ip_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:ip_active2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[90]原语 a= @udf SSDB.hclear with FF:ip_active2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:account_time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[91]原语 a= @udf SSDB.hclear with FF:account_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:account_active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[92]原语 a= @udf SSDB.hclear with FF:account_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'FF:account_active2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[93]原语 a= @udf SSDB.hclear with FF:account_active2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/FF_url2.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[95]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/FF_ip2.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[96]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/FF_app2.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[97]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/FF_user3.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[98]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/merge.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[99]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/parm_iter.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[100]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/urlimit.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[101]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/dic.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[102]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/api_mon.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[103]原语 s= @udf FBI.local_cmd with sudo rm -rf /data/xlink... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/app_mon.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[104]原语 s= @udf FBI.local_cmd with sudo rm -rf /data/xlink... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/xlink/object_guess.pkl'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[105]原语 s = @udf FBI.local_cmd with sudo rm -rf /data/xlin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /opt/openfbi/workspace/xlink'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[106]原语 s = @udf FBI.local_cmd with sudo rm -rf /opt/openf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /opt/openfbi/workspace/dt_table'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[107]原语 s = @udf FBI.local_cmd with sudo rm -rf /opt/openf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /opt/openfbi/workspace/hx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[108]原语 s = @udf FBI.local_cmd with sudo rm -rf /opt/openf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /opt/openfbi/workspace/sensitive'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[109]原语 s = @udf FBI.local_cmd with sudo rm -rf /opt/openf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE agent_datalink'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[110]原语 s = load ckh by ckh with TRUNCATE TABLE agent_data... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_abroad'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[111]原语 s = load ckh by ckh with TRUNCATE TABLE api_abroad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_delay'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[112]原语 s = load ckh by ckh with TRUNCATE TABLE api_delay 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_dns'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[113]原语 s = load ckh by ckh with TRUNCATE TABLE api_dns 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[114]原语 s = load ckh by ckh with TRUNCATE TABLE api_filein... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_ftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[115]原语 s = load ckh by ckh with TRUNCATE TABLE api_ftp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_httpdata'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[116]原语 s = load ckh by ckh with TRUNCATE TABLE api_httpda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[117]原语 s = load ckh by ckh with TRUNCATE TABLE api_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_imap'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[118]原语 s = load ckh by ckh with TRUNCATE TABLE api_imap 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_link'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[119]原语 s = load ckh by ckh with TRUNCATE TABLE api_link 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[120]原语 s = load ckh by ckh with TRUNCATE TABLE api_link_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_model'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[121]原语 s = load ckh by ckh with TRUNCATE TABLE api_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_modsecurity'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[122]原语 s = load ckh by ckh with TRUNCATE TABLE api_modsec... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[123]原语 s = load ckh by ckh with TRUNCATE TABLE api_monito... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_pop3'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[124]原语 s = load ckh by ckh with TRUNCATE TABLE api_pop3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[125]原语 s = load ckh by ckh with TRUNCATE TABLE api_risk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_smb'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[126]原语 s = load ckh by ckh with TRUNCATE TABLE api_smb 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_smtp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[127]原语 s = load ckh by ckh with TRUNCATE TABLE api_smtp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_tftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[128]原语 s = load ckh by ckh with TRUNCATE TABLE api_tftp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_visit_day'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[129]原语 s = load ckh by ckh with TRUNCATE TABLE api_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[130]原语 s = load ckh by ckh with TRUNCATE TABLE api_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE datafilter'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[131]原语 s = load ckh by ckh with TRUNCATE TABLE datafilter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE compress'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[132]原语 s = load ckh by ckh with TRUNCATE TABLE compress 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE datafilter_alarm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[133]原语 s = load ckh by ckh with TRUNCATE TABLE datafilter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE date_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[134]原语 s = load ckh by ckh with TRUNCATE TABLE date_alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE filter_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[135]原语 s = load ckh by ckh with TRUNCATE TABLE filter_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE ip_link'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[136]原语 s = load ckh by ckh with TRUNCATE TABLE ip_link 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE ip_link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[137]原语 s = load ckh by ckh with TRUNCATE TABLE ip_link_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE merge_urls'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[138]原语 s = load ckh by ckh with TRUNCATE TABLE merge_urls... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE r_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[139]原语 s = load ckh by ckh with TRUNCATE TABLE r_req_alm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE risk_api'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[140]原语 s = load ckh by ckh with TRUNCATE TABLE risk_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE sen_http_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[141]原语 s = load ckh by ckh with TRUNCATE TABLE sen_http_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE sensitive_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[142]原语 s = load ckh by ckh with TRUNCATE TABLE sensitive_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE sensitive_data_alarm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[143]原语 s = load ckh by ckh with TRUNCATE TABLE sensitive_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE stat_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[144]原语 s = load ckh by ckh with TRUNCATE TABLE stat_req_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'TRUNCATE TABLE api_business'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[145]原语 s = load ckh by ckh with TRUNCATE TABLE api_busine... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[146]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[147]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table aaa'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[148]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sensitive_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[149]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_account_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[150]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table middle_biao'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[151]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table ip_label_library'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[152]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table account_label_library'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[153]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table report_app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[154]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table risk_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[155]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table disk_resource'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[156]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table app_label_library'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[157]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table app_sx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[158]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table owasp_report'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[159]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table monitor_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[160]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[161]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table ip_datalink'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[162]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table Report_management'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[163]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[164]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table SNMP_test'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[165]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table api_daily'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[166]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table report_test'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[167]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_risk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[168]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table rule_file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[169]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table alarm_report'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[170]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table dgydelme'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[171]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table data_fbiuser'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[172]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table audit_statistics'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[173]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table app_datalink'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[174]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table api_label_library'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[175]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table agreement_report'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[176]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table api19_risk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[177]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table hx_account'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[178]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table hx_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[179]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table hx_app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[180]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table hx_ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[181]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table app_word'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[182]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table report'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[183]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[184]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[185]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table fileinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[186]原语 s = @udf RS.exec_mysql_sql with (mysql1,truncate t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[第25行if语句中]执行第[187]原语 run sensitive_table.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'zts_Audit_overview.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[188]原语 run zts_Audit_overview.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第25行if语句中]执行第[189]原语 run dsaw_overview.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sleep 60s'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[190]原语 s = @udf FBI.local_cmd with sleep 60s 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'init 6'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[191]原语 s = @udf FBI.local_cmd with init 6 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_25

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



