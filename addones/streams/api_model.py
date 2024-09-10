#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_model.xlk
#datetime: 2024-08-30T16:10:58.294692
#copyright: OpenFBI

import sys 
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
sys.path.append("../")
import json
from . import *
import threading
try:
	import numpy as np 
	import  pandas as pd
	from avenger.fbiprocesser import *
	from avenger.fglobals import *

except:
	pass



#流和批共享的函数：

#数组到DF
def push_arrays_to_df(arrays,name=""):
	if len(arrays)==0:
		return 0
		
	try:
		#lockP.acquire()
		b  = arrays.copy()
		del arrays[0:len(b)]
		#arrays.clear()
		#lockP.release()

		df = pd.DataFrame(b)
		#设置index 为0
		df['seq19821221'] = 0
		df.set_index('seq19821221',inplace=True)
		if fbi_global.runtime.is_have(name):
			o = fbi_global.runtime.get(name)
			dfs=[o.df,df]
			dfz = pd.concat(dfs,sort=True)
			o.df = dfz
		else:
			o = FbiTable(name,df)
			fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			o.df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_arrays_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_arrays_to_df

#字典到DF
def push_dict_to_df(d,name=""):
	try:
		dd = d.copy() #浅复制，保持不变
		df = pd.DataFrame(data=list(dd.values()),index=list(dd.keys()))
		o = FbiTable(name,df)
		fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_dict_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_dict_to_df


#mysql到DF
def mysql_to_df(a,cols,name=""):
	try:
		df = pd.DataFrame(data=a,columns=cols)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_mysql_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
	return df
#end mysql_to_df

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

#LastModifyDate:　2024-01-09T11:43:47    Author:   qh

#LastModifyDate:　2024-01-09T10:26:37    Author:   rzc

#LastModifyDate:　2024-01-08T09:15:09    Author:   superFBI

#LastModifyDate:　2024-01-06T15:47:30    Author:   superFBI

#LastModifyDate:　2024-01-06T13:53:28    Author:   superFBI

#LastModifyDate:　2024-01-05T09:54:25.740756    Author:   superFBI

#LastModifyDate:　2023-12-27T13:59:12.229975    Author:   superFBI

#LastModifyDate:　2023-12-20T11:19:07.229000    Author:   superFBI

#LastModifyDate:　2023-12-20T11:05:32.958214    Author:   superFBI

#LastModifyDate:　2023-09-25T18:03:04.434533    Author:   superFBI

#LastModifyDate:　2023-08-08T18:37:17.256513    Author:   pjb

#处理访问信息，最终数据保存在clickhouse中

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "数据泄露风险模型"
	stream["meta_desc"] = "风险模型构建1479，从api_visit主题中消费数据，存入ckh数据库表api_model"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/model"}
	stream["source"] = {"shm_name":"httpub","count":8}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_model" in a:
		stream["sends"] = 1
		set_param("syslog","1")
	else:
		stream["sends"] = 0
		set_param("syslog","0")
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	stream["stw"]["stw_flow"]={"times":60,"fun":"flow"}
	stream["count"] = 0
	stream["count-10"] = 0
	stream["ap"] = load_ssdb_hall("FF:acc_ip")
	stream["up"] = load_ssdb_hall("FF:url_ip")
	stream["ua"] = load_ssdb_hall("FF:url_acc")
	stream["au"] = load_ssdb_hall("FF:acc_url")
	stream["pu"] = load_ssdb_hall("FF:ip_url")
	#stream["risk_url"] = load_ssdb_hall("FF:risk_url")
	r = load_ssdb_kv("risk_url_xlk")["data"]
	stream["risk_url"] = []
	for item in r:
		stream["risk_url"].append(item[0])
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	c = load_ssdb_kv("model_config")
	stream["model1_count"] = c["setting"]["model1"]["srcip_count"]
	stream["model1_on"] = c["setting"]["switch"]["model1"]
	stream["model4_on"] = c["setting"]["switch"]["model4"]
	stream["model6_on"] = c["setting"]["switch"]["model6"]
	stream["model7_on"] = c["setting"]["switch"]["model7"]
	stream["model8_on"] = c["setting"]["switch"]["model8"]
	stream["model9_on"] = c["setting"]["switch"]["model9"]
	stream["model1_conf"] = delem(c["setting"]["model1"]["whitelist"])
	stream["model4_conf"] = delem(c["setting"]["model4"]["whitelist"])
	stream["model6_conf"] = delem(c["setting"]["model6"]["whitelist"])
	stream["model7_conf"] = delem(c["setting"]["model7"]["whitelist"])
	stream["model8_conf"] = delem(c["setting"]["model8"]["whitelist"])
	stream["model9_conf"] = delem(c["setting"]["model9"]["whitelist"])
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	srcip_model = load_ssdb_kv("srcip_model_xlk")["data"]
	stream["srcip_model"] = []
	for item in srcip_model:
		stream["srcip_model"].append(item[0])
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	data_type=o.get("data_type")
	if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
		srcip = o.get("src_ip")
		if srcip in stream["srcip_model"]:
			url = o.get("url")
			if stream["all_combo"] or url in stream["monitor_url"]:
				account = o.get("account")
				ktimestamp = o["timestamp"]
				o["timestamp"] = iso_to_datetime(o["timestamp"])
				v = clone_o(o)
				if o.get("realip"):
					srcip = o.get("realip")
			#1.同一账号多终端访问敏感数据
				#if stream["model1_on"]:
				http_api = deepcopy(v)
				ps = 0
				for i in stream["model1_conf"]:
					a = 0
					for k in i:
						if http_api[k] == i[k]:
							a = a + 1
					if len(i) == a:
						ps = 1
						break
				if not stream["model1_conf"] or ps:
					if account and url in stream["risk_url"]:
						if account not in stream["ap"]:
							list1 = []
							list1.append(srcip)
							stream["ap"][account] = list1
							to_ssdb_h("FF:acc_ip", account, stream["ap"][account])
						elif srcip not in stream["ap"][account]:
							stream["ap"][account].append(srcip)
							to_ssdb_h("FF:acc_ip", account, stream["ap"][account])
							if stream["model1_on"]:
								if len(stream["ap"][account]) > stream["model1_count"]:
									http_api = deepcopy(v)
									http_api["id"] = xlink_uuid(1)
									http_api["type"] = 1
									http_api["level"] = 1
									http_api["proof"] = o.get("id")
									http_api["desc"] = "一个账号在多个终端上登录并访问敏感接口"
									srcips = stream["ap"][account]
									http_api["message"] = "账号“" + account + "”在多个终端上登录并访问敏感接口，其他登录终端有" + str(srcips)
									proofs = {}
									proofs["判定标准"] = "账号多终端访问敏感数据：同一账号在终端上访问敏感数据接口，当该账号出现在不同终端的数据大于设定的阈值时发出告警"
									proofs["账号"] = account
									proofs["终端"] = srcips
									proofs["阈值"] = stream["model1_count"]
									proofs["结果"] = "同一账号在" + str(len(stream["ap"][account])) + "个终端上登录过，且都访问了敏感接口"
									proofs["证据"] = {}
									proofs["证据"]["时间"] = "HTTP协议ID"
									proofs["证据"][str(o.get("timestamp"))] = o.get("id")
									proofs = ujson.dumps(proofs, ensure_ascii=False)
									http_api["proofs"] = proofs
									to_table(http_api)
									if stream["sends"]:
										s = deepcopy(http_api)
										s["event_type"] = "model"
										#to_kfk(s)
										to_json_file("/data/syslog_file/eve",s)
			#9.重要接口新终端或账户访问行为
				#if stream["model8_on"]:
				http_api = deepcopy(v)
				ps = 0
				for i in stream["model8_conf"]:
					a = 0
					for k in i:
						if http_api[k] == i[k]:
							a = a + 1
					if len(i) == a:
						ps = 1
						break
				if not stream["model8_conf"] or ps:
					if url not in stream["up"]:
						list1 = []
						list1.append(srcip)
						stream["up"][url] = list1
						to_ssdb_h("FF:url_ip", url, stream["up"][url])
					elif srcip not in stream["up"][url]:
						stream["up"][url].append(srcip)
						to_ssdb_h("FF:url_ip", url, stream["up"][url])
						if stream["model8_on"]:
							http_api["id"] = xlink_uuid(1)
							http_api["type"] = 8
							http_api["level"] = 0
							http_api["proof"] = o.get("id")
							http_api["desc"] = "重要接口新终端访问行为"
							http_api["message"] = "新终端“" + srcip + "”访问审计接口" + url
							proofs = {}
							proofs["判定标准"] = "新终端访问重要接口：重要接口（开启审计的接口）在被首次出现的终端访问时发出告警"
							proofs["接口"] = url
							proofs["终端"] = srcip
							proofs["结果"] = "终端第一次访问了开启审计功能的接口"
							proofs["证据"] = {}
							proofs["证据"]["时间"] = "HTTP协议ID"
							proofs["证据"][str(o.get("timestamp"))] = o.get("id")
							proofs = ujson.dumps(proofs, ensure_ascii=False)
							http_api["proofs"] = proofs
							to_table(http_api)
							if stream["sends"]:
								s = deepcopy(http_api)
								s["event_type"] = "model"
								#to_kfk(s)
								to_json_file("/data/syslog_file/eve",s)
				#if stream["model9_on"]:
				if account:
					http_api = deepcopy(v)
					ps = 0
					for i in stream["model9_conf"]:
						a = 0
						for k in i:
							if http_api[k] == i[k]:
								a = a + 1
						if len(i) == a:
							ps = 1
							break
					if not stream["model9_conf"] or ps:
						if url not in stream["ua"]:
							list1 = []
							list1.append(account)
							stream["ua"][url] = list1
							to_ssdb_h("FF:url_ip", url, stream["ua"][url])
						elif account not in stream["ua"][url]:
							stream["ua"][url].append(account)
							to_ssdb_h("FF:url_ip", url, stream["ua"][url])
							if stream["model9_on"]:
								http_api["id"] = xlink_uuid(1)
								http_api["type"] = 9
								http_api["level"] = 0
								http_api["proof"] = o.get("id")
								http_api["desc"] = "重要接口新终端或账户访问行为"
								http_api["message"] = "新账号“" + account + "”访问审计接口" + url
								proofs = {}
								proofs["判定标准"] = "新账号访问重要接口：重要接口（开启审计的接口）在被首次出现的账号访问时发出告警"
								proofs["接口"] = url
								proofs["账号"] = account
								proofs["结果"] = "账号第一次访问了开启审计功能的接口"
								proofs["证据"] = {}
								proofs["证据"]["时间"] = "HTTP协议ID"
								proofs["证据"][str(o.get("timestamp"))] = o.get("id")
								proofs = ujson.dumps(proofs, ensure_ascii=False)
								http_api["proofs"] = proofs
								to_table(http_api)
								if stream["sends"]:
									s = deepcopy(http_api)
									s["event_type"] = "model"
									#to_kfk(s)
									to_json_file("/data/syslog_file/eve",s)
			#7.同一终端或账户访问操作基线偏离行为
				#if stream["model6_on"]:
				http_api = deepcopy(v)
				ps = 0
				for i in stream["model6_conf"]:
					a = 0
					for k in i:
						if http_api[k] == i[k]:
							a = a + 1
					if len(i) == a:
						ps = 1
						break
				if not stream["model6_conf"] or ps:
					if srcip not in stream["pu"]:
						list1 = []
						list1.append(url)
						stream["pu"][srcip] = list1
						to_ssdb_h("FF:ip_url", srcip, stream["pu"][srcip])
					elif url not in stream["pu"][srcip]:
						stream["pu"][srcip].append(url)
						to_ssdb_h("FF:ip_url", srcip, stream["pu"][srcip])
						if stream["model6_on"]:
							http_api["id"] = xlink_uuid(1)
							http_api["type"] = 6
							http_api["level"] = 0
							http_api["proof"] = o.get("id")
							http_api["desc"] = "终端访问操作非常用接口"
							http_api["message"] = "终端“" + srcip + "”访问了非常用接口" + url
							proofs = {}
							proofs["判定标准"] = "终端访问操作基线偏离行为：终端在第一访问之前未访问过的接口时发出告警"
							proofs["接口"] = url
							proofs["终端"] = srcip
							proofs["结果"] = "终端访问了之前没有访问过的接口"
							proofs["证据"] = {}
							proofs["证据"]["时间"] = "HTTP协议ID"
							proofs["证据"][str(o.get("timestamp"))] = o.get("id")
							proofs = ujson.dumps(proofs, ensure_ascii=False)
							http_api["proofs"] = proofs
							to_table(http_api)
							if stream["sends"]:
								s = deepcopy(http_api)
								s["event_type"] = "model"
								#to_kfk(s)
								to_json_file("/data/syslog_file/eve",s)
				#if stream["model7_on"]:
				if account:
					http_api = deepcopy(v)
					ps = 0
					for i in stream["model7_conf"]:
						a = 0
						for k in i:
							if http_api[k] == i[k]:
								a = a + 1
						if len(i) == a:
							ps = 1
							break
					if not stream["model7_conf"] or ps:
						if srcip not in stream["au"]:
							list1 = []
							list1.append(url)
							stream["au"][account] = list1
							to_ssdb_h("FF:acc_url", account, stream["au"][account])
						elif url not in stream["au"][account]:
							stream["au"][account].append(url)
							to_ssdb_h("FF:acc_url", account, stream["au"][account])
							if stream["model7_on"]:
								http_api["id"] = xlink_uuid(1)
								http_api["type"] = 7
								http_api["level"] = 0
								http_api["proof"] = o.get("id")
								http_api["desc"] = "账户访问操作非常用接口"
								http_api["message"] = "账户“" + account + "”访问了非常用接口" + url
								proofs = {}
								proofs["判定标准"] = "账号访问操作基线偏离行为：账号在第一访问之前未访问过的接口时发出告警"
								proofs["接口"] = url
								proofs["账号"] = account
								proofs["结果"] = "账号访问了之前没有访问过的接口"
								proofs["证据"] = {}
								proofs["证据"]["时间"] = "HTTP协议ID"
								proofs["证据"][str(o.get("timestamp"))] = o.get("id")
								proofs = ujson.dumps(proofs, ensure_ascii=False)
								http_api["proofs"] = proofs
								to_table(http_api)
								if stream["sends"]:
									s = deepcopy(http_api)
									s["event_type"] = "model"
									#to_kfk(s)
									to_json_file("/data/syslog_file/eve",s)
			#4.频繁身份登陆验证行为
				if stream["model4_on"]:
					http_api = deepcopy(v)
					ps = 0
					for i in stream["model4_conf"]:
						a = 0
						for k in i:
							if http_api[k] == i[k]:
								a = a + 1
						if len(i) == a:
							ps = 1
							break
					if not stream["model4_conf"] or ps:
						api_type = o.get("api_type")
						if api_type == "1":
							k = iso_to_timestamp(ktimestamp)
							#http_api = deepcopy(v)
							http_api["id"] = xlink_uuid(1)
							http_api["type"] = 4
							http_api["level"] = 1
							http_api["suid"] = o.get("id")
							http_api["response"] = o.get("http_response_body")
							http_api["desc"] = "单一终端频繁访问登录接口"
							http_api["message"] = "终端“" + srcip + "”频繁登录接口" + http_api.get("url")
							push_stw("stw_flow",k,http_api)
#end 

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'model_config', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'model_config as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[342]原语 model_config = load ssdb ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'bcount', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model4"]["count"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[343]原语 bcount = jaas model_confi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'srcip,url', 'agg': 'srcip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[344]原语 df2 = group df by srcip,u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[345]原语 df2 = @udf df2 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'df2', 'by': 'srcip_count > $bcount'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[346]原语 df2 = filter df2 by srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df2,df', 'by': '[srcip,url],[srcip,url]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[347]原语 df3 = join df2,df by [src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'srcip,url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[348]原语 df3 = distinct df3 by (sr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'acc', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[349]原语 acc = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[350]原语 proof = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[351]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'bcount', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$bcount,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[352]原语 bcount = @sdf sys_str wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'df3', 'with': 'url=$2,srcip=$1,srcip_count=$3', 'run': '""\nf = filter df by (srcip == "@srcip" and url == "@url")\na = loc f by account\na = distinct a by account\na = @udf a by udf0.df_T\na = @udf a by udf0.df_cs2l\nacc = union (acc,a)\nb = loc f by suid\nb= @udf b by udf0.df_T\nb = @udf b by udf0.df_cs2l\nproof = union (proof,b)\nc = loc f by timestamp,suid,response\n#rename c as ("uid":"suid")\n#assert $b == 10 as break with 123\nd = @udf c by model.proof4 with @srcip,@url,$bcount,@srcip_count\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[353]原语 foreach df3 run "f = filt... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'acc', 'Action': '@udf', '@udf': 'acc', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[370]原语 acc = @udf acc by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'acc', 'Action': 'loc', 'loc': 'acc', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[371]原语 acc = loc acc drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[372]原语 df3 = @udf df3 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[373]原语 df3 = @udf df3 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[374]原语 df3 = loc df3 drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'proof', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[375]原语 proof = @udf proof by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proof', 'Action': 'loc', 'loc': 'proof', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[376]原语 proof = loc proof drop in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[377]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[378]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df3,acc', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[379]原语 df3 = join df3,acc by ind... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.srcip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[380]原语 alter df3.srcip_count as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.s0', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[381]原语 alter df3.s0 as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'message', 'with': 'df3["message"] + \',次数:\' + df3["srcip_count"] + \'尝试账号：\' + df3["s0"]'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[382]原语 df3 = add message with (d... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'drop': 'srcip_count,s0,suid,response'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[383]原语 df3 = loc df3 drop (srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df3,proof', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[384]原语 df3 = join df3,proof by i... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'df3', 'by': '"s0":"proof"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[385]原语 rename df3 by ("s0":"proo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.proof', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[386]原语 alter df3.proof as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df3,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[387]原语 df3 = join df3,proofs by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.timestamp', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[388]原语 alter df3.timestamp as da... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df3', 'to': 'ckh', 'by': 'ckh', 'with': 'api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[389]原语 store df3 to ckh by ckh w... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"@syslog" == "1"', 'with': '""\n#define kfka as "@ss"\n#k = @udf KFK.df_link with kfka\nalter df3.timestamp as str\ndf3 = add event_type by ("model")\n#a = @udf df3 by KFK.fast_store with kfka,api_send\na = @udf df3 by df2jsonfile.pushf\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=390
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[390]原语 if "@syslog" == "1" with ... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[398]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[399]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[400]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[401]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(table,"api_model")
#end 

#系统定时函数，st为时间戳 
def send60(st):
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_model" in a:
		stream["sends"] = 1
		set_param("syslog","1")
	else:
		stream["sends"] = 0
		set_param("syslog","0")
	r = load_ssdb_kv("risk_url_xlk")["data"]
	b = []
	for item in r:
		b.append(item[0])
	stream["risk_url"] = b
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	c = []
	for item in s:
		c.append(item[0])
	stream["monitor_url"] = c
	srcip_model = load_ssdb_kv("srcip_model_xlk")["data"]
	src = []
	for item in srcip_model:
		src.append(item[0])
	stream["srcip_model"] = src
	cc = load_ssdb_kv("model_config")
	stream["model1_count"] = cc["setting"]["model1"]["srcip_count"]
	stream["model1_on"] = cc["setting"]["switch"]["model1"]
	stream["model4_on"] = cc["setting"]["switch"]["model4"]
	stream["model6_on"] = cc["setting"]["switch"]["model6"]
	stream["model7_on"] = cc["setting"]["switch"]["model7"]
	stream["model8_on"] = cc["setting"]["switch"]["model8"]
	stream["model9_on"] = cc["setting"]["switch"]["model9"]
	stream["model1_conf"] = delem(cc["setting"]["model1"]["whitelist"])
	stream["model4_conf"] = delem(cc["setting"]["model4"]["whitelist"])
	stream["model6_conf"] = delem(cc["setting"]["model6"]["whitelist"])
	stream["model7_conf"] = delem(cc["setting"]["model7"]["whitelist"])
	stream["model8_conf"] = delem(cc["setting"]["model8"]["whitelist"])
	stream["model9_conf"] = delem(cc["setting"]["model9"]["whitelist"])
	stream["all_combo"] = cc["setting"]["switch"]["all_combo"]
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_o(o):
	http_api = {}
	http_api["timestamp"] = o.get("timestamp")
	http_api["url_a"] = o.get("url")
	http_api["account"] = o.get("account")
	http_api["url"] = o.get("url_c")
	http_api["srcip"] = o.get("src_ip")
	http_api["real_ip"] = o.get("realip")
	http_api["srcport"] = o.get("src_port")
	http_api["dstip"] = o.get("dest_ip")
	http_api["dstport"] = o.get("dest_port")
	http_api["app"] = o.get("app")
	return http_api
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def delem(a):
	for i in a:
		for k in list(i.keys()):
			if not i[k]:
				del i[k]
	for i in range(len(a)):
		a.remove({})
	return a
#end 

#自定义批处理函数，使用FBI语句块 
def save (k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model', 'Action': '@udf', '@udf': 'model', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[480]原语 model = @udf model by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'model', 'to': 'ckh', 'by': 'ckh', 'with': 'api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[481]原语 store model to ckh by ckh... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'model'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[483]原语 drop model... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_model.xlk]执行第[484]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
#from method_fun import *
from copy import deepcopy
import ujson
#end 

#udf

#end 
