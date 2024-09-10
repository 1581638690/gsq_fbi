#!/bin/bash


find script/system -name "*.fea" -type f -print  -exec rm -rf {} \;
rm m*.pyc -rf
rm cm.pyc fio.pyc fsets.pyc fshow.pyc fst.pyc fsys.pyc fglobals.pyc sysrule.pyc xlink.pyc logstash.pyc -rf
rm version.txt version2.txt events.pyc timer.pyc -rf

vid=$1
myPath="../workspace"
file="fbi*-*-*$vid.tar.gz"
src="$myPath/$file"
odir="../"

#存在fbi文件才执行，否则不干
if [ -f $src ]; then 
	cp $src $odir
	#delete the driver path
	rm driver -rf
	mkdir db_bak
    #需要备份的问题件
	cp redis-server.sh db_bak/ -rf
    cp fbi_extends.py db_bak/  -rf
	cd $odir
	tar -xf $file
	rm $file -rf
	cd -
	#恢复文件
	cp db_bak/redis-server.sh . -rf
    cp db_bak/fbi_extends.py . -rf 
	cp script_system/system/* script/system/ -rf
fi


