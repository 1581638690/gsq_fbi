#!/bin/bash

pgrep -f fbi-server | xargs kill -s 9  1>/dev/null 2>&1
pgrep -f fbi-gateway | xargs kill -s 9  1>/dev/null 2>&1
pgrep -f fbi-dataserver | xargs kill -s 9  1>/dev/null 2>&1
pgrep -f data-server | xargs kill -s 9  1>/dev/null 2>&1
#pgrep -f jupyter-notebook | xargs kill -s 9
pgrep -f fbi-master | xargs kill -s 9  1>/dev/null 2>&1
pgrep -f wssh | xargs kill -s 9  1>/dev/null 2>&1
echo "the fbi-engine stoped!"
