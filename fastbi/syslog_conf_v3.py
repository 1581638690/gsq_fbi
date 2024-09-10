#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: syslog_conf
#datetime: 2024-08-30T16:10:53.659171
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_send as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[17]原语 a = load ssdb by ssdb0 with qh_send as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 's', 'Action': '@sdf', '@sdf': '@send', 'by': 'sys_str2', 'with': 'replace("|",",")'}
	ptree['@sdf'] = replace_ps(ptree['@sdf'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[18]原语 s = @sdf @send by sys_str2 with replace("|",",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["sends"]="$s"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[20]原语 jaas a by a["sends"]="$s" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["syslog_proto"]="@proto"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[21]原语 jaas a by a["syslog_proto"]="@proto" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["syslog_ip"]="@ip"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[22]原语 jaas a by a["syslog_ip"]="@ip" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["syslog_port"]="@port"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[23]原语 jaas a by a["syslog_port"]="@port" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK"]="@SDK"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[24]原语 jaas a by a["SDK"]="@SDK" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK_enc"]="@SDKenc"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[25]原语 jaas a by a["SDK_enc"]="@SDKenc" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK_ip_or_id"]="@SDK_ip_or_id"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[26]原语 jaas a by a["SDK_ip_or_id"]="@SDK_ip_or_id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK_IP"]="@SDK_ip"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[27]原语 jaas a by a["SDK_IP"]="@SDK_ip" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK_port"]="@SDK_port"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[28]原语 jaas a by a["SDK_port"]="@SDK_port" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SDK_protocol"]="@SDK_protocol"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[29]原语 jaas a by a["SDK_protocol"]="@SDK_protocol" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SOC_ip"]="@SOC_ip"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[30]原语 jaas a by a["SOC_ip"]="@SOC_ip" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'a', 'by': 'a["SOC_port"]="@SOC_port"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[31]原语 jaas a by a["SOC_port"]="@SOC_port" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'qh_send'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[syslog_conf.fbi]执行第[32]原语 store a to ssdb with qh_send 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],33

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



