#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_new_data1/batch_imp
#datetime: 2024-08-30T16:10:58.979616
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
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[14]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datas', 'Action': 'load', 'load': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[16]原语 datas = load csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '请求数据标签,返回数据标签'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[18]原语 datas = loc datas drop 请求数据标签,返回数据标签 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"接口":"url","uri":"api","协议版本":"protocol","首次发现时间":"first_time","接口名":"name","应用名":"app","请求类型":"method","资源类型":"data_type","风险标签":"risk_label","访问数量":"visits_num","访问IP数量":"srcip_num","访问流量":"visits_flow","敏感标签":"sensitive_label","部署数量":"dstip_num","目的IP":"dstip","目的端口":"dstport","最后修改时间":"last_time","审计状态":"api_status","接口标签":"scope","应用类型":"app_type","访问账号数量":"account_num","合并接口名":"url_merges","子接口":"url_sum","合并状态":"merge_state","参数":"parameter","风险标签.1":"risk_label_value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[19]原语 rename datas as ("接口":"url","uri":"api","协议版本":"pr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"1" if x ==\'敏感\' else "0"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[20]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.api_status', 'Action': 'lambda', 'lambda': 'api_status', 'by': 'x:"1" if x ==\'已审计\' else "0"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[21]原语 datas.api_status = lambda api_status by x:"1" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:1 if x =="内部应用" else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[22]原语 datas.app_type = lambda app_type by x:1 if x =="内部... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[24]原语 api_type = load ssdb by ssdb0 with dd:API-api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_type', 'Action': 'add', 'add': 'id', 'by': 'api_type.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[25]原语 api_type  = add id by api_type.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_type', 'as': '"value":"接口类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[26]原语 rename api_type as ("value":"接口类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,api_type', 'by': '接口类型,接口类型', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[27]原语 datas = join datas,api_type by 接口类型,接口类型 with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '接口类型'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[28]原语 datas = loc datas drop 接口类型 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"id":"api_type"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[29]原语 rename datas as ("id":"api_type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'risk_level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-risk_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[31]原语 risk_level = load ssdb by ssdb0 with dd:API-risk_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk_level', 'Action': 'add', 'add': 'id', 'by': 'risk_level.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[32]原语 risk_level  = add id by risk_level.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk_level', 'as': '"value":"风险等级"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[33]原语 rename risk_level as ("value":"风险等级") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,risk_level', 'by': '风险等级,风险等级', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[34]原语 datas = join datas,risk_level by 风险等级,风险等级 with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '风险等级'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[35]原语 datas = loc datas drop 风险等级 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"id":"risk_level"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[36]原语 rename datas as ("id":"risk_level") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[38]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'active', 'Action': 'add', 'add': 'id', 'by': 'active.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[39]原语 active  = add id by active.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'active', 'as': '"value":"活跃状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[40]原语 rename active as ("value":"活跃状态") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,active', 'by': '活跃状态,活跃状态', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[41]原语 datas = join datas,active by 活跃状态,活跃状态 with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '活跃状态'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[42]原语 datas = loc datas drop 活跃状态 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"id":"active"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[43]原语 rename datas as ("id":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'auth_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-auth_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[45]原语 auth_type = load ssdb by ssdb0 with dd:API-auth_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'auth_type', 'Action': 'add', 'add': 'id', 'by': 'auth_type.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[46]原语 auth_type  = add id by auth_type.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'auth_type', 'as': '"value":"接口认证类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[47]原语 rename auth_type as ("value":"接口认证类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,auth_type', 'by': '接口认证类型,接口认证类型', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[48]原语 datas = join datas,auth_type by 接口认证类型,接口认证类型 with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '接口认证类型'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[49]原语 datas = loc datas drop 接口认证类型 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"id":"auth_type"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[50]原语 rename datas as ("id":"auth_type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[51]原语 datas = @udf datas by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[52]原语 datas = @udf datas by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'CRUD.save_object_mtable', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[54]原语 datas = @udf datas by CRUD.save_object_mtable with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '导入成功', 'with': '导入失败'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[58]原语 assert not_have_error() as alert to 导入成功 with 导入失败... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'datas', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[59]原语 push datas as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_imp.fbi]执行第[60]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],60

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



