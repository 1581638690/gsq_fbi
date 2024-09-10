#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_set_risklevel
#datetime: 2024-08-30T16:10:54.355935
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
		add_the_error('[qh_set_risklevel.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_r', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url,id from data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[33]原语 api_r = @udf RS.load_mysql_sql with (mysql1,select... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct api,type from api19_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[34]原语 api19_risk = load db by mysql1 with select distinc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk.type', 'Action': 'str', 'str': 'type', 'by': "findall('API19-[1-9]')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[35]原语 api19_risk.type = str type by (findall("API19-[1-9... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk.type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[36]原语 alter api19_risk.type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk.type', 'Action': 'lambda', 'lambda': 'type', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[37]原语 api19_risk.type = lambda type by (x:x[2:-2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'api19_risk', 'Action': 'distinct', 'distinct': 'api19_risk', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[38]原语 api19_risk = distinct api19_risk by (api,type) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk.type', 'Action': 'lambda', 'lambda': 'type', 'by': "x:x+';'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[39]原语 api19_risk.type = lambda type by (x:x+";") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api19_risk1', 'Action': 'group', 'group': 'api19_risk', 'by': 'api', 'agg': 'type:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[40]原语 api19_risk1 = group api19_risk by api agg type:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk1.type_sum', 'Action': 'lambda', 'lambda': 'type_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[41]原语 api19_risk1.type_sum = lambda type_sum by (x:x[:-1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api19_risk1', 'Action': 'add', 'add': 'risk_label_value', 'by': 'df["type_sum"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[42]原语 api19_risk1 = add risk_label_value by (df["type_su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-1','API19-1损坏的对象级别授权')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[43]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-2','API19-2损坏的用户身份验证')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[44]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-3','API19-3过度的数据暴露')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[45]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-4','API19-4缺乏资源和速率限制')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[46]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-7','API19-7安全性配置错误')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[47]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api19_risk1.risk_label_value', 'Action': 'str', 'str': 'risk_label_value', 'by': "replace('API19-8','API19-8注入')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[48]原语 api19_risk1.risk_label_value = str risk_label_valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_risk1', 'Action': '@udf', '@udf': 'api19_risk1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[49]原语 api19_risk1 = @udf api19_risk1 by udf0.df_reset_in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk1', 'as': '"risk_label_sum":"risk_label","api":"url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[50]原语 rename api19_risk1 as ("risk_label_sum":"risk_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api', 'Action': 'join', 'join': 'api_r,api19_risk1', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[51]原语 api = join api_r,api19_risk1 by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_fillna_cols', 'with': "type_sum:'0',risk_label_value:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[52]原语 api = @udf api by udf0.df_fillna_cols with type_su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api', 'Action': 'filter', 'filter': 'api', 'by': "risk_label_value != '0'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[53]原语 api = filter api by (risk_label_value != "0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_rowl', 'with': 'lambda x:"2" if "19-1" in x[2] or "19-2" in x[2] or "19-4" in x[2] or "19-7" in x[2] or "19-8" in x[2] else "1" '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[54]原语 api = @udf api by udf0.df_rowl with (lambda x:"2" ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api', 'as': '"lambda0":"risk_level","type_sum":"risk_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[55]原语 rename api as ("lambda0":"risk_level","type_sum":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[56]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[57]原语 api = @udf api by CRUD.save_table with (mysql1,dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[62]原语 sens = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'app:str,url:str,src_ip:str,account:str,key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[63]原语 alter sens by app:str,url:str,src_ip:str,account:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[64]原语 api1 = load db by mysql1 with select id,url from d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api1', 'by': 'id:int,url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[65]原语 alter api1 by id:int,url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens', 'by': "type == '响应体'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[67]原语 sens1 = filter sens by type == "响应体" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': 'url,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[68]原语 sens1 = loc sens1 by url,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens1', 'Action': 'distinct', 'distinct': 'sens1', 'by': 'url,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[69]原语 sens1 = distinct sens1 by url,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('身份证','0')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[70]原语 sens1.key = str key by (replace("身份证","0")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('手机号','1')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[71]原语 sens1.key = str key by (replace("手机号","1")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('邮箱','2')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[72]原语 sens1.key = str key by (replace("邮箱","2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('地址','3')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[73]原语 sens1.key = str key by (replace("地址","3")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('婚姻状况','4')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[74]原语 sens1.key = str key by (replace("婚姻状况","4")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('宗教信仰','5')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[75]原语 sens1.key = str key by (replace("宗教信仰","5")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('发票代码','6')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[76]原语 sens1.key = str key by (replace("发票代码","6")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人识别号或社会统一信用代码','7')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[77]原语 sens1.key = str key by (replace("纳税人识别号或社会统一信用代码",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人名称或公司名称','8')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[78]原语 sens1.key = str key by (replace("纳税人名称或公司名称","8"))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('银行卡号','9')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[79]原语 sens1.key = str key by (replace("银行卡号","9")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('收入','10')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[80]原语 sens1.key = str key by (replace("收入","10")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('姓名','11')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[81]原语 sens1.key = str key by (replace("姓名","11")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens1', 'Action': 'distinct', 'distinct': 'sens1', 'by': 'url,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[83]原语 sens1 = distinct sens1 by (url,key) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens1', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[84]原语 sens1 = filter sens1 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens1', 'Action': 'add', 'add': 'key', 'by': "sens1.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[86]原语 sens1 = add key by (sens1.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens1', 'Action': 'group', 'group': 'sens1', 'by': 'url', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[87]原语 sens1 = group sens1 by url agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[88]原语 sens1.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens1.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[89]原语 alter sens1.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[90]原语 sens1.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[91]原语 sens1 = @udf sens1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens1', 'as': '"key_sum":"res_llabel"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[93]原语 rename sens1 as ("key_sum":"res_llabel") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens1', 'Action': 'join', 'join': 'api1,sens1', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[94]原语 sens1 = join api1,sens1 by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[95]原语 sens1 = @udf sens1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[96]原语 sens1 = @udf sens1 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens2', 'Action': 'filter', 'filter': 'sens', 'by': "type == '请求体'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[100]原语 sens2 = filter sens by type == "请求体" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens2', 'by': 'url,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[101]原语 sens2 = loc sens2 by url,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens2', 'Action': 'distinct', 'distinct': 'sens2', 'by': 'url,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[102]原语 sens2 = distinct sens2 by url,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('身份证','0')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[103]原语 sens2.key = str key by (replace("身份证","0")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('手机号','1')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[104]原语 sens2.key = str key by (replace("手机号","1")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('邮箱','2')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[105]原语 sens2.key = str key by (replace("邮箱","2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('地址','3')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[106]原语 sens2.key = str key by (replace("地址","3")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('婚姻状况','4')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[107]原语 sens2.key = str key by (replace("婚姻状况","4")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('宗教信仰','5')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[108]原语 sens2.key = str key by (replace("宗教信仰","5")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('发票代码','6')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[109]原语 sens2.key = str key by (replace("发票代码","6")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人识别号或社会统一信用代码','7')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[110]原语 sens2.key = str key by (replace("纳税人识别号或社会统一信用代码",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人名称或公司名称','8')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[111]原语 sens2.key = str key by (replace("纳税人名称或公司名称","8"))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('银行卡号','9')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[112]原语 sens2.key = str key by (replace("银行卡号","9")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('收入','10')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[113]原语 sens2.key = str key by (replace("收入","10")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens2.key', 'Action': 'str', 'str': 'key', 'by': "replace('姓名','11')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[114]原语 sens2.key = str key by (replace("姓名","11")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens2', 'Action': 'distinct', 'distinct': 'sens2', 'by': 'url,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[115]原语 sens2 = distinct sens2 by (url,key) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens2', 'Action': 'filter', 'filter': 'sens2', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[116]原语 sens2 = filter sens2 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens2', 'Action': 'add', 'add': 'key', 'by': "sens2.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[118]原语 sens2 = add key by (sens2.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens2', 'Action': 'group', 'group': 'sens2', 'by': 'url', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[119]原语 sens2 = group sens2 by url agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[120]原语 sens2.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens2.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[121]原语 alter sens2.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[122]原语 sens2.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[123]原语 sens2 = @udf sens2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens2', 'as': '"key_sum":"req_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[125]原语 rename sens2 as ("key_sum":"req_label") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens2', 'Action': 'join', 'join': 'api1,sens2', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[126]原语 sens2 = join api1,sens2 by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[127]原语 sens2 = @udf sens2 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[128]原语 sens2 = @udf sens2 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[195]原语 sen_level = load ssdb by ssdb0 with sensitive as j... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_level', 'Action': '@udf', '@udf': 'sen_level', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[196]原语 sen_level = @udf sen_level by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_level', 'by': 'data:string'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[197]原语 alter sen_level by data:string 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sen_level.sensitive_label', 'Action': 'str', 'str': 'data', 'by': 'findall("level\': \'(.*?)\'")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[198]原语 sen_level.sensitive_label = str data by (findall("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sen_level.key', 'Action': 'str', 'str': 'data', 'by': 'findall("rekey\': \'(.*?)\',")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[199]原语 sen_level.key = str data by (findall("rekey": "(.*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_level', 'Action': '@udf', '@udf': 'sen_level', 'by': 'udf0.df_drop_col', 'with': 'data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[200]原语 sen_level = @udf sen_level by udf0.df_drop_col wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_level', 'by': 'key:string,sensitive_label:string'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[201]原语 alter sen_level by key:string,sensitive_label:stri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_level.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[203]原语 sen_level.key = lambda key by (x:x[2:-2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_level.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[204]原语 sen_level.sensitive_label = lambda sensitive_label... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'senapi', 'Action': 'loc', 'loc': 'sens', 'by': 'url,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[206]原语 senapi = loc sens by url,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'senapi', 'Action': 'join', 'join': 'senapi,sen_level', 'by': 'key,key', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[207]原语 senapi = join senapi,sen_level by key,key with lef... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'senapi', 'Action': '@udf', '@udf': 'senapi', 'by': 'udf0.df_fillna_cols', 'with': "url:'',key:'',sensitive_label:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[208]原语 senapi = @udf senapi by udf0.df_fillna_cols with u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'senapi', 'Action': 'filter', 'filter': 'senapi', 'by': 'sensitive_label != ""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[209]原语 senapi = filter senapi by sensitive_label != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'senapi', 'Action': '@udf', '@udf': 'senapi', 'by': 'udf0.df_drop_col', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[210]原语 senapi = @udf senapi by udf0.df_drop_col with key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'senapi', 'Action': 'distinct', 'distinct': 'senapi', 'by': 'url,sensitive_label'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[211]原语 senapi = distinct senapi by url,sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'senapi.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[212]原语 alter senapi.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapi.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x + \',\' if x != "" else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[213]原语 senapi.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'senapi', 'Action': 'group', 'group': 'senapi', 'by': 'url', 'agg': 'sensitive_label:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[214]原语 senapi = group senapi by url agg sensitive_label:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'senapi', 'Action': '@udf', '@udf': 'senapi', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[215]原语 senapi = @udf senapi by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'senapi', 'as': '"sensitive_label_sum":"sensitive_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[216]原语 rename senapi as ("sensitive_label_sum":"sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapi.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'3' if '3' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[217]原语 senapi.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapi.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'2' if '2' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[218]原语 senapi.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapi.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'1' if '1' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[219]原语 senapi.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select url,id from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[220]原语 api = load db by mysql1 with select url,id from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api', 'Action': 'join', 'join': 'api,senapi', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[221]原语 api = join api,senapi by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api.sensitive_label', 'as': 'float64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[222]原语 alter api.sensitive_label as float64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_fillna_cols', 'with': 'sensitive_label:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[223]原语 api = @udf api by udf0.df_fillna_cols with sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api.sensitive_label', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[224]原语 alter api.sensitive_label as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api', 'Action': 'filter', 'filter': 'api', 'by': 'sensitive_label != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[225]原语 api = filter api by (sensitive_label != 0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[226]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[227]原语 api = @udf api by CRUD.save_table with (mysql1,dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'senapp', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,sensitive_label from data_api_new where sensitive_label != 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[231]原语 senapp = load db by mysql1 with select app,sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'senapp', 'Action': 'distinct', 'distinct': 'senapp', 'by': 'app,sensitive_label'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[232]原语 senapp = distinct senapp by (app,sensitive_label) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'senapp.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[233]原语 alter senapp.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapp.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x + \',\' if x != "" else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[234]原语 senapp.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'senapp', 'Action': 'group', 'group': 'senapp', 'by': 'app', 'agg': 'sensitive_label:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[235]原语 senapp = group senapp by app agg sensitive_label:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'senapp', 'Action': '@udf', '@udf': 'senapp', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[236]原语 senapp = @udf senapp by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'senapp', 'as': '"sensitive_label_sum":"sensitive_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[237]原语 rename senapp as ("sensitive_label_sum":"sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapp.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'3' if '3' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[238]原语 senapp.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapp.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'2' if '2' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[239]原语 senapp.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'senapp.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'1' if '1' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[240]原语 senapp.sensitive_label = lambda sensitive_label by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,id from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[241]原语 app = load db by mysql1 with select app,id from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'app,senapp', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[242]原语 app = join app,senapp by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app.sensitive_label', 'as': 'float64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[243]原语 alter app.sensitive_label as float64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_fillna_cols', 'with': 'sensitive_label:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[244]原语 app = @udf app by udf0.df_fillna_cols with sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app.sensitive_label', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[245]原语 alter app.sensitive_label as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app', 'Action': 'filter', 'filter': 'app', 'by': 'sensitive_label != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[246]原语 app = filter app by (sensitive_label != 0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[247]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[248]原语 app = @udf app by CRUD.save_table with (mysql1,dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_set_risklevel.fbi]执行第[250]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],250

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



