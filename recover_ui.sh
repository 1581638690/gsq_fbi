#!/bin/bash


echo "从备份中恢复UI"
vid=$1

cd /opt/openfbi/mPig/
tar -xf  html.$vid.tar.bz2
cd -
