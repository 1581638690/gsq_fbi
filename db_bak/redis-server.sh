#!/bin/bash


/opt/openfbi/bin/redis-server /opt/openfbi/conf/redis.conf --bind 127.0.0.1 >/dev/null 2>&1 &
echo "OK!"