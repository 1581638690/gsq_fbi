#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: link_data
#datetime: 2024-08-09T16:57:50.019181
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
		add_the_error('[link_data.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[18]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a.index.size == 1', 'with': 'qw = eval a by iloc[0,1]'}
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[19]原语 if a.index.size == 1 with qw = eval a by iloc[0,1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'a.index.size == 1', 'with': 'node_type = eval a by iloc[0,1]'}
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[20]原语 if a.index.size == 1 with node_type = eval a by il... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$qw' == 'app'", 'with': "a.aaa = lambda aaa by ( x:x.split(':')[0] )"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[21]原语 if "$qw" == "app" with a.aaa = lambda aaa by ( x:x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'q', 'Action': 'eval', 'eval': 'a', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[24]原语 q = eval a by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$q > 0', 'with': 'd = eval a by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[25]原语 if $q > 0 with d =  eval a by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$q' != '0'", 'with': '""\nrun app_query.fbi with @nodes = $d\n"', 'else': '"\n\n###节点\nnode = load pq by link/link_type.pq\n\n## 节点出入度的和\nnode_count = load pq by link/S_O_count.pq\nalter node_count.S_count.O_count as int\nnode_count = add count1 by df[\'S_count\']+df[\'O_count\']\nnode_count = loc node_count by id,count1\n\n##关系\nedges = @udf GL.query_http_mkd with g.V().Tag(\'aaa\').Out([\'link_sql\',\'link_http\',\'link_http1\',\'link_belong\',\'link_belong1\'],\'path\').GetLimit(1000000)\nedge_text = if $edges != None with edges = @udf edges by FBI.json2df\naa = if $edge_text == False with edges = @udf udf0.new_df with (aaa,id,path)\nrename edges as (\'aaa\':\'S\',\'id\':\'O\',\'path\':\'P\')\n################################### 数据库关系取 30\nlimit5 = load db by mysql1 with select dbms_obj as nn from dbms_obj order by count desc limit 10\n######################################################## 入度1\nedge1 = join limit5,edges by nn,O with left\nedge1 = @udf edge1 by udf0.df_fillna with \'\'\nedge1 = filter edge1 by S != \'\'\nedge1 = loc edge1 by S,O,P\n###取前100 的节点\nedge1 = join edge1,node_count by S,id with left\nedge1 = order edge1 by count1 with desc limit 100\nedge1 = loc edge1 by S,O,P\nedge1 = distinct edge1 by S,O,P\n######################################################## 入度2\ndd = loc edge1 by S\ndd = distinct dd by S\nrename dd as (\'S\':\'dd\')\nedge2 = join dd,edges by dd,O with left\nedge2 = @udf edge2 by udf0.df_fillna with \'\'\nedge2 = filter edge2 by S != \'\'\nedge2 = loc edge2 by S,O,P\nedge2 = distinct edge2 by S,O,P\n###取前100 的节点\nedge2 = join edge2,node_count by S,id with left\nedge2 = order edge2 by count1 with desc limit 100\nedge2 = loc edge2 by S,O,P\nedge2 = distinct edge2 by S,O,P\n######################################################## 入度3\ndd = loc edge2 by S\ndd = distinct dd by S\nrename dd as (\'S\':\'dd\')\nedge3 = join dd,edges by dd,O with left\nedge3 = @udf edge3 by udf0.df_fillna with \'\'\nedge3 = filter edge3 by S != \'\'\nedge3 = loc edge3 by S,O,P\n###取前100 的节点\nedge3 = join edge3,node_count by S,id with left\nedge3 = order edge3 by count1 with desc limit 100\nedge3 = loc edge3 by S,O,P\nedge3 = distinct edge3 by S,O,P\n######################################################## 入度4\ndd = loc edge3 by S\ndd = distinct dd by S\nrename dd as (\'S\':\'dd\')\nedge4 = join dd,edges by dd,O with left\nedge4 = @udf edge4 by udf0.df_fillna with \'\'\nedge4 = filter edge4 by S != \'\'\nedge4 = loc edge4 by S,O,P\n###取前100 的节点\nedge4 = join edge4,node_count by S,id with left\nedge4 = order edge4 by count1 with desc limit 100\nedge4 = loc edge4 by S,O,P\nedge4 = distinct edge4 by S,O,P\n########################### 合并==================合并==================合并==================合并==================\nedge = union edge1,edge2,edge3,edge4\nedge = loc edge by S,O,P\n############ 遇到 管理终端 查数据库对象\nedge_sql = loc edge by S\nedge_sql = distinct edge_sql by S\nedge_sql = join edge_sql,node by S,id with left\nedge_sql = filter edge_sql by type == \'管理终端\' or type == \'业务终端\'\nif edge_sql.index.size <= 10 with """\nedge_sql = filter edge_sql by type == \'管理终端\'\ndd = loc edge_sql by S\nrename dd as (\'S\':\'dd\')\nedge_sql = join dd,edges by dd,S with left\nedge_sql = loc edge_sql by S,O,P\nedge = union edge,edge_sql\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['funs']=block_if_27
		ptree['funs2']=block_if_else_27
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[27]原语 if "$q" != "0" with "run app_query.fbi with @nodes... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge', 'Action': 'distinct', 'distinct': 'edge', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[114]原语 edge = distinct edge by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_http_acc.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[117]原语 ddd = load pq by link/link_http_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge', 'Action': 'join', 'join': 'edge,ddd', 'by': '[S,O],[zd,url_name]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[118]原语 edge = join edge,ddd by [S,O],[zd,url_name] with l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'edge', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[119]原语 edge = @udf edge by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[120]原语 edge = loc edge by S,O,P,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_http1_acc.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[121]原语 ddd = load pq by link/link_http1_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge', 'Action': 'join', 'join': 'edge,ddd', 'by': '[S,O],[zd,app]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[122]原语 edge = join edge,ddd by [S,O],[zd,app] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'edge', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[123]原语 edge = @udf edge by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P,account,account1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[124]原语 edge = loc edge by S,O,P,account,account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'pq', 'by': 'link/link_sql_user.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[125]原语 ddd = load pq by link/link_sql_user.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge', 'Action': 'join', 'join': 'edge,ddd', 'by': '[S,O],[app,db]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[126]原语 edge = join edge,ddd by [S,O],[app,db] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'edge', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[127]原语 edge = @udf edge by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P,account,account1,user'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[128]原语 edge = loc edge by S,O,P,account,account1,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'edge', 'by': 'udf0.df_row_lambda', 'with': "x: x[3] if x[3] != '' else x[4]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[129]原语 edge = @udf edge by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edge', 'as': "'lambda1':'D1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[130]原语 rename edge as ("lambda1":"D1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'edge', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[5] != '' else x[6]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[131]原语 edge = @udf edge by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edge', 'as': "'lambda1':'D'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[132]原语 rename edge as ("lambda1":"D") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P,D'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[133]原语 edge = loc edge by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge', 'Action': 'distinct', 'distinct': 'edge', 'by': 'S,O,P,D'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[134]原语 edge = distinct edge by S,O,P,D 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'edge', 'as': 'edges'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[136]原语 push edge as edges 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'edge', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_edges'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[137]原语 store edge to ssdb by ssdb0 with link_edges 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt1', 'Action': 'loc', 'loc': 'edge', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[143]原语 tt1 = loc edge by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt2', 'Action': 'loc', 'loc': 'edge', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[144]原语 tt2 = loc edge by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt2', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[145]原语 rename tt2 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tt', 'Action': 'union', 'union': 'tt1,tt2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[146]原语 tt = union tt1,tt2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node', 'Action': 'join', 'join': 'tt,node', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[147]原语 node = join tt,node by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node', 'Action': '@udf', '@udf': 'node', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[148]原语 node = @udf node by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'num1', 'Action': 'group', 'group': 'edge', 'by': 'S', 'agg': 'S:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[150]原语 num1 = group edge by S agg S:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'num1', 'Action': 'loc', 'loc': 'num1', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[151]原语 num1 = loc num1 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'num2', 'Action': 'group', 'group': 'edge', 'by': 'O', 'agg': 'O:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[152]原语 num2 = group edge by O agg O:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'num2', 'Action': 'loc', 'loc': 'num2', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[153]原语 num2 = loc num2 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node', 'Action': 'join', 'join': 'node,num1', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[154]原语 node = join node,num1 by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node', 'Action': 'join', 'join': 'node,num2', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[155]原语 node = join node,num2 by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node', 'Action': '@udf', '@udf': 'node', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[156]原语 node = @udf node by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node', 'Action': 'add', 'add': 'num', 'by': 'df["S_count"]+df["O_count"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[157]原语 node = add num by (df["S_count"]+df["O_count"]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node', 'Action': 'add', 'add': 'light', 'by': "'false'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[159]原语 node = add light by ("false") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node.detail_type', 'Action': 'lambda', 'lambda': 'type', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[160]原语 node.detail_type = lambda type by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node.detail_type', 'Action': 'lambda', 'lambda': 'detail_type', 'by': "x:x if x != '业务终端' else '终端'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[161]原语 node.detail_type = lambda detail_type by (x:x if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node.detail_type', 'Action': 'lambda', 'lambda': 'detail_type', 'by': "x:x if x != '管理终端' else '终端'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[162]原语 node.detail_type = lambda detail_type by (x:x if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node', 'Action': 'add', 'add': 'count', 'by': '10'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[163]原语 node = add count by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node', 'Action': 'loc', 'loc': 'node', 'by': 'id,type,light,count,num,detail_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[164]原语 node = loc node by id,type,light,count,num,detail_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'node', 'Action': 'distinct', 'distinct': 'node', 'by': 'id,type,light,count,num,detail_type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[165]原语 node = distinct node by id,type,light,count,num,de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_zh', 'Action': 'filter', 'filter': 'node', 'by': "type =='应用账号'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[167]原语 node_zh = filter node  by type =="应用账号" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_zh', 'Action': 'order', 'order': 'node_zh', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[168]原语 node_zh = order  node_zh  by num with desc limit 1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_zh', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[169]原语 node_zh = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_zd2', 'Action': 'filter', 'filter': 'node', 'by': "type =='数据终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[170]原语 node_zd2 = filter node  by type =="数据终端" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_zd2', 'Action': 'order', 'order': 'node_zd2', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[171]原语 node_zd2 = order  node_zd2  by num with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_zd2', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[172]原语 node_zd2 = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_zd3', 'Action': 'filter', 'filter': 'node', 'by': "type =='管理终端' or type == '业务终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[173]原语 node_zd3 = filter node  by type =="管理终端" or type =... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_zd3', 'Action': 'order', 'order': 'node_zd3', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[174]原语 node_zd3 = order  node_zd3  by num with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_zd3', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[175]原语 node_zd3 = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_jk', 'Action': 'filter', 'filter': 'node', 'by': "type =='接口'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[176]原语 node_jk = filter node  by type =="接口" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_jk', 'Action': 'order', 'order': 'node_jk', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[177]原语 node_jk = order  node_jk  by num with desc limit 1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_jk', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[178]原语 node_jk = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_yy', 'Action': 'filter', 'filter': 'node', 'by': "type =='应用'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[179]原语 node_yy = filter node  by type =="应用" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_yy', 'Action': 'order', 'order': 'node_yy', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[180]原语 node_yy = order  node_yy  by num with desc limit 1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_yy', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[181]原语 node_yy = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_sjk', 'Action': 'filter', 'filter': 'node', 'by': "type =='数据库'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[182]原语 node_sjk= filter node  by type =="数据库" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node_sjk', 'Action': 'order', 'order': 'node_sjk', 'by': 'num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[183]原语 node_sjk = order  node_sjk  by num with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_sjk', 'Action': 'add', 'add': 'top10', 'by': "'true'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[184]原语 node_sjk = add top10 by ("true") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'node_zs', 'Action': 'union', 'union': 'node_zh,node_zd1,node_zd2,node_zd3,node_jk,node_yy,node_sjk'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[185]原语 node_zs = union node_zh,node_zd1,node_zd2,node_zd3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node_zs', 'Action': 'loc', 'loc': 'node_zs', 'by': 'id ,type ,top10'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[186]原语 node_zs = loc node_zs by id ,type ,top10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node_zs1', 'Action': 'join', 'join': 'node ,node_zs', 'by': '[id,type],[id,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[187]原语 node_zs1 = join  node ,node_zs by [id,type],[id,ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node_zs1.top10', 'Action': 'lambda', 'lambda': 'top10', 'by': "x:x if x == 'true' else 'false'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[188]原语 node_zs1.top10 = lambda top10 by (x:x if x == "tru... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node', 'Action': 'loc', 'loc': 'node_zs1', 'by': 'id,type,light,count,num,detail_type,top10'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[189]原语 node = loc node_zs1 by id,type,light,count,num,det... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'node_type', 'Action': 'group', 'group': 'node', 'by': 'detail_type', 'agg': 'detail_type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[190]原语 node_type = group node by detail_type agg detail_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node_type', 'Action': '@udf', '@udf': 'node_type', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[191]原语 node_type = @udf node_type by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_type1', 'Action': 'filter', 'filter': 'node_type', 'by': "detail_type=='终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[192]原语 node_type1 = filter node_type by detail_type=="终端"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node_type1.detail_type', 'Action': 'lambda', 'lambda': 'detail_type', 'by': "x:x if x != '终端' else '业务终端'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[193]原语 node_type1.detail_type = lambda detail_type by (x:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node_type.detail_type', 'Action': 'lambda', 'lambda': 'detail_type', 'by': "x:x if x != '终端' else '管理终端'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[194]原语 node_type.detail_type = lambda detail_type by (x:x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'node_type', 'Action': 'union', 'union': 'node_type,node_type1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[195]原语 node_type= union node_type,node_type1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'node_type', 'as': "'detail_type':'type'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[196]原语 rename node_type as ("detail_type":"type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node', 'Action': 'join', 'join': 'node,node_type', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[197]原语 node = join node,node_type by type,type with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'edge.index.size == 0', 'with': 'node = @udf udf0.new_df with id,type,light,count,num'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[199]原语 if edge.index.size == 0 with node = @udf udf0.new_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'node', 'as': 'nodes'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[201]原语 push node as nodes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_nodes'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[202]原语 store node to ssdb by ssdb0 with link_nodes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_edge_open.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[209]原语 bb = @udf ZFile.rm_file with link/link_edge_open.p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_node_open.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[210]原语 bb = @udf ZFile.rm_file with link/link_node_open.p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[link_data.fbi]执行第[215]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],215

#主函数结束,开始块函数

def block_if_27(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'run', 'run': 'app_query.fbi', 'with': '@nodes = $d'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {} with {}'.format(ptree['run'],ptree['with']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第27行if语句中]执行第[28]原语 run app_query.fbi with @nodes = $d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_27

def block_if_else_27(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'node', 'Action': 'load', 'load': 'pq', 'by': 'link/link_type.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[29]原语 node = load pq by link/link_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'node_count', 'Action': 'load', 'load': 'pq', 'by': 'link/S_O_count.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[32]原语 node_count = load pq by link/S_O_count.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'node_count.S_count.O_count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[33]原语 alter node_count.S_count.O_count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_count', 'Action': 'add', 'add': 'count1', 'by': "df['S_count']+df['O_count']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[34]原语 node_count = add count1 by df["S_count"]+df["O_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node_count', 'Action': 'loc', 'loc': 'node_count', 'by': 'id,count1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[35]原语 node_count = loc node_count by id,count1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edges', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': "g.V().Tag('aaa').Out(['link_sql','link_http','link_http1','link_belong','link_belong1'],'path').GetLimit(1000000)"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[38]原语 edges = @udf GL.query_http_mkd with g.V().Tag("aaa... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'edge_text', 'Action': 'if', 'if': '$edges != None', 'with': 'edges = @udf edges by FBI.json2df'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[39]原语 edge_text = if $edges != None with edges = @udf ed... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'aa', 'Action': 'if', 'if': '$edge_text == False', 'with': 'edges = @udf udf0.new_df with (aaa,id,path)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[40]原语 aa = if $edge_text == False with edges = @udf udf0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edges', 'as': "'aaa':'S','id':'O','path':'P'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[41]原语 rename edges as ("aaa":"S","id":"O","path":"P") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'limit5', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj as nn from dbms_obj order by count desc limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[43]原语 limit5 = load db by mysql1 with select dbms_obj as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge1', 'Action': 'join', 'join': 'limit5,edges', 'by': 'nn,O', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[45]原语 edge1 = join limit5,edges by nn,O with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge1', 'Action': '@udf', '@udf': 'edge1', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[46]原语 edge1 = @udf edge1 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge1', 'Action': 'filter', 'filter': 'edge1', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[47]原语 edge1 = filter edge1 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge1', 'Action': 'loc', 'loc': 'edge1', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[48]原语 edge1 = loc edge1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge1', 'Action': 'join', 'join': 'edge1,node_count', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[50]原语 edge1 = join edge1,node_count by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'edge1', 'Action': 'order', 'order': 'edge1', 'by': 'count1', 'with': 'desc limit 100'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[51]原语 edge1 = order edge1 by count1 with desc limit 100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge1', 'Action': 'loc', 'loc': 'edge1', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[52]原语 edge1 = loc edge1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge1', 'Action': 'distinct', 'distinct': 'edge1', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[53]原语 edge1 = distinct edge1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'edge1', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[55]原语 dd = loc edge1 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dd', 'Action': 'distinct', 'distinct': 'dd', 'by': 'S'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[56]原语 dd = distinct dd by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dd', 'as': "'S':'dd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[57]原语 rename dd as ("S":"dd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge2', 'Action': 'join', 'join': 'dd,edges', 'by': 'dd,O', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[58]原语 edge2 = join dd,edges by dd,O with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge2', 'Action': '@udf', '@udf': 'edge2', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[59]原语 edge2 = @udf edge2 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge2', 'Action': 'filter', 'filter': 'edge2', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[60]原语 edge2 = filter edge2 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge2', 'Action': 'loc', 'loc': 'edge2', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[61]原语 edge2 = loc edge2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge2', 'Action': 'distinct', 'distinct': 'edge2', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[62]原语 edge2 = distinct edge2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge2', 'Action': 'join', 'join': 'edge2,node_count', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[64]原语 edge2 = join edge2,node_count by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'edge2', 'Action': 'order', 'order': 'edge2', 'by': 'count1', 'with': 'desc limit 100'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[65]原语 edge2 = order edge2 by count1 with desc limit 100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge2', 'Action': 'loc', 'loc': 'edge2', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[66]原语 edge2 = loc edge2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge2', 'Action': 'distinct', 'distinct': 'edge2', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[67]原语 edge2 = distinct edge2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'edge2', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[69]原语 dd = loc edge2 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dd', 'Action': 'distinct', 'distinct': 'dd', 'by': 'S'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[70]原语 dd = distinct dd by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dd', 'as': "'S':'dd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[71]原语 rename dd as ("S":"dd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge3', 'Action': 'join', 'join': 'dd,edges', 'by': 'dd,O', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[72]原语 edge3 = join dd,edges by dd,O with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge3', 'Action': '@udf', '@udf': 'edge3', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[73]原语 edge3 = @udf edge3 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge3', 'Action': 'filter', 'filter': 'edge3', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[74]原语 edge3 = filter edge3 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge3', 'Action': 'loc', 'loc': 'edge3', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[75]原语 edge3 = loc edge3 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge3', 'Action': 'join', 'join': 'edge3,node_count', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[77]原语 edge3 = join edge3,node_count by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'edge3', 'Action': 'order', 'order': 'edge3', 'by': 'count1', 'with': 'desc limit 100'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[78]原语 edge3 = order edge3 by count1 with desc limit 100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge3', 'Action': 'loc', 'loc': 'edge3', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[79]原语 edge3 = loc edge3 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge3', 'Action': 'distinct', 'distinct': 'edge3', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[80]原语 edge3 = distinct edge3 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'edge3', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[82]原语 dd = loc edge3 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dd', 'Action': 'distinct', 'distinct': 'dd', 'by': 'S'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[83]原语 dd = distinct dd by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dd', 'as': "'S':'dd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[84]原语 rename dd as ("S":"dd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge4', 'Action': 'join', 'join': 'dd,edges', 'by': 'dd,O', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[85]原语 edge4 = join dd,edges by dd,O with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge4', 'Action': '@udf', '@udf': 'edge4', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[86]原语 edge4 = @udf edge4 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge4', 'Action': 'filter', 'filter': 'edge4', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[87]原语 edge4 = filter edge4 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge4', 'Action': 'loc', 'loc': 'edge4', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[88]原语 edge4 = loc edge4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge4', 'Action': 'join', 'join': 'edge4,node_count', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[90]原语 edge4 = join edge4,node_count by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'edge4', 'Action': 'order', 'order': 'edge4', 'by': 'count1', 'with': 'desc limit 100'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[91]原语 edge4 = order edge4 by count1 with desc limit 100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge4', 'Action': 'loc', 'loc': 'edge4', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[92]原语 edge4 = loc edge4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge4', 'Action': 'distinct', 'distinct': 'edge4', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[93]原语 edge4 = distinct edge4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'edge', 'Action': 'union', 'union': 'edge1,edge2,edge3,edge4'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[95]原语 edge = union edge1,edge2,edge3,edge4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge', 'Action': 'loc', 'loc': 'edge', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[96]原语 edge = loc edge by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge_sql', 'Action': 'loc', 'loc': 'edge', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[98]原语 edge_sql = loc edge by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'edge_sql', 'Action': 'distinct', 'distinct': 'edge_sql', 'by': 'S'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[99]原语 edge_sql = distinct edge_sql by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge_sql', 'Action': 'join', 'join': 'edge_sql,node', 'by': 'S,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[100]原语 edge_sql = join edge_sql,node by S,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge_sql', 'Action': 'filter', 'filter': 'edge_sql', 'by': "type == '管理终端' or type == '业务终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[101]原语 edge_sql = filter edge_sql by type == "管理终端" or ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'edge_sql.index.size <= 10', 'with': '"'}
	try:
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[102]原语 if edge_sql.index.size <= 10 with " 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'edge_sql', 'Action': 'filter', 'filter': 'edge_sql', 'by': "type == '管理终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[103]原语 edge_sql = filter edge_sql by type == "管理终端" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'edge_sql', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[104]原语 dd = loc edge_sql by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dd', 'as': "'S':'dd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[105]原语 rename dd as ("S":"dd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'edge_sql', 'Action': 'join', 'join': 'dd,edges', 'by': 'dd,S', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[106]原语 edge_sql = join dd,edges by dd,S with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'edge_sql', 'Action': 'loc', 'loc': 'edge_sql', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[107]原语 edge_sql = loc edge_sql by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'edge', 'Action': 'union', 'union': 'edge,edge_sql'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第27行if_else语句中]执行第[108]原语 edge = union edge,edge_sql 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_27

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



