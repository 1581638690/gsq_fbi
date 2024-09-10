#xlink脚本
#file: {ID}.xlk
#name: {meta_name}
#描述： {meta_desc}
#创建时间: {create_date}

#查看流计算服务
#a = @udf FBI.x_finder3_list

#启动
#a = @udf FBI.x_finder3_start with {ID}

#停止
#a = @udf FBI.x_finder3_stop with {ID}

#查询错误日志
#a = load ssdb by ssdb0 query qrange,X_log:{ID},0,1000

#查看xlink内部信息, 每５秒更新
#在对象查看器里输入　printf::{ID}

#断点调试
#debug_on(1)


#初始化
init => {{
	stream["meta_name"] = "{meta_name}"
	stream["meta_desc"] = "{meta_desc}"
	stream["source"]= {{"unix_udp":"/tmp/test_unix","mode":"json"}}
	#stream["source"]= {{"link":"192.168.1.175:6379","topic":"csr-data","redis":"list","topics":["csr-data2"],"username":"xxxx","password":"yyyy"}}
	#stream["source"] = {{"shm_name":"httpub","count":8}}
	#stream["source"]= {{"unix_udp":"0.0.0.0","port":514,"mode":"bin"}}
	#stream["source"]= {{"link":"192.168.1.190:9092","topic":"zichan","group":"x2","start-0":True}}
	stream["es"]={{"link":"http://192.168.1.175:59200","_index":"stream","_id":""}}
	stream["kfk"]={{"link":"192.168.2.190:9092","topic":"stream","key":""}}
	#stream["stw"]["stw_flow"]={{"times":60,"fun":"flow"}}
	#stream["stw"]["stw_http"]={{"times":60,"fun":"http"}}
	#stream["st"]["st_10s"]={{"times":10,"fun":"print10"}}

	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0

	#chk的链接
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	
	#创建ckh的pool
	pools["ckh"] = []

	#从ssdb中加载配置，可以和json表单配合
	setting = load_ssdb_kv("setting")
	stream["link"] = setting["kfk"]["origin"]["link"]

	#从ssdb中加载一个hashmap的字典，用于比对去重等
	stream["url2"] = load_ssdb_hall("FF:url2")
}}


#事件处理函数
events => {{
	#时间窗口，需要一个到秒时间戳
	k = iso_to_timestamp(o["timestamp"])
	#k =  int(o["time_int"]/1000)

	#调试需要的变量
	debug={{}}

	#测试函数
	o["test"] = ss(o["event_type"],o["event_type"],o["event_type"])
	
	stream["count"] +=1
	stream["count-10"] +=1
	if o["event_type"]=="flow":
		#进入断点调试
		debug_on(1)
		e = clone_event(o)
		debug["新事件"] = e
		push_stw("stw_flow",k,e)
	if o["event_type"] =="http":
		push_stw("stw_http",k,o)
	#to_es(o)
	#to_kfk(o)
	to_table(o)
	to_pool("ckh",o)
	#push_stw("stw_10s",k,o)

	#返回调试值
	return debug
}}

#系统定时函数
print10 => {{
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
	
	#数据存储到ckh的flow表中
	store_ckh(pools["ckh"],"flow") 

	#调用FBI块语句
	push_arrays_to_df(table,"flow")
	save()
}}

#窗口函数，使用FBI的原语
flow => stw{{

	df2 = group df by dest_ip agg count
	df3 = @udf df by udf0.df_sum
	store df2 to ssdb by ssdb0 with DF:agg=>@k
    store df3 to ssdb by ssdb0 with DF:sum=>@k    
    @udf flow by CRUD.save_table with (msyql,df)
	assert df by df.index.size >0 as xlink to 调度成功[df.index.size] with 调度失败!
}}

#窗口函数，使用FBI的原语
http => stw{{
	df2 = group df by dest_ip agg count
	df3 = @udf df by udf0.df_sum
	store df2 to ssdb by ssdb0 with DF:agg=>@k
    store df3 to ssdb by ssdb0 with DF:sum=>@k
	t2 = @sdf format_timestamp with (@k,"%Y-%m-%dT%H:%M:%S")
	#调试语句
	assert True as xlink to 调度成功[$t2] with 调度失败!
}}

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用
#使用push_arrays_to_df函数生成df,在语句块中使用
#如: push_arrays_to_df(table,"flow")
save => fbi{{
	@udf flow by CRUD.save_table with (msyql,flow_info)
	drop flow
}}

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
ss => (d1,d2,d3){{
	return d1+d2+d3
}}


#克隆一个新事件,创建一个新的变量，并返回
clone_event =>(o){{
	e={{}}
	e["timestamp"]= o["timestamp"]
	e["src_ip"]= o["src_ip"]
	e["dest_ip"]= o["dest_ip"]
	e["dest_port"]= o["dest_port"]
	return e
}}

#base64字符串的解码,处理被截断的情况
base64_decode =>(x){{
	try:
		a =  base64.b64decode(x).decode("utf-8")
	except Exception as e:
		a = base64.b64decode(x)[0:e.start].decode("utf-8")
	return a
}}

#需要额外引入的包
imports =>{{
	import sys
	import gc
	import base64
}}
