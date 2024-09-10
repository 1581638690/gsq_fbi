#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api19_tree
#datetime: 2024-08-30T16:10:54.009778
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
		add_the_error('[api19_tree.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id as _id,api,api_name,app,app_name,dest_ip,dest_port,method,length,first_time,last_time,state,type from api19_risk order by last_time desc'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[16]原语 api19_risk = load db by mysql1 with select id as _... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk', 'by': '_id:int,api:str,api_name:str,app:str,app_name:str,dest_ip:str,dest_port:int,method:str,length:int,first_time:str,last_time:str,state:str,type:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[17]原语 alter api19_risk by _id:int,api:str,api_name:str,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_risk', 'Action': '@udf', '@udf': 'api19_risk', 'by': 'udf0.df_fillna_cols', 'with': "api_name:'',app:'',app_name:'',dest_ip:'',dest_port:0,method:'',length:0,first_time:'',last_time:'',state:'',type:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[18]原语 api19_risk = @udf api19_risk by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_risk', 'Action': 'filter', 'filter': 'api19_risk', 'by': "type != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[19]原语 api19_risk = filter api19_risk by type != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type2', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct type2 as tree_name from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[21]原语 type2 = load db by mysql1 with select distinct typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'type2', 'by': 'tree_name:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[22]原语 alter type2 by tree_name:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type2', 'Action': 'add', 'add': 'tre_level', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[23]原语 type2 = add tre_level by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type2', 'Action': 'add', 'add': 'parent_id', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[24]原语 type2 = add parent_id by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type,type1 as tree_name,type2,level from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[25]原语 type1 = load db by mysql1 with select type,type1 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'type1', 'by': 'type:str,tree_name:str,type2:str,level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[26]原语 alter type1 by type:str,tree_name:str,type2:str,le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type_num', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[27]原语 type_num = loc api19_risk by type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'type_num', 'Action': 'group', 'group': 'type_num', 'by': 'type', 'agg': 'type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[28]原语 type_num = group type_num by type agg type:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type_num', 'Action': '@udf', '@udf': 'type_num', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[29]原语 type_num = @udf type_num by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type_num', 'as': "'type_count':'tree_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[30]原语 rename type_num as ("type_count":"tree_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'type1', 'Action': 'join', 'join': 'type1,type_num', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[32]原语 type1 = join type1,type_num by type,type with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type1', 'Action': '@udf', '@udf': 'type1', 'by': 'udf0.df_fillna_cols', 'with': 'tree_num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[33]原语 type1 = @udf type1 by udf0.df_fillna_cols with tre... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type1', 'Action': 'add', 'add': 'tre_level', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[34]原语 type1 = add tre_level by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type1', 'Action': 'add', 'add': 'parent_id', 'by': '"a1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[35]原语 type1 = add parent_id by ("a1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'tt', 'Action': 'group', 'group': 'type1', 'by': 'type2', 'agg': 'tree_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[36]原语 tt = group type1 by type2 agg tree_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': 'index', 'to': 'tree_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[37]原语 tt = loc tt by index to tree_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type1', 'Action': 'loc', 'loc': 'type1', 'by': 'tree_name,tre_level,parent_id,type2,tree_num,level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[43]原语 type1 = loc type1 by tree_name,tre_level,parent_id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'type2', 'Action': 'join', 'join': 'type2,tt', 'by': 'tree_name,tree_name', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[44]原语 type2 = join type2,tt by tree_name,tree_name with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type2', 'as': "'tree_num_sum':'tree_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[45]原语 rename type2 as ("tree_num_sum":"tree_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type111', 'Action': 'union', 'union': 'type2,type1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[46]原语 type111 = union type2,type1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type111', 'Action': 'loc', 'loc': 'type111', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[47]原语 type111 = loc type111 by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type111', 'Action': 'loc', 'loc': 'type111', 'by': 'drop', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[48]原语 type111 = loc type111 by drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type111', 'Action': 'loc', 'loc': 'type111', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[49]原语 type111 = loc type111 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'type111.id', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:x+1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[50]原语 type111.id = lambda id by (x:x+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'type_for', 'Action': 'filter', 'filter': 'type111', 'by': 'tre_level == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[51]原语 type_for = filter type111 by tre_level == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type_for', 'Action': 'loc', 'loc': 'type_for', 'by': 'id,tree_name,tre_level,parent_id,tree_num,level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[52]原语 type_for = loc type_for by id,tree_name,tre_level,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,tree_name,tre_level,parent_id,tree_num,level'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[53]原语 type = @udf udf0.new_df with id,tree_name,tre_leve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'type_for', 'with': 'id = $1,tree_name = $2', 'run': '""\ntype_1 = filter type111 by type2 == \'@tree_name\'\ntype_1 = @udf type_1 by udf0.df_replace with (a1,@id)\ntype_1 = loc type_1 by id,tree_name,tre_level,parent_id,tree_num,level\ntype = union type,type_1\n""'}
	try:
		ptree['lineno']=54
		ptree['funs']=block_foreach_54
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[54]原语 foreach type_for run "type_1 = filter type111 by t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type', 'Action': 'union', 'union': 'type_for,type'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[60]原语 type = union type_for,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type', 'Action': '@udf', '@udf': 'type', 'by': 'udf0.df_fillna_cols', 'with': "level:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[62]原语 type = @udf type by udf0.df_fillna_cols with level... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'type.tree_color', 'Action': 'lambda', 'lambda': 'level', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[63]原语 type.tree_color = lambda level by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'type.tree_color', 'Action': 'lambda', 'lambda': 'tree_color', 'by': "x:'#E83131' if x == '高' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[64]原语 type.tree_color = lambda tree_color by (x:"#E83131... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'type.tree_color', 'Action': 'lambda', 'lambda': 'tree_color', 'by': "x:'#F66B36' if x == '中' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[65]原语 type.tree_color = lambda tree_color by (x:"#F66B36... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'type.tree_color', 'Action': 'lambda', 'lambda': 'tree_color', 'by': "x:'#F6D343' if x == '低' else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[66]原语 type.tree_color = lambda tree_color by (x:"#F6D343... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type', 'as': "'level':'tree_grade'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[67]原语 rename type as ("level":"tree_grade") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'type', 'as': 'tree_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[68]原语 alter type as tree_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type', 'Action': 'loc', 'loc': 'type', 'by': 'id,parent_id,tre_level,tree_name,tree_num,tree_grade,tree_color'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[69]原语 type = loc type by id,parent_id,tre_level,tree_nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'API_1_data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[70]原语 store type to ssdb by ssdb0 with API_1_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type,type1 from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[75]原语 api_type = load db by mysql1 with select type,type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_type', 'by': 'type:str,type1:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[76]原语 alter api_type by type:str,type1:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'api_type', 'with': 'type=$1,type1=$2', 'run': '""\n\ntt = filter api19_risk by type == \'@type\'\n#tt = filter api19_risk by type == \'API19-1-1\'\ntt = order tt by last_time with desc limit 10000\n#alter tt.first_time.last_time as str\n#保存为pkl文件\n#store tt to pkl by dt_table/api19_risk_@type1.pkl\ntt = loc tt by _id,api,app,dest_ip,dest_port,method,last_time,state,type\n#重命名\nrename tt as (\'api\':\'接口\',\'api_name\':\'接口名\',\'app\':\'应用\',\'app_name\':\'应用名\',\'dest_ip\':\'部署IP\',\'dest_port\':\'部署端口\',\'method\':\'请求类型\',\'length\':\'返回数据最大数据量\',\'first_time\':\'首次发现时间\',\'last_time\':\'最新监测时间\',\'state\':\'弱点状态\',\'type\':\'弱点类型\',\'more\':\'详情\')\ntt = loc tt by _id,接口,应用,部署IP,部署端口,请求类型,最新监测时间,弱点状态\n#清空Q\nb = load ssdb by ssdb0 query qclear,api19_risk_@type1,-,-\n#保存Q\nstore tt to ssdb by ssdb0 with api19_risk_@type1 as Q\n\n""'}
	try:
		ptree['lineno']=77
		ptree['funs']=block_foreach_77
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[77]原语 foreach api_type run "tt = filter api19_risk by ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,count(*) as api_num from data_api_new where merge_state != 1 group by app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[101]原语 api_num = load db by mysql1 with select app,count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_num', 'by': 'app:str,api_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[102]原语 alter api_num by app:str,api_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'risk_num', 'Action': 'group', 'group': 'api19_risk', 'by': 'app', 'agg': 'api:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[104]原语 risk_num = group api19_risk by app agg api:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk_num', 'Action': 'loc', 'loc': 'risk_num', 'by': 'index', 'to': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[105]原语 risk_num = loc risk_num by index to app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'lel', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type1 as type,level from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[107]原语 lel = load db by mysql1 with select type1 as type,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'lel', 'by': 'type:str,level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[108]原语 alter lel by type:str,level:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type', 'Action': 'loc', 'loc': 'api_type', 'by': 'type', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[109]原语 type = loc api_type by type to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type', 'as': "'type1':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[110]原语 rename type as ("type1":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'rr', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'app,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[111]原语 rr = loc api19_risk by app,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'rr', 'Action': 'group', 'group': 'rr', 'by': 'app,type', 'agg': 'type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[112]原语 rr = group rr by app,type agg type:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'rr', 'by': 'type_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[113]原语 alter rr by type_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'rr', 'Action': '@udf', '@udf': 'rr', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[114]原语 rr = @udf rr by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'rr', 'Action': '@udf', '@udf': 'rr,type', 'by': 'SP.tag2dict', 'with': 'type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[115]原语 rr = @udf rr,type by SP.tag2dict with type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'rr', 'Action': 'join', 'join': 'rr,lel', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[116]原语 rr = join rr,lel by type,type with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'rr', 'Action': 'order', 'order': 'rr', 'by': 'type_count', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[117]原语 rr = order rr by type_count with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'fx1', 'Action': 'loc', 'loc': 'rr', 'by': 'app,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[118]原语 fx1 = loc rr by app,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'rr', 'by': 'type_count:str,level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[119]原语 alter rr by type_count:str,level:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'rr', 'Action': 'add', 'add': 'type_count', 'by': 'df[\'type\'] +" ["+ df[\'level\'] + "] " +"("+ df[\'type_count\'] + ")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[120]原语 rr = add type_count by df["type"] +" ["+ df["level... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'rr.type_count', 'Action': 'lambda', 'lambda': 'type_count', 'by': "x: x+' ,'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[121]原语 rr.type_count = lambda type_count by (x: x+" ,") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'rr', 'Action': 'group', 'group': 'rr', 'by': 'app', 'agg': 'type_count:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[122]原语 rr = group rr by app agg type_count:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'rr', 'Action': '@udf', '@udf': 'rr', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[123]原语 rr = @udf rr by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'rr.type_count_sum', 'Action': 'lambda', 'lambda': 'type_count_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[124]原语 rr.type_count_sum = lambda type_count_sum by (x:x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'rr', 'as': "'type_count_sum':'type_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[125]原语 rename rr as ("type_count_sum":"type_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'app,state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[127]原语 ss = loc api19_risk by app,state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss', 'Action': 'group', 'group': 'ss', 'by': 'app,state', 'agg': 'state:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[128]原语 ss = group ss by app,state agg state:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss', 'by': 'state_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[129]原语 alter ss by state_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[130]原语 ss = @udf ss by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ss', 'Action': 'order', 'order': 'ss', 'by': 'state_count', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[131]原语 ss = order ss by state_count with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss', 'by': 'state_count:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[132]原语 alter ss by state_count:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss', 'Action': 'add', 'add': 'state_count', 'by': 'df[\'state\'] +"("+ df[\'state_count\'] + ")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[133]原语 ss = add state_count by  df["state"] +"("+ df["sta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss.state_count', 'Action': 'lambda', 'lambda': 'state_count', 'by': "x: x+' ,'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[134]原语 ss.state_count = lambda state_count by (x: x+" ,")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss', 'Action': 'group', 'group': 'ss', 'by': 'app', 'agg': 'state_count:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[135]原语 ss = group ss by app agg state_count:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[136]原语 ss = @udf ss by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss.state_count_sum', 'Action': 'lambda', 'lambda': 'state_count_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[137]原语 ss.state_count_sum = lambda state_count_sum by (x:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss', 'as': "'state_count_sum':'state_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[138]原语 rename ss as ("state_count_sum":"state_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'app,dest_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[140]原语 dd = loc api19_risk by app,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dd', 'Action': 'distinct', 'distinct': 'dd', 'by': 'app,dest_ip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[141]原语 dd = distinct dd by app,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dd.dest_ip', 'Action': 'lambda', 'lambda': 'dest_ip', 'by': "x:x+' ,'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[142]原语 dd.dest_ip = lambda dest_ip by (x:x+" ,") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'dd', 'Action': 'group', 'group': 'dd', 'by': 'app', 'agg': 'dest_ip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[143]原语 dd = group dd by app agg dest_ip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[144]原语 dd = @udf dd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dd.dest_ip_sum', 'Action': 'lambda', 'lambda': 'dest_ip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[145]原语 dd.dest_ip_sum = lambda dest_ip_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'app,app_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[147]原语 risk = loc api19_risk by app,app_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,dd', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[148]原语 risk = join risk,dd by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,api_num', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[149]原语 risk = join risk,api_num by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,risk_num', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[150]原语 risk = join risk,risk_num by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,ss', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[151]原语 risk = join risk,ss by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'risk,rr', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[152]原语 risk = join risk,rr by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[154]原语 app = load db by mysql1 with select app from data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'risk', 'Action': 'join', 'join': 'app,risk', 'by': 'app,app', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[155]原语 risk = join app,risk by app,app with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'risk', 'Action': 'distinct', 'distinct': 'risk', 'by': 'app,dest_ip_sum,api_num,api_count,state_num,type_num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[157]原语 risk = distinct risk by app,dest_ip_sum,api_num,ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': 'index', 'to': '_id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[158]原语 risk = loc risk by index to _id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'risk._id', 'Action': 'lambda', 'lambda': '_id', 'by': 'x:x+1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[159]原语 risk._id = lambda _id by (x:x+1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_fillna_cols', 'with': "app:'',app_name:'',dest_ip_sum:'',api_num:0,api_count:0,state_num:'',type_num:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[160]原语 risk = @udf risk by udf0.df_fillna_cols with app:"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'risk', 'Action': 'filter', 'filter': 'risk', 'by': "app != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[161]原语 risk = filter risk by app != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'risk', 'Action': 'order', 'order': 'risk', 'by': 'api_count', 'with': 'desc limit 50000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[162]原语 risk = order risk by api_count with desc limit 500... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'pq', 'by': 'dt_table/app_risk.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[163]原语 store risk to pq by dt_table/app_risk.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': '_id,app,app_name,api_num,api_count,state_num,type_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[164]原语 risk = loc risk by _id,app,app_name,api_num,api_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk', 'as': "'app':'应用','app_name':'应用名','dest_ip_sum':'服务器IP','api_num':'接口总数','api_count':'接口弱点量','state_num':'弱点状态分布','type_num':'弱点类型分布'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[166]原语 rename risk as ("app":"应用","app_name":"应用名","dest_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_risk,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[168]原语 b = load ssdb by ssdb0 query qclear,app_risk,-,- 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_risk', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[170]原语 store risk to ssdb by ssdb0 with app_risk as Q 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api19_tree.fbi]执行第[179]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],179

#主函数结束,开始块函数

def block_foreach_54(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'type_1', 'Action': 'filter', 'filter': 'type111', 'by': "type2 == '@tree_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第54行foreach语句中]执行第[55]原语 type_1 = filter type111 by type2 == "@tree_name" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'type_1', 'Action': '@udf', '@udf': 'type_1', 'by': 'udf0.df_replace', 'with': 'a1,@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第54行foreach语句中]执行第[56]原语 type_1 = @udf type_1 by udf0.df_replace with (a1,@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type_1', 'Action': 'loc', 'loc': 'type_1', 'by': 'id,tree_name,tre_level,parent_id,tree_num,level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第54行foreach语句中]执行第[57]原语 type_1 = loc type_1 by id,tree_name,tre_level,pare... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type', 'Action': 'union', 'union': 'type,type_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第54行foreach语句中]执行第[58]原语 type = union type,type_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_54

def block_foreach_77(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt', 'Action': 'filter', 'filter': 'api19_risk', 'by': "type == '@type'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[79]原语 tt = filter api19_risk by type == "@type" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'tt', 'Action': 'order', 'order': 'tt', 'by': 'last_time', 'with': 'desc limit 10000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[81]原语 tt = order tt by last_time with desc limit 10000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': '_id,api,app,dest_ip,dest_port,method,last_time,state,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[85]原语 tt = loc tt by _id,api,app,dest_ip,dest_port,metho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt', 'as': "'api':'接口','api_name':'接口名','app':'应用','app_name':'应用名','dest_ip':'部署IP','dest_port':'部署端口','method':'请求类型','length':'返回数据最大数据量','first_time':'首次发现时间','last_time':'最新监测时间','state':'弱点状态','type':'弱点类型','more':'详情'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[87]原语 rename tt as ("api":"接口","api_name":"接口名","app":"应... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': '_id,接口,应用,部署IP,部署端口,请求类型,最新监测时间,弱点状态'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[88]原语 tt = loc tt by _id,接口,应用,部署IP,部署端口,请求类型,最新监测时间,弱点状... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,api19_risk_@type1,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[90]原语 b = load ssdb by ssdb0 query qclear,api19_risk_@ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tt', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api19_risk_@type1', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[92]原语 store tt to ssdb by ssdb0 with api19_risk_@type1 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_77

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



