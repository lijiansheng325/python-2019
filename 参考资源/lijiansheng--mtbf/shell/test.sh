#!/bin/bash

i=0

while ((i<10))
do
	adb -s JRZH69U8AYS84PIV install -r ../apk/Utf7Ime.apk > tmp.txt &
	sleep 2
	adb -s JRZH69U8AYS84PIV shell input tap 469 1721
	adb -s JRZH69U8AYS84PIV shell input tap 807 1857
	sleep 13
	cat -v tmp.txt |tr -d "^M" > tmp1.txt
	flag=0
	for line in `cat tmp1.txt`
	do
		echo $line
		if [ "$line" == "refused" ];then
			flag=1
		fi
	done
	if [ $flag -ne 0 ];then
		echo "不允许后台命令安装程序,重新尝试!!!"
		let ++i
		continue
	else
		echo "已经允许安装程序"
		break		
	fi
done

rm -r tmp.txt
rm -r tmp1.txt
