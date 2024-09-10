#!/bin/bash
#ssdb 实例的启停
conf=$1
act=$2
ulimit -n 10240
now=`date -Iseconds`
case $act in
start)
	/opt/openfbi/ssdb-1.9.6/ssdb-server $conf -d -s restart
;;
stop)
	pgrep -f ssdb-server | xargs kill -s 9
;;
restart)
	echo "$now restart..." >>/data/ssdb/ssdb.log
	pgrep -f ssdb-server | xargs kill -s 9
	echo "$now kill ssdb-server" >>/data/ssdb/ssdb.log
	sleep 3
	/opt/openfbi/ssdb-1.9.6/ssdb-server $conf -d -s restart
	now=`date -Iseconds`
	echo "$now 启动完成">>/data/ssdb/ssdb.log
;;
esac

