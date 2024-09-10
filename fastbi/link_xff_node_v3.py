#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: link_xff_node
#datetime: 2024-08-30T16:10:53.147324
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
		add_the_error('[link_xff_node.fbi]执行第[11]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'edge', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': "g.V().Tag('aaa').Out(['acc_xff','link_xff','xff_ip','link_x_http','link_x_http1'],'path').GetLimit(1000000)"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[12]原语 edge = @udf GL.query_http_mkd with g.V().Tag("aaa"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'edge_text', 'Action': 'if', 'if': '$edge != None', 'with': 'edge = @udf edge by FBI.json2df'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=13
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[13]原语 edge_text = if $edge != None with edge = @udf edge... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'edge', 'as': "'aaa':'S','id':'O','path':'P'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[14]原语 rename edge as ("aaa":"S","id":"O","path":"P") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'edge.P', 'Action': 'str', 'str': 'P', 'by': "replace('1','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[15]原语 edge.P = str P by replace("1","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'edge.P', 'Action': 'str', 'str': 'P', 'by': "replace('link_xff','xff_ip')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[16]原语 edge.P = str P by replace("link_xff","xff_ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's11', 'Action': 'loc', 'loc': 'edge', 'by': 'S,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[18]原语 s11 = loc edge by S,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 's', 'Action': 'group', 'group': 's11', 'by': 'S,P', 'agg': 'S:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[19]原语 s = group s11 by S,P agg S:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[20]原语 s = loc s by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 's1', 'Action': 'group', 'group': 's11', 'by': 'S', 'agg': 'S:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[21]原语 s1 = group s11 by S agg S:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's1', 'Action': 'loc', 'loc': 's1', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[22]原语 s1 = loc s1 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'qw', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,http访问(出),代理(出),访问(从属)_1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[23]原语 qw = @udf udf0.new_df with (id,http访问(出),代理(出),访问(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 's', 'with': 'id = $1', 'run': '""\naa = filter s by id == \'@id\'\naa = loc aa by idx1 to index\naa = loc aa by S_count\naa = @udf aa by udf0.df_T\nrename aa as (\'xff_ip\':\'代理(出)\',\'link_x_http\':\'http访问(出)\',\'acc_xff\':\'访问(从属)_1\')\naa = add id by (\'@id\')\nqw = union qw,aa\nqw = distinct qw by id,http访问(出),代理(出),访问(从属)_1\n""'}
	try:
		ptree['lineno']=24
		ptree['funs']=block_foreach_24
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[24]原语 foreach s run "aa = filter s by id == "@id"aa = lo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'o11', 'Action': 'loc', 'loc': 'edge', 'by': 'O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[35]原语 o11 = loc edge by O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'o', 'Action': 'group', 'group': 'o11', 'by': 'O,P', 'agg': 'O:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[36]原语 o = group o11 by O,P agg O:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'o', 'Action': 'loc', 'loc': 'o', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[37]原语 o = loc o by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'o1', 'Action': 'group', 'group': 'o11', 'by': 'O', 'agg': 'O:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[38]原语 o1 = group o11 by O agg O:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'o1', 'Action': 'loc', 'loc': 'o1', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[39]原语 o1 = loc o1 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'kkkk', 'Action': 'join', 'join': 's1,o1', 'by': 'id,id', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[40]原语 kkkk = join s1,o1 by id,id with outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'kkkk', 'Action': '@udf', '@udf': 'kkkk', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[41]原语 kkkk = @udf kkkk by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'kkkk', 'to': 'pq', 'by': 'link/S_O_xff_count.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[42]原语 store kkkk to pq by link/S_O_xff_count.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'qw1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,http访问(入),代理(入),访问(从属)_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[43]原语 qw1 = @udf udf0.new_df with (id,http访问(入),代理(入),访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'o', 'with': 'id = $1', 'run': '""\naa1 = filter o by id == \'@id\'\naa1 = loc aa1 by idx1 to index\naa1 = loc aa1 by O_count\naa1 = @udf aa1 by udf0.df_T\nrename aa1 as (\'xff_ip\':\'代理(入)\',\'link_x_http\':\'http访问(入)\',\'acc_xff\':\'访问(从属)_2\')\naa1 = add id by (\'@id\')\nqw1 = union qw1 ,aa1\nqw1 = distinct qw1 by id,http访问(入),代理(入),访问(从属)_2\n""'}
	try:
		ptree['lineno']=44
		ptree['funs']=block_foreach_44
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[44]原语 foreach o run "aa1 = filter o by id == "@id"aa1 = ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zs', 'Action': 'join', 'join': 'qw,qw1', 'by': 'id,id', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[54]原语 zs = join qw,qw1 by id,id with  outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zs', 'Action': '@udf', '@udf': 'zs', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[55]原语 zs = @udf zs by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zs', 'Action': 'add', 'add': '访问(从属)', 'by': "df['访问(从属)_1']+df['访问(从属)_2']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[56]原语 zs = add 访问(从属) by df["访问(从属)_1"]+df["访问(从属)_2"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zs', 'Action': 'loc', 'loc': 'zs', 'by': 'id,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[57]原语 zs = loc zs by id,http访问(出),代理(出),http访问(入),代理(入),... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ttt', 'Action': 'load', 'load': 'pq', 'by': 'link/ip_type.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[60]原语 ttt = load pq by link/ip_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'qqq', 'Action': 'group', 'group': 'ttt', 'by': 'type', 'agg': 'type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[62]原语 qqq = group ttt by type  agg type:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ttt1', 'Action': 'filter', 'filter': 'ttt', 'by': "type == '应用账号'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[64]原语 ttt1 = filter ttt by type == "应用账号" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ttt1', 'as': "'id':'account'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[65]原语 rename ttt1 as ("id":"account") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'acc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select account,dept,active,type 类型 from data_account_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[66]原语 acc = load db by mysql1 with select account,dept,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[67]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'acc.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[68]原语 alter acc.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'acc', 'Action': '@udf', '@udf': 'acc,active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[69]原语 acc = @udf acc,active by SP.tag2dict with active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'ttt1,acc', 'by': 'account,account', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[70]原语 account = join ttt1,acc by account,account with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[71]原语 account = @udf account by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'id,account,type,dept,active,类型'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[72]原语 account = loc account by id,account,type,dept,acti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'account ,zs', 'by': 'account,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[73]原语 account = join account ,zs by account,id with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[74]原语 account = @udf account by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'account,type,dept,类型,active,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[75]原语 account = loc account by account,type,dept,类型,acti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account', 'as': "'account':'节点名称','type':'节点类型','dept':'部门','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[76]原语 rename account as ("account":"节点名称","type":"节点类型",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'ttt1', 'with': 'id = $1', 'run': '""\nnode = filter account by 节点名称 == \'@id\'\nstore node to ssdb by ssdb0 with link_xff:@id\n""'}
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
		add_the_error('[link_xff_node.fbi]执行第[77]原语 foreach ttt1 run "node = filter account by 节点名称 ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ttt2', 'Action': 'filter', 'filter': 'ttt', 'by': "type == '终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[83]原语 ttt2 = filter ttt by type == "终端" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select srcip id,visit_flow,dep,active,type type1,visit_num,flag 标签备注 from data_ip_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[84]原语 src = load db by mysql1 with select srcip id,visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active2', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[85]原语 active2 = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'src.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[86]原语 alter src.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'src', 'Action': '@udf', '@udf': 'src,active2', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[87]原语 src = @udf src,active2 by SP.tag2dict with active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'ttt2,src', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[88]原语 account = join ttt2,src by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[89]原语 account = @udf account by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'account ,zs', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[90]原语 account = join account ,zs by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[91]原语 account = @udf account by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'id,type,dep,type1,标签备注,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[92]原语 account = loc account by id,type,dep,type1,标签备注,ht... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account', 'as': "'id':'节点名称','type':'节点类型','dep':'部门','type1':'终端类型','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[93]原语 rename account as ("id":"节点名称","type":"节点类型","dep"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'ttt2', 'with': 'id = $1', 'run': '""\nnode = filter account by 节点名称 == \'@id\'\nstore node to ssdb by ssdb0 with link_xff:@id\n""'}
	try:
		ptree['lineno']=94
		ptree['funs']=block_foreach_94
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[94]原语 foreach ttt2 run "node = filter account by 节点名称 ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ttt3', 'Action': 'filter', 'filter': 'ttt', 'by': "type == '接口'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[102]原语 ttt3 = filter ttt by type == "接口" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select url id,method,active ,api_type from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[103]原语 src = load db by mysql1 with select url id,method,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active2', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[104]原语 active2 = load ssdb by ssdb0 with dd:API-api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'src.api_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[105]原语 alter src.api_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'src', 'Action': '@udf', '@udf': 'src,active2', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[106]原语 src = @udf src,active2 by SP.tag2dict with api_typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'src.id', 'Action': 'lambda', 'lambda': 'id', 'by': " x:x.split('/')[2] "}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[107]原语 src.id = lambda id by ( x:x.split("/")[2] ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'src.id', 'Action': 'lambda', 'lambda': 'id', 'by': " x:x.split(':')[0] "}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[108]原语 src.id = lambda id by ( x:x.split(":")[0] ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active2', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[109]原语 active2 = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'src.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[110]原语 alter src.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'src', 'Action': '@udf', '@udf': 'src,active2', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[111]原语 src = @udf src,active2 by SP.tag2dict with active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'src_count', 'Action': 'group', 'group': 'src', 'by': 'id,api_type', 'agg': 'api_type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[112]原语 src_count = group src by id,api_type agg api_type:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'src_count', 'Action': 'loc', 'loc': 'src_count', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[113]原语 src_count = loc src_count by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'src_count', 'Action': 'add', 'add': 'id', 'by': "src_count.id + '-' + src_count.idx1 +'接口' "}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[114]原语 src_count = add id by (src_count.id  + "-" + src_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'src_count', 'Action': 'loc', 'loc': 'src_count', 'by': 'id ,api_type_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[115]原语 src_count = loc src_count by id ,api_type_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'src', 'Action': 'add', 'add': 'id', 'by': "src.id + '-' + src.api_type +'接口' "}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[116]原语 src = add id by (src.id  + "-" + src.api_type +"接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'src', 'Action': 'join', 'join': 'src ,src_count', 'by': 'id,id', 'with': 'inner'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[117]原语 src = join src ,src_count by id,id with inner 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'src', 'Action': 'distinct', 'distinct': 'src', 'by': 'id,method,active ,api_type,api_type_count'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[118]原语 src = distinct src by id,method,active ,api_type,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'ttt3,src', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[120]原语 account = join ttt3,src by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[121]原语 account = @udf account by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'account ,zs', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[122]原语 account = join account ,zs by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[123]原语 account = @udf account by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'id,type,method,api_type_count,active,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[124]原语 account = loc account by id,type,method,api_type_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account', 'as': "'id':'节点名称','type':'节点类型','method':'请求类型','api_type_count':'接口数量','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[125]原语 rename account as ("id":"节点名称","type":"节点类型","meth... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'ttt3', 'with': 'id = $1', 'run': '""\nnode = filter account by 节点名称 == \'@id\'\nstore node to ssdb by ssdb0 with link_xff:@id\n""'}
	try:
		ptree['lineno']=126
		ptree['funs']=block_foreach_126
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[126]原语 foreach ttt3 run "node = filter account by 节点名称 ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ttt4', 'Action': 'filter', 'filter': 'ttt', 'by': "type == '应用'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[133]原语 ttt4 = filter ttt by type == "应用" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app id,dstip_num,active,api_num from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[134]原语 src = load db by mysql1 with select app id,dstip_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'src.id', 'Action': 'lambda', 'lambda': 'id', 'by': " x:x.split(':')[0] "}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[136]原语 src.id = lambda id by ( x:x.split(":")[0] ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active2', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[137]原语 active2 = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'src.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[138]原语 alter src.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'src', 'Action': '@udf', '@udf': 'src,active2', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[139]原语 src = @udf src,active2 by SP.tag2dict with active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'ttt4,src', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[140]原语 account = join ttt4,src by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[141]原语 account = @udf account by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'account ,zs', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[142]原语 account = join account ,zs by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[143]原语 account = @udf account by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'id,type,dstip_num,api_num,active,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[144]原语 account = loc account by id,type,dstip_num,api_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account', 'as': "'id':'节点名称','type':'节点类型','dstip_num':'部署数量','api_num':'接口数量','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[145]原语 rename account as ("id":"节点名称","type":"节点类型","dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'ttt4', 'with': 'id = $1', 'run': '""\nnode = filter account by 节点名称 == \'@id\'\nstore node to ssdb by ssdb0 with link_xff:@id\n""'}
	try:
		ptree['lineno']=146
		ptree['funs']=block_foreach_146
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[146]原语 foreach ttt4 run "node = filter account by 节点名称 ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ttt5', 'Action': 'filter', 'filter': 'ttt', 'by': "type == '代理'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[152]原语 ttt5 = filter ttt by type == "代理" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select srcip id,visit_flow,dep,active,type type1,visit_num,flag 标签备注 from data_ip_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[155]原语 src = load db by mysql1 with select srcip id,visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'ttt5,src', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[156]原语 account = join ttt5,src by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[157]原语 account = @udf account by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'account ,zs', 'by': 'id,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[158]原语 account = join account ,zs by id,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[159]原语 account = @udf account by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'id,type,dep,type1,标签备注,http访问(出),代理(出),http访问(入),代理(入),访问(从属)'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[160]原语 account = loc account by id,type,dep,type1,标签备注,ht... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account', 'as': "'id':'节点名称','type':'节点类型','dep':'部门','type1':'终端类型'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[161]原语 rename account as ("id":"节点名称","type":"节点类型","dep"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'ttt5', 'with': 'id = $1', 'run': '""\nnode = filter account by 节点名称 == \'@id\'\nstore node to ssdb by ssdb0 with link_xff:@id\n""'}
	try:
		ptree['lineno']=162
		ptree['funs']=block_foreach_162
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[162]原语 foreach ttt5 run "node = filter account by 节点名称 ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[link_xff_node.fbi]执行第[167]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],167

#主函数结束,开始块函数

def block_foreach_24(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa', 'Action': 'filter', 'filter': 's', 'by': "id == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[25]原语 aa = filter s by id == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'aa', 'by': 'idx1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[26]原语 aa = loc aa by idx1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'aa', 'by': 'S_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[27]原语 aa = loc aa by S_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[28]原语 aa = @udf aa by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'aa', 'as': "'xff_ip':'代理(出)','link_x_http':'http访问(出)','acc_xff':'访问(从属)_1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[29]原语 rename aa as ("xff_ip":"代理(出)","link_x_http":"http... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'aa', 'Action': 'add', 'add': 'id', 'by': "'@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[30]原语 aa = add id by ("@id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'qw', 'Action': 'union', 'union': 'qw,aa'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[31]原语 qw = union qw,aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'qw', 'Action': 'distinct', 'distinct': 'qw', 'by': 'id,http访问(出),代理(出),访问(从属)_1'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第24行foreach语句中]执行第[32]原语 qw = distinct qw by id,http访问(出),代理(出),访问(从属)_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_24

def block_foreach_44(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa1', 'Action': 'filter', 'filter': 'o', 'by': "id == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[45]原语 aa1 = filter o by id == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa1', 'Action': 'loc', 'loc': 'aa1', 'by': 'idx1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[46]原语 aa1 = loc aa1 by idx1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa1', 'Action': 'loc', 'loc': 'aa1', 'by': 'O_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[47]原语 aa1 = loc aa1 by O_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa1', 'Action': '@udf', '@udf': 'aa1', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[48]原语 aa1 = @udf aa1 by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'aa1', 'as': "'xff_ip':'代理(入)','link_x_http':'http访问(入)','acc_xff':'访问(从属)_2'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[49]原语 rename aa1 as ("xff_ip":"代理(入)","link_x_http":"htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'aa1', 'Action': 'add', 'add': 'id', 'by': "'@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[50]原语 aa1 = add id by ("@id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'qw1', 'Action': 'union', 'union': 'qw1 ,aa1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[51]原语 qw1 = union qw1 ,aa1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'qw1', 'Action': 'distinct', 'distinct': 'qw1', 'by': 'id,http访问(入),代理(入),访问(从属)_2'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第44行foreach语句中]执行第[52]原语 qw1 = distinct qw1 by id,http访问(入),代理(入),访问(从属)_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_44

def block_foreach_77(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node', 'Action': 'filter', 'filter': 'account', 'by': "节点名称 == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[78]原语 node = filter account by 节点名称 == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第77行foreach语句中]执行第[79]原语 store node to ssdb by ssdb0 with link_xff:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_77

def block_foreach_94(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node', 'Action': 'filter', 'filter': 'account', 'by': "节点名称 == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[95]原语 node = filter account by 节点名称 == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第94行foreach语句中]执行第[96]原语 store node to ssdb by ssdb0 with link_xff:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_94

def block_foreach_126(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node', 'Action': 'filter', 'filter': 'account', 'by': "节点名称 == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第126行foreach语句中]执行第[127]原语 node = filter account by 节点名称 == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第126行foreach语句中]执行第[128]原语 store node to ssdb by ssdb0 with link_xff:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_126

def block_foreach_146(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node', 'Action': 'filter', 'filter': 'account', 'by': "节点名称 == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第146行foreach语句中]执行第[147]原语 node = filter account by 节点名称 == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第146行foreach语句中]执行第[148]原语 store node to ssdb by ssdb0 with link_xff:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_146

def block_foreach_162(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node', 'Action': 'filter', 'filter': 'account', 'by': "节点名称 == '@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第162行foreach语句中]执行第[163]原语 node = filter account by 节点名称 == "@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第162行foreach语句中]执行第[164]原语 store node to ssdb by ssdb0 with link_xff:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_162

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



