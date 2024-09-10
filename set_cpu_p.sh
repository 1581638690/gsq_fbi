#!/bin/bash

#cpu 高性能模式
cpus=`cat /proc/cpuinfo | grep "processor"  | awk -F":" '{print $2}'`

for cpu in $cpus
do
    #echo $cpu
    echo "performance" >/sys/devices/system/cpu/cpu$cpu/cpufreq/scaling_governor
done
