#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/jsonFrom
#datetime: 2024-08-30T16:10:57.140366
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '参数,中文名,默认值,类型,字典关联,排版,状态,必填,提示,显示,宽度'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[10]原语 a = @udf udf0.new_df with 参数,中文名,默认值,类型,字典关联,排版,状态... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '@dd2,zz,dfgdfdfsdfs.fea,文本框,没有关联字典,2,均能操作,false,false,true,'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[11]原语 a = @udf a by udf0.df_append with @dd2,zz,dfgdfdfs... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '@dd3,姓名,admin,文本框,没有关联字典,2,均能操作,true,false,true,'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[12]原语 a = @udf a by udf0.df_append with @dd3,姓名,admin,文本... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '@dd4,性别,男,文本框,没有关联字典,2,均能操作,false,false,true,'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[13]原语 a = @udf a by udf0.df_append with @dd4,性别,男,文本框,没有... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'jsonForm:k1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[14]原语 store a to ssdb with  jsonForm:k1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '参数,中文名,默认值,类型,字典关联,排版,状态,必填,提示,显示,宽度'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[17]原语 b = @udf udf0.new_df with 参数,中文名,默认值,类型,字典关联,排版,状态... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_append', 'with': '@ddd2,zz,dfgdfdfsdfs.fea,文本框,没有关联字典,2,均能操作,false,false,true,'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[18]原语 b = @udf b by udf0.df_append with @ddd2,zz,dfgdfdf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_append', 'with': '@ddd3,姓名,admin,标签式单选,dd:data_gov_ak_usename,2,均能操作,false,false,true,'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[19]原语 b = @udf b by udf0.df_append with @ddd3,姓名,admin,标... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b', 'to': 'ssdb', 'with': 'jsonForm:k2'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[20]原语 store b to ssdb with  jsonForm:k2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[23]原语 dd = @udf udf0.new_df with name,value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '表单1,jsonForm:k1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[24]原语 dd = @udf dd by udf0.df_append with 表单1,jsonForm:k... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '表单2,jsonForm:k2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[25]原语 dd = @udf dd by udf0.df_append with 表单2,jsonForm:k... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'dd', 'by': 'value', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[26]原语 dd = loc dd by value to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'with': 'dd:Form_test'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/jsonFrom.fbi]执行第[28]原语 store dd to ssdb with dd:Form_test 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],32

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



