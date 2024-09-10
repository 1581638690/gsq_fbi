#!/bin/bash

pgrep -f fbi-fst | xargs kill -s 9  1>/dev/null 2>&1
echo "stop the fbi-fst engine!"
