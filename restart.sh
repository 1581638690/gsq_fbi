#!/bin/bash


function check_port_close()
{
	printf .
	while :
	do
		a=`lsof -i:$1 | wc -l`
		if [ "$a" -gt "0" ];then
            printf .
		else
			break
		fi
	done
	echo $1
}

./stop.sh
#check_port_close 9000
#check_port_close 9999
#check_port_close 8998
sleep 1
./start.sh

#if [ ! -d /opt/fbi-base ]; then 
#	./start.sh
#else
#	./ustart.sh
#fi

