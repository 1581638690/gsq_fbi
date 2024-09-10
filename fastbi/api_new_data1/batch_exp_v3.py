#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_new_data1/batch_exp
#datetime: 2024-08-30T16:10:58.992133
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
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[22]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'v', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '@ids,replace("|",",")'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[24]原语 v = @sdf sys_str with (@ids,replace("|",",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ids1', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '@ids==""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[26]原语 ids1 = @sdf sys_eval with (@ids=="") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'cc', 'Action': 'if', 'if': '$ids1', 'with': '""\n#获取表单中的条件信息\ndatas = @udf udf0.new_df with id\na = load ssdb by ssdb0 with @data_key\n#保存\ndatas,c = @udf a by CRUD.query_table with (@link,@table)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=34
		ptree['funs']=block_if_34
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[34]原语 cc = if $ids1 with "#获取表单中的条件信息datas = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'a', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$ids1,"datas =@udf CRUD.load_mysql_sql with (@link,select * from @table where id in ($v))"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[41]原语 a = @sdf sys_unif_run with ($ids1,"datas =@udf CRU... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'gmt_create,gmt_modified,creator,owner'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[43]原语 datas = loc datas drop (gmt_create,gmt_modified,cr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"敏感" if x ==\'1\' else "非敏感"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[44]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.api_status', 'Action': 'lambda', 'lambda': 'api_status', 'by': 'x:"已审计" if x ==\'1\' else "未审计"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[45]原语 datas.api_status = lambda api_status by x:"已审计" if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:"内部应用" if x ==1 else "外部应用"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[46]原语 datas.app_type = lambda app_type by x:"内部应用" if x ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[48]原语 api_type = load ssdb by ssdb0 with dd:API-api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_type', 'Action': 'add', 'add': 'id', 'by': 'api_type.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[49]原语 api_type  = add id by api_type.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_type', 'as': '"value":"接口类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[50]原语 rename api_type as ("value":"接口类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.api_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[51]原语 datas = alter datas.api_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,api_type', 'by': 'api_type,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[52]原语 datas = join datas,api_type by api_type,id with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,api_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[53]原语 datas = loc datas drop id,api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'risk_level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-risk_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[55]原语 risk_level = load ssdb by ssdb0 with dd:API-risk_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk_level', 'Action': 'add', 'add': 'id', 'by': 'risk_level.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[56]原语 risk_level  = add id by risk_level.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk_level', 'as': '"value":"风险等级"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[57]原语 rename risk_level as ("value":"风险等级") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,risk_level', 'by': 'risk_level,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[58]原语 datas = join datas,risk_level by risk_level,id wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[59]原语 datas = loc datas drop id,risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[61]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'active', 'Action': 'add', 'add': 'id', 'by': 'active.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[62]原语 active  = add id by active.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'active', 'as': '"value":"活跃状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[63]原语 rename active as ("value":"活跃状态") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[64]原语 datas = alter datas.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,active', 'by': 'active,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[65]原语 datas = join datas,active by active,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[66]原语 datas = loc datas drop id,active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'req_label', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[68]原语 req_label = load ssdb by ssdb0 with dd:reqs_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'req_label', 'as': '"data":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[69]原语 rename req_label as ("data":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'req_label', 'Action': 'loc', 'loc': 'req_label', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[70]原语 req_label = loc req_label by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'req_label', 'Action': 'order', 'order': 'req_label', 'by': 'id', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[71]原语 req_label = order req_label by id with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'req_label', 'Action': 'alter', 'alter': 'req_label.id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[72]原语 req_label = alter req_label.id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.req_label', 'Action': 'lambda', 'lambda': 'req_label', 'by': 'x:x.replace("[","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[73]原语 datas.req_label = lambda req_label by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.req_label', 'Action': 'lambda', 'lambda': 'req_label', 'by': 'x:x.replace("]","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[74]原语 datas.req_label = lambda req_label by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.req_label', 'Action': 'lambda', 'lambda': 'req_label', 'by': 'x:x.replace(\'"\',"")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[75]原语 datas.req_label = lambda req_label by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas,req_label', 'by': 'DT.tag2dict', 'with': 'req_label'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[76]原语 datas = @udf datas,req_label by DT.tag2dict with r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"req_label":"请求数据标签"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[77]原语 rename datas as ("req_label":"请求数据标签") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'res_llabel', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[79]原语 res_llabel = load ssdb by ssdb0 with dd:reqs_label... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'res_llabel', 'as': '"data":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[80]原语 rename res_llabel as ("data":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'res_llabel', 'Action': 'loc', 'loc': 'res_llabel', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[81]原语 res_llabel = loc res_llabel by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'res_llabel', 'Action': 'order', 'order': 'res_llabel', 'by': 'id', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[82]原语 res_llabel = order res_llabel by id with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'res_llabel', 'Action': 'alter', 'alter': 'res_llabel.id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[83]原语 res_llabel = alter res_llabel.id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.res_llabel', 'Action': 'lambda', 'lambda': 'res_llabel', 'by': 'x:x.replace("[","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[84]原语 datas.res_llabel = lambda res_llabel by x:x.replac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.res_llabel', 'Action': 'lambda', 'lambda': 'res_llabel', 'by': 'x:x.replace("]","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[85]原语 datas.res_llabel = lambda res_llabel by x:x.replac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.res_llabel', 'Action': 'lambda', 'lambda': 'res_llabel', 'by': 'x:x.replace(\'"\',"")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[86]原语 datas.res_llabel = lambda res_llabel by x:x.replac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas,res_llabel', 'by': 'DT.tag2dict', 'with': 'res_llabel'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[87]原语 datas = @udf datas,res_llabel by DT.tag2dict with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"res_llabel":"返回数据标签"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[88]原语 rename datas as ("res_llabel":"返回数据标签") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'auth_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-auth_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[91]原语 auth_type = load ssdb by ssdb0 with dd:API-auth_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'auth_type', 'Action': 'add', 'add': 'id', 'by': 'auth_type.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[92]原语 auth_type  = add id by auth_type.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'auth_type', 'as': '"value":"接口认证类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[93]原语 rename auth_type as ("value":"接口认证类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.auth_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[94]原语 datas = alter datas.auth_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,auth_type', 'by': 'auth_type,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[95]原语 datas = join datas,auth_type by auth_type,id with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,auth_type,id_x,id_y'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[96]原语 datas = loc datas drop id,auth_type,id_x,id_y 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"url":"接口","api":"uri","protocol":"协议版本","first_time":"首次发现时间","name":"接口名","app":"应用名","method":"请求类型","data_type":"资源类型","risk_label":"风险标签","visits_num":"访问数量","srcip_num":"访问IP数量","visits_flow":"访问流量","sensitive_label":"敏感标签","dstip_num":"部署数量","dstip":"目的IP","dstport":"目的端口","last_time":"最后修改时间","api_status":"审计状态","scope":"接口标签","app_type":"应用类型","account_num":"访问账号数量","url_merges":"合并接口名","url_sum":"子接口","merge_state":"合并状态","parameter":"参数","risk_label_value":"风险标签"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[98]原语 rename datas as ("url":"接口","api":"uri","protocol"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datas', 'to': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[99]原语 store datas to csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_new_data1/batch_exp.fbi]执行第[101]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],101

#主函数结束,开始块函数

def block_if_34(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第34行if语句中]执行第[36]原语 datas = @udf udf0.new_df with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第34行if语句中]执行第[37]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第34行if语句中]执行第[39]原语 datas,c = @udf a by CRUD.query_table with (@link,@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_34

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



