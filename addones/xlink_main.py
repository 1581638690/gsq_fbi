#!/opt/fbi-base/bin/python3
# -*- coding: utf-8 -*- 

import sys
import os
sys.path.append("../lib")
sys.path.append("/opt/openfbi/fbi-bin")
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
import json
import time
import socket
try:
	import numpy as np
	import pandas as pd
	pd.options.future.infer_string = True
	from confluent_kafka import Consumer,OFFSET_BEGINNING,TopicPartition,Producer,KafkaException
	from elasticsearch7 import Elasticsearch,helpers
except:
	pass
import threading
import gc
from datetime import datetime
import signal
from collections import deque
import redis
from avenger.fsys import have_days, is_out_days
from streams import stream,ssdb_printf,is_have_same_task,add_error_to_log,add_info_to_log,register_signal,gen_consumer,print_break,get_redis_client,to_redis_only_all,redis_memory,flush_scw,init,init_log
from multiprocessing import Process,Queue,Pool
import traceback 
import glob
import shutil
import psutil
from clickhouse_driver import Client as CKH_Client
import lz4.block as ccc
import importlib



#add by gjw on 2022-0728 兼容高性能和高兼容性
try:
	import orjson
	import ujson
except:
	import json as orjson
	import json as ujson

from xlink_core import *

#总体配置
cfg={}

#add by gjw 启动后台进程，复制网上
def StartDaemon(fun):
	# fork进程
	try:
		if os.fork() > 0: os._exit(0)
	except OSError as error:
		print(('fork #1 failed: %d (%s)' % (error.errno, error.strerror)))
		os._exit(1)   
	#os.chdir('/') #记住当前目录
	os.setsid()
	os.umask(0)
	try:
		pid = os.fork()
		if pid > 0:
			print(('Daemon PID %d' % pid))
			os._exit(0)
	except OSError as error:
		print(('fork #2 failed: %d (%s)' % (error.errno, error.strerror)))
		os._exit(1)
	# 重定向标准IO,运行正常流程
	
	try:
		sys.stdout.flush()
		sys.stderr.flush()
		si = open("/dev/null", 'r')
		so = open("/dev/null", 'w+')
		#so = open("logs/"+cfg["stream"]+".err", 'w+')
		#se = open("/dev/null", 'w+')		
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(so.fileno(), sys.stderr.fileno())
	except:
		pass
	print("后台开始运行")
	# 在子进程中执行代码
	fun() # function demo


#多任务时任务id
xlink_pids={}

#add by gjw on 20240223
def xlink_muli_daemon():
	ppid = os.getpid()
	add_info_to_log("守护开始",f'PID:{ppid},主任务+{stream["max_xlink"]}')
	while stream["run"]:
		pids = xlink_pids.copy()
		for xid,pid in pids.items():
			try:
				p = psutil.Process(pid)
				if p.status() =='zombie':
					os.waitpid(pid,os.WNOHANG)
					raise Exception("Zombie")
				#暂时不用
				"""
				mem = round(p.memory_info()[0]/1024/1024/1024)				
				if mem >stream["max_mem"]:
					print(f"Memory(GB). {mem} > stream['max_mem']")
				"""
			except:
				try:
					#print(f"Start Process xlink task: {xid}")
					add_info_to_log(f"守护监测[{xid}]",f'任务ID:{xid},PID-{pid}异常，启动新任务')
					if xid==-1:
						p1 = Process(target=x_start)
						p1.daemon=False
						p1.start()
						xlink_pids[xid]=p1.pid
					else:
						p1 = Process(target=sub_xlink_task,args=(stream,xid))
						p1.daemon=False
						p1.start()
						xlink_pids[xid]=p1.pid
					add_info_to_log(f"守护启动[{xid}]",f'任务ID:{xid},PID-{p1.pid}，启动成功')
				except Exception as e:
					add_error_to_log(f"守护启动[{xid}]",f'任务ID:{xid}异常',f"错误原因:{e}")
			#end if
		#end for
		time.sleep(30) #频度太高，会影响性能
	#end while
	add_info_to_log("守护退出",f'PID:{ppid}')


if __name__=="__main__":

	#add by gjw on 2024-0809 hash的种子给固定下来,好像不起作用
	#os.environ['PYTHONHASHSEED'] = '0'

	if len(sys.argv)<2:
		print("xlink_main.py stream=流插件")
		exit()
	for cmd in sys.argv:
		ps = cmd.split("=")
		if len(ps)<2:
			cfg[ps[0]]="Y"
		else:
			k = ps[0].strip()
			v = ps[1].strip()
			cfg[k] = v 
	print(cfg)
	
	if is_have_same_task("stream="+cfg["stream"]) and "-D" in cfg:
		print("xlink启动出错,已经存在[%s]的任务在运行，不能同时运行多个相同的任务！"%(cfg["stream"]))		
		exit()

	#Begin 开始加载插件，进行消息处理

	#exec("import streams.%s as xlink"%(cfg["stream"]))
	xlink = importlib.import_module("streams.%s"%(cfg["stream"]))
	
	stream["name"] = cfg["stream"]
	stream["module"] = stream["name"]
	stream["task_id"]= -1 #主服务
	try:
		#0
		init_log()
		#1
		xlink.Inits()
		#2
		init()
	except Exception as e:
		print("初始化出错：%s"%(e))
		print("错误跟踪:{}".format(traceback.format_exc()))
		add_error_to_log("初始化出错","错误跟踪:{}".format(traceback.format_exc()),"初始化出错：%s"%(e))
		exit()


	#add by gjw on 2024-0410 redis list_json模式的自适应负载
	if "redis" in stream["source"] and (stream["source"]["redis"]=="list_json" or stream["source"]["redis"]=="json"):
		topic = stream["source"]["topic"]
		if "topics" in stream["source"]:
			if topic not in stream["source"]["topics"]:
				stream["source"]["topics"].append(topic)
		else:
			stream["source"]["topics"]=[topic]
		
		topics = len(stream["source"]["topics"])

		if topics >5:
			stream["max_xlink"] =  int(topics/5)

	if "unix_udp" in stream["source"] and "port" in stream["source"]:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_socket.setblocking(0)
		while True:
			try:		
				# 绑定套接字到指定地址
				server_socket.bind((stream["source"]["unix_udp"],stream["source"]["port"]))
				
				stream["server_socket"] = server_socket
				add_info_to_log("构建Socket","Unix_UDP {}-{} Sokcet准备完毕".format(stream["source"]["unix_udp"],stream["source"]["port"]))
				break
			except Exception as ke:
				add_error_to_log("启动出错","Unix_UDP",ke.__str__())
				time.sleep(2)


	#add by gjw on 20230524 子任务并行计算
	if "max_xlink" in stream:	
		#0..号任务，创建一个子进程		
		for i in range(0,stream["max_xlink"]):
			p1 = Process(target=sub_xlink_task,args=(stream,i))
			p1.daemon=False
			p1.start()
			xlink_pids[i]=p1.pid
			add_info_to_log(f"启动xlink子任务[{i}]",f"ID-{i},PID-{p1.pid}")
		
		#主服务的参数
		if "files" in stream["source"]:
			#文件的id从１开始，适应znsm的规则, 主进程处理１号文件，可以看到实时处理信息
			stream["task_file_id"] = 1
			stream["source"]["files"] = stream["source"]["files"].format(1)
		elif "unix_udp" in stream["source"] and "port" not in stream["source"]:
			stream["source"]["socket"] = "{}.{}".format(stream["source"]["unix_udp"],1) #对应1
		elif "redis" in stream["source"] and (stream["source"]["redis"]=="list_json" or stream["source"]["redis"]=="json"):
			stream["redis_json_id"] = 0
		
		#meta信息
		ss=""
		for k,v in stream["source"].items():
			ss +="%s: %s,"%(k,v)
		ss +="子任务并行:{}".format(stream["max_xlink"])
		stream["source_meta"] = ss

		#启动主服务
		p1 = Process(target=x_start)
		p1.daemon=False
		p1.start()
		xlink_pids[-1]=p1.pid
		add_info_to_log("启动xlink主任务[-1]",f"PID-{p1.pid}")
	#end if

	#meta信息
	ss=""
	for k,v in stream["source"].items():
		ss +="%s: %s,"%(k,v)
	stream["source_meta"] = ss
	print("Xlink: %s 参数:%s"%(cfg["stream"],ss))
	print("===========================XLNK2===============================\n")
	add_info_to_log("启动参数",f"{ss}")
		
	#主进程或服务	
	if "max_xlink" in stream:
		#多个任务
		xlink_muli_daemon()
		#StartDaemon(xlink_muli_daemon)
	else:
		#单个任务
		StartDaemon(x_start)
