#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/ML_studio
#datetime: 2024-08-30T16:10:57.162471
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
	
	
	ptree={'runtime': runtime, 'Action': 'use', 'use': 'pub'}
	try:
		use_fun(ptree)
		workspace=ptree['work_space']
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[6]原语 use pub 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ML.load_A'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[8]原语 a =@udf  ML.load_A 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'a', 'as': '0:"0",1:"1",2:"2",3:"3"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[9]原语 rename a as (0:"0",1:"1",2:"2",3:"3") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'types', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_types'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[10]原语 types = @udf a by udf0.df_types 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'a', 'by': '0,1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[13]原语 a1 = loc a by (0,1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A:1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[14]原语 store a1 to ssdb by ssdb0 with A:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a2', 'Action': 'loc', 'loc': 'a', 'by': '1,2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[15]原语 a2 = loc a by (1,2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A:2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[16]原语 store a2 to ssdb by ssdb0 with A:2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a3', 'Action': 'loc', 'loc': 'a', 'by': '2,3'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[17]原语 a3 = loc a by (2,3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A:3'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[18]原语 store a3 to ssdb by ssdb0 with A:3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a4', 'Action': 'loc', 'loc': 'a', 'by': '3,0'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[19]原语 a4 = loc a by (3,0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A:4'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[20]原语 store a4 to ssdb by ssdb0 with A:4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'df0@sys', 'by': 'ML.load_A', 'with': 'target'}
	ptree['@udf'] = replace_ps(ptree['@udf'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[23]原语 c = @udf df0@sys by ML.load_A with target 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ac1', 'Action': 'join', 'join': 'a1,c', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[24]原语 ac1 = join a1,c by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ac1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'AC:1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[25]原语 store ac1 to ssdb by ssdb0 with AC:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ac2', 'Action': 'join', 'join': 'a2,c', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[26]原语 ac2 = join a2,c by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ac2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'AC:2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[27]原语 store ac2 to ssdb by ssdb0 with AC:2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ac3', 'Action': 'join', 'join': 'a3,c', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[28]原语 ac3 = join a3,c by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ac3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'AC:3'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[29]原语 store ac3 to ssdb by ssdb0 with AC:3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ac4', 'Action': 'join', 'join': 'a4,c', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[30]原语 ac4 = join a4,c by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ac4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'AC:4'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[31]原语 store ac4 to ssdb by ssdb0 with AC:4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'mk', 'Action': '@udf', '@udf': 'a', 'by': 'ML.kmeans', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[34]原语 mk = @udf a by ML.kmeans with (3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'mk', 'Action': 'join', 'join': 'a,mk', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[36]原语 mk = join a,mk by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mk1', 'Action': 'loc', 'loc': 'mk', 'by': '0,1,k'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[37]原语 mk1 = loc mk by (0,1,k) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'mk1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'MK:1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[38]原语 store mk1 to ssdb by ssdb0 with MK:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mk2', 'Action': 'loc', 'loc': 'mk', 'by': '1,2,k'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[39]原语 mk2 = loc mk by (1,2,k) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'mk2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'MK:2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[40]原语 store mk2 to ssdb by ssdb0 with MK:2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mk3', 'Action': 'loc', 'loc': 'mk', 'by': '2,3,k'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[41]原语 mk3 = loc mk by (2,3,k) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'mk3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'MK:3'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[42]原语 store mk3 to ssdb by ssdb0 with MK:3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mk4', 'Action': 'loc', 'loc': 'mk', 'by': '3,0,k'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[43]原语 mk4 = loc mk by (3,0,k) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'mk4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'MK:4'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[44]原语 store mk4 to ssdb by ssdb0 with MK:4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a', 'by': 'ML.pca', 'with': '2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[48]原语 a2 = @udf a by ML.pca with (2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_mk', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.kmeans', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[53]原语 a2_mk = @udf a2 by ML.kmeans with (3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_mk', 'Action': 'join', 'join': 'a2,a2_mk', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[54]原语 a2_mk = join a2,a2_mk by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_mk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:mk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[55]原语 store a2_mk to ssdb by ssdb0 with A2:mk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_ac', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.ac', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[58]原语 a2_ac = @udf a2 by ML.ac with (3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_ac', 'Action': 'join', 'join': 'a2,a2_ac', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[59]原语 a2_ac = join a2,a2_ac by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_ac', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:ac'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[60]原语 store a2_ac to ssdb by ssdb0 with A2:ac 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_ap', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.ap'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[63]原语 a2_ap = @udf a2 by ML.ap 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_ap', 'Action': 'join', 'join': 'a2,a2_ap', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[64]原语 a2_ap = join a2,a2_ap by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_ap', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:ap'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[65]原语 store a2_ap to ssdb by ssdb0 with A2:ap 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_db', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.dbscan'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[69]原语 a2_db = @udf a2 by ML.dbscan 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_db', 'Action': 'join', 'join': 'a2,a2_db', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[70]原语 a2_db = join a2,a2_db by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_db', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:db'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[71]原语 store a2_db to ssdb by ssdb0 with A2:db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_br', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.brich'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[74]原语 a2_br = @udf a2 by ML.brich 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_br', 'Action': 'join', 'join': 'a2,a2_br', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[75]原语 a2_br = join a2,a2_br by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_br', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:br'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[76]原语 store a2_br to ssdb by ssdb0 with A2:br 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a', 'by': 'ML.mds'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[80]原语 a2 = @udf a by ML.mds 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_mk', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.kmeans', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[85]原语 a2_mk = @udf a2 by ML.kmeans with (3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_mk', 'Action': 'join', 'join': 'a2,a2_mk', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[86]原语 a2_mk = join a2,a2_mk by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_mk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2_1:mk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[87]原语 store a2_mk to ssdb by ssdb0 with A2_1:mk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_ac', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.ac', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[90]原语 a2_ac = @udf a2 by ML.ac with (3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_ac', 'Action': 'join', 'join': 'a2,a2_ac', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[91]原语 a2_ac = join a2,a2_ac by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_ac', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2_1:ac'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[92]原语 store a2_ac to ssdb by ssdb0 with A2_1:ac 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_ap', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.ap'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[95]原语 a2_ap = @udf a2 by ML.ap 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_ap', 'Action': 'join', 'join': 'a2,a2_ap', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[96]原语 a2_ap = join a2,a2_ap by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_ap', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2_1:ap'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[97]原语 store a2_ap to ssdb by ssdb0 with A2_1:ap 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_db', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.dbscan'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[100]原语 a2_db = @udf a2 by ML.dbscan 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_db', 'Action': 'join', 'join': 'a2,a2_db', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[101]原语 a2_db = join a2,a2_db by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_db', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2_1:db'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[102]原语 store a2_db to ssdb by ssdb0 with A2_1:db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2_br', 'Action': '@udf', '@udf': 'a2', 'by': 'ML.brich'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[105]原语 a2_br = @udf a2 by ML.brich 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a2_br', 'Action': 'join', 'join': 'a2,a2_br', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[106]原语 a2_br = join a2,a2_br by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a2_br', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2_1:br'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[107]原语 store a2_br to ssdb by ssdb0 with A2_1:br 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'svm', 'Action': '@udf', '@udf': 'a,c', 'by': 'ML.svm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[111]原语 svm = @udf a,c by ML.svm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'svm_1', 'Action': '@udf', '@udf': 'svm,a', 'by': 'ML.predict'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[112]原语 svm_1 = @udf svm,a by ML.predict 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'svm_a2', 'Action': 'join', 'join': 'a2,svm_1', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[113]原语 svm_a2 = join a2,svm_1 by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'svm_a2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:svm_a2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[114]原语 store svm_a2 to ssdb by ssdb0 with A2:svm_a2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'gnb', 'Action': '@udf', '@udf': 'a,c', 'by': 'ML.gnb'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[118]原语 gnb = @udf a,c by ML.gnb 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'gnb_1', 'Action': '@udf', '@udf': 'gnb, a', 'by': 'ML.predict'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[119]原语 gnb_1 = @udf gnb, a by ML.predict 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'gnb_a2', 'Action': 'join', 'join': 'a2,gnb_1', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[120]原语 gnb_a2 = join a2,gnb_1 by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'gnb_a2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'A2:gnb_a2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[121]原语 store gnb_a2 to ssdb by ssdb0 with A2:gnb_a2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dt', 'Action': '@udf', '@udf': 'a,c', 'by': 'ML.dt'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[125]原语 dt = @udf a,c by ML.dt 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dt_score', 'Action': '@udf', '@udf': 'dt, a,c', 'by': 'ML.score'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/ML_studio.fbi]执行第[126]原语 dt_score = @udf dt, a,c by ML.score 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],127

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



