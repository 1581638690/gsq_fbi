#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_splitting
#datetime: 2024-08-30T16:10:53.582704
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
		add_the_error('[api_splitting.fbi]执行第[23]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[24]原语 url_df = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'url_df', 'by': 'df.index.size !=0', 'as': 'break', 'with': '请选择需要拆分的接口'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[api_splitting.fbi]执行第[25]原语 assert url_df by df.index... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[25]原语 assert url_df by df.index.size !=0 as break with 请... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'url_df', 'Action': 'add', 'add': 'id', 'by': 'url_df.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[27]原语 url_df=add id by url_df.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa', 'Action': 'filter', 'filter': 'url_df', 'by': 'index!=0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[28]原语 aa=filter url_df by index!=0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'un_b', 'Action': 'filter', 'filter': 'url_df', 'by': 'index==0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[29]原语 un_b=filter url_df by index==0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'y_mege', 'Action': 'filter', 'filter': 'url_df', 'by': 'index==0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[30]原语 y_mege=filter url_df by index==0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'aa', 'with': 'id=$0', 'run': '""\na=filter aa by id==\'@id\'\nstate=loc a by merge_state\nurl=loc a by url\nurl.url=lambda url by (x:x if "{p1}" in x or "{p2}" in x or "{dst}" in x else "")\nurl=eval url by iloc[0,0]\nmerge_state=eval state by iloc[0,0]\nassert a by $merge_state==2 or ($merge_state==0 and \'$url\'!="") as break with 请选择手工合并过的接口或存在合并类型的接口\nurls=loc a by url_sum\nurl_sum=eval urls by iloc[0,0]\n#取出一个字符判断是否存在url_sum\nbb=loc urls by url_sum\nbb.url_sum=lambda url_sum by x:x[0:4]\nb=eval bb by iloc[0,0]\nif \'$b\'!="" with un_b=union (un_b,a)\nif \'$b\'=="" with y_mege=union (y_mege,a)\n#转化为str\n""'}
	try:
		ptree['lineno']=31
		ptree['funs']=block_foreach_31
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[31]原语 foreach aa run "a=filter aa by id=="@id"state=loc ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'un_b', 'with': 'id=$0', 'run': '""\nuu=filter un_b by id==\'@id\'\nuu=loc uu drop id\nurls=loc uu by url_sum\nurls.url_sum=lambda url_sum by x:x.split(";|")\nalter urls.url_sum as str\nurls.url_sum=lambda url_sum by x:x.replace("[","(")\nurls.url_sum=lambda url_sum by x:x.replace("]",")")\nurl_sum=eval urls by iloc[0,0]\nmysql_db=load db by mysql1 with select id,url from data_api_new\ndelete_db=join uu,mysql_db by url,url with left\nid=loc delete_db by id\nid=eval id by iloc[0,0]\n@udf CRUD.delete_object_mtable with (@link,@table,$id)\ndf =load db by mysql1 with select * from data_api_new where url in $url_sum\n#让他们的merge_state变为0\ndf=@udf df by udf0.df_set with (merge_state=0)\ndf=@udf df by udf0.df_set with (url_merges="")\njoin_db=join df,mysql_db by [id,url],[id,url] with left\njoin_db=@udf join_db by udf0.df_fillna with 0\njoin_db=@udf join_db by udf0.df_set_index with id\n@udf join_db by CRUD.save_table with (mysql1,data_api_new)\n#然后继续查找状态码是为2的接口\napi = @udf RS.load_mysql_sql with (mysql1,select url,url_sum from data_api_new where merge_state = 2)\nb=@udf SSDB.hclear with api_merge\nstore api to ssdb by ssdb0 with api_merge as H\n""'}
	try:
		ptree['lineno']=49
		ptree['funs']=block_foreach_49
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[49]原语 foreach un_b run "uu=filter un_b by id=="@id"uu=lo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'y_mege', 'with': 'id=$0', 'run': '""\n#对自动合并进行拆分\n#对ｍｅｒｇｅ＿ｓｔａｔｅ等于0的时候进行拆分\nyy=filter y_mege by id==\'@id\'\nyy=loc yy drop id\nurl=loc yy by url\nurl=eval url by iloc[0,0]\nckh_df=load ckh by ckh with select * from merge_urls where url=\'$url\'\nckh_df=distinct ckh_df by y_url with first\n#将y_url 转化为url，删除url\nckh_df=loc ckh_df drop url\nrename ckh_df as ("y_url":"url")\n\nckh_df.url=lambda url by x:x.split("?")[0]\n\n#取出url列\nurls=loc ckh_df by url\nurls=@udf urls by udf0.df_T\nurls=@udf urls by udf0.df_cs2l\nrename urls as ("s0":"t_url")\nalter urls.t_url as str\nurls.t_url=lambda t_url by x:x.replace("[","(")\nurls.t_url=lambda t_url by x:x.replace("]",")")\nt_url=eval urls by iloc[0,0]\ndf =load db by mysql1 with select url,id from data_api_new where url in $t_url\n\n#将进行拆分的数据进行隐藏\nmysql_db1=load db by mysql1 with select id,url from data_api_new\ndb1=join yy,mysql_db1 by url,url with left\ndb1=@udf db1 by udf0.df_set with merge_state=1\ndb1=@udf db1 by udf0.df_set with z_cf=1\ndb1=@udf db1 by udf0.df_set with api_status=0\ndb1=@udf db1 by udf0.df_fillna with 0\ndb1=@udf db1 by udf0.df_set_index with id\n\ndb1=loc db1 drop btn_show\n#db1=distinct db1 by url\n@udf db1 by CRUD.save_table with (mysql1,data_api_new)\n\n#取出隐藏的接口 包含被合并的接口，也包含自动合并拆分的接口，被拆分的接口在main_json里面还是会存在那么 拆分的接口就不会进行 if url_c in 1里面 则表示该url_c 就等于原始接口\n#Delete 注释 by rzc on 2023-03-08 18:03:41\napi = @udf RS.load_mysql_sql with (mysql1,select url from data_api_new where merge_state = 1 and z_cf = 1)\na=@udf SSDB.hclear with api_merge1\napi = @udf api by udf0.df_set_index with url\napi = add url by (api.index)\nstore api to ssdb by ssdb0 with api_merge1 as H\n\n\nckh_df=add merge_state by 0\nckh_df=join ckh_df,df by url,url with left\n#判断拆分之前的接口是否开启审计\napi_status=loc yy by api_status\napi_status=eval api_status by iloc[0,0]\nckh_df=@udf ckh_df by udf0.df_set with api_status=$api_status\nckh_df=@udf ckh_df by udf0.df_fillna with 0\nckh_df=filter ckh_df by id==0\nckh_df=@udf ckh_df by udf0.df_set_index with id\nckh_df=loc ckh_df drop timestamp\n@udf ckh_df by CRUD.save_table with (mysql1,data_api_new)\n\n#Delete 注释 by rzc on 2023-06-20 10:39:05\n#c = @udf SSDB.hclear with FF:url2\n#\tapi = load db by mysql1 with select url from data_api_new where merge_state!=2\n#\tapi.url = lambda url by x:x[0:255]\n#\tapi = add value with True\n#\tapi = @udf api by udf0.df_set_index with url\n#\tstore api to ssdb by ssdb0 with FF:url2 as H\n""'}
	try:
		ptree['lineno']=76
		ptree['funs']=block_foreach_76
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[76]原语 foreach y_mege run  "#对自动合并进行拆分#对ｍｅｒｇｅ＿ｓｔａｔｅ等于0的时候... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_splitting.fbi]执行第[150]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],150

#主函数结束,开始块函数

def block_foreach_31(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a', 'Action': 'filter', 'filter': 'aa', 'by': "id=='@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[32]原语 a=filter aa by id=="@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'state', 'Action': 'loc', 'loc': 'a', 'by': 'merge_state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[33]原语 state=loc a by merge_state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'url', 'Action': 'loc', 'loc': 'a', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[34]原语 url=loc a by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'url.url', 'Action': 'lambda', 'lambda': 'url', 'by': 'x:x if "{p1}" in x or "{p2}" in x or "{dst}" in x else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[35]原语 url.url=lambda url by (x:x if "{p1}" in x or "{p2}... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url', 'Action': 'eval', 'eval': 'url', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[36]原语 url=eval url by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'merge_state', 'Action': 'eval', 'eval': 'state', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[37]原语 merge_state=eval state by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'a', 'by': '$merge_state==2 or ($merge_state==0 and \'$url\'!="")', 'as': 'break', 'with': '请选择手工合并过的接口或存在合并类型的接口'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[第31行foreach语句中]执行第[38]原语 assert a by $merge_state=... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[38]原语 assert a by $merge_state==2 or ($merge_state==0 an... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urls', 'Action': 'loc', 'loc': 'a', 'by': 'url_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[39]原语 urls=loc a by url_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_sum', 'Action': 'eval', 'eval': 'urls', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[40]原语 url_sum=eval urls by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'bb', 'Action': 'loc', 'loc': 'urls', 'by': 'url_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[42]原语 bb=loc urls by url_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'bb.url_sum', 'Action': 'lambda', 'lambda': 'url_sum', 'by': 'x:x[0:4]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[43]原语 bb.url_sum=lambda url_sum by x:x[0:4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'eval', 'eval': 'bb', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[44]原语 b=eval bb by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '\'$b\'!=""', 'with': 'un_b=union (un_b,a)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=45
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[45]原语 if "$b"!="" with un_b=union (un_b,a) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '\'$b\'==""', 'with': 'y_mege=union (y_mege,a)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=46
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第31行foreach语句中]执行第[46]原语 if "$b"=="" with y_mege=union (y_mege,a) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_31

def block_foreach_49(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'uu', 'Action': 'filter', 'filter': 'un_b', 'by': "id=='@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[50]原语 uu=filter un_b by id=="@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'uu', 'Action': 'loc', 'loc': 'uu', 'drop': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[51]原语 uu=loc uu drop id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urls', 'Action': 'loc', 'loc': 'uu', 'by': 'url_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[52]原语 urls=loc uu by url_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urls.url_sum', 'Action': 'lambda', 'lambda': 'url_sum', 'by': 'x:x.split(";|")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[53]原语 urls.url_sum=lambda url_sum by x:x.split(";|") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'urls.url_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[54]原语 alter urls.url_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urls.url_sum', 'Action': 'lambda', 'lambda': 'url_sum', 'by': 'x:x.replace("[","(")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[55]原语 urls.url_sum=lambda url_sum by x:x.replace("[","("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urls.url_sum', 'Action': 'lambda', 'lambda': 'url_sum', 'by': 'x:x.replace("]",")")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[56]原语 urls.url_sum=lambda url_sum by x:x.replace("]",")"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_sum', 'Action': 'eval', 'eval': 'urls', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[57]原语 url_sum=eval urls by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mysql_db', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[58]原语 mysql_db=load db by mysql1 with select id,url from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'delete_db', 'Action': 'join', 'join': 'uu,mysql_db', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[59]原语 delete_db=join uu,mysql_db by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'id', 'Action': 'loc', 'loc': 'delete_db', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[60]原语 id=loc delete_db by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'id', 'Action': 'eval', 'eval': 'id', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[61]原语 id=eval id by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'CRUD.delete_object_mtable', 'with': '@link,@table,$id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[62]原语 @udf CRUD.delete_object_mtable with (@link,@table,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select * from data_api_new where url in $url_sum'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[63]原语 df =load db by mysql1 with select * from data_api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_set', 'with': 'merge_state=0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[65]原语 df=@udf df by udf0.df_set with (merge_state=0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_set', 'with': 'url_merges=""'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[66]原语 df=@udf df by udf0.df_set with (url_merges="") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'join_db', 'Action': 'join', 'join': 'df,mysql_db', 'by': '[id,url],[id,url]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[67]原语 join_db=join df,mysql_db by [id,url],[id,url] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_db', 'Action': '@udf', '@udf': 'join_db', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[68]原语 join_db=@udf join_db by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_db', 'Action': '@udf', '@udf': 'join_db', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[69]原语 join_db=@udf join_db by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'join_db', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[70]原语 @udf join_db by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url,url_sum from data_api_new where merge_state = 2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[72]原语 api = @udf RS.load_mysql_sql with (mysql1,select u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'api_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[73]原语 b=@udf SSDB.hclear with api_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_merge', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[74]原语 store api to ssdb by ssdb0 with api_merge as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_49

def block_foreach_76(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'yy', 'Action': 'filter', 'filter': 'y_mege', 'by': "id=='@id'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[79]原语 yy=filter y_mege by id=="@id" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'yy', 'Action': 'loc', 'loc': 'yy', 'drop': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[80]原语 yy=loc yy drop id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'url', 'Action': 'loc', 'loc': 'yy', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[81]原语 url=loc yy by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url', 'Action': 'eval', 'eval': 'url', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[82]原语 url=eval url by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ckh_df', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select * from merge_urls where url='$url'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[83]原语 ckh_df=load ckh by ckh with select * from merge_ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ckh_df', 'Action': 'distinct', 'distinct': 'ckh_df', 'by': 'y_url', 'with': 'first'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[84]原语 ckh_df=distinct ckh_df by y_url with first 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ckh_df', 'Action': 'loc', 'loc': 'ckh_df', 'drop': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[86]原语 ckh_df=loc ckh_df drop url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ckh_df', 'as': '"y_url":"url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[87]原语 rename ckh_df as ("y_url":"url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ckh_df.url', 'Action': 'lambda', 'lambda': 'url', 'by': 'x:x.split("?")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[89]原语 ckh_df.url=lambda url by x:x.split("?")[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urls', 'Action': 'loc', 'loc': 'ckh_df', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[92]原语 urls=loc ckh_df by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urls', 'Action': '@udf', '@udf': 'urls', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[93]原语 urls=@udf urls by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urls', 'Action': '@udf', '@udf': 'urls', 'by': 'udf0.df_cs2l'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[94]原语 urls=@udf urls by udf0.df_cs2l 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'urls', 'as': '"s0":"t_url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[95]原语 rename urls as ("s0":"t_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'urls.t_url', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[96]原语 alter urls.t_url as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urls.t_url', 'Action': 'lambda', 'lambda': 't_url', 'by': 'x:x.replace("[","(")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[97]原语 urls.t_url=lambda t_url by x:x.replace("[","(") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urls.t_url', 'Action': 'lambda', 'lambda': 't_url', 'by': 'x:x.replace("]",")")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[98]原语 urls.t_url=lambda t_url by x:x.replace("]",")") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_url', 'Action': 'eval', 'eval': 'urls', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[99]原语 t_url=eval urls by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select url,id from data_api_new where url in $t_url'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[100]原语 df =load db by mysql1 with select url,id from data... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mysql_db1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[103]原语 mysql_db1=load db by mysql1 with select id,url fro... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'db1', 'Action': 'join', 'join': 'yy,mysql_db1', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[104]原语 db1=join yy,mysql_db1 by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db1', 'Action': '@udf', '@udf': 'db1', 'by': 'udf0.df_set', 'with': 'merge_state=1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[105]原语 db1=@udf db1 by udf0.df_set with merge_state=1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db1', 'Action': '@udf', '@udf': 'db1', 'by': 'udf0.df_set', 'with': 'z_cf=1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[106]原语 db1=@udf db1 by udf0.df_set with z_cf=1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db1', 'Action': '@udf', '@udf': 'db1', 'by': 'udf0.df_set', 'with': 'api_status=0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[107]原语 db1=@udf db1 by udf0.df_set with api_status=0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db1', 'Action': '@udf', '@udf': 'db1', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[108]原语 db1=@udf db1 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'db1', 'Action': '@udf', '@udf': 'db1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[109]原语 db1=@udf db1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'db1', 'Action': 'loc', 'loc': 'db1', 'drop': 'btn_show'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[111]原语 db1=loc db1 drop btn_show 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'db1', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[113]原语 @udf db1 by CRUD.save_table with (mysql1,data_api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url from data_api_new where merge_state = 1 and z_cf = 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[117]原语 api = @udf RS.load_mysql_sql with (mysql1,select u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'api_merge1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[118]原语 a=@udf SSDB.hclear with api_merge1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'url'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[119]原语 api = @udf api by udf0.df_set_index with url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'url', 'by': 'api.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[120]原语 api = add url by (api.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_merge1', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[121]原语 store api to ssdb by ssdb0 with api_merge1 as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ckh_df', 'Action': 'add', 'add': 'merge_state', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[124]原语 ckh_df=add merge_state by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ckh_df', 'Action': 'join', 'join': 'ckh_df,df', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[125]原语 ckh_df=join ckh_df,df by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_status', 'Action': 'loc', 'loc': 'yy', 'by': 'api_status'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[127]原语 api_status=loc yy by api_status 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_status', 'Action': 'eval', 'eval': 'api_status', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[128]原语 api_status=eval api_status by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ckh_df', 'Action': '@udf', '@udf': 'ckh_df', 'by': 'udf0.df_set', 'with': 'api_status=$api_status'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[129]原语 ckh_df=@udf ckh_df by udf0.df_set with api_status=... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ckh_df', 'Action': '@udf', '@udf': 'ckh_df', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[130]原语 ckh_df=@udf ckh_df by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ckh_df', 'Action': 'filter', 'filter': 'ckh_df', 'by': 'id==0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[131]原语 ckh_df=filter ckh_df by id==0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ckh_df', 'Action': '@udf', '@udf': 'ckh_df', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[132]原语 ckh_df=@udf ckh_df by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ckh_df', 'Action': 'loc', 'loc': 'ckh_df', 'drop': 'timestamp'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[133]原语 ckh_df=loc ckh_df drop timestamp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'ckh_df', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第76行foreach语句中]执行第[134]原语 @udf ckh_df by CRUD.save_table with (mysql1,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_76

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



