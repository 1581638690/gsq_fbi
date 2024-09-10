#!/bin/bash


echo "更新UI文件包"
vid=$1

d=`date +%Y-%m-%d`
echo "备份UI文件"
cd /opt/openfbi/mPig/
tar -cjf  html.$d.tar.bz2 html
cd -

echo "复制文件"
myPath="/opt/openfbi/workspace"
file="mPig*RC*-$vid.tar.xz"
src="$myPath/$file"
cd $myPath
tar -xf $src
cp mPig/html/* /opt/openfbi/mPig/html -rf
rm mPig -rf
cd -
