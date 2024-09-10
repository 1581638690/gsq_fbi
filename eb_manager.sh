#!/bin/bash
#ZHDS eb 实例的启停
act=$1
case $act in
start)
	start-stop-daemon --start -b --exec /opt/ds/es/bin/elasticsearch 
	#start-stop-daemon --start -b --exec /opt/ds/filebeat/filebeat -- -c  /opt/ds/filebeat/filebeat.yml
	echo "Start ok!"
;;
stop)
	pgrep -f elasticsearch | xargs kill -s 2
	#pgrep -f filebeat | xargs kill -s 2
	echo "Stop ok!"
;;
restart)
	echo "now not ok!"
;;
esac

