#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: update_url
#datetime: 2024-08-30T16:10:54.241607
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'protocol_data as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[update_url.fbi]执行第[6]原语 df=load ssdb by ssdb0 with protocol_data as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'merge_off', 'Action': 'jaas', 'jaas': 'df', 'by': 'df["function"]["event"]["merge_off"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[update_url.fbi]执行第[7]原语 merge_off=jaas df by df["function"]["event"]["merg... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$merge_off=="true"', 'with': '""\napilist11 = load db by mysql1 with (select id,url,ltten_url from data_api_new)\napilist1=loc apilist11 by id,url,ltten_url\nmerge_urls=load ckh by ckh with select url,y_url from merge_urls\nrename apilist11 as {"url":"y_url"}\n#通过join进行合并数据\nmergeurls=join apilist11,merge_urls by y_url,y_url\napilist11 =loc mergeurls drop ltten_url\nrename apilist11 as {"url":"ltten_url"}\nrename apilist11 as {"y_url":"url"}\n#更新到data_api_new的表中\napi = @udf apilist11 by udf0.df_set_index with id\napi = @udf api by CRUD.save_table with (mysql1,data_api_new)\n\n###################进行更新数据###################\n#查出mysql表 找到{dst}中两个不同的数据，然后提取出url 将ltten_url给替换上 删除掉 url,\nfilter_df=@udf apilist1 by handi_merge.drop_dst\n#先进行去重\ndis=distinct filter_df by ltten_url\n#全连接\nmerge=join dis,filter_df by id,id with right\n#筛选出值为空的NaN\ndrop_url=filter merge by url_x isnull\ndrop_url = @udf drop_url by udf0.df_set_index with id\n#删除表数据\n@udf drop_url by CRUD.delete_mobject_mtable with (mysql1,data_api_new)\n\nupdate_url=filter merge by url_x notnull\n#取出url列\n\nupdate_url=loc update_url by id,ltten_url_x\nrename update_url as {"ltten_url_x":"url"}\nupdate_url = @udf update_url by udf0.df_set_index with id\nupdate_url = @udf update_url by CRUD.save_table with (mysql1,data_api_new)\n##################\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=8
		ptree['funs']=block_if_8
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[update_url.fbi]执行第[8]原语 if $merge_off=="true" with "apilist11 = load db by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],43

#主函数结束,开始块函数

def block_if_8(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'apilist11', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,ltten_url from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[9]原语 apilist11 = load db by mysql1 with (select id,url,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'apilist1', 'Action': 'loc', 'loc': 'apilist11', 'by': 'id,url,ltten_url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[10]原语 apilist1=loc apilist11 by id,url,ltten_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'merge_urls', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select url,y_url from merge_urls'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[11]原语 merge_urls=load ckh by ckh with select url,y_url f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'apilist11', 'as': '{"url":"y_url"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[12]原语 rename apilist11 as {"url":"y_url"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'mergeurls', 'Action': 'join', 'join': 'apilist11,merge_urls', 'by': 'y_url,y_url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[14]原语 mergeurls=join apilist11,merge_urls by y_url,y_url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'apilist11', 'Action': 'loc', 'loc': 'mergeurls', 'drop': 'ltten_url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[15]原语 apilist11 =loc mergeurls drop ltten_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'apilist11', 'as': '{"url":"ltten_url"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[16]原语 rename apilist11 as {"url":"ltten_url"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'apilist11', 'as': '{"y_url":"url"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[17]原语 rename apilist11 as {"y_url":"url"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'apilist11', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[19]原语 api = @udf apilist11 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[20]原语 api = @udf api by CRUD.save_table with (mysql1,dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'filter_df', 'Action': '@udf', '@udf': 'apilist1', 'by': 'handi_merge.drop_dst'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[24]原语 filter_df=@udf apilist1 by handi_merge.drop_dst 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dis', 'Action': 'distinct', 'distinct': 'filter_df', 'by': 'ltten_url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[26]原语 dis=distinct filter_df by ltten_url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'merge', 'Action': 'join', 'join': 'dis,filter_df', 'by': 'id,id', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[28]原语 merge=join dis,filter_df by id,id with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'drop_url', 'Action': 'filter', 'filter': 'merge', 'by': 'url_x isnull'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[30]原语 drop_url=filter merge by url_x isnull 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'drop_url', 'Action': '@udf', '@udf': 'drop_url', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[31]原语 drop_url = @udf drop_url by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'drop_url', 'by': 'CRUD.delete_mobject_mtable', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[33]原语 @udf drop_url by CRUD.delete_mobject_mtable with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'update_url', 'Action': 'filter', 'filter': 'merge', 'by': 'url_x notnull'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[35]原语 update_url=filter merge by url_x notnull 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'update_url', 'Action': 'loc', 'loc': 'update_url', 'by': 'id,ltten_url_x'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[38]原语 update_url=loc update_url by id,ltten_url_x 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'update_url', 'as': '{"ltten_url_x":"url"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[39]原语 rename update_url as {"ltten_url_x":"url"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'update_url', 'Action': '@udf', '@udf': 'update_url', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[40]原语 update_url = @udf update_url by udf0.df_set_index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'update_url', 'Action': '@udf', '@udf': 'update_url', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第8行if语句中]执行第[41]原语 update_url = @udf update_url by CRUD.save_table wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_8

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



