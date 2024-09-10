#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: dbms_tree
#datetime: 2024-08-30T16:10:55.619701
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
		add_the_error('[dbms_tree.fbi]执行第[10]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'sen_label_tree.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[12]原语 run sen_label_tree.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'ID,tree_name,parent_id,tree_url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[14]原语 df = @udf udf0.new_df with (ID,tree_name,parent_id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_append', 'with': '全部,全部,0,modeling:dbms_user&ifQuery'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[15]原语 df = @udf df by udf0.df_append with (全部,全部,0,model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct db_type ID,db_type tree_name from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[17]原语 dbms_type = load db by mysql1 with select distinct... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms_type', 'Action': 'add', 'add': 'parent_id', 'by': '"全部"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[18]原语 dbms_type = add parent_id by ("全部") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dbms_type.tree_url', 'Action': 'lambda', 'lambda': 'tree_name', 'by': 'x: "modeling:dbms_user&@db_type=" + x +"&ifQuery"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[19]原语 dbms_type.tree_url = lambda tree_name by x: "model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct dbms_obj ID,dbms_obj tree_name,db_type parent_id from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[22]原语 dbms_obj = load db by mysql1 with select distinct ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dbms_obj.tree_url', 'Action': 'lambda', 'lambda': 'tree_name', 'by': 'x: "modeling:dbms_user&@dbms_obj=" + x +"&ifQuery"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[23]原语 dbms_obj.tree_url = lambda tree_name by x: "modeli... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_sql', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct dbms_obj parent_id,user tree_name from dbms_user where user != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[25]原语 dbms_sql = load db by mysql1 with select distinct ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms_sql', 'Action': 'add', 'add': 'ID', 'by': 'dbms_sql.index +1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[26]原语 dbms_sql = add ID by dbms_sql.index +1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms_sql', 'Action': '@udf', '@udf': 'dbms_sql', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:dbms_sql&@user=" + x["tree_name"] +"&@dbms_obj=" + x["parent_id"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[27]原语 dbms_sql = @udf dbms_sql by udf0.df_row_lambda wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbms_sql', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[28]原语 rename dbms_sql as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tree', 'Action': 'union', 'union': 'dbms_type,dbms_obj,dbms_sql,df'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[29]原语 tree = union dbms_type,dbms_obj,dbms_sql,df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tree.ID', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[30]原语 alter tree.ID as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tree.parent_id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[31]原语 alter tree.parent_id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tree', 'Action': '@udf', '@udf': 'tree', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[32]原语 tree = @udf tree by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tree', 'Action': 'loc', 'loc': 'tree', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[33]原语 tree = loc tree drop index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tree', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:data_dbms_obj_tree'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[34]原语 store tree to ssdb by ssdb0 with dd:data_dbms_obj_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'db_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct db_type from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[37]原语 db_type = load db by mysql1 with select distinct d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db_type', 'Action': '@udf', '@udf': 'db_type', 'by': 'udf0.df_set_index', 'with': 'db_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[38]原语 db_type = @udf db_type by udf0.df_set_index with d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'db_type', 'Action': 'add', 'add': 'db_type', 'by': 'db_type.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[39]原语 db_type = add db_type by db_type.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'db_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:db_type'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[40]原语 store db_type to ssdb by ssdb0 with dd:db_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo_proto', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct app_proto ID,app_proto tree_name from fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[43]原语 fileinfo_proto = load db by mysql1 with select dis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo_proto', 'Action': 'add', 'add': 'parent_id', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[44]原语 fileinfo_proto = add parent_id by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'fileinfo_proto.tree_url', 'Action': 'lambda', 'lambda': 'tree_name', 'by': 'x: "modeling:fileinfo&@app_proto=" + x +"&ifQuery"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[45]原语 fileinfo_proto.tree_url = lambda tree_name by x: "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct type ID,type tree_name,app_proto parent_id from fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[47]原语 fileinfo_type = load db by mysql1 with select dist... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'fileinfo_type', 'Action': '@udf', '@udf': 'fileinfo_type', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:fileinfo&@app_proto=" + x["parent_id"] +"&@type=" + x["tree_name"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[48]原语 fileinfo_type = @udf fileinfo_type by udf0.df_row_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fileinfo_type', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[49]原语 rename fileinfo_type as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo_distip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct type parent_id,dstip tree_name from fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[51]原语 fileinfo_distip = load db by mysql1 with select di... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo_distip', 'Action': 'add', 'add': 'ID', 'by': 'fileinfo_distip.index +1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[52]原语 fileinfo_distip = add ID by fileinfo_distip.index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'fileinfo_distip', 'Action': '@udf', '@udf': 'fileinfo_distip', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:fileinfo&@dstip=" + x["tree_name"] +"&@type=" + x["parent_id"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[53]原语 fileinfo_distip = @udf fileinfo_distip by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fileinfo_distip', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[54]原语 rename fileinfo_distip as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tree', 'Action': 'union', 'union': 'fileinfo_proto,fileinfo_type,fileinfo_distip'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[55]原语 tree = union fileinfo_proto,fileinfo_type,fileinfo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tree.ID', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[56]原语 alter tree.ID as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tree.parent_id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[57]原语 alter tree.parent_id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'tree', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:data_fileinfo_tree'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[58]原语 store tree to ssdb by ssdb0 with dd:data_fileinfo_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'qh_json.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[62]原语 run qh_json.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_class', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[63]原语 sen_class = load ssdb by ssdb0 with dd:reqs_label1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_class', 'as': '"class":"ID"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[64]原语 rename sen_class as ("class":"ID") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_class', 'Action': 'add', 'add': 'tree_name', 'by': 'sen_class.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[65]原语 sen_class = add tree_name by sen_class.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_class', 'Action': '@udf', '@udf': 'sen_class', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[66]原语 sen_class = @udf sen_class by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_class', 'Action': 'add', 'add': 'parent_id', 'by': 'sen_class.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[67]原语 sen_class = add parent_id by sen_class.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_class', 'Action': 'loc', 'loc': 'sen_class', 'drop': 'data'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[68]原语 sen_class = loc sen_class drop data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sen_class', 'Action': 'distinct', 'distinct': 'sen_class', 'by': 'ID'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[69]原语 sen_class = distinct sen_class by ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_class.parent_id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[70]原语 alter sen_class.parent_id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_class.tree_url', 'Action': 'lambda', 'lambda': 'tree_name', 'by': 'x: "modeling:sen_class&@obj=" + x +"&ifQuery"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[71]原语 sen_class.tree_url = lambda tree_name by x: "model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_label', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[73]原语 sen_label = load ssdb by ssdb0 with dd:reqs_label1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_label', 'Action': 'add', 'add': 'ID', 'by': 'sen_label.data'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[74]原语 sen_label = add ID by sen_label.data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_label', 'Action': 'add', 'add': 'tree_name', 'by': 'sen_label.data'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[75]原语 sen_label = add tree_name by sen_label.data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_label', 'as': '"class":"parent_id"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[78]原语 rename sen_label as ("class":"parent_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_label', 'Action': 'loc', 'loc': 'sen_label', 'drop': 'data,class'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[79]原语 sen_label = loc sen_label drop data,class 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_label.parent_id', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[80]原语 alter sen_label.parent_id as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_label.tree_url', 'Action': 'lambda', 'lambda': 'tree_name', 'by': 'x: "modeling:sen_obj&@sen_key=" + x +"&ifQuery"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[81]原语 sen_label.tree_url = lambda tree_name by x: "model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select CONCAT(sen_key,type) ID,type tree_name,sen_key parent_id from sen_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[83]原语 sen_type = load db by mysql1 with select CONCAT(se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_type', 'Action': '@udf', '@udf': 'sen_type', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:sen_type&@sen_key=" + x["parent_id"] +"&@type="+ x["tree_name"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[84]原语 sen_type = @udf sen_type by udf0.df_row_lambda wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_type', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[85]原语 rename sen_type as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,sen_type'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[86]原语 sen_label = union sen_label,sen_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_app_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[91]原语 label_app = load db by mysql1 with select sen_key ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_app', 'Action': '@udf', '@udf': 'label_app', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[93]原语 label_app = @udf label_app by udf0.df_fillna with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_app', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[94]原语 alter label_app by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_app', 'Action': 'add', 'add': 'ID', 'by': '"应用(" + label_app.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[95]原语 label_app = add ID by ("应用(" + label_app.ID +")") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_app', 'Action': 'add', 'add': 'tree_name', 'by': 'label_app.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[96]原语 label_app = add tree_name by label_app.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_app', 'Action': 'add', 'add': 'ID', 'by': 'label_app.ID + label_app.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[97]原语 label_app = add ID by label_app.ID + label_app.par... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_app', 'Action': '@udf', '@udf': 'label_app', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:app_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[98]原语 label_app = @udf label_app by udf0.df_row_lambda w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_app', 'Action': 'loc', 'loc': 'label_app', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[99]原语 label_app = loc label_app drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_app', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[100]原语 rename label_app as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_app'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[101]原语 sen_label = union sen_label,label_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_api_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[105]原语 label_api = load db by mysql1 with select sen_key ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_api', 'Action': '@udf', '@udf': 'label_api', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[107]原语 label_api = @udf label_api by udf0.df_fillna with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_api', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[108]原语 alter label_api by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_api', 'Action': 'add', 'add': 'ID', 'by': '"接口(" + label_api.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[109]原语 label_api = add ID by ("接口(" + label_api.ID +")") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_api', 'Action': 'add', 'add': 'tree_name', 'by': 'label_api.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[110]原语 label_api = add tree_name by label_api.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_api', 'Action': 'add', 'add': 'ID', 'by': 'label_api.ID + label_api.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[111]原语 label_api = add ID by label_api.ID + label_api.par... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_api', 'Action': '@udf', '@udf': 'label_api', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:api_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[112]原语 label_api = @udf label_api by udf0.df_row_lambda w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_api', 'Action': 'loc', 'loc': 'label_api', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[113]原语 label_api = loc label_api drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_api', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[114]原语 rename label_api as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_api'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[115]原语 sen_label = union sen_label,label_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_acc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_acc_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[119]原语 label_acc = load db by mysql1 with select sen_key ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_acc', 'Action': '@udf', '@udf': 'label_acc', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[121]原语 label_acc = @udf label_acc by udf0.df_fillna with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_acc', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[122]原语 alter label_acc by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_acc', 'Action': 'add', 'add': 'ID', 'by': '"应用账号(" + label_acc.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[123]原语 label_acc = add ID by ("应用账号(" + label_acc.ID +")"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_acc', 'Action': 'add', 'add': 'tree_name', 'by': 'label_acc.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[124]原语 label_acc = add tree_name by label_acc.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_acc', 'Action': 'add', 'add': 'ID', 'by': 'label_acc.ID + label_acc.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[125]原语 label_acc = add ID by label_acc.ID + label_acc.par... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_acc', 'Action': '@udf', '@udf': 'label_acc', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:acc_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[126]原语 label_acc = @udf label_acc by udf0.df_row_lambda w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_acc', 'Action': 'loc', 'loc': 'label_acc', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[127]原语 label_acc = loc label_acc drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_acc', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[128]原语 rename label_acc as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_acc'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[129]原语 sen_label = union sen_label,label_acc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_src_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[133]原语 label_src = load db by mysql1 with select sen_key ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_src', 'Action': '@udf', '@udf': 'label_src', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[135]原语 label_src = @udf label_src by udf0.df_fillna with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_src', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[136]原语 alter label_src by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_src', 'Action': 'add', 'add': 'ID', 'by': '"终端(" + label_src.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[137]原语 label_src = add ID by ("终端(" + label_src.ID +")") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_src', 'Action': 'add', 'add': 'tree_name', 'by': 'label_src.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[138]原语 label_src = add tree_name by label_src.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_src', 'Action': 'add', 'add': 'ID', 'by': 'label_src.ID + label_src.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[139]原语 label_src = add ID by label_src.ID + label_src.par... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_src', 'Action': '@udf', '@udf': 'label_src', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:src_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[140]原语 label_src = @udf label_src by udf0.df_row_lambda w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_src', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[141]原语 rename label_src as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_src'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[142]原语 sen_label = union sen_label,label_src 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_dbms_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[146]原语 label_dbms = load db by mysql1 with select sen_key... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_dbms', 'Action': '@udf', '@udf': 'label_dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[148]原语 label_dbms = @udf label_dbms by udf0.df_fillna wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_dbms', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[149]原语 alter label_dbms by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbms', 'Action': 'add', 'add': 'ID', 'by': '"数据库对象(" + label_dbms.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[150]原语 label_dbms = add ID by ("数据库对象(" + label_dbms.ID +... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbms', 'Action': 'add', 'add': 'tree_name', 'by': 'label_dbms.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[151]原语 label_dbms = add tree_name by label_dbms.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbms', 'Action': 'add', 'add': 'ID', 'by': 'label_dbms.ID + label_dbms.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[152]原语 label_dbms = add ID by label_dbms.ID + label_dbms.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_dbms', 'Action': '@udf', '@udf': 'label_dbms', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:dbms_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[153]原语 label_dbms = @udf label_dbms by udf0.df_row_lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_dbms', 'Action': 'loc', 'loc': 'label_dbms', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[154]原语 label_dbms = loc label_dbms drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_dbms', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[155]原语 rename label_dbms as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_dbms'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[156]原语 sen_label = union sen_label,label_dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_dbuser', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_dbuser_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[160]原语 label_dbuser = load db by mysql1 with select sen_k... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_dbuser', 'Action': '@udf', '@udf': 'label_dbuser', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[162]原语 label_dbuser = @udf label_dbuser by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_dbuser', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[163]原语 alter label_dbuser by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbuser', 'Action': 'add', 'add': 'ID', 'by': '"数据库账号(" + label_dbuser.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[164]原语 label_dbuser = add ID by ("数据库账号(" + label_dbuser.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbuser', 'Action': 'add', 'add': 'tree_name', 'by': 'label_dbuser.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[165]原语 label_dbuser = add tree_name by label_dbuser.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_dbuser', 'Action': 'add', 'add': 'ID', 'by': 'label_dbuser.ID + label_dbuser.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[166]原语 label_dbuser = add ID by label_dbuser.ID + label_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_dbuser', 'Action': '@udf', '@udf': 'label_dbuser', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:dbuser_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[167]原语 label_dbuser = @udf label_dbuser by udf0.df_row_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_dbuser', 'Action': 'loc', 'loc': 'label_dbuser', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[168]原语 label_dbuser = loc label_dbuser drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_dbuser', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[169]原语 rename label_dbuser as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_dbuser'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[170]原语 sen_label = union sen_label,label_dbuser 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_file', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key tree_name,count(id) ID,CONCAT(sen_key, type) parent_id,type,sen_key from sen_file_tree group by sen_key,parent_id,type,sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[174]原语 label_file = load db by mysql1 with select sen_key... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_file', 'Action': '@udf', '@udf': 'label_file', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[176]原语 label_file = @udf label_file by udf0.df_fillna wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'label_file', 'by': 'type:str,sen_key:str,ID:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[177]原语 alter label_file by type:str,sen_key:str,ID:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_file', 'Action': 'add', 'add': 'ID', 'by': '"文件对象(" + label_file.ID +\')\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[178]原语 label_file = add ID by ("文件对象(" + label_file.ID +"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_file', 'Action': 'add', 'add': 'tree_name', 'by': 'label_file.ID'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[179]原语 label_file = add tree_name by label_file.ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'label_file', 'Action': 'add', 'add': 'ID', 'by': 'label_file.ID + label_file.parent_id'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[180]原语 label_file = add ID by label_file.ID + label_file.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label_file', 'Action': '@udf', '@udf': 'label_file', 'by': 'udf0.df_row_lambda', 'with': 'x: "modeling:file_sen_tree&@sen_key=" + x["sen_key"] +"&@type="+ x["type"] +"&ifQuery"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[181]原语 label_file = @udf label_file by udf0.df_row_lambda... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label_file', 'Action': 'loc', 'loc': 'label_file', 'drop': 'sen_key,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[182]原语 label_file = loc label_file drop sen_key,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label_file', 'as': '"lambda1":"tree_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[183]原语 rename label_file as ("lambda1":"tree_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sen_label', 'Action': 'union', 'union': 'sen_label,label_file,sen_class'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[184]原语 sen_label = union sen_label,label_file,sen_class 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sen_label', 'Action': 'distinct', 'distinct': 'sen_label', 'by': 'parent_id,ID'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[185]原语 sen_label = distinct sen_label by parent_id,ID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_label', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:data_label_tree'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[187]原语 store sen_label to ssdb by ssdb0 with dd:data_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[dbms_tree.fbi]执行第[193]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],193

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



