#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_risk_save
#datetime: 2024-08-30T16:10:54.677371
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
		add_the_error('[api_risk_save.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[21]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a._id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[22]原语 alter a._id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'id', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[24]原语 id = eval a by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,api,api_name,app,app_name,dest_ip,dest_port,method,length,first_time,last_time,type,more from api19_risk where id = '$id'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[25]原语 api = load db by mysql1 with select id,api,api_nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,api', 'by': '_id,id'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[26]原语 a = join a,api by _id,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'id,api,api_name,app,app_name,dest_ip,dest_port,method,length,first_time,last_time,type,more,弱点状态'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[27]原语 a = loc a by id,api,api_name,app,app_name,dest_ip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,11]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[28]原语 type = eval a by iloc[0,11] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'a', 'as': "'弱点状态':'state'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[29]原语 rename a as ("弱点状态":"state") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.first_time.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[30]原语 alter a.first_time.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[31]原语 a = loc a by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'b', 'Action': 'loc', 'loc': 'a', 'by': 'id,api,state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[32]原语 b = loc a by id,api,state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[33]原语 b = @udf b by CRUD.save_table with (mysql1,api19_r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('b',ptree)", 'as': 'alert', 'to': '保存成功！', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[35]原语 assert find_df("b",ptree) as  alert  to 保存成功！ with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id as _id,api,api_name,app,app_name,dest_ip,dest_port,method,length,first_time,last_time,state,type,more from api19_risk where type = '$type' order by last_time desc"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[39]原语 api19_risk = load db by mysql1 with select id as _... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt', 'Action': '@udf', '@udf': 'api19_risk', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[40]原语 tt = @udf api19_risk by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt', 'Action': 'filter', 'filter': 'tt', 'by': "type != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[41]原语 tt = filter tt by type != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'tt', 'Action': 'order', 'order': 'tt', 'by': 'last_time', 'with': 'desc limit 10000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[42]原语 tt = order tt by last_time with desc limit 10000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tt.first_time.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[43]原语 alter tt.first_time.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': '_id,api,app,dest_ip,dest_port,method,last_time,state,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[46]原语 tt = loc tt by _id,api,app,dest_ip,dest_port,metho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt', 'as': "'api':'接口','api_name':'接口名','app':'应用','app_name':'应用名','dest_ip':'部署IP','dest_port':'部署端口','method':'请求类型','length':'返回数据最大数据量','first_time':'首次发现时间','last_time':'最新监测时间','state':'弱点状态','type':'弱点类型','more':'详情'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[48]原语 rename tt as ("api":"接口","api_name":"接口名","app":"应... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': '_id,接口,应用,部署IP,部署端口,请求类型,最新监测时间,弱点状态'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[49]原语 tt = loc tt by _id,接口,应用,部署IP,部署端口,请求类型,最新监测时间,弱点状... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,api19_risk_@type,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[51]原语 b = load ssdb by ssdb0 query qclear,api19_risk_@ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tt', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api19_risk_@type', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[53]原语 store tt to ssdb by ssdb0 with api19_risk_@type as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_risk_save.fbi]执行第[59]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],59

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



