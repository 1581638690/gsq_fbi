#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: link_data_open
#datetime: 2024-08-30T16:10:53.476337
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
		add_the_error('[link_data_open.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[14]原语 dd = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'dd', 'by': 'nodeType,nodeName,nodeExpandTypes'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[15]原语 dd = loc dd by nodeType,nodeName,nodeExpandTypes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[16]原语 type = eval dd by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'nodes', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[17]原语 nodes = eval dd by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type1', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[18]原语 type1 = eval dd by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'node_type', 'Action': 'load', 'load': 'pq', 'by': 'link/link_type.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[21]原语 node_type = load pq by link/link_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge_out', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': "g.V('$nodes').Tag('aaa').Out(['link_sql','link_http','link_http1','link_belong','link_belong1'],'path').All()"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[25]原语 edge_out = @udf GL.query_http_mkd with g.V("$nodes... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'text1', 'Action': 'if', 'if': '$edge_out != None', 'with': 'edge_out = @udf edge_out by FBI.json2df'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=26
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[26]原语 text1 = if $edge_out != None with edge_out = @udf ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'aa', 'Action': 'if', 'if': '$text1 == False', 'with': 'edge_out = @udf udf0.new_df with (aaa,id,path)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=27
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[27]原语 aa = if $text1 == False with edge_out = @udf udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edge_out', 'as': "'aaa':'S','id':'O','path':'P'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[28]原语 rename edge_out as ("aaa":"S","id":"O","path":"P")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge_in', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': "g.V('$nodes').Tag('aaa').In(['link_sql','link_http','link_http1','link_belong','link_belong1'],'path').All()"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[31]原语 edge_in = @udf GL.query_http_mkd with g.V("$nodes"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'text2', 'Action': 'if', 'if': '$edge_in != None', 'with': 'edge_in = @udf edge_in by FBI.json2df'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=32
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[32]原语 text2 = if $edge_in != None with edge_in = @udf ed... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'aa', 'Action': 'if', 'if': '$text2 == False', 'with': 'edge_in = @udf udf0.new_df with (aaa,id,path)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=33
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[33]原语 aa = if $text2 == False with edge_in = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edge_in', 'as': "'aaa':'O','id':'S','path':'P'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[34]原语 rename edge_in as ("aaa":"O","id":"S","path":"P") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '应用账号'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[37]原语 if "$type" == "应用账号" with edge1 = join edge_out,no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '管理终端'", 'with': '""\nif \'$type1\' == \'应用账号\' with edge1 = join edge_in,node_type by S,id with left\nif \'$type1\' == \'应用\' or \'$type1\' == \'接口\' or \'$type1\' == \'数据库\' with edge1 = join edge_out,node_type by O,id with left\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=40
		ptree['funs']=block_if_40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[40]原语 if "$type" == "管理终端" with "if "$type1" == "应用账号" w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '业务终端'", 'with': '""\nif \'$type1\' == \'应用账号\' with edge1 = join edge_in,node_type by S,id with left\nif \'$type1\' == \'应用\' or \'$type1\' == \'接口\' with edge1 = join edge_out,node_type by O,id with left\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=46
		ptree['funs']=block_if_46
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[46]原语 if "$type" == "业务终端" with "if "$type1" == "应用账号" w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '接口'", 'with': '""\nif \'$type1\' == \'终端\' with edge1 = join edge_in,node_type by S,id with left\nif \'$type1\' == \'应用\' with edge1 = join edge_out,node_type by O,id with left\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=52
		ptree['funs']=block_if_52
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[52]原语 if "$type" == "接口" with "if "$type1" == "终端" with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '应用'", 'with': '""\nif \'$type1\' == \'终端\' or \'$type1\' == \'接口\' with edge1 = join edge_in,node_type by S,id with left\nif \'$type1\' == \'数据库\' with edge1 = join edge_out,node_type by O,id with left\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=58
		ptree['funs']=block_if_58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[58]原语 if "$type" == "应用" with "if "$type1" == "终端" or "$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '数据库'", 'with': 'edge1 = join edge_in,node_type by S,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=64
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[64]原语 if "$type" == "数据库" with edge1 = join edge_in,node... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type' == '数据终端'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=67
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[67]原语 if "$type" == "数据终端" with edge1 = join edge_out,no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'edge1.type', 'Action': 'str', 'str': 'type', 'by': "replace('业务','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[69]原语 edge1.type = str type by replace("业务","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'edge1.type', 'Action': 'str', 'str': 'type', 'by': "replace('管理','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[70]原语 edge1.type = str type by replace("管理","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'edge1.type', 'Action': 'str', 'str': 'type', 'by': "replace('数据','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[71]原语 edge1.type = str type by replace("数据","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge1', 'Action': 'filter', 'filter': 'edge1', 'by': "type == '$type1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[72]原语 edge1 = filter edge1 by type == "$type1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge1', 'Action': 'loc', 'loc': 'edge1', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[73]原语 edge1 = loc edge1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'edge', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'link_edges'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[75]原语 edge = load ssdb by ssdb0 with link_edges 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'edge', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[76]原语 edge = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'eee', 'Action': 'join', 'join': 'edge,edge1', 'by': '[S,O,P],[S,O,P]', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[77]原语 eee = join edge,edge1 by [S,O,P],[S,O,P] with oute... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'eee', 'Action': '@udf', '@udf': 'eee', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[78]原语 eee = @udf eee by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edges', 'Action': 'filter', 'filter': 'eee', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[79]原语 edges = filter eee by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edges', 'Action': 'loc', 'loc': 'edges', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[80]原语 edges = loc edges by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'edges.index.size > 0', 'with': '""\n### http、sql关系线加字 D ----------------------------------------\nddd = load pq by link/link_http_acc.pq\nedges = join edges,ddd by [S,O],[zd,url_name] with left\nedges = @udf edges by udf0.df_fillna with \'\'\nedges = loc edges by S,O,P,account\nddd = load pq by link/link_http1_acc.pq\nedges = join edges,ddd by [S,O],[zd,app] with left\nedges = @udf edges by udf0.df_fillna with \'\'\nedges = loc edges by S,O,P,account,account1\nddd = load pq by link/link_sql_user.pq\nedges = join edges,ddd by [S,O],[app,db] with left\nedges = @udf edges by udf0.df_fillna with \'\'\nedges = loc edges by S,O,P,account,account1,user\nedges = @udf edges by udf0.df_row_lambda with (x: x[3] if x[3] != \'\' else x[4])\nrename edges as (\'lambda1\':\'D1\')\nedges = @udf edges by udf0.df_row_lambda with (x: x[5] if x[5] != \'\' else x[6])\nrename edges as (\'lambda1\':\'D\')\nedges = loc edges by S,O,P,D\nedges = distinct edges by S,O,P,D\n### http、sql关系线加字 D ----------------------------------------\nedge = union edge,edges\nedge = loc edge by S,O,P,D\nedge = distinct edge by S,O,P,D\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=82
		ptree['funs']=block_if_82
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[82]原语 if edges.index.size > 0 with "### http、sql关系线加字  D... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'edge', 'as': 'edges'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[107]原语 push edge as edges 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa1', 'Action': 'load', 'load': 'pq', 'by': 'link/link_edge_open.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[109]原语 aa1 = load pq by link/link_edge_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'edges', 'Action': 'union', 'union': 'edges,aa1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[110]原语 edges = union edges,aa1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edges', 'Action': 'distinct', 'distinct': 'edges', 'by': 'S,O,P,D'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[111]原语 edges = distinct edges by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'edges', 'to': 'pq', 'by': 'link/link_edge_open.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[112]原语 store edges to pq by link/link_edge_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'edges', 'Action': 'load', 'load': 'pq', 'by': 'link/link_edge_open.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[113]原语 edges = load pq by link/link_edge_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt1', 'Action': 'loc', 'loc': 'edges', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[116]原语 tt1 = loc edges by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt2', 'Action': 'loc', 'loc': 'edges', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[117]原语 tt2 = loc edges by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt2', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[118]原语 rename tt2 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tt', 'Action': 'union', 'union': 'tt1,tt2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[119]原语 tt = union tt1,tt2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'node', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'link_nodes'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[121]原语 node = load ssdb by ssdb0 with link_nodes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[122]原语 node = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'eee', 'Action': 'join', 'join': 'node,tt', 'by': 'id,S', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[123]原语 eee = join node,tt by id,S with outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'eee', 'Action': '@udf', '@udf': 'eee', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[124]原语 eee = @udf eee by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'nodes', 'Action': 'filter', 'filter': 'eee', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[125]原语 nodes = filter eee by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'nodes.index.size > 0', 'with': '""\nnodes = loc nodes by S\nnodes = join nodes,node_type by S,id with left\nnodes = @udf nodes by udf0.df_fillna with \'\'\n## 计算节点关系数量\nnum1 = group edge by S agg S:count\nnum1 = loc num1 by index to id\nnum2 = group edge by O agg O:count\nnum2 = loc num2 by index to id\nnodes = join nodes,num1 by id,id with left\nnodes = join nodes,num2 by id,id with left\nnodes = @udf nodes by udf0.df_fillna with 0\nnodes = add num by (df["S_count"]+df["O_count"])\nnodes = add light by (\'false\')\nnodes = add count by 10\n#\t##过滤节点\n#\tnodes.detail_type = lambda type by (x:x)\n#\tnodes.detail_type = lambda detail_type by (x:x if x != \'业务终端\' else \'终端\')\n#\tnodes.detail_type = lambda detail_type by (x:x if x != \'管理终端\' else \'终端\')\n#\tnodes = loc nodes by id,type,light,count,num,detail_type\n#\tnodes = distinct nodes by id,type,light,count,num,detail_type\nnode = union nodes,node1\nnode = @udf node by udf0.df_fillna with \'\'\nnode = loc node by id,type,light,count,num,detail_type,top10,detail_type_count\nnode = distinct node by id,type,light,count,num,detail_type,top10,detail_type_count\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=127
		ptree['funs']=block_if_127
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[127]原语 if nodes.index.size > 0 with "nodes = loc nodes by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'node', 'as': 'nodes'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[153]原语 push node as nodes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa1', 'Action': 'load', 'load': 'pq', 'by': 'link/link_node_open.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[155]原语 aa1 = load pq by link/link_node_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'nodes', 'Action': 'union', 'union': 'nodes,aa1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[156]原语 nodes = union nodes,aa1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nodes', 'Action': 'loc', 'loc': 'nodes', 'by': 'id,type,light,count,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[157]原语 nodes = loc nodes by id,type,light,count,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'nodes', 'Action': 'distinct', 'distinct': 'nodes', 'by': 'id,type,light,count,num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[158]原语 nodes = distinct nodes by id,type,light,count,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'nodes', 'to': 'pq', 'by': 'link/link_node_open.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[159]原语 store nodes to pq by link/link_node_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'nodes', 'Action': 'load', 'load': 'pq', 'by': 'link/link_node_open.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[160]原语 nodes = load pq by link/link_node_open.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[link_data_open.fbi]执行第[162]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],162

#主函数结束,开始块函数

def block_if_40(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '应用账号'", 'with': 'edge1 = join edge_in,node_type by S,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=41
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[41]原语 if "$type1" == "应用账号" with edge1 = join edge_in,no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '应用' or '$type1' == '接口' or '$type1' == '数据库'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=42
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[42]原语 if "$type1" == "应用" or "$type1" == "接口" or "$type1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_40

def block_if_46(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '应用账号'", 'with': 'edge1 = join edge_in,node_type by S,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[47]原语 if "$type1" == "应用账号" with edge1 = join edge_in,no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '应用' or '$type1' == '接口'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=48
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[48]原语 if "$type1" == "应用" or "$type1" == "接口" with edge1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_46

def block_if_52(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '终端'", 'with': 'edge1 = join edge_in,node_type by S,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=53
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第52行if语句中]执行第[53]原语 if "$type1" == "终端" with edge1 = join edge_in,node... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '应用'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=54
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第52行if语句中]执行第[54]原语 if "$type1" == "应用" with edge1 = join edge_out,nod... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_52

def block_if_58(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '终端' or '$type1' == '接口'", 'with': 'edge1 = join edge_in,node_type by S,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=59
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[59]原语 if "$type1" == "终端" or "$type1" == "接口" with edge1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$type1' == '数据库'", 'with': 'edge1 = join edge_out,node_type by O,id with left'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=60
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[60]原语 if "$type1" == "数据库" with edge1 = join edge_out,no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_58

def block_if_82(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_http_acc.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[84]原语 ddd = load pq by link/link_http_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edges', 'Action': 'join', 'join': 'edges,ddd', 'by': '[S,O],[zd,url_name]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[85]原语 edges = join edges,ddd by [S,O],[zd,url_name] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'edges', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[86]原语 edges = @udf edges by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edges', 'Action': 'loc', 'loc': 'edges', 'by': 'S,O,P,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[87]原语 edges = loc edges by S,O,P,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_http1_acc.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[88]原语 ddd = load pq by link/link_http1_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edges', 'Action': 'join', 'join': 'edges,ddd', 'by': '[S,O],[zd,app]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[89]原语 edges = join edges,ddd by [S,O],[zd,app] with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'edges', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[90]原语 edges = @udf edges by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edges', 'Action': 'loc', 'loc': 'edges', 'by': 'S,O,P,account,account1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[91]原语 edges = loc edges by S,O,P,account,account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_sql_user.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[92]原语 ddd = load pq by link/link_sql_user.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edges', 'Action': 'join', 'join': 'edges,ddd', 'by': '[S,O],[app,db]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[93]原语 edges = join edges,ddd by [S,O],[app,db] with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'edges', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[94]原语 edges = @udf edges by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edges', 'Action': 'loc', 'loc': 'edges', 'by': 'S,O,P,account,account1,user'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[95]原语 edges = loc edges by S,O,P,account,account1,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'edges', 'by': 'udf0.df_row_lambda', 'with': "x: x[3] if x[3] != '' else x[4]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[96]原语 edges = @udf edges by udf0.df_row_lambda with (x: ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edges', 'as': "'lambda1':'D1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[97]原语 rename edges as ("lambda1":"D1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'edges', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[5] != '' else x[6]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[98]原语 edges = @udf edges by udf0.df_row_lambda with (x: ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edges', 'as': "'lambda1':'D'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[99]原语 rename edges as ("lambda1":"D") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edges', 'Action': 'loc', 'loc': 'edges', 'by': 'S,O,P,D'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[100]原语 edges = loc edges by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edges', 'Action': 'distinct', 'distinct': 'edges', 'by': 'S,O,P,D'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[101]原语 edges = distinct edges by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'edge', 'Action': 'union', 'union': 'edge,edges'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[103]原语 edge = union edge,edges 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P,D'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[104]原语 edge = loc edge by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge', 'Action': 'distinct', 'distinct': 'edge', 'by': 'S,O,P,D'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[105]原语 edge = distinct edge by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_82

def block_if_127(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nodes', 'Action': 'loc', 'loc': 'nodes', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[128]原语 nodes = loc nodes by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'nodes', 'Action': 'join', 'join': 'nodes,node_type', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[129]原语 nodes = join nodes,node_type by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'nodes', 'Action': '@udf', '@udf': 'nodes', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[130]原语 nodes = @udf nodes by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'num1', 'Action': 'group', 'group': 'edge', 'by': 'S', 'agg': 'S:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[132]原语 num1 = group edge by S agg S:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'num1', 'Action': 'loc', 'loc': 'num1', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[133]原语 num1 = loc num1 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'num2', 'Action': 'group', 'group': 'edge', 'by': 'O', 'agg': 'O:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[134]原语 num2 = group edge by O agg O:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'num2', 'Action': 'loc', 'loc': 'num2', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[135]原语 num2 = loc num2 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'nodes', 'Action': 'join', 'join': 'nodes,num1', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[136]原语 nodes = join nodes,num1 by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'nodes', 'Action': 'join', 'join': 'nodes,num2', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[137]原语 nodes = join nodes,num2 by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'nodes', 'Action': '@udf', '@udf': 'nodes', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[138]原语 nodes = @udf nodes by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'nodes', 'Action': 'add', 'add': 'num', 'by': 'df["S_count"]+df["O_count"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[139]原语 nodes = add num by (df["S_count"]+df["O_count"]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'nodes', 'Action': 'add', 'add': 'light', 'by': "'false'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[140]原语 nodes = add light by ("false") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'nodes', 'Action': 'add', 'add': 'count', 'by': '10'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[141]原语 nodes = add count by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'node', 'Action': 'union', 'union': 'nodes,node1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[148]原语 node = union nodes,node1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node', 'Action': '@udf', '@udf': 'node', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[149]原语 node = @udf node by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node', 'Action': 'loc', 'loc': 'node', 'by': 'id,type,light,count,num,detail_type,top10,detail_type_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[150]原语 node = loc node by id,type,light,count,num,detail_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'node', 'Action': 'distinct', 'distinct': 'node', 'by': 'id,type,light,count,num,detail_type,top10,detail_type_count'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第127行if语句中]执行第[151]原语 node = distinct node by id,type,light,count,num,de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_127

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



