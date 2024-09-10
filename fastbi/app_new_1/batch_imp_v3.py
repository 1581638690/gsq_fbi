#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_new_1/batch_imp
#datetime: 2024-08-30T16:10:56.524610
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
		add_the_error('[app_new_1/batch_imp.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datas', 'Action': 'load', 'load': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[19]原语 datas = load csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[20]原语 datas = @udf datas by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"应用IP/域名":"app","标题":"app_title","应用名称":"name","首次发现时间":"first_time","服务器信息":"server","访问数量":"visits_num","访问流量":"visits_flow","审计访问数量":"monitor_flow","接口数量":"api_num","审计接口数量":"imp_api_num","访问IP数量":"srcip_num","访问账号数量":"account_num","敏感标签":"sensitive_label","部署数量":"dstip_num","目的IP":"dstip","目的端口":"dstport","审计访问数量.1":"sj_num","最后修改时间":"last_time","审计状态":"app_status","应用标签":"scope","应用类型":"app_type","子应用":"app_sum","合并应用名":"app_merges","合并状态":"merge_state"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[21]原语 rename datas as ("应用IP/域名":"app","标题":"app_title",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"1" if x ==\'敏感\' else "0"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[23]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_status', 'Action': 'lambda', 'lambda': 'app_status', 'by': 'x:"1" if x ==\'已审计\' else "0"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[24]原语 datas.app_status = lambda app_status by x:"1" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:1 if x =="内部应用" else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[25]原语 datas.app_type = lambda app_type by x:1 if x =="内部... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sx', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_sx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[27]原语 sx = load ssdb by ssdb0 with dd:app_sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sx', 'Action': 'add', 'add': 'id', 'by': 'sx.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[28]原语 sx  = add id by sx.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sx', 'as': '"sysname":"关联应用","id":"sx"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[29]原语 rename sx as ("sysname":"关联应用","id":"sx") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,sx', 'by': '关联应用,关联应用', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[30]原语 datas = join datas,sx by 关联应用,关联应用 with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,关联应用'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[31]原语 datas = loc datas drop id,关联应用 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[32]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'active', 'Action': 'add', 'add': 'id', 'by': 'active.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[33]原语 active  = add id by active.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'active', 'as': '"value":"活跃状态","id":"active"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[34]原语 rename active as ("value":"活跃状态","id":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,active', 'by': '活跃状态,活跃状态', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[35]原语 datas = join datas,active by 活跃状态,活跃状态 with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': '活跃状态'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[36]原语 datas = loc datas drop 活跃状态 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datas.scope', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[37]原语 alter datas.scope as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datas.app_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[38]原语 alter datas.app_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datas.app_merges', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[39]原语 alter datas.app_merges as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[40]原语 datas = @udf datas by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[42]原语 datas = @udf datas by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'CRUD.save_object_mtable', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[44]原语 datas = @udf datas by CRUD.save_object_mtable with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '导入成功', 'with': '导入失败'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[48]原语 assert not_have_error() as alert to 导入成功 with 导入失败... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'datas', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[49]原语 push datas as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_imp.fbi]执行第[50]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],50

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



