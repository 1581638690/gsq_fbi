#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_operation_event_oper.xlk
#datetime: 2024-08-30T16:10:58.408013
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

#LastModifyDate:　2024-08-29T14:36:53    Author:   rzc

#LastModifyDate:　2024-08-29T12:25:34    Author:   rzc

#LastModifyDate:　2024-08-29T12:19:24    Author:   rzc

#LastModifyDate:　2024-08-29T11:54:46    Author:   rzc

#LastModifyDate:　2024-08-29T11:24:57    Author:   rzc

#LastModifyDate:　2024-08-29T11:19:04    Author:   rzc

#LastModifyDate:　2024-08-29T11:13:27    Author:   rzc

#LastModifyDate:　2024-08-27T17:59:00    Author:   rzc

#LastModifyDate:　2024-08-26T11:41:37    Author:   rzc

#LastModifyDate:　2024-08-26T11:37:10    Author:   rzc

#LastModifyDate:　2024-08-23T17:58:37    Author:   rzc

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "对API接口数据进行分析"
	stream["meta_desc"] = "分析API接口数据，账户做了什么操作行为"
	stream["source"]= {"unix_udp":"/tmp/operation_events_oper"}
	
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	stream["st"]["st_30f"]={"times":10,"fun":"print30"}
	stream["st"]["st_10f"]={"times":10,"fun":"print10"}
	stream["st"]["st_5s"]={"times":5,"fun":"print5"}
	#chk的链接
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	
	#创建ckh的pool
	pool["event_model"] = []
	stream["con_rules"] = load_model_data("operevent")
	try:
		with open("/data/xlink/models_paths/table_dic.pkl","rb")as fp:
			stream["table_dic"] = pickle.load(fp)
	except:
		stream["table_dic"] = {}
	try:
		with open("/data/xlink/models_paths/tree_dic.pkl","rb")as fp:
			stream["tree_dic"] = pickle.load(fp)
	except:
		stream["tree_dic"] = {}
	try:
		with open("/data/xlink/models_paths/dict_tree.pkl","rb")as fp:
			stream["dict_tree"] = pickle.load(fp)
	except:
		stream["dict_tree"] = {}
		
	stream["action_dict"] ={}
	stream["gjxz"]={"预警主题类型":{"":"全部","0":"企业","1":"事件","2":"人员"},"反馈状态":{"":"全部","0":"未反馈","1":"已反馈"}}
	stream["url_list"] =  [
		"/hsdsh/peopleEnterprise/getEnterpriseBidding",
		"/hsdsh/peopleEnterprise/getPersonMaritalStatus",
		"/hsdsh/peopleEnterprise/getPersonEducationData",
		"/hsdsh/peopleEnterprise/getPersonMarriageInfo",
		"/hsdsh/peopleEnterprise/getPersonSocialInfo",
		"/hsdsh/peopleEnterprise/getPersonAccumulationFund",
		"/hsdsh/peopleEnterprise/getVehicleTrafficRecords",
		"/hsdsh/peopleEnterprise/getAccessControlRecords"
		]
	stream["basic_dict"] = {}
	stream["d_none"] = [{"url":"/hsdsh/collectionLibrary/getCollectionLibraryByType","parameter":"typeName=机关事业单位&depName="},
	{"url":"/pcip//risen/yjxx/getYjxxList","parameter":"page=0&pageSize=10"},
	{"url":"/pcip//risen/yjxx/getYjxxList","parameter":"page=0&pageSize=1"}
	]
	
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	
	# 获取当前的信息
	url =o.get("url")
	url_parts = url.split("//",1)[1]
	url = "/" + url_parts.split("/",1)[1]
	#printf("url",url)
	parameter = o.get("parameter")
	timestamp = o.get("time")
	o["url"]=url
	request_body_json = o.get("request_body_json")
	
	o["parameter"] = par_value_match(url,parameter)
	o["request_body_json"] = request_value_match(url,request_body_json)
	response_body = o.get("response_body","")
	# 数据字典结构
	stream["dict_tree"] = dict_common(url,response_body,stream["dict_tree"])
	# 组织目录结构
	stream["tree_dic"] = tree_common(url,response_body,stream["tree_dic"])
	#printf("tree_dic",stream["tree_dic"])
	session_id = o.get("session_id")
	#stream["count"]+=1
	ify_result = read_model_identify(stream["con_rules"],o)
	
		
	status_msg = ""
	action_name = "访问"
	subName =""
	url_type = ""
	parameter_json = o["parameter_json"]
	# 获取当前接口的名称 如果没有，就按照现在的，如果存在就进行覆盖
	
	url_name=o.get("name","")
	
	# 获取当前应用的名称，如果不存在，就按照模型生成的，如果存在就不使用模型的
	uapp_name= o.get("app_name","")
	# 现在已知存在操作 和返回结果两种行为了，默认
	ret_res = {}
	event = {}
	label_info_dict = {}
	if ify_result and isinstance(ify_result,dict):
		# 获取当前接口的名称 如果没有，就按照现在的，如果存在就进行覆盖
		label_info_dict = ify_result.get("label_info",{})
		
		label_name = label_info_dict.get("name","")
		if url_name =="" and label_name:
			url_name = label_name
		else:
			url_name = url_name 
		app_name = label_info_dict.get("app_name","")
		if uapp_name == "" and app_name:
			uapp_name = app_name
		else:
			uapp_name = uapp_name
		actions = label_info_dict.get("操作事件","")
		if not actions:
			action_name = action_name
		else:
			action_name = actions
		url_name = QueryApiName(url_name,label_info_dict,parameter,parameter_json)
		#printf("url_name",url_name)
		# add rzc 6/4
		url_type =label_info_dict.get("操作类型","")
		#printf("url_type",url_type)
		data_event = ify_result.get("data",{}) # 存在操作事件
		
		
		if data_event:
			# 获取事件信息,做一个列表 对事件信息进行处理
			event,ret_res,status_msg,subName,url_name = data_event_oper(data_event,subName,event,ret_res,label_info_dict,status_msg,url_name)
								
	
	ju_con = validate_interface_params(url,parameter,stream["d_none"])
	if ju_con:
		event = {}
		ret_res = {}
		status_msg=""
	
	if status_msg!="":
		event_dic = {"url":url,"time":iso_to_datetime(o["time"]),"cookie":o.get("cookie"),"flow_id":o.get("flow_id",""),"app":o.get("app"),"account":o.get("account"),"name":url_name,"parameter":o.get("parameter"),"app_name":uapp_name,"id":o.get("id"),"dstip":o.get("dstip"),"user_info": o.get("user_info"),"event":event,"request_body":o.get("request_body",""),"response_body":o.get("response_body",""),"res":ret_res,"action":action_name,"status_msg":status_msg}
		#printf("event_dic",event_dic)
		# 行为链条动作获取
		interface_url= "/hsdsh/es/searchForHitList"
		move_interface ={"search":"/hsdsh/es/search","YjxxList":"/hsdsh/pcip/risen/yjxx/getYjxxList"}
		#s = deepcopy(event_dic)
		event_dic["subName"] = subName
		# 根据埋点接口获取历史数据
		printf("session_id",session_id)
		event_dic,founds_url = associat_action.retrieve_forward(stream["action_dict"],event_dic,session_id,interface_url)
		# 存储行为链条数据信息
		stream["action_dict"],founds = associat_action.session_action_relation(session_id,interface_url,stream["action_dict"],event_dic,url_type,stream["url_list"],move_interface)
		printf("action_dict",stream["action_dict"])
		#printf("founds",founds)
		#对企业基本信息进行匹配
		
		qy_res,m_found = company_basic_infos(url,event_dic,stream["basic_dict"],url_type)
		
		#Delete 注释 by rzc on 2024-08-23 13:46:32
#if url == "/hsdsh/peopleEnterprise/selectListForPg" and "gj_qxb_qyjbxxb" in o.get("request_body"):

#			#printf("qy_res",qy_res)

#			printf("basic_dict",stream["basic_dict"])

#			printf("founds",founds)

#			printf("url_type",url_type)

#			printf("qy_ress",qy_res)

#			printf("dic",event_dic)

#			

#			printf("m_found",m_found)

		if qy_res and m_found:
			stream["basic_dict"] = {}
			event_dic = qy_res
			founds = True
		#printf("basic_dicts",stream["basic_dict"])
		if founds and m_found:
		#if founds:
			if "日志状态" not in label_info_dict or  ("日志状态" in label_info_dict and event):
				del event_dic["subName"]
				event_dic["res"] = ujson.dumps(event_dic["res"],ensure_ascii=False)
				event_dic["event"] = ujson.dumps(event_dic["event"],ensure_ascii=False)
				if isinstance(event_dic["request_body"],dict):
					event_dic["request_body"] = ujson.dumps(event_dic["request_body"],ensure_ascii=False)
				if isinstance(event_dic["response_body"],dict):
					event_dic["response_body"] = ujson.dumps(event_dic["response_body"],ensure_ascii=False)
				if "e_operas" not in stream:
					stream["e_operas"] =list(event_dic.keys())
				to_pool("event_model",list(event_dic.values()))
			#event_dic["time"] = timestamp
			#to_unix_udp(event_dic,"/tmp/monitor_opera")
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	
#end 

#系统定时函数，st为时间戳 
def print5(st):
	if "e_operas" in stream:
		store_ckh2(pool["event_model"],"event_monitor_oper",stream["e_operas"])
#end 

#系统定时函数，st为时间戳 
def print30(st):
	stream["con_rules"] = load_model_data("operevent")
	
	
	#with open("/data/xlink/models_paths/table_dic_bak.pkl","wb") as fp:
		#pickle.dump(stream["table_dic"],fp)
		
	# 移动到原来的文件中
	
	#os.replace("/data/xlink/models_paths/table_dic_bak.pkl","/data/xlink/models_paths/table_dic.pkl")
	
	try:
		with open("/data/xlink/models_paths/table_dic.pkl","rb")as fp:
			stream["table_dic"] = pickle.load(fp)
	except:
		time.sleep(4)
		with open("/data/xlink/models_paths/table_dic.pkl","rb")as fp:
			stream["table_dic"] = pickle.load(fp)
	
	with open("/data/xlink/models_paths/tree_dic_bak.pkl","wb")as fp:
		pickle.dump(stream["tree_dic"],fp)
	os.replace("/data/xlink/models_paths/tree_dic_bak.pkl","/data/xlink/models_paths/tree_dic.pkl")
	with open("/data/xlink/models_paths/dict_tree_bak.pkl","wb")as fp:
		pickle.dump(stream["dict_tree"],fp)
	os.replace("/data/xlink/models_paths/dict_tree_bak.pkl","/data/xlink/models_paths/dict_tree.pkl")
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def validate_interface_params(url,parameter,d_none):
	#判断 对应的接口与参数 让其值为空
	for url_p in d_none:
		d_url = url_p.get("url")
		d_par = url_p.get("parameter")
		if d_url == url and d_par == parameter:
			return True
		continue
	return False
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def data_event_oper(data_event,subName,event,ret_res,label_info_dict,status_msg,url_name):
	for http_pos,action_name_value in data_event.items():
		for action,name_value in action_name_value.items():
			for name,value in name_value.items():
				value_lst=[]
				if action == "操作":
					if name == "教育类型":
						value_res = value[0]
						if value_res in label_info_dict:
							# 获取到类型分类
							subName =label_info_dict.get(value_res,"")
					elif name == "序号":
						value_res = value[0]
						if value_res == -1:
							pass
							#del name_value["序号"]
						else:
							value_lst.append(value_res)
							event.setdefault(name,value_lst)
					else:
						# 判断值是否存在与标签之中，若存在则将值写成标签值得内容
						event,url_name=label_data(value_lst,value,label_info_dict,event,name,url_name)
				elif action == "返回结果":
					if name == "执行状态":
						# 获取到执行结果
						value_res = value[0]
						if value_res ==  "true" or value_res == "0000" or value_res == True:
							status_msg = "请求成功"
						elif value_res == "false" or value_res == False:
							
							status_msg = "请求失败"
						else:
							status_msg = value_res
					else:
						ret_res,url_name=label_data(value_lst,value,label_info_dict,ret_res,name,url_name)
	return event,ret_res,status_msg,subName,url_name
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def par_value_match(url,parameter):
	#if  "/hsdsh/pcip/risen/yjxx/getYjxxList" in url:
	if  "/pcip//risen/yjxx/getYjxxList" == url:
		list_yj = []
		par_lst = parameter.split("&")
		for par in par_lst:
			key,value = par.split("=")
			
			if key=="page":
				if len(value)>1:
					page_num =int(value[:-1])+1
					list_yj.append(f"{key}={page_num}")
				else:
					list_yj.append(par)
			elif key == "yjxxWarningType":
				value_dic = stream["gjxz"].get("预警主题类型")
				values = value_dic.get(value)
				list_yj.append(f"{key}={values}")
			elif key == "yjxxFeedbackStatus":
				value_dic = stream["gjxz"].get("反馈状态")
				values = value_dic.get(value)
				list_yj.append(f"{key}={values}")
			else:
				list_yj.append(par)
		return "&".join(list_yj)
	return parameter
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def request_value_match(url,request_body_json):
	# 获取表单数据
	if url == "/dataasset/risen/rb/data/directory/showRbDataDirectory":
		start = request_body_json.get("start","")
		if len(start)>1:
			page_num =int(start[:-1])+1
		else:
			page_num = int(start) +1
		request_body_json["start"] = page_num
		return request_body_json
	return request_body_json
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def label_data(value_lst,value,label_info_dict,event,name,url_name):
	for v in value:
		if isinstance(v,str):
			v=v.replace("<span style='color: #e79a46'>","")
			v = v.replace("</span>","")
		founds = False
		if v is True:
			v ="true"
		elif v is False:
			v="false"
		if isinstance(v,list) or isinstance(v,dict):
			value_lst.append(v)
			continue
		# 目录管理
		if name == "组织名称":
			tree_name,v = tree_path(stream["tree_dic"],v)
			value_lst.append(v)
			if tree_name:
				url_name = "数据目录-目录管理-" + tree_name # 若tree_name不为空 就将接口名等于该名字
		if name == "字典名":
			dict_name,v = tree_path(stream["dict_tree"],v)
			value_lst.append(v)
			if dict_name:
				url_name = "数据目录-字典管理-" + dict_name # 若tree_name不为空 就将接口名等于该名字
		if name == "标签名":
			dict_name,v = tree_path(stream["dict_tree"],v)
			value_lst.append(v)
			if dict_name:
				url_name = "数据开发-离线开发-" + dict_name # 若tree_name不为空 就将接口名等于该名字
		#归集表
		for id,table_value in stream["table_dic"].items():
			table_comment = table_value.get("tableComment")
			table_name = table_value.get("tableName")
			if v == table_name or (name=="表id名称" and v ==id):
				# 如果值等于表名称，就将中文名称赋值为v
				v = table_comment
				value_lst.append(v)
				founds = True
				break
		# 循环值信息，如果值 存在与标签信息中
		if v in label_info_dict and not founds:#如果值存在于字典之中，那么这个字典中的值是列表，就需要将数据取出来
			label_value = label_info_dict.get(v,"") # 获取到标签的值
			if label_value:
				value_lst.append(label_value)
		else:
				# 如果不存在的话 就存入新的值
			value_lst.append(v)
	if value_lst:
		value_lst = remove_duplicates(value_lst)
		if value_lst!=[]:
			event.setdefault(name,value_lst)
	return event,url_name
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def remove_duplicates(mixed_array):
	
	result=[]
	for item in mixed_array:
		if item not in result and item!=[]:
			result.append(item)
	return result
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def QueryApiName(url_name,label_info,parameter,parameter_json=None):
	for key in label_info:
		if "参数分类" not in key:
			continue
		par_name = label_info.get(key,"")
		keyword,cls = par_name.split(">>")
		#key_true,key_false = cls.split("/")
		target = parameter_json or {}
		#result = key_true if target and keyword in target else key_false
		if (keyword in target or keyword in target.values()) or keyword in parameter:
			url_name = cls
	
	return url_name
	
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def table_common(url,response_body,table_dic):
	if url == "/hsdsh/original/getOriginalTable":
		response_body = ujson.loads(response_body)
		data = response_body.get("data",[])
		if data:
			for item in data:
				system = item.get("system","")
				tableName = item.get("tableName","")
				tableComment = item.get("tableComment","")
				id = str(item.get("id"))
				topics =item.get("topic","")
				table_dic.setdefault(id,{}).setdefault("topic",topics)
				table_dic.setdefault(id,{}).setdefault("tableName",tableName)
				table_dic.setdefault(id,{}).setdefault("tableComment",tableComment)
				table_dic.setdefault(id,{}).setdefault("system",system)
	return table_dic
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def tree_path(tree_dic,org_uuid):
	path = []
	current_uuid = org_uuid
	url_name = tree_dic.get(org_uuid,{}).get("fullname","")
	while current_uuid:
		org_info = tree_dic.get(current_uuid)
		if not org_info:
			break
		path.append(org_info["fullname"])
		current_uuid = org_info["parentuuid"]
	return " -> ".join(reversed(path)),url_name
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def tree_common(url,response_body,tree_dic):
	if url == "/dataasset/api/dataasset/other/queryOrgTree":
		response_body = ujson.loads(response_body)
		data = response_body.get("data",[])
		if data:
			for item in data:
				crorgUuid = item.get("crorgUuid","")
				crorgFullName = item.get("crorgFullName","")
				crorgParentUuid = item.get("crorgParentUuid","")
				tree_dic.setdefault(crorgUuid,{}).setdefault("fullname",crorgFullName)
				tree_dic.setdefault(crorgUuid,{}).setdefault("parentuuid",crorgParentUuid)
	return tree_dic
				
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def dict_common(url,response_body,dict_tree):
	if url in ["/dataasset/api/dataasset/dataDictionary/listAll","/dataasset/api/dataasset/dataDictionary/likeTree"]:
		response_body = ujson.loads(response_body)
		data = response_body.get("data",[])
		if data:
			for item in data:
				crorgUuid = item.get("crdctUuid","")
				crorgFullName = item.get("crdctName","")
				crorgParentUuid = item.get("crdctParentUuid","")
				dict_tree.setdefault(crorgUuid,{}).setdefault("fullname",crorgFullName)
				dict_tree.setdefault(crorgUuid,{}).setdefault("parentuuid",crorgParentUuid)
	return dict_tree
				
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def company_basic_infos(url,event_dic,basic_dic,url_type):
	m_found= False
	parameter = event_dic.get("parameter")
	request_body = event_dic.get("request_body")
	main_url = "/hsdsh/es/searchForHitList"
	if url_type !="详情":
		return {},True
	if url == main_url:
		if main_url not in basic_dic and "企业" in parameter:
			basic_dic[main_url] = event_dic
			return {}, m_found
		else:
			return {},True
	if url == "/hsdsh/peopleEnterprise/selectListForPg":
		if main_url in basic_dic and "gj_qxb_qyjbxxb" in request_body:
			jbxx_res = event_dic.get("res")
			basic_dic[main_url]["res"] = jbxx_res
			m_found = True
			return basic_dic[main_url],m_found
	return {},True
	
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
#from model_information import *
from intell_analy_new import *
import pickle
import os
import time
import associat_action
from copy import deepcopy
#end 

#udf

#end 
