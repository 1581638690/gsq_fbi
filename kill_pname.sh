#!/bin/bash
#kill progess by name

echo $1
pgrep -f $1
pgrep -f $1 | xargs kill -s 9 1>/dev/null 2>&1



