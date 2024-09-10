#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 


import sys
import os
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
import socket
try:
	import _pickle as pickle
except:
	import pickle

import json
import time
from datetime import datetime
try:
	from kafka import KafkaConsumer
	from confluent_kafka import Consumer,OFFSET_BEGINNING,TopicPartition,OFFSET_STORED
	from avenger.fglobals import *
except:
	pass
from pyssdb import Client
from clickhouse_driver import Client as CKH_Client
from collections import deque
import threading
import redis
import signal
import importlib
import copy
import random
import traceback
import lz4.block as ccc

#add by gjw on 2022-0728 兼容高性能和高兼容性
try:
	import orjson
	import ujson
except:
	import json as orjson
	import json as ujson

from multiprocessing import shared_memory,resource_tracker
import logging
from logging.handlers import RotatingFileHandler

#初始化主root
root_logger = logging.getLogger('xlink')
root_logger.setLevel(logging.INFO)


#全局的初始化定义
stream={
	"name": "",
	"run": True,
	"run2": True,
	"run3": True,
	"run4": True,
	"suspend": False, #挂起状态
	"pm_ssdb_printf": False,
	"source": {"link":"127.0.0.1:9092","topic":"suricata","group": "x","start-0":False},
	"pools":{"es":deque(),"kfk":deque(),"table":[],"kv":[],"default":[]},
	"redis_pools":{},
	"redis_pubs":{},
	"redis_links":[], #同时多个分发的链接
	"redis_times": False, #redis times计数，超过10S,就会发送
	"ckh_times":{}, #ckh times计数，超过60S,就会发送
	"kfk_pools":{},
	"kfk_events":{},
	"unix_pools":{}, #unix_udp第一次发送超时的缓冲池
	"unix_udp_drops":{}, #unix_udp缓冲池满的丢失计数
	"stw":{}, #stw的配置
	"st":{}, #系统定时任务
	"scw":{}, #计数窗口
	"pools2":{}, #stw的数据
	"printf":{}, #自己想要输出的信息
	"last_failed_reason":"",
	"total":{ #内部监控信息 
	        "msgs":0, #消息总数
			"errors":0, #接收出错信息
			"empty":0, #空闲时间或次数
			"sleep":0, #内存挂起休息时间或次数
			"sleep1":0, #外部挂起休息时间或次数,redis
			"json_errors":0, #json处理错误数
			"events":0, #正确事件数
			"events_errs":0, #错误事件数		
			"events_drop":0, #丢弃次数统计
			"startup":"", #启动时间
			"lasterror":"", #最后错误信息
			},
	"ssdb":"127.0.0.1:8888",
	"debug": False, #调试模式
	"break": False, #出错中断
	"redis_pub_depth": 500,#一个队列最多保留500条压缩分块消息
	"redis_pub_batch": 500, # 发布的批次200
	"redis_list_depth": 15000, # 单个队列最多保留1万
    "redis_max_mem": 8, # 10G内存
	"ckh_batch": 30000, #ckh的一个批次提交的数量
	"pre_totals": 0, #上一次处理间隔的消息数
	"pre_events": 0, #上一次处理间隔的事件数
	"last_err_info":"",
	"json_files":{}, #jsonfile的信息，文件名:{文件句柄，消息个数}	
	"client_udp": socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
	"perf_funs":[] #监控的内部函数
}


#add by gjw on 20240104
#内部使用的变量，unix模式使用
in_pools={}
#内部使用的变量，pubshm模式使用
in_shm_pools={}

#pubshm的配置
pubshm_cfg={}

#add by gjw on 2021-0914  增加对两个池的处理
lockP= threading.Lock() #对pool池的锁
table= stream["pools"]["table"]

pool = stream["pools"] #将要废弃
pools = stream["pools"]



#初始化日志
def init_log():
	# 创建一个handler，用于写入日志文件
	#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大10M
	fh =  RotatingFileHandler(f'logs/{stream["name"]}.log', maxBytes=100*1024,backupCount=1)

	# 定义handler的输出格式
	formatter = logging.Formatter('%(message)s')
	fh.setFormatter(formatter)
	# 给logger添加handler
	root_logger.addHandler(fh)

def init():	
	#默认最大使用内存,G
	if "max_mem" not in stream:
		if "max_xlink" in stream:
			stream["max_mem"] = 2
		else:
			stream["max_mem"] = 4
		
	#共享内存发布的模式
	if "pubshm" in stream:
		if stream["task_id"] ==-1:
			shm = create_pubshm(stream["pubshm"]["shm_name"],stream["pubshm"]["size"])
		else:
			shm = create_pubshm(f'{stream["pubshm"]["shm_name"]}_{stream["task_id"]}',stream["pubshm"]["size"])
		pubshm_cfg[stream["pubshm"]["shm_name"]] ={"shm":shm,"size":stream["pubshm"]["size"],"seek":0}
		#初始化缓冲池
		in_shm_pools[stream["pubshm"]["shm_name"]]=[]
	
	#多个不同的共享文件，最多10个，pubshm_{i}
	for i in range(1,10):
		pubshm = f"pubshm_{i}"
		if pubshm in stream:
			if stream["task_id"] ==-1:
				shm = create_pubshm(stream[pubshm]["shm_name"],stream[pubshm]["size"])
			else:
				shm = create_pubshm(f'{stream[pubshm]["shm_name"]}_{stream["task_id"]}',stream[pubshm]["size"])
			pubshm_cfg[stream[pubshm]["shm_name"]]={"shm":shm,"size":stream[pubshm]["size"],"seek":0}
			#初始化缓冲池
			in_shm_pools[stream[pubshm]["shm_name"]]=[]
	
#end def

def create_pubshm(name,size):
	shm_file = f'xlink_shm_{name}.pub'
	shm_path = "/dev/shm/"+shm_file
	if os.path.exists(shm_path):
		#os.remove(shm_path)
		shm = shared_memory.SharedMemory(name=shm_file) #使用原有定义好的
	else:
		shm = shared_memory.SharedMemory(name=shm_file,create=True, size=size) #建立
	resource_tracker.unregister(shm._name, 'shared_memory')
	return shm
	

#发布消息，128条后真正写入
def pub_shm(o,shm_name=""):
	if len(in_shm_pools[shm_name]) <128:
		in_shm_pools[shm_name].append(o)
	else:
		in_shm_pools[shm_name].append(o)
		shm = pubshm_cfg[shm_name]["shm"]
		i = pubshm_cfg[shm_name]["seek"]
		buf = pickle.dumps(in_shm_pools[shm_name])
		length = len(buf)
		# 16=2+8+4+(length)+2(留给结束标记)
		if i+length+16 >pubshm_cfg[shm_name]["size"]:
			shm.buf[i:i+2] = b'\xab\xce' #代表结束，重头开始
			i=0
		#写入内存		
		shm.buf[i+2:i+10] = time.time_ns().to_bytes(8)
		shm.buf[i+10:i+14] = length.to_bytes(4)		
		shm.buf[i+14:i+14+length] = buf
		#所有数据写完后,再写这个完整的标记,防止订阅着过早的读
		shm.buf[i:i+2] = b'\xab\xcd'
		i += 14+length
		#记录状态
		pubshm_cfg[shm_name]["seek"] = i
		in_shm_pools[shm_name]=[]
#end fun

#发布单条，实时写入
def pub_shm_one(o,shm_name=""):
	shm = pubshm_cfg[shm_name]["shm"]
	i = pubshm_cfg[shm_name]["seek"]
	buf = pickle.dumps([o])
	length = len(buf)
	# 16=2+8+4+(length)+2(留给结束标记)
	if i+length+16 >pubshm_cfg[shm_name]["size"]:
		shm.buf[i:i+2] = b'\xab\xce' #代表结束，重头开始
		i=0
	#写入内存		
	shm.buf[i+2:i+10] = time.time_ns().to_bytes(8)
	shm.buf[i+10:i+14] = length.to_bytes(4)		
	shm.buf[i+14:i+14+length] = buf
	#所有数据写完后,再写这个完整的标记,防止订阅着过早的读
	shm.buf[i:i+2] = b'\xab\xcd'
	i += 14+length
	#记录状态
	pubshm_cfg[shm_name]["seek"] = i
#end fun


#放入池
pool_size = 50000
def to_es(o):
	stream["pools"]["es"].append(o)
	
def to_kfk(o={}):
	stream["pools"]["kfk"].append(o)	

def to_kfk2(topic,o):
	stream["kfk_pools"][topic].append(o)	

def to_kfk_with_topic(topic,o={}):
	stream["kfk_pools"][topic].append(o)

def to_table(o={}):	
	if len(stream["pools"]["table"]) > pool_size:
		time.sleep(0.01)
	stream["pools"]["table"].append(o)	
	

def to_kv(k="",o={}):
	c.set(k,ujson.dumps(o))

def to_pool(k="default",o={}):
	if len(stream["pools"][k]) > pool_size:
		time.sleep(0.01)
	stream["pools"][k].append(o)



#add by gjw on 2024-0411

xlink_data_path="/data/xlink"

def load_pkl(file_path):
	try:
		with open(f"{xlink_data_path}/{file_path}","rb") as f:
			return pickle.load(f)
	except:
		return {}


def store_pkl(o,file_path):
	o2 = o.copy()
	with open(f"{xlink_data_path}/{file_path}","wb+") as f:
		pickle.dump(o2,f)
	


#unix_udp的操作

#根据socket_file获取client
def gen_client_by_file(socket_file):
	client_file = f"client_{socket_file}"
	try:
		client_unix = stream[client_file]
	except:
		client_unix = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
		client_unix.setblocking(0)
		stream[client_file] = client_unix
	return client_unix

#放置数据到unix缓冲池中
def put_unix_pool(socket_file,data):
	try:
		pool = stream["unix_pools"][socket_file]
	except:
		stream["unix_pools"][socket_file]=[]
		pool = stream["unix_pools"][socket_file]
	
	if len(pool) >1000:
		try:
			stream["unix_udp_drops"][socket_file] +=1
		except:
			stream["unix_udp_drops"][socket_file]=0
		stream["total"]["events_drop"] +=1
	else:
		pool.append(data)

#发送缓冲池里所有数据
def send_all_unix_pool():
	for socket_file,pool in stream["unix_pools"].items():
		client_unix = gen_client_by_file(socket_file)
		err_count=0
		while len(pool) >0:
			data = pool.pop()
			try:
				client_unix.sendto(data,socket_file)
				err_count=0
			except BlockingIOError:
				time.sleep(0.00001)
				try:
					client_unix.sendto(data,socket_file)
					err_count=0
				except:
					try:
						stream["unix_udp_drops"][socket_file] +=1
					except:
						stream["unix_udp_drops"][socket_file]=0
					stream["total"]["events_drop"] +=1
					if err_count >10: #连续10个失败，就停止发送
						break
			except Exception as e:
				stream["total"]["events_errs"] +=1
				add_error_to_log("发送缓冲池消息失败","Unix_udp {}".format(socket_file),e.__str__())
	#end for
	#add by gjw on 2024-0419 发送未发送的数据
	for socket_file,pool in in_pools.items():
		data = pickle.dumps(pool)
		if len(data) < 1048000:
			send_unix_udp(data,socket_file)
		else:
			for o in pool:
				data = pickle.dumps(o)
				send_unix_udp(data,socket_file)
		in_pools[socket_file]=[]
	#end for
#end send_all_unix_pool()


#发送缓冲池里所有数据,不管是否发送成功，紧急发送
def send_all_unix_pool2():
	for socket_file,pool in stream["unix_pools"].items():
		client_unix = gen_client_by_file(socket_file)
		while len(pool) >0:
			data = pool.pop()
			try:
				client_unix.sendto(data,socket_file)
			except BlockingIOError:
				try:
					client_unix.sendto(data,socket_file)
				except:
					try:
						stream["unix_udp_drops"][socket_file] +=1
					except:
						stream["unix_udp_drops"][socket_file]=0
					stream["total"]["events_drop"] +=1
			except Exception as e:
				stream["total"]["events_errs"] +=1
				add_error_to_log("紧急发送缓冲池消息失败","Unix_udp {}".format(socket_file),e.__str__())
	#end for
#end send_all_unix_pool()
			

#一个队列
def to_unix_udp(o,socket_file=""):
	try:
		in_pools[socket_file].append(o)
	except:
		in_pools[socket_file] = [o]
		
	def send_one_by_one(a):
		for o in a:
			data = pickle.dumps(o)
			send_unix_udp(data,socket_file)
	
	if len(in_pools[socket_file]) >=32:
		data = pickle.dumps(in_pools[socket_file])
		send_unix_udp(data,socket_file)
		"""
		if len(data) < 1048000:
			send_unix_udp(data,socket_file)
		elif len(data) < 2048000: #二分法再发送一次
			size = 16
			for i in range(2):
				data1 = pickle.dumps(in_pools[socket_file][0*size:size*(i+1)])
				if len(data1) <1048000:
					send_unix_udp(data1,socket_file)
				else:
					send_one_by_one(in_pools[socket_file][0*size:size*(i+1)])
		else:
			send_one_by_one(in_pools[socket_file])
		"""
		in_pools[socket_file]=[]
#end fun

#立即发送，发送失败则缓存，原样发送，一般不对外
def send_unix_udp(data,socket_file=""):
	client_unix = gen_client_by_file(socket_file)
	try:		
		client_unix.sendto(data,socket_file)
	except BlockingIOError:
		put_unix_pool(socket_file,data)
	except Exception as e:
		stream["total"]["events_errs"] +=1
		add_error_to_log("发送消息失败","Unix_udp {}".format(socket_file),e.__str__())
#end

#和任务bind的队列
def to_unix_udp_task(o,socket_file=""):	
	if stream["task_id"] !=-1:
		socket_file="{}.{}".format(socket_file,stream["task_id"]+2)
	else:
		socket_file="{}.{}".format(socket_file,1)
	to_unix_udp(o,socket_file)
#end

#发布多个队列
def pub_unix_udp(o,socket_files=[]):
	pub_socket_file=f"pub_{socket_files[0]}_len_{len(socket_files)}"
	if pub_socket_file not in in_pools:
		in_pools[pub_socket_file] = [o]
	else:
		in_pools[pub_socket_file].append(o)
	
	if len(in_pools[pub_socket_file]) >=32:
		data = pickle.dumps(in_pools[pub_socket_file])
		if len(data) < 600000:
			for socket_file in socket_files:
				client_unix = gen_client_by_file(socket_file)
				try:		
					client_unix.sendto(data,socket_file)
				except:
					pass
		else:
			for o in in_pools[pub_socket_file]:
				data = pickle.dumps(o)
				for socket_file in socket_files:
					client_unix = gen_client_by_file(socket_file)
					try:		
						client_unix.sendto(data,socket_file)
					except:
						pass
		
		in_pools[pub_socket_file]=[]
	#end if
#end

#并行队列
def to_unix_udp_n(o,socket_file="",n=1,hash_route=False):
	if hash_route==False:
		#默认，根据事件数量随机分配
		random_num = stream["total"]["events"] % (n+1)
	else:
		#根据传进来的值的hash做分配
		random_num = hash_route.__hash__() % (n+1)
	
	socket_file="{}.{}".format(socket_file,random_num+1)
	
	to_unix_udp(o,socket_file)
#end 


# udp　sokcet操作
#一个队列
def to_udp_json(o,addr=('127.0.0.1',10000)):	
	client_udp = stream["client_udp"]
	try:
		data = orjson.dumps(o)
		client_udp.sendto(data,addr)
	except BlockingIOError as e:
		stream["total"]["events_drop"] +=1
#end

def to_udp_utf8(o,addr=('127.0.0.1',10000)):
	client_udp = stream["client_udp"]
	try:
		client_udp.sendto(o.encode("utf8"),addr)
	except BlockingIOError as e:
		stream["total"]["events_drop"] +=1
#end


#file 的写入操作

#add by gjw on 2023-0710, 写入json文件
def to_json_file(fp="",o={}):
	if fp not in stream["json_files"]:
		if "task_file_id"  in stream:
			filename = "{}_{}.{}".format(fp,datetime.now().isoformat(),stream["task_file_id"])
		else:
			filename = "{}_{}".format(fp,datetime.now().isoformat())
		f = open(filename,"a+")
		stream["json_files"][fp] = {"f":f,"count":0}
	
	stream["json_files"][fp]["f"].write(ujson.dumps(o,ensure_ascii=False))
	stream["json_files"][fp]["f"].write("\r\n")
	stream["json_files"][fp]["f"].flush()
	stream["json_files"][fp]["count"] +=1

	if stream["json_files"][fp]["count"] >=1000:
		stream["json_files"][fp]["f"].close()
		if "task_file_id"  in stream:
			filename = "{}_{}.{}".format(fp,datetime.now().isoformat(),stream["task_file_id"])
		else:
			filename = "{}_{}".format(fp,datetime.now().isoformat())
		f = open(filename,"a+")
		stream["json_files"][fp] = {"f":f,"count":0}
#end

#redis 的入库操作
import redis

def get_redis_client(link="redis"):
	try:
		if "redis_client" in stream and "link" in stream["redis_client"]:
			stream["redis_client"][link].close()
		else:
			stream["redis_client"]={link:None}
	except Exception as e:
		raise Exception("Redis关闭链接失败:{}".format(e))
	try:
		password = '4d7d4f6ef5d627f43a65d9b4b2ccc875'
		username = None
		if "password" in stream[link]:
			password = stream[link]["password"]
		if "username" in stream[link]:
			username = stream[link]["username"]
		client = redis.Redis(host=stream[link]["host"], port=stream[link]["port"], decode_responses=True,username=username,password=password)
	except Exception as e:
		add_error_to_log("Redis建立链接",f'Redis[{stream[link]["host"]}-{stream[link]["port"]}]',e.__str__())
		client = None
	stream["redis_client"][link] = client
	return client

def redis_client(link="redis"):
	if link in stream["redis_client"]:
		return stream["redis_client"][link]
	else:
		return get_redis_client(link)


#modify by gjw on 2022-1209 发送单个队列
def to_redis(k="default",o={},link="redis"):
	if link not in stream["redis_pools"]:
		stream["redis_pools"][link] = {}
	if k not in stream["redis_pools"][link]:
		stream["redis_pools"][link][k] = []

	stream["redis_pools"][link][k].append(o)
	
	if len(stream["redis_pools"][link][k]) >=stream["redis_batch"]:
		try:
			msg = pickle.dumps(stream["redis_pools"][link][k])
			msg = ccc.compress(msg)
			redis_client(link).rpush(k,msg)	
		except Exception as e:
			add_error_to_log("发送消息","Redis[{}-{}][{}][{}]".format(stream[link]["host"],stream[link]["port"],k,len(stream["redis_pools"][link][k])),e.__str__())
			get_redis_client(link)
		finally:
			stream["redis_pools"][link][k].clear()	
#end 


#modify by gjw on 2024-0229 发送单个队列,使用json方式，直接发送
def to_redis_json(k="default",o={},link="redis"):
	try:
		redis_client(link).rpush(k,orjson.dumps(o))	
	except Exception as e:
		add_error_to_log("发送消息","Redis[{}-{}][{}]".format(stream[link]["host"],stream[link]["port"],k),e.__str__())
		get_redis_client(link)
#end 

#到点集中发
def to_redis_only_all():
	#到点集中发
	if stream["redis_times"]:
		#redis list 
		for link in stream["redis_pools"].keys():
			for k in stream["redis_pools"][link].keys():
				if len(stream["redis_pools"][link][k]) >0:
					try:
						#add by gjw on 20231012 对redis内存的保护,清空所有数据
						if redis_memory(redis_client(link)) > stream["redis_max_mem"]+1:
							redis_client(link).flushdb()
							add_error_to_log("Redis数据库","Redis[{}-{}]".format(stream[link]["host"],stream[link]["port"]),"内存超过{}G,数据清空".format(stream["redis_max_mem"]))
						
						msg = pickle.dumps(stream["redis_pools"][link][k])	
						msg = ccc.compress(msg)
						#群发，数据默认存在第一个链接下
						if len(stream["redis_links"]) >0 and link==stream["redis_links"][0]:
							for link0 in stream["redis_links"]:
								redis_client(link0).rpush(k,msg)
						else:
							link0 = link
							redis_client(link0).rpush(k,msg)
					except Exception as e:
						add_error_to_log("发送消息","Redis[{}-{}][{}]".format(stream[link]["host"],stream[link]["port"],k),e.__str__())
						get_redis_client(link)
					finally:
						stream["redis_pools"][link][k].clear()
		#redis pubsub
		for link in stream["redis_pubs"].keys():
			for k in stream["redis_pubs"][link].keys():
				if len(stream["redis_pubs"][link][k]):
					write_pubmsg_to_redis(k,link)
		stream["redis_times"]=False
	#enf if 

#modify by gjw on 2022-1209 集中计时规则
def to_redis_n(k="default",o={},n=1,link="redis"):
	#add by gjw on 2023-0906 支持多个链接
	if isinstance(link,str):
		links=[link]
	else:
		links=link
		link = links[0]
	
	if link not in stream["redis_pools"]:
		stream["redis_pools"][link] = {}
	if k not in stream["redis_pools"][link]:
		stream["redis_pools"][link][k] = []
	
	stream["redis_pools"][link][k].append(o)
	if len(stream["redis_pools"][link][k]) >stream["redis_batch"]:
		try:
			if n==1:				
				msg = pickle.dumps(stream["redis_pools"][link][k])
				msg = ccc.compress(msg)
				for link0 in links:
					redis_client(link0).rpush(k,msg)		
			else:
				n = n+1
				size = int(len(stream["redis_pools"][link][k])/n)+1 #批次
				for i in range(0,n):
					tmp_array=stream["redis_pools"][link][k][i*size:i*size+size]
					msg = pickle.dumps(tmp_array)
					msg = ccc.compress(msg)
					if i == n-1: #最后一个分片						
						for link0 in links:				
							redis_client(link0).rpush("{}".format(k),msg)
					else:						
						for link0 in links:
							redis_client(link0).rpush("{}-{}".format(k,i),msg)
				#end for			
		except Exception as e:
			add_error_to_log("发送消息","Redis[{}-{}][{}]".format(stream[link0]["host"],stream[link0]["port"],k),e.__str__())
			get_redis_client(link0)
		finally:
			stream["redis_pools"][link][k].clear()
#end 



#redis的内存，G为单位
def redis_memory(client):
	info = client.info()
	return info["used_memory_rss"]/1024/1024/1024


#add by gjw on 20230403 增加pub模式 ，支持多个pub乱序操作
def pub_redis(k="default",o={},link="redis"):
	if link not in stream["redis_pubs"]:
		stream["redis_pubs"][link] = {}
	if k not in stream["redis_pubs"][link]:
		stream["redis_pubs"][link][k] = []
	stream["redis_pubs"][link][k].append(o)

	if len(stream["redis_pubs"][link][k]) > stream["redis_pub_batch"]:
		write_pubmsg_to_redis(k,link)
	#end if 

#写入数据到redis中,使用自己定义的pubsub模式
def write_pubmsg_to_redis(k,link):
	try:
		#获取当前索引
		cur_index = redis_client(link).get("{}_index".format(k))			
		if cur_index==None: #第一次
			cur_index = 0
			redis_client(link).set("{}_index".format(k),0)
		cur_index = int(cur_index)

		batch=100
		length = int(len(stream["redis_pubs"][link][k])/batch)+1

		for i in range(length):
			#分块压缩消息
			msg = pickle.dumps(stream["redis_pubs"][link][k][i*batch:i*batch+batch])
			msg = ccc.compress(msg)
			#发布消息
			redis_client(link).rpush("{}_{}".format(k,cur_index),msg)

		#判断队列长度llen
		llen =  redis_client(link).llen("{}_{}".format(k,cur_index))
		if int(llen) > stream["redis_pub_depth"]:
			#获取一下最新index, 只有一个切换者
			new_index = redis_client(link).get("{}_index".format(k))
			if int(new_index) == cur_index:
				#切换新队列
				redis_client(link).set("{}_index".format(k),cur_index+1)

				#要删除的队列
				last_index = redis_client(link).get("{}_last_index".format(k))			
				if last_index==None: #第一次
					last_index = 0
				last_index = int(last_index)
				#判断内存大小
				while  redis_memory(redis_client(link)) >= stream["redis_max_mem"]:				
					ret = redis_client(link).delete("{}_{}".format(k,last_index))
					last_index +=1
					if ret==1 or ret=="1" or int(ret)==1: #如果为空则继续										
						redis_client(link).set("{}_last_index".format(k),last_index)
						#redis的内存反馈有延迟，避免删除太猛
						time.sleep(0.05)
				#内存清理结束
		
	except Exception as e:
		add_error_to_log("pub消息","Redis[{}-{}][{}]".format(stream[link]["host"],stream[link]["port"],k),e.__str__())
		get_redis_client(link)
	finally:
		stream["redis_pubs"][link][k].clear()
#end

#得到处理池中的所有数据请清空，add by gjw on 20220920
def get_pool(k="default"):
	lockP.acquire()
	result = copy.deepcopy(stream["pools"][k])
	stream["pools"][k].clear()
	lockP.release()
	return result

#add by gjw on 20200612 
def store_ckh(array,table=""):	
	#add by gjw on 2022-12-07 增加计时
	if table not in stream["ckh_times"]:
		stream["ckh_times"][table] = time.time()

	now = time.time()
	times = now-stream["ckh_times"][table]
	length = len(array)
	if length>stream["ckh_batch"] or (length >0 and times >=10):#10秒钟
		stream["ckh_times"][table] = now
		m = int(length /stream["ckh_batch"])
		if m==0:
			m=1
		#add by gjw on 2022-12-05 加速释放锁
		b = array[0:m*stream["ckh_batch"]]
		size = len(b)
		del array[0:size]
		i=0
		#lockP.acquire()
		#add by gjw on stream["ckh_batch"]022-12-05 优化入库函数		
		while i < size:
			try:
				c = b[i:i+stream["ckh_batch"]]
				records=list(map(transate_ckh,c))
				stream["CKH"].execute('INSERT INTO %s (%s) VALUES'%(table,",".join(b[0].keys())),records)
				i +=stream["ckh_batch"]
			except Exception as e:
				raise Exception("store_ckh: 总条数:%s 本次条数:%s  错误: %s, 数据样例: %s..."%(size,len(records),e,records[0]))
		# finally:
		# 	lockP.release()
	#end if
			

#转换ckh的类型
def transate_ckh(record):
	new_r=[]
	for k,v in record.items():
		if type(v) in [int,float,str,datetime]:
			new_r.append(v)
		else:
			#new_r.append(ujson.dumps(v,ensure_ascii=False))
			new_r.append(str(v))
	return new_r


#add by gjw  keys中是字段名，处理性能好
def store_ckh2(array,table="",keys=[]):	
	#add by gjw on 2022-12-07 增加计时
	if table not in stream["ckh_times"]:
		stream["ckh_times"][table] = time.time()

	now = time.time()
	times = now-stream["ckh_times"][table]
	length = len(array)
	if length >=stream["ckh_batch"]: #整批处理
		stream["ckh_times"][table] = now
		m = int(length /stream["ckh_batch"])
		size = m*stream["ckh_batch"]
		b = array[0:size]
		del array[0:size] #删除相关数据
		for i in range(m):
			try:
				c = b[i:i*stream["ckh_batch"]+stream["ckh_batch"]]				
				stream["CKH"].execute('INSERT INTO %s (%s) VALUES'%(table,",".join(keys)),c)
			except Exception as e:
				raise Exception("store_ckh: 总条数:%s 本次条数:%s  错误: %s, 数据样例: %s..."%(size,len(c),e,c[0]))
	elif times >=10 and length >0: #10秒，到点处理
		stream["ckh_times"][table] = now
		size = len(array) #再次判断
		try:
			b = array[0:size]
			del array[0:size] #删除相关数据
			stream["CKH"].execute('INSERT INTO %s (%s) VALUES'%(table,",".join(keys)),b)
		except Exception as e:
			raise Exception("store_ckh: 总条数:%s 本次条数:%s  错误: %s, 数据样例: %s..."%(size,len(b),e,b[0]))
	else:
		pass
	#end if


def find_max_columns(array):
	max = 0
	result = {}
	for a in array:
		if len(a) >max:
			max = len(a)
			result = a.copy()
	return result

#add by gjw on 20220919
def create_table_ckh(record,table=""):
	if len(record)==0: return 0
	fields=[]
	i = 0 
	order_key = ""
	for k,v in record.items():
		if isinstance(v,int):
			field = "{} Int64 NULL".format(k)
		elif isinstance(v,float):
			field = "{} Float64 NULL".format(k)
		elif isinstance(v,str):
			field = "{} String NULL".format(k)
		elif isinstance(v,datetime):
			field = "{} DateTime64(6) NULL".format(k)
		else:
			field = "{} String NULL".format(k)
		#第一个字段用来排序，不能为空
		if i==0:
			order_key = k
			field = field[:-4] #去掉NULL
			i = 1
		fields.append(field)

	drop_sql = "DROP table IF EXISTS {}".format(table)
	create_sql = "CREATE Table {} ({}) ENGINE =MergeTree() order by {}".format(table,", ".join(fields),order_key)
	try:
		stream["CKH"].execute(drop_sql)
		stream["CKH"].execute(create_sql)
	except Exception as e:
		raise Exception("create_table_ckh: %s %s",create_sql,e)

#临时存储，出错会自动建表
def store_ckh_auto(array,table=""):
	try:
		store_ckh(array,table)
	except:
		create_table_ckh(find_max_columns(array),table)
		store_ckh(array,table)
		
#FBI语句块设置参数,add by gjw on 20221029
def set_param(name,value):
	if name[0]=="@":
		fbi_global.runtime.ps[name] = value
	else:
		fbi_global.runtime.ps["@"+name] = value
	fbi_global.runtime.keys = list(fbi_global.runtime.ps)
	fbi_global.runtime.keys.sort(key=len,reverse = True)

#end set_param


#想要监控的输出的内容
def printf(k,o):
	stream["printf"][k]=[k,str(o)]

#显示处理函数线程处理函数
def ssdb_printf():
	if stream["suspend"]:
		printf("当前时间","<font color='red'>{}</font> 挂起(自身内存超过{}G)".format(datetime.now().isoformat()[0:19],stream["max_mem"]))
	else:
		printf("当前时间","<font color='green'>{}</font>".format(datetime.now().isoformat()[0:19]))

	printf("启动时间",stream["total"]["startup"][0:19])
	printf("数据源",stream["source_meta"])
	
	if "startup_timestamp" in stream:
		run_times= time.time() - stream["startup_timestamp"]
	else:
		run_times=1 # 不要等于0, 除数不能为0
	
	if "PreEvent" in stream:#并行前置执行
		printf("事件并行","<font color='green'>事件前置并行处理: {}</font>".format(stream["PreEvent"]))
	if "PreEvent_Error" in stream:
		printf("前置事件出错","<font color='red'>{}</font>".format(stream["PreEvent_Error"]))
	else:# 串行才有
		if stream["debug"]:
			printf("调试模式","<font color='red'>事件调试模式,不影响运行</font>")
		else:
			if "调试模式" in stream["printf"]:
				del stream["printf"]["调试模式"]

		if stream["break"]:
			printf("出错中断","<font color='orange'>事件处理函数出错即中断运行</font>")
		else:
			if "出错中断" in stream["printf"]:
				del stream["printf"]["出错中断"]
	
	#计算EPS和unix_udp_drops
	eps={}
	eps["msg_avg_eps"] = int(stream["total"]["msgs"]/run_times)
	eps["ev_avg_eps"] =	int(stream["total"]["events"]/run_times)
	eps["msg_real_eps"]	= 	int((stream["total"]["msgs"]-stream["pre_totals"])/3)
	eps["ev_real_eps"] = 	int((stream["total"]["events"]-stream["pre_events"])/3)
	eps["total_events"] = stream["total"]["events"]
	eps["total_errors"] = stream["total"]["events_errs"]
	eps["total_drops"] = stream["total"]["events_drop"]
	eps["unix_udp_drops"] =  stream["unix_udp_drops"]
	stream["pre_totals"] = stream["total"]["msgs"]
	stream["pre_events"] = stream["total"]["events"]

	#并行计算
	if "max_xlink" in stream:
		if stream["name"][-5:].find("__")==-1: #(主任务)
			eps2 = copy.deepcopy(eps) #必须深拷贝，因为unix_udp_drops是个对象
			for i in range(stream["max_xlink"]):
				try:
					with open("/dev/shm/xlink_{}__{}:eps".format(stream["name"],i),"r") as f:
						a = f.read()
						sub_eps = ujson.loads(a)
				except:
					sub_eps = {"msg_avg_eps":0,"ev_avg_eps":0,"msg_real_eps":0,"ev_real_eps":0,"total_events":0,"total_errors":0,"total_drops":0,"unix_udp_drops":{}}
				eps2["msg_avg_eps"] += sub_eps["msg_avg_eps"]
				eps2["ev_avg_eps"] += sub_eps["ev_avg_eps"]
				eps2["msg_real_eps"] += sub_eps["msg_real_eps"]
				eps2["ev_real_eps"] += sub_eps["ev_real_eps"]
				#事件总数
				eps2["total_events"] += sub_eps["total_events"]
				eps2["total_errors"] += sub_eps["total_errors"]
				eps2["total_drops"] += sub_eps["total_drops"]
				
				#add by gjw on 20240103 unix_udp_drops合计技术
				for k,v in sub_eps["unix_udp_drops"].items():
					if k in eps2["unix_udp_drops"]:
						eps2["unix_udp_drops"][k] +=v
					else:
						eps2["unix_udp_drops"][k] = v
				#end for
			
			printf("事件信息[合计]","正确总数: {} ,错误总数: {}, 丢弃总数: {}".format(eps2["total_events"],eps2["total_errors"],eps2["total_drops"]))

			printf("EPS信息[合计]","消息平均EPS: {},  消息EPS: {}, 事件平均EPS: {}, 事件EPS: {}".format(
				eps2["msg_avg_eps"],eps2["msg_real_eps"],
				eps2["ev_avg_eps"],eps2["ev_real_eps"]
			))
			s=""			
			for k,v in eps2["unix_udp_drops"].items():
				s += f"{k}=>{v}, "
			if s!="":
				printf(f"发送超时[合计]",s)

		else:#(子任务)
			save_eps(stream["name"],eps)
	#end 
	
	#消息总数
	if "sum" in stream["total"]:
		printf("消息总数","总数:{}, json错误{}, 错误:{}, 空闲:{}, 剩余: {}, 内挂:{},外挂:{}".format(stream["total"]["msgs"],
			stream["total"]["json_errors"],stream["total"]["errors"],stream["total"]["empty"],stream["total"]["sum"],
			stream["total"]["sleep"],stream["total"]["sleep1"]))
	else:
		printf("消息总数","总数:{}, json错误{}, 错误:{}, 空闲:{}, 内挂:{},外挂:{}".format(stream["total"]["msgs"],
			stream["total"]["json_errors"],stream["total"]["errors"],stream["total"]["empty"],stream["total"]["sleep"],stream["total"]["sleep1"]))
	
	printf("事件总数","正确:{}, 错误:{}, 丢弃:{} ".format(stream["total"]["events"],stream["total"]["events_errs"], stream["total"]["events_drop"]))	
	printf("EPS信息","消息平均EPS: {}, 消息EPS:{},事件平均EPS: {} ,事件EPS:{} ".format(
				eps["msg_avg_eps"],	eps["msg_real_eps"],
				eps["ev_avg_eps"], eps["ev_real_eps"]
		))	
	
	#时间窗口
	for name,window in stream["pools2"].items():
		if stream["stw"][name]["MIN"] >0:
			deal_event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(stream["stw"][name]["MIN"]))
		else:
			deal_event_time = "--"
		printf("数窗[%s]"%(stream["stw"][name]["fun"]),"周期:{},SIZE:{},调次: {:.1f},出错:{},数量:{},耗时:{:.2f}s,  时间:{}".format(stream["stw"][name]["times"],
			len(window),stream["stw"][name]["count"],stream["stw"][name]["error"],
			stream["stw"][name]["length"],stream["stw"][name]["cost"],deal_event_time))

		if "times2" in stream["stw"][name]:
			printf("数窗2[%s]"%(stream["stw"][name]["fun2"]),"周期:{},调次:{},出错:{},耗时:{:.2f}s".format(stream["stw"][name]["times2"],
			stream["stw"][name]["count2"],stream["stw"][name]["error2"],
			stream["stw"][name]["cost2"]))
	#定时函数
	for name,cfg in stream["st"].items():
		printf("定函[%s]"%(cfg["fun"]),
			"周期:{},调次: {},出错: {},运行: {},返回: {},耗时: {:.2f}s".format(cfg["times"],cfg["count"],
				cfg["errors"],cfg["run"],
				cfg["return"],cfg["cost"]))
	
	#计数窗口
	for name,cfg in stream["scw"].items():
		timestamp=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(stream["scw"][name]["last_time"]))
		printf("计窗[%s]"%(cfg["fun"]),"基准:{}, 计数:{}, 调用时间:{}, 耗时:{:.2f}s".format(stream["scw"][name]["count"], len(stream["pools"][name]),timestamp,stream["scw"][name]["cost"]))
		
	printf("ES池事件数",len(stream["pools"]["es"]))
	printf("Table池事件数",len(stream["pools"]["table"]))

	if "kfk" in stream:
		#kafka的事件总量
		s = "{0}:{1}".format(stream["kfk"]["topic"],len(stream["pools"]["kfk"]))
		if "topics" in stream["kfk"]:
			for topic in stream["kfk"]["topics"]:
				s += ",{0}:{1}".format(topic,len(stream["kfk_pools"][topic]))
		printf("KFK池事件数",s)
		#处理完的事件数
		s2=""
		for topic,count in stream["kfk_events"].items():
			s2 += "{0}:{1},".format(topic,count)
		printf("KFK处理总数",s2)
	
	s3=""
	for k,pool in stream["pools"].items():
		if k not in ["es","table","kfk","kv"]:
			s3 +="{}:{} ".format(k,len(pool))
	
	printf("其它池事件数",s3)		
	printf("最后信息(错误)",load_last_error_or_info(stream["name"]))
	df = {"columns":["nane","msg"],"data":list(stream["printf"].values()),"index":list(range(0,len(stream["printf"])))}
	
	with open(f"/dev/shm/printf::{stream['name']}", "w+")  as f:
		f.write(ujson.dumps(df))

	#c.set("printf::%s"%(stream["name"]),ujson.dumps(df))
	
#end ssdb_printf


"""
ssdb的内置操作函数：

"""

#存储一个对象到hashmap中
def to_ssdb_h(name,key,o={}):
	if len(key) >200:
		key = key[0:200]
	c.hset(name,key,ujson.dumps(o))


#存储整个kv字典结构中的信息
def to_ssdb_hall(name,kv):
	kv2 = kv.copy()
	c2 = Client("127.0.0.1",8888)
	for key,o in kv2.items():
		if len(key) >200:
			key = key[0:200]
		try:
			c2.hset(name,key,ujson.dumps(o))
		except:
			pass
	c2.close()

#扫描hashmap的一个区间
def scan_ssdb_h(name,k1,k2):
	data = c.hscan(name,k1,k2,100000)
	#处理返回的数据
	length = len(data)
	if length % 2 !=0: length = length -1
	h={}
	for i in range(0,length,2):
		k = data[i]
		d = data[i+1]
		h[k] = ujson.loads(d)
	return h

#加载整个hashmap
def load_ssdb_hall(name):
	data = c.hgetall(name)
	#处理返回的数据
	length = len(data)
	if length % 2 !=0: length = length -1
	h={}
	for i in range(0,length,2):
		k = data[i]
		d = data[i+1]
		h[k] = ujson.loads(d)
	return h

#装载一个kv对象
def load_ssdb_kv(key):
	if len(key) >200:
		key = key[0:200]
	v = c.get( key  )
	if v=="" or v==None:
		raise Exception("{}的key不存在".format(key))
	return ujson.loads(v)

#存储一个kv对象
def to_ssdb_kv(key,o):
	if len(key) >200:
		key = key[0:200]
	v = c.set( key ,ujson.dumps(o) )
	return True
	
#清除一个kv对象
def clear_ssdb_kv(key):
	if len(key) >200:
		key = key[0:200]
	c.delete( key )
	return 0
	
#清除整个hashmap
def clear_ssdb_hall(name):
	c.hclear(name)
	return 0 
	
#清除一个hashmap对象
def del_ssdb_h(name,key):
	c.hdel(name,key)
	return 0

#装载一个hashmap对象
def load_ssdb_h(name,key):
	d = c.hget(name,key)
	if d !=None and d!="":
		o = ujson.loads(d)
	else:
		o = {}
	return o

#是否存在hashmap对象
def exists_ssdb_h(name,key):
	d = c.hexists(name,key)
	return d

#hashmap对象中的个数
def size_ssdb_h(name):
	d = c.hsize(name)
	return d

#操作一个队列
def do_ssdb_q(query):
	link = c
	action,name,start,end = query.split(",")
	action = action.strip()
	if action =="qrange":
		data = link.qrange(name.strip(),start.strip(),end.strip())
		size = link.qsize(name.strip())
		data2 = [[name.strip(),size]]
	#add by gjw on 2020-0304
	elif action =="qpop":
		size = start.strip()
		data = link.qrange(name.strip(),0,size)
		link.qpop_front(name.strip(),size)
		qsize = link.qsize(name.strip())
		data2 = [[name.strip(),qsize]]
	elif action =="qclear":
		qsize = link.qsize(name.strip())
		data = ['{"count":%s}'%(qsize)]
		link.qclear(name.strip())
		data2=[]
	elif action =="qslice":
		data = link.qslice(name.strip(),start.strip(),end.strip())
		size = link.qsize(name.strip())
		data2 = [[name.strip(),size]]
	elif action =="qlast":
		size = link.qsize(name.strip())
		start = 0 if size-int(end.strip()) <0 else size-int(end.strip())
		data = link.qrange(name.strip(),str(start), str(size))
		data2 = [[ name.strip(),size if size-int(end.strip())<0 else int(end.strip()) ]]
	elif action =="qlist":
		index = link.qlist(name.strip(),start.strip(),180)
		size0 = int(end.strip())
		data=[]
		for i in index:
			idata = link.qrange(i,"0",size0) #满足条件的第一个name的前xx条数据
			data.extend(idata)
			if len(data) >size0:
				data = data[0:size0]
				break;
		data2=[]
		count = 0
		ssum = 0
		for key_name in index:
			size = link.qsize(key_name)
			data2.append([key_name,size])
			count +=1
			ssum +=size
		data2.append(["count",count])
		data2.append(["sum",ssum])
	else:
		data=[]
		data2 =[]
	try:
		data = map(lambda x :ujson.loads(x),data)
	except Exception as e:
		pass
	return data,data2

def _dict(a,k,v):
	for k1,v1 in v.items():
		if isinstance(v1,dict):
			_dict(a,"%s.%s"%(k,k1),v1)
		else:
			a["%s.%s"%(k,k1)] = v1
#end _dict


def iso_to_timestamp(a):
	ta=(int(a[0:4]),int(a[5:7]),int(a[8:10]),int(a[11:13]),int(a[14:16]),int(a[17:19]),0,0,0)
	return int(time.mktime(ta)) 

lambda_iso_to_timestamp = lambda a : int(time.mktime((int(a[0:4]),int(a[5:7]),int(a[8:10]),int(a[11:13]),int(a[14:16]),int(a[17:19]),0,0,0)))

iso_to_datetime = lambda a : datetime(int(a[0:4]),int(a[5:7]),int(a[8:10]),int(a[11:13]),int(a[14:16]),int(a[17:19]),int(a[20:26]))

def now_timestamp():
	return int(time.time())


#放置秒级时间窗口
def push_stw(name,key,o):
	if key not in stream["pools2"][name]:
		stream["pools2"][name][key]=[]
	stream["pools2"][name][key].append(o)

#end

#放置计数窗口 add by gjw on 20230901
def push_scw(name,o):
	stream["pools"][name].append(o)	

#已经废弃, add by gjw on 20240122	,改有线程自动控制
def flush_scw():
	stream["pools"][name].clear()

c = Client("127.0.0.1",8888)

def push_df_ssdb(name,key,df):
	c.hset("DF:"+name,key,df.to_json(orient="split",date_format='iso', date_unit='s'))

def scan_df_ssdb(name,k1,k2):
	data = c.hscan("DF:"+name,k1,k2,10000)
	#处理返回的数据
	length = len(data)
	dfs=[]
	counts=[]
	for i in range(0,length,2):
		k = data[i]
		d = data[i+1]
		if d!="":
			res = ujson.loads(d)
		else:
			res={"data":[],"index":[],"columns":[]}
		df = pd.DataFrame(res["data"],columns=res["columns"],index=res["index"])
		df["@k"] = k
		dfs.append(df)
		counts.append([k,df.index.size])
	if len(dfs) >0:
		dfz = pd.concat(dfs,sort=False)
	else:
		dfz = pd.DataFrame()
	return dfz

#=====================================
def is_have_same_task(task):
	import psutil as ps
	i=0
	pids = ps.pids()
	for pid in pids:
		try:
			proc = ps.Process(pid)
			cmdlines =  proc.cmdline()
		except:
			continue		
		same=False
		for line in cmdlines:
			if line==task: #完全相同				
				same=True
		if same:		
			i +=1
	#end if
	if i >=2: return True #有一个是自己
	return False

#保存到X_log中
def add_error_to_log(name,params,error):
	try:
		d={}
		d["user"] = "x_finder3"
		d["timestamp"] = datetime.now().isoformat()
		d["nav_name"]= stream["name"]
		d["action"]= name
		d["params"] = params
		d["operate_result"] = "错误"
		d["failed_reason"] = error
		stream["last_failed_reason"] = error
		root_logger.error(ujson.dumps(d,ensure_ascii=False))
		save_last_error_or_info(stream["name"],"{0}-{1}-{2}-{3}".format(d["timestamp"],d["action"],error,d["params"]))
	except Exception as e:
		pass

#保存到X_log中
def add_info_to_log(name,params):
	try:
		d={}
		d["user"] = "x_finder3"
		d["timestamp"] = datetime.now().isoformat()
		d["nav_name"]= stream["name"]
		d["action"]= name
		d["params"] = params
		d["operate_result"] = "信息"
		d["failed_reason"] = ""
		root_logger.info(ujson.dumps(d,ensure_ascii=False))
		#save_last_error_or_info(stream["name"],"{0}-{1}-{2}".format(d["timestamp"],d["action"],d["params"]))
	except Exception as e:
		pass

def save_last_error_or_info(name,err_info):	
	stream["last_err_info"] = err_info

def load_last_error_or_info(name):	
	return stream["last_err_info"]

#保存自己的eps数到shm
def save_eps(name,info):
	try:			
		with open("/dev/shm/xlink_{}:eps".format(name),"w+") as f:
			f.write(ujson.dumps(info))
	except Exception:
		pass


def gen_consumer():

	consumer = Consumer({
		'bootstrap.servers': stream["source"]["link"],
		'group.id': stream["source"]["group"],
	    'session.timeout.ms': 10000,
		'auto.offset.reset': 'latest',
		"fetch.message.max.bytes": 128*1024*1024,
		"queued.min.messages": 500000,
		"queued.max.messages.kbytes": 2097151,
		"auto.commit.interval.ms": 10000,
		"max.poll.interval.ms": 600000
	})
	topic = stream["source"]["topic"]

	#增加对多主题的支持
	if "topics" in stream["source"]:
		topics = stream["source"]["topics"]
		topics.append(topic)
	else:
		topics = [topic]

	if stream["source"]["start-0"] ==True:
		tps=[]
		for topic in topics:
			meta = consumer.list_topics(topic)
			size = len(meta.topics[topic].partitions)	
			#add by gjw on 20230410
			if "parts"	in 	stream["source"]:
				parts = stream["source"]["parts"]
			else:
				parts = meta.topics[topic].partitions
			for i in range(size):
				if i in parts:
					tp = TopicPartition(topic,i,OFFSET_BEGINNING)
					tps.append(tp)
		consumer.assign(tps)
	
	else:
		#on_revoke=kfk_re_assign
		#consumer.subscribe(topics,on_lost=kfk_re_assign)
		#add by gjw on 20230410 根据已经commited的数据来订阅消息
		tps=[]
		for topic in topics:
			meta = consumer.list_topics(topic)
			size = len(meta.topics[topic].partitions)	
			#add by gjw on 20230410
			if "parts"	in 	stream["source"]:
				parts = stream["source"]["parts"]
			else:
				parts = meta.topics[topic].partitions
			for i in range(size):
				if i in parts:
					tp = TopicPartition(topic,i,OFFSET_STORED)
					tps.append(tp)
		consumer.assign(tps)

	return consumer
# 生成一个消费者

#重新分配分区情况，从已有分区的0开始
def kfk_re_assign(consumer, tps):
	info = ""
	for tp in tps:
		info +="{}-{}-{},".format(tp.topic,tp.partition,tp.offset)
	add_info_to_log("kfk消费者","offset on_lost,详细信息: "+info)
	
	# try:
	# 	topic = stream["source"]["topic"]
	# 	meta = consumer.list_topics(topic)
	# 	size = len(meta.topics[topic].partitions)
	# 	tps=[]
	# 	for i in range(size):
	# 		tp = TopicPartition(topic,i,OFFSET_BEGINNING)
	# 		tps.append(tp)
	# 	consumer.assign(tps)
	# except Exception as e:
	# 	add_error_to_log("kfk消费者","建立失败",e.__str__())
	


# 处理信号，信号值10
def receive_signal(signum, stack):
	stream["run"] = False
	add_info_to_log("退出","收到退出消息!")

#2022-0907

class DateEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj,datetime):
			return obj.strftime("%Y-%m-%d %H:%M:%S")
		else:
			return json.JSONEncoder.default(self,obj)



# 输出stream的目前的信息，信号值37
def printk_stream(signum,stack):
	stream_clone = {}
	try:
		for k,v in stream.items():
			if k in ["pools","pools2","kfk_pools","redis_pools","unix_pools"]:
				stream_clone[k]={}
				for k1,v1 in v.items():
					stream_clone[k][k1] = len(v1)
			elif k in ["redis_client","perf_funs","printf","当前消息","total","unix_udp_drops","st","stw"]: #不处理
				continue
			elif type(v) in [int,str,float]:
				stream_clone[k] = v
			elif type(v)==list:
				if len(v)==0:continue
				stream_clone["{}:总数".format(k)] = len(v)
				stream_clone[k] = str(v[0:100])
			elif type(v)==dict:
				if len(v)==0:continue
				stream_clone[k] ={"总数":len(v)}
				for i,k1 in enumerate(v.keys()):
					if i<20:
						stream_clone[k][k1] = str(v[k1])
					else:
						break
			else:
				stream_clone[k] = str(v)
				
		#add by gjw on 2024-0117 增加内存监控	
		from pympler import asizeof
		stream_clone["stream_Mem(KB)"] = int(asizeof.asizeof(stream)/1024)
		stream_clone["pools_Mem(KB)"] = int(asizeof.asizeof(pool)/1024)
		stream_clone["inpools_Mem(KB)"] = int(asizeof.asizeof(in_pools)/1024)
		g = globals()
		for k,v in g.items():
			try:
				size = int(asizeof.asizeof(v)/1024)
				if size >0:
					stream_clone[f"{k}_Mem(KB)"] = size
			except:
				pass
		import json
		c.set("sys:stream:{}".format(stream["name"]),json.dumps(stream_clone,skipkeys=True,cls=DateEncoder))
	except Exception as e:
		info = {"stream输出发生错误":e.__str__(),"错误跟踪":"{}".format(traceback.format_exc())}
		c.set("sys:stream:{}".format(stream["name"]),ujson.dumps(info))


def xlink_stats_finished():
	b={"status":"finished","time":datetime.now().isoformat()[0:19]}
	c.hset("system:xlinks",stream["name"],json.dumps(b))



# 处理信号，信号值34，断点消息处理
def event_debug_break(signum, stack):
	name = stream["name"]
	info={"时间":datetime.now().isoformat()[0:19]}
	if "break_info" in stream and stream["break_info"]:
		
		try:
			o = pickle.loads(stream["break_info"])
		except:	
			try:
				o = orjson.loads(stream["break_info"])
			except:
				o = stream["break_info"]
	
		if isinstance(o,bytes):
			info["消息体o"] = o.decode("utf8")
		else:
			info["消息体o"] = o
		
		#只去一条进行处理
		if isinstance(o,list):
			o = o[0]
		try:
			from line_profiler import LineProfiler
			from io import StringIO
			lp = LineProfiler()
			for fun in stream["perf_funs"]:
				lp.add_function(fun)
			out = StringIO()
			cc = importlib.import_module("streams.%s"%(stream["module"]))
			importlib.reload(cc)
			
			#result = cc.Events(o)
			lp_wrap = lp(cc.Events)
			result = lp_wrap(o)
			lp.print_stats(out)
			print_break(o,result,"",out.getvalue())
			out.close()
		except Exception as e:
			info["中断事件处理出错"] =e.__str__()
			c.set("sys:break:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))
	else:
		info["中断事件处理"] ="没有找到可用的断点消息"
		c.set("sys:break:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))
	

# 处理信号，信号值38，进入监控模式!
def pm_on(signum, stack):
	stream["pm_ssdb_printf"] = True	
	#add_info_to_log("监控","进入监控模式!")

# 处理信号，信号值35,单事件
def event_debug_one(signum, stack):	
	name = stream["name"]
	b = time.time()
	info={"时间":datetime.now().isoformat()[0:19]}
	if "当前消息" in stream and stream["当前消息"]:		
		try:
			o = pickle.loads(stream["当前消息"])
		except:
			try:
				o = orjson.loads(stream["当前消息"])
			except:
				o = stream["当前消息"]
		#只去一条进行处理
		if isinstance(o,list):
			o = o[0]
		#事件处理	
		try:
			from line_profiler import LineProfiler
			from io import StringIO
			lp = LineProfiler()
			for fun in stream["perf_funs"]:
				lp.add_function(fun)
			out = StringIO()
			cc = importlib.import_module("streams.%s"%(stream["module"]))
			importlib.reload(cc)
			
			#result = cc.Events(o)
			lp_wrap = lp(cc.Events)
			result = lp_wrap(o)
			lp.print_stats(out)
			out.flush()
			info["代码性能"]=out.getvalue()			
			out.close()
			#处理result
			if result is None:
				info["返回值"] = "None"
			else:
				for i,a in enumerate(result):
					info["返回值{}".format(i)] = a
		except Exception as e:
			info["事件处理出错"] ="{}, traceback:{}".format(e.__str__(),traceback.format_exc())
	else:
		info["事件处理出错"] ="没有找到可用的当前消息"
	if isinstance(o,bytes):
		info["消息体o"] = o.decode("utf8")
	else:
		info["消息体o"] = o
	info["Cost_Time(s)"]=time.time()-b
	try:
		c.set("sys:debug:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))
	except Exception as e:
		info = {"调试输出发生错误":e.__str__()}
		c.set("sys:debug:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))	
#end if


#开启调试，可以在事件处理或其他python代码端中使用
def debug_on(num=1):
	if num==1 and stream["debug"]==False:
		stream["debug"] = True
		add_info_to_log("调试","有断点信息")
		stream["break_info"] = stream["当前消息"]

#观察调试函数，可以在任意位置调用
def debug_fun(main_fun,*args):
	from line_profiler import LineProfiler
	from io import StringIO
	lp = LineProfiler()
	for fun in stream["perf_funs"]:
		lp.add_function(fun)
	out = StringIO()
	
	lp_wrap = lp(main_fun)
	result = lp_wrap(*args)
	lp.print_stats(out)
	stream["debug_fun"] = out.getvalue()
	out.close()
	return result

#打印断点信息
def print_break(o,result,topic="",s=""):
	info={"时间":datetime.now().isoformat()[0:19],"队列":topic,"代码性能":s,"消息体o":o,}
	#处理result
	if result is None:
		info["返回值"] = "None"
	elif isinstance(result,list):
		for i,a in enumerate(result):
			info["返回值-{}".format(i)] = a
	elif isinstance(result,dict):
		for k,a in result.items():
			info["返回值-{}".format(k)] = a
	else:
		info["返回值"] = result

	try:
		c.set("sys:break:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))
	except Exception as e:
		info = {"调试输出发生错误":e.__str__()}
		c.set("sys:break:{}".format(stream["name"]),json.dumps(info,skipkeys=True,cls=DateEncoder))
	

# 处理信号，信号值10, 流继续
def event_debug_off(signum, stack):
	stream["debug"] = False
	#更新模块
	try:
		if "streams.%s"%(stream["name"]) in sys.modules:
			cc = sys.modules["streams.%s"%(stream["name"])]
			importlib.reload(cc)
		add_info_to_log("调试","退出调试模式,更新代码!")
	except Exception as e:
		add_error_to_log("调试","更新代码失败!",e.__str__())
	
"""
调试信号
参数：任务名,信号值

信号含义如下：
34  , 开启调试,断点处理
35  , 单条执行
36  , 退出调试,流更新
37  , 查看stream
38  , 开启监控信息
"""
def register_signal():
	# 注册信号处理程序,10退出
	signal.signal(signal.SIGUSR1, receive_signal)

	#add by gjw on 2022-0907

	# 注册信号处理程序,34断掉调试
	signal.signal(signal.SIGRTMIN, event_debug_break)

	# 注册信号处理程序,35单条运行
	signal.signal(signal.SIGRTMIN+1, event_debug_one)

	# 注册信号处理程序,36退出事件调试，流更新
	signal.signal(signal.SIGRTMIN+2, event_debug_off)

	# 注册信号处理程序,37打印stream
	signal.signal(signal.SIGRTMIN+3, printk_stream)

	# 注册信号处理程序,38开启监控信息
	signal.signal(signal.SIGRTMIN+4, pm_on)

