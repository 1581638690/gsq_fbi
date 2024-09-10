#!/bin/bash

py=/opt/fbi-base/bin


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/openfbi/lib
export PYTHONHASHSEED=0

ulimit -n 1024000

#2G
sudo sysctl -w net.core.wmem_max=2097152000
sudo sysctl -w net.core.rmem_max=2097152000
#100M
sudo sysctl -w net.core.wmem_default=104857600
sudo sysctl -w net.core.rmem_default=104857600
#depth
sysctl -w net.unix.max_dgram_qlen=500000
sysctl -w net.core.netdev_max_backlog=200000

myPath="../workspace"
confPath="../conf"
xlinks_path="script/xlinks"
report_path="/opt/openfbi/workspace/report"
report_path2="/opt/openfbi/mPig/html/bi/report/"
xlink_data_path="/data/xlink"

if [ ! -d $myPath ]; then
	ln -s /data/workspace $myPath
fi

if [ ! -d $confPath ]; then 
	mkdir $confPath
fi

if [ ! -d $xlinks_path ]; then 
	mkdir -p $xlinks_path
fi

if [ ! -d $report_path ]; then 
	mkdir -p $report_path
fi

if [ ! -d $report_path2 ]; then 
	mkdir -p $report_path2
fi

if [ ! -d $xlink_data_path ]; then 
	mkdir -p $xlink_data_path
fi


#cpu 高性能模式
/opt/openfbi/fbi-bin/set_cpu_p.sh 1>/dev/null 2>&1

#先停止
/opt/openfbi/fbi-bin/stop.sh 1>/dev/null 2>&1

#报告输出需要
export OPENSSL_CONF=/etc/ssl

#启动
echo "start the fbi-server..."
$py/python3 fbi-server.pyc
echo "start the gate_way..."
$py/gunicorn  -w 4 -b 127.0.0.1:9999 -D --timeout 300 --worker-class=gevent --graceful-timeout 300 fbi-gateway:app 
$py/gunicorn -w 4 -b 127.0.0.1:8998 -D --pythonpath lib  -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"  fbi-dataserver:app
#gateway3
$py/gunicorn  -k uvicorn.workers.UvicornWorker -w 4 --bind "127.0.0.1:9998" -D  --timeout 120 --graceful-timeout 300  fbi-gateway3:root

#进程守护
$py/python3 fbi-master.pyc
#远程管理
/opt/fbi-base/bin/wssh --address=127.0.0.1 --port=8999 1>/dev/null 2>&1 &
echo "OK!"

