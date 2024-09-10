#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_sdk
#datetime: 2024-08-30T16:10:55.949181
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
		add_the_error('[qh_sdk.fbi]执行第[8]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_send as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[10]原语 zz = load ssdb by ssdb0 with qh_send as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[11]原语 SDK = jaas zz by zz["SDK"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$SDK == "1"', 'with': '""\nSDK_protocol = jaas zz by zz["SDK_protocol"] as sdf\nSDK_IP = jaas zz by zz["SDK_IP"] as sdf\nSDK_port = jaas zz by zz["SDK_port"] as sdf\nSDK_ip_or_id = jaas zz by zz["SDK_ip_or_id"] as sdf\nSOC_ip = jaas zz by zz["SOC_ip"] as sdf\nSOC_port = jaas zz by zz["SOC_port"] as sdf\n\nSDK_protocol = @sdf sys_str with ($SDK_protocol,[1:-1])\nSDK_IP= @sdf sys_str with ($SDK_IP,[1:-1])\nSDK_ip_or_id= @sdf sys_str with ($SDK_ip_or_id,[1:-1])\nSOC_ip = @sdf sys_str with ($SOC_ip,[1:-1])\n\ndf1 = @udf udf0.new_df\ndf1 = add a by 1\ndf1 = @udf df1 by udf0.df_append with (utf-8)\ndf2 = @udf df1 by net2.cert with $SDK_ip_or_id,$SDK_IP,$SDK_port,$SDK_protocol,$SOC_ip,$SOC_port\ndf3 = @udf df2 by FBI.df2json\n"', 'else': '"\ndf2 = @udf udf0.new_df\ndf2 = add a by 0\ndf2 = @udf df2 by udf0.df_append with (0)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=12
		ptree['funs']=block_if_12
		ptree['funs2']=block_if_else_12
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[12]原语 if $SDK == "1" with "SDK_protocol = jaas zz by zz[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'eval', 'eval': 'df2', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[37]原语 s = eval df2 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$s == "1"', 'with': '""\nstore df3 to ssdb with cert:TorF\n"', 'else': '"\ndf4 = @udf udf0.new_df\ndf4 = add a by 0\ndf4 = @udf df4 by udf0.df_append with (0)\nstore df4 to ssdb with cert:TorF\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=38
		ptree['funs']=block_if_38
		ptree['funs2']=block_if_else_38
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[38]原语 if $s == "1" with "store df3 to ssdb with cert:Tor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_sdk.fbi]执行第[47]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],50

#主函数结束,开始块函数

def block_if_12(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_protocol', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_protocol"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[13]原语 SDK_protocol = jaas zz by zz["SDK_protocol"] as sd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_IP', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_IP"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[14]原语 SDK_IP = jaas zz by zz["SDK_IP"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_port', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[15]原语 SDK_port = jaas zz by zz["SDK_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_ip_or_id', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_ip_or_id"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[16]原语 SDK_ip_or_id = jaas zz by zz["SDK_ip_or_id"] as sd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SOC_ip', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SOC_ip"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[17]原语 SOC_ip = jaas zz by zz["SOC_ip"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SOC_port', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SOC_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[18]原语 SOC_port = jaas zz by zz["SOC_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SDK_protocol', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SDK_protocol,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[20]原语 SDK_protocol = @sdf sys_str with ($SDK_protocol,[1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SDK_IP', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SDK_IP,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[21]原语 SDK_IP= @sdf sys_str with ($SDK_IP,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SDK_ip_or_id', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SDK_ip_or_id,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[22]原语 SDK_ip_or_id= @sdf sys_str with ($SDK_ip_or_id,[1:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SOC_ip', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SOC_ip,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[23]原语 SOC_ip = @sdf sys_str with ($SOC_ip,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[25]原语 df1 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'a', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[26]原语 df1 = add a by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': 'utf-8'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[27]原语 df1 = @udf df1 by udf0.df_append with (utf-8) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df1', 'by': 'net2.cert', 'with': '$SDK_ip_or_id,$SDK_IP,$SDK_port,$SDK_protocol,$SOC_ip,$SOC_port'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[28]原语 df2 = @udf df1 by net2.cert with $SDK_ip_or_id,$SD... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df2', 'by': 'FBI.df2json'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if语句中]执行第[29]原语 df3 = @udf df2 by FBI.df2json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_12

def block_if_else_12(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if_else语句中]执行第[12]原语 df2 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df2', 'Action': 'add', 'add': 'a', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第12行if_else语句中]执行第[13]原语 df2 = add a by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第12行if_else语句中]执行第[14]原语 df2 = @udf df2 by udf0.df_append with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_12

def block_if_38(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df3', 'to': 'ssdb', 'with': 'cert:TorF'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第38行if语句中]执行第[39]原语 store df3 to ssdb with cert:TorF 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_38

def block_if_else_38(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第38行if_else语句中]执行第[38]原语 df4 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df4', 'Action': 'add', 'add': 'a', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第38行if_else语句中]执行第[39]原语 df4 = add a by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4', 'Action': '@udf', '@udf': 'df4', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第38行if_else语句中]执行第[40]原语 df4 = @udf df4 by udf0.df_append with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df4', 'to': 'ssdb', 'with': 'cert:TorF'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第38行if_else语句中]执行第[41]原语 store df4 to ssdb with cert:TorF 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_38

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



