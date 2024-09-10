#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_model
#datetime: 2024-08-30T16:10:56.064464
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
		add_the_error('[qh_model.fbi]执行第[14]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'senapi', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct url_c as url from sen_http_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[25]原语 senapi = load ckh by ckh with select distinct url_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'senapi', 'by': 'url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[26]原语 alter senapi by url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'senapi', 'to': 'ssdb', 'with': 'risk_url_xlk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[27]原语 store senapi to ssdb with risk_url_xlk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'murl', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url from data_api_new where api_status = 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[29]原语 murl =  @udf RS.load_mysql_sql with (mysql1,select... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'murl', 'by': 'url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[30]原语 alter murl by url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'murl', 'to': 'ssdb', 'with': 'monitor_url_xlk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[31]原语 store murl to ssdb with monitor_url_xlk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcip', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select srcip from data_ip_new where type != '其他' and type != '应用'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[33]原语 srcip = @udf RS.load_mysql_sql with (mysql1,select... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'srcip', 'by': 'srcip:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[34]原语 alter srcip by srcip:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcip', 'to': 'ssdb', 'with': 'srcip_model_xlk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[35]原语 store srcip to ssdb with srcip_model_xlk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[37]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[38]原语 month = @sdf format_now with ($month1,"%Y-%m-%dT00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,response_count as res_type,count(*) as num from sen_http_count where timestamp > '$month' group by url,res_type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[40]原语 sens = load ckh by ckh with select url,response_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_fillna_cols', 'with': "url:'',res_type:'',num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[41]原语 sens = @udf sens by udf0.df_fillna_cols with url:"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'url:str,res_type:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[42]原语 alter sens by url:str,res_type:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "res_type != '' and res_type != 'null' and res_type != '{}' and res_type != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[43]原语 sens = filter sens by res_type != "" and res_type ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.res_type', 'Action': 'str', 'str': 'res_type', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[44]原语 sens.res_type = str res_type by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': 'res_type unlike name'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[45]原语 sens = filter sens by res_type unlike name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_d2df', 'with': 'res_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[46]原语 sens = @udf sens by udf0.df_d2df with res_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'num:int,value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[47]原语 alter sens by num:int,value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'num', 'by': 'df["num"] * df["value"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[61]原语 sens = add num by df["num"] * df["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens', 'by': 'url,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[62]原语 sens1 = loc sens by url,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,request_count as req_type,count(*) as num from sen_http_count where timestamp > '$month' and url != '' group by url,req_type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[64]原语 sens = load ckh by ckh with select url,request_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_fillna_cols', 'with': "url:'',req_type:'',num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[65]原语 sens = @udf sens by udf0.df_fillna_cols with url:"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'url:str,req_type:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[66]原语 alter sens by url:str,req_type:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "req_type != '' and req_type != 'null' and req_type != '{}' and req_type != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[67]原语 sens = filter sens by req_type != "" and req_type ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.req_type', 'Action': 'str', 'str': 'req_type', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[68]原语 sens.req_type = str req_type by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': 'req_type unlike name'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[69]原语 sens = filter sens by req_type unlike name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_d2df', 'with': 'req_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[70]原语 sens = @udf sens by udf0.df_d2df with req_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'num:int,value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[71]原语 alter sens by num:int,value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'num', 'by': 'df["num"] * df["value"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[85]原语 sens = add num by df["num"] * df["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens', 'by': 'url,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[86]原语 sens2 = loc sens by url,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens', 'Action': 'union', 'union': 'sens1,sens2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[88]原语 sens = union sens1,sens2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens', 'Action': 'union', 'union': 'sens,sss'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[90]原语 sens = union sens,sss 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens', 'by': 'url', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[91]原语 sens = group sens by url agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[92]原语 sens = @udf sens by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'num_sum':'count1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[93]原语 rename sens as ("num_sum":"count1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'senh_count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url_c as url,count(uuid) as count2 from sen_http_count where timestamp > '$month' group by url"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[96]原语 senh_count = load ckh by ckh with select url_c as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'senh_count', 'by': 'url:str,count2:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[97]原语 alter senh_count by url:str,count2:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens', 'Action': 'join', 'join': 'sens,senh_count', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[98]原语 sens = join sens,senh_count by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'mean', 'by': 'sens["count1"]/sens["count2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[99]原语 sens = add mean by (sens["count1"]/sens["count2"])... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'url,mean'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[100]原语 sens = loc sens by url,mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'ssdb', 'with': 'sens_mean'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[101]原语 store sens to ssdb with sens_mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct urld from api_monitor where yw_count >= 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[104]原语 a = load ckh by ckh with select distinct urld from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a', 'by': 'urld:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[105]原语 alter a by urld:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'data', 'with': 'a["urld"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[106]原语 a = add data with (a["urld"]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 'a', 'by': 'urld', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[107]原语 s = loc a by urld to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'dd:bs_model'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[108]原语 store s to ssdb with dd:bs_model 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_model.fbi]执行第[110]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],110

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



