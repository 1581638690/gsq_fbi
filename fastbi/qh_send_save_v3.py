#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_send_save
#datetime: 2024-08-30T16:10:56.155790
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
		add_the_error('[qh_send_save.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_send as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[16]原语 zz = load ssdb by ssdb0 with qh_send as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'syslog', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_o"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[17]原语 syslog = jaas zz by zz["syslog_o"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'kafka', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["kafka_o"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[18]原语 kafka = jaas zz by zz["kafka_o"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[19]原语 SDK = jaas zz by zz["SDK"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$SDK == "1"', 'with': '""\nSDK_IP = jaas zz by zz["SDK_IP"] as sdf\nSDK_port = jaas zz by zz["SDK_port"] as sdf\nSDK_ip_or_id = jaas zz by zz["SDK_ip_or_id"] as sdf\nSOC_ip = jaas zz by zz["SOC_ip"] as sdf\nSOC_port = jaas zz by zz["SOC_port"] as sdf\nSDK_IP= @sdf sys_str with ($SDK_IP,[1:-1])\nSDK_port= @sdf sys_str with ($SDK_port,[1:-1])\nSDK_ip_or_id= @sdf sys_str with ($SDK_ip_or_id,[1:-1])\nSOC_ip = @sdf sys_str with ($SOC_ip,[1:-1])\nSOC_port = @sdf sys_str with ($SOC_port,[1:-1])\ndf1 = @udf udf0.new_df\ndf1 = add a by 1\ndf1 = @udf df1 by udf0.df_append with ($SDK_ip_or_id)\nassert df1 by df.iloc[0,0] != "" as alert with SDK认证IP或ID不能为空\ndf1 = @udf df1 by udf0.df_append with ($SDK_IP)\nassert df1 by df.iloc[1,0] != "" as alert with SDKIP不能为空\ndf1 = @udf df1 by udf0.df_append with ($SDK_port)\nassert df1 by df.iloc[2,0] != "" as alert with SDK端口不能为空\ndf1 = @udf df1 by udf0.df_append with ($SOC_ip)\nassert df1 by df.iloc[3,0] != "" as alert with SOC平台IP不能为空\ndf1 = @udf df1 by udf0.df_append with ($SDK_port)\nassert df1 by df.iloc[4,0] != "" as alert with SOC平台端口不能为空\nassert not_have_error() as exit with 已退出\nrun qh_sdk.fbi\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=21
		ptree['funs']=block_if_21
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[21]原语 if $SDK == "1" with "SDK_IP = jaas zz by zz["SDK_I... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$syslog == "0"', 'with': '""\na = @udf FBI.x_finder3_stop2 with api_2syslog\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=47
		ptree['funs']=block_if_47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[47]原语 if $syslog == "0" with "a = @udf FBI.x_finder3_sto... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$kafka == "0"', 'with': '""\na = @udf FBI.x_finder3_stop2 with api_2kafka\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=50
		ptree['funs']=block_if_50
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[50]原语 if $kafka == "0" with "a = @udf FBI.x_finder3_stop... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$syslog == "1"', 'with': '""\nsip = jaas zz by zz["syslog_ip"] as sdf\nsport = jaas zz by zz["syslog_port"] as sdf\nsip = @sdf sys_str with ($sip,[1:-1])\nsport= @sdf sys_str with ($sport,[1:-1])\ndf1 = @udf udf0.new_df\ndf1 = add a by 1\ndf1 = @udf df1 by udf0.df_append with ($sip)\nassert df1 by df.iloc[0,0] != "" as alert with syslogIP不能为空\ndf1 = @udf df1 by udf0.df_append with ($sport)\nassert df1 by df.iloc[1,0] != "" as alert with syslog端口不能为空\nassert not_have_error() as exit with 已退出\na = @udf FBI.x_finder3_stop2 with api_2syslog\na = @udf FBI.x_finder3_start with api_2syslog\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=53
		ptree['funs']=block_if_53
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[53]原语 if $syslog == "1" with "sip = jaas zz by zz["syslo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$kafka == "1"', 'with': '""\nkip = jaas zz by zz["kafka_ip"] as sdf\nkport = jaas zz by zz["kafka_port"] as sdf\nkip = @sdf sys_str with ($kip,[1:-1])\nkport= @sdf sys_str with ($kport,[1:-1])\ndf1 = @udf udf0.new_df\ndf1 = add a by 1\ndf1 = @udf df1 by udf0.df_append with ($kip)\nassert df1 by df.iloc[0,0] != "" as alert with kafkaIP不能为空\ndf1 = @udf df1 by udf0.df_append with ($kport)\nassert df1 by df.iloc[1,0] != "" as alert with kafka端口不能为空\nassert not_have_error() as exit with 已退出\na = @udf FBI.x_finder3_stop2 with api_2kafka\na = @udf FBI.x_finder3_start with api_2kafka\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=68
		ptree['funs']=block_if_68
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[68]原语 if $kafka == "1" with "kip = jaas zz by zz["kafka_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_send_save.fbi]执行第[85]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],85

#主函数结束,开始块函数

def block_if_21(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_IP', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_IP"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[22]原语 SDK_IP = jaas zz by zz["SDK_IP"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_port', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[23]原语 SDK_port = jaas zz by zz["SDK_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SDK_ip_or_id', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_ip_or_id"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[24]原语 SDK_ip_or_id = jaas zz by zz["SDK_ip_or_id"] as sd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SOC_ip', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SOC_ip"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[25]原语 SOC_ip = jaas zz by zz["SOC_ip"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'SOC_port', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SOC_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[26]原语 SOC_port = jaas zz by zz["SOC_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第21行if语句中]执行第[27]原语 SDK_IP= @sdf sys_str with ($SDK_IP,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SDK_port', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SDK_port,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[28]原语 SDK_port= @sdf sys_str with ($SDK_port,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第21行if语句中]执行第[29]原语 SDK_ip_or_id= @sdf sys_str with ($SDK_ip_or_id,[1:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[第21行if语句中]执行第[30]原语 SOC_ip = @sdf sys_str with ($SOC_ip,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'SOC_port', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SOC_port,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[31]原语 SOC_port = @sdf sys_str with ($SOC_port,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[32]原语 df1 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'a', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[33]原语 df1 = add a by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$SDK_ip_or_id'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[34]原语 df1 = @udf df1 by udf0.df_append with ($SDK_ip_or_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[0,0] != ""', 'as': 'alert', 'with': 'SDK认证IP或ID不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[35]原语 assert df1 by df.iloc[0,0] != "" as alert with SDK... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$SDK_IP'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[36]原语 df1 = @udf df1 by udf0.df_append with ($SDK_IP) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[1,0] != ""', 'as': 'alert', 'with': 'SDKIP不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[37]原语 assert df1 by df.iloc[1,0] != "" as alert with SDK... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$SDK_port'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[38]原语 df1 = @udf df1 by udf0.df_append with ($SDK_port) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[2,0] != ""', 'as': 'alert', 'with': 'SDK端口不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[39]原语 assert df1 by df.iloc[2,0] != "" as alert with SDK... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$SOC_ip'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[40]原语 df1 = @udf df1 by udf0.df_append with ($SOC_ip) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[3,0] != ""', 'as': 'alert', 'with': 'SOC平台IP不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[41]原语 assert df1 by df.iloc[3,0] != "" as alert with SOC... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$SDK_port'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[42]原语 df1 = @udf df1 by udf0.df_append with ($SDK_port) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[4,0] != ""', 'as': 'alert', 'with': 'SOC平台端口不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[43]原语 assert df1 by df.iloc[4,0] != "" as alert with SOC... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'exit', 'with': '已退出'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[第21行if语句中]执行第[44]原语 assert not_have_error() a... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[44]原语 assert not_have_error() as exit with 已退出 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'qh_sdk.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第21行if语句中]执行第[45]原语 run qh_sdk.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_21

def block_if_47(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_2syslog'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第47行if语句中]执行第[48]原语 a = @udf FBI.x_finder3_stop2 with api_2syslog 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_47

def block_if_50(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_2kafka'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第50行if语句中]执行第[51]原语 a = @udf FBI.x_finder3_stop2 with api_2kafka 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_50

def block_if_53(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'sip', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_ip"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[54]原语 sip = jaas zz by zz["syslog_ip"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'sport', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[55]原语 sport = jaas zz by zz["syslog_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'sip', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$sip,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[56]原语 sip = @sdf sys_str with ($sip,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'sport', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$sport,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[57]原语 sport= @sdf sys_str with ($sport,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[58]原语 df1 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'a', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[59]原语 df1 = add a by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$sip'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[60]原语 df1 = @udf df1 by udf0.df_append with ($sip) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[0,0] != ""', 'as': 'alert', 'with': 'syslogIP不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[61]原语 assert df1 by df.iloc[0,0] != "" as alert with sys... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$sport'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[62]原语 df1 = @udf df1 by udf0.df_append with ($sport) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[1,0] != ""', 'as': 'alert', 'with': 'syslog端口不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[63]原语 assert df1 by df.iloc[1,0] != "" as alert with sys... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'exit', 'with': '已退出'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[第53行if语句中]执行第[64]原语 assert not_have_error() a... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[64]原语 assert not_have_error() as exit with 已退出 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_2syslog'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[65]原语 a = @udf FBI.x_finder3_stop2 with api_2syslog 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_2syslog'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[66]原语 a = @udf FBI.x_finder3_start with api_2syslog 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_53

def block_if_68(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'kip', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["kafka_ip"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[69]原语 kip = jaas zz by zz["kafka_ip"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'kport', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["kafka_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[70]原语 kport = jaas zz by zz["kafka_port"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'kip', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$kip,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[71]原语 kip = @sdf sys_str with ($kip,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'kport', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$kport,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[72]原语 kport= @sdf sys_str with ($kport,[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[73]原语 df1 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'a', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[74]原语 df1 = add a by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$kip'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[75]原语 df1 = @udf df1 by udf0.df_append with ($kip) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[0,0] != ""', 'as': 'alert', 'with': 'kafkaIP不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[76]原语 assert df1 by df.iloc[0,0] != "" as alert with kaf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$kport'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[77]原语 df1 = @udf df1 by udf0.df_append with ($kport) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'df1', 'by': 'df.iloc[1,0] != ""', 'as': 'alert', 'with': 'kafka端口不能为空'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[78]原语 assert df1 by df.iloc[1,0] != "" as alert with kaf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'exit', 'with': '已退出'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[第68行if语句中]执行第[79]原语 assert not_have_error() a... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[79]原语 assert not_have_error() as exit with 已退出 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_stop2', 'with': 'api_2kafka'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[80]原语 a = @udf FBI.x_finder3_stop2 with api_2kafka 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.x_finder3_start', 'with': 'api_2kafka'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[81]原语 a = @udf FBI.x_finder3_start with api_2kafka 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_68

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



