#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api19_search
#datetime: 2024-08-30T16:10:56.212741
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
		add_the_error('[api19_search.fbi]执行第[4]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,api,app,dest_ip,dest_port,method,last_time,state,type from api19_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[7]原语 api19_risk = load db by mysql1 with select id,api,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_risk', 'Action': 'filter', 'filter': 'api19_risk', 'by': 'api like @api'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[8]原语 api19_risk = filter api19_risk by api like @api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select type1,weakness,possibility,influence,advise from api19_type where type1 = '@type'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[11]原语 api = load db by mysql1 with select type1,weakness... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'api', 'by': 'type1,weakness,possibility,influence,advise'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[15]原语 aa = loc api by type1,weakness,possibility,influen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'aa', 'as': 'aa_data'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[16]原语 push aa as aa_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'layout', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[19]原语 layout = @udf udf0.new_df with (key) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'layout', 'Action': '@udf', '@udf': 'layout', 'by': 'udf0.df_append', 'with': "'aa_data'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[20]原语 layout = @udf layout by udf0.df_append with ("aa_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'layout', 'as': 'bj_layout_data'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[21]原语 push layout as bj_layout_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api19_risk_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[24]原语 api19_risk_type = load ssdb by ssdb0 with dd:api19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk_type', 'Action': 'loc', 'loc': 'api19_risk_type', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[25]原语 api19_risk_type = loc api19_risk_type by index to ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api19_risk', 'Action': 'join', 'join': 'api19_risk,api19_risk_type', 'by': 'type,type'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[26]原语 api19_risk = join api19_risk,api19_risk_type by ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_risk', 'Action': 'filter', 'filter': 'api19_risk', 'by': "value == '@type'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[27]原语 api19_risk = filter api19_risk by value == "@type"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'id,api,app,dest_ip,dest_port,method,last_time,state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[29]原语 api19_risk = loc api19_risk by id,api,app,dest_ip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk_count', 'Action': 'eval', 'eval': 'api19_risk', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[30]原语 api19_risk_count = eval api19_risk by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'acount', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[31]原语 acount = @udf udf0.new_df with count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'acount', 'Action': '@udf', '@udf': 'acount', 'by': 'udf0.df_append', 'with': '$api19_risk_count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[32]原语 acount = @udf acount by udf0.df_append with ($api1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk', 'as': "'id':'_id','api':'接口','app':'应用','dest_ip':'部署IP','dest_port':'部署端口','method':'请求类型','last_time':'最新监测时间','state':'弱点状态','value':'弱点类型'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[33]原语 rename api19_risk as ("id":"_id","api":"接口","app":... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'api19_risk', 'as': 'api19_risk'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[35]原语 push api19_risk as api19_risk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'acount', 'as': 'api19_risk_count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[37]原语 push acount as api19_risk_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api19_search.fbi]执行第[42]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],42

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



