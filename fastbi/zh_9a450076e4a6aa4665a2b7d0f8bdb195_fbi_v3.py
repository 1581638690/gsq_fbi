#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: zh_9a450076e4a6aa4665a2b7d0f8bdb195_fbi
#datetime: 2024-08-30T16:10:58.598768
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
		add_the_error('[Avl8eqf/确定.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[16]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urls', 'Action': 'loc', 'loc': 'a', 'by': 'urls_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[19]原语 urls=loc a by urls_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url', 'Action': 'eval', 'eval': 'urls', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[20]原语 url=eval urls by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'eurl', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select url from data_api_new where url='$url'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[22]原语 eurl=load db by mysql1 with select url from data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'eurl', 'by': 'df.index.size <=0', 'as': 'break', 'with': '已存在相同的接口名'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[Avl8eqf/确定.fbi]执行第[23]原语 assert eurl by df.index.s... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[23]原语 assert eurl by df.index.size <=0 as break with  已存... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'eurl.index.size <=0', 'with': '""\n\nb=eval a by (iloc[0,0])\n\nbb = load ssdb by ssdb0 with $b\n\naa=loc a by urls_sum\nrename aa as ("urls_sum":"urls_merge")\n\n#对bb添加两列 urls_merge\nurl_merge=eval aa by iloc[0,0]\nbb=add url_merges by (\'$url_merge\')\nbb=add merge_state by 1\nbb=add url_sum by ("")\n#添加状态码 1为被合并 0为未合并 2为合并后的 所以 1不展示\nbb1=@udf bb by handi_merge.merge\n#判断是否存在相同的接口名称\n\n#df.url_sum=lambda url_sum by (x:x.split(";|") if x!="" else x)\nalter bb1.url_sum as str\n#查询mysql表 查询当前合并接口是否存在\nmysql_db=load db by mysql1 with select id,url from data_api_new\njoin_db=join bb1,mysql_db by url,url with left\njoin_db=@udf join_db by udf0.df_fillna with 0\n#p_db=filter join_db by id==0\njoin_db=@udf join_db by udf0.df_set_index with id\n@udf join_db by CRUD.save_table with (mysql1,data_api_new)\n\n#push p_db as table\n#取出合并接口的数据\napi = @udf RS.load_mysql_sql with (mysql1,select url,url_sum from data_api_new where merge_state = 2)\na=@udf SSDB.hclear with api_merge\napi = @udf api by udf0.df_set_index with url\napi = add url by (api.index)\nstore api to ssdb by ssdb0 with api_merge as H\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=25
		ptree['funs']=block_if_25
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[25]原语 if eurl.index.size <=0 with "b=eval a by (iloc[0,0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[Avl8eqf/确定.fbi]执行第[68]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],68

#主函数结束,开始块函数

def block_if_25(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[27]原语 b=eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'bb', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '$b'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[29]原语 bb = load ssdb by ssdb0 with $b 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'a', 'by': 'urls_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[31]原语 aa=loc a by urls_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'aa', 'as': '"urls_sum":"urls_merge"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[32]原语 rename aa as ("urls_sum":"urls_merge") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_merge', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[35]原语 url_merge=eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bb', 'Action': 'add', 'add': 'url_merges', 'by': "'$url_merge'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[36]原语 bb=add url_merges by ("$url_merge") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bb', 'Action': 'add', 'add': 'merge_state', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[37]原语 bb=add merge_state by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bb', 'Action': 'add', 'add': 'url_sum', 'by': '""'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[38]原语 bb=add url_sum by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb1', 'Action': '@udf', '@udf': 'bb', 'by': 'handi_merge.merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[40]原语 bb1=@udf bb by handi_merge.merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'bb1.url_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[44]原语 alter bb1.url_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mysql_db', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[46]原语 mysql_db=load db by mysql1 with select id,url from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'join_db', 'Action': 'join', 'join': 'bb1,mysql_db', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[47]原语 join_db=join bb1,mysql_db by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_db', 'Action': '@udf', '@udf': 'join_db', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[48]原语 join_db=@udf join_db by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_db', 'Action': '@udf', '@udf': 'join_db', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[50]原语 join_db=@udf join_db by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'join_db', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[51]原语 @udf join_db by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url,url_sum from data_api_new where merge_state = 2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[55]原语 api = @udf RS.load_mysql_sql with (mysql1,select u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'api_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[56]原语 a=@udf SSDB.hclear with api_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[57]原语 api = @udf api by udf0.df_set_index with url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'url', 'by': 'api.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[58]原语 api = add url by (api.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_merge', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第25行if语句中]执行第[59]原语 store api to ssdb by ssdb0 with api_merge as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_25

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



