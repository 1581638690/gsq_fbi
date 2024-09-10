#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_json
#datetime: 2024-08-30T16:10:54.715711
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
		add_the_error('[qh_json.fbi]执行第[7]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[25]原语 zz = load ssdb by ssdb0 with sensitive as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zz', 'Action': '@udf', '@udf': 'zz', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[26]原语 zz = @udf zz by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zz.data', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[27]原语 alter zz.data as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.data', 'Action': 'str', 'str': 'data', 'by': 'findall("rekey\': \'(.*?)\',")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[28]原语 zz.data = str data by (findall("rekey": "(.*?)",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zz.data', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[29]原语 alter zz.data as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.data', 'Action': 'str', 'str': 'data', 'by': 'replace("[\'","")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[30]原语 zz.data = str data by (replace("["","")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.data', 'Action': 'str', 'str': 'data', 'by': 'replace("\']","")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[31]原语 zz.data = str data by (replace(""]","")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zzz', 'Action': 'loc', 'loc': 'zz', 'by': 'data'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[32]原语 zzz = loc zz by data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zzz', 'to': 'ssdb', 'with': 'dd:reqs_label'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[33]原语 store zzz to ssdb with dd:reqs_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zzz', 'Action': 'add', 'add': 'id', 'by': 'zzz.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[34]原语 zzz = add id by zzz.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[36]原语 zz = load ssdb by ssdb0 with sensitive as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zz', 'Action': '@udf', '@udf': 'zz', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[37]原语 zz = @udf zz by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zz', 'as': '"data":"class"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[38]原语 rename zz as ("data":"class") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zz.class', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[39]原语 alter zz.class as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.class', 'Action': 'str', 'str': 'class', 'by': 'findall("class\': \'(.*?)\',")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[40]原语 zz.class = str class by (findall("class": "(.*?)",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'zz.class', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[41]原语 alter zz.class as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.class', 'Action': 'str', 'str': 'class', 'by': 'replace("[\'","")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[42]原语 zz.class = str class by (replace("["","")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'zz.class', 'Action': 'str', 'str': 'class', 'by': 'replace("\']","")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[43]原语 zz.class = str class by (replace(""]","")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zzz1', 'Action': 'loc', 'loc': 'zz', 'by': 'class'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[44]原语 zzz1 = loc zz by class 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'zzz1', 'Action': 'add', 'add': 'id', 'by': 'zzz1.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[46]原语 zzz1 = add id by zzz1.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zzz2', 'Action': 'join', 'join': 'zzz1,zzz', 'by': 'id,id'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[47]原语 zzz2 = join zzz1,zzz by id,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zzz2', 'Action': 'loc', 'loc': 'zzz2', 'by': 'class,data'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[48]原语 zzz2 = loc zzz2 by class,data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zzz2', 'to': 'ssdb', 'with': 'dd:reqs_label1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[49]原语 store zzz2 to ssdb with dd:reqs_label1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_json.fbi]执行第[51]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],51

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



