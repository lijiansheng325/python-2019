#!/system/bin/sh

dump(){
if [ -a $xml ];then
	rm $xml
fi
while true;do

	`$su uiautomator dump $xml 1>/dev/null 2>&1`
	if [ -a $xml ];then
		if [ $1 -eq 1 ];then
			`$su busybox sed -i 's/ /\n/g' $xml`
		elif [ $1 -eq 2 ];then
			`$su busybox sed -i 's/<node/\n<node/g' $xml`
		fi
		break
	fi
done
}

#input函数定义
press(){
case $1 in
#UP
	UP)
        	`$su input keyevent 19`
	;;
#DOWN
	DOWN)
        	`$su input keyevent 20`
	;;
#LEFT
	LEFT)
        	`$su input keyevent 21`
	;;
#RIGHT
	RIGHT)
            `$su input keyevent 22`
	;;
#OK
	OK)
            `$su input keyevent 23`
	;;
#BACK
	BACK)
        	`$su input keyevent 4`
	;;
#HOME
	HOME)
        	`$su input keyevent 3`
	;;
esac
}

##多次按键定义
presst(){
local z=0
while [ $z -ne $2 ]
do
    press $1
    sleep $3
    local z=$((z+1))
done
}

#开机向导
precondition(){

dump 1

tmpv=`grep "focused=\"false\"" $xml|busybox awk -F"\"" '{print $10}'`

echo $tmpv
if [ `echo $tmpv|busybox awk -F " " '{print $1}'` == "com.stv.dvbplayer" ];then
	echo ""
else 
	press HOME
	flagNo=1
	while true;do
		if [ flagNo -eq 5 ];then
			press OK
			break;
		fi
		dump 2
		tmp1=`grep "focused=\"true\"" $xml|busybox awk -F"\"" '{print $8}'`
		echo $tmp1
		if [  `echo $tmp1|busybox awk -F "id/" '{print $2}'` == "box_desktop" ];then
			press OK
			break
		fi
		press LEFT
		flagNo=$(($flagNo + 1))
	done
fi

}






#run test
check_su=`ls /system/xbin/|busybox grep -c -w su`

if [ $check_su -eq 0 ];then
	su=""
	# comment "检查su" "无su"
	case `getprop|grep "ro.product.name"|busybox awk '{print substr($2,2,length($2)-2)}'` in "android_x600")
			exit
		;;
	esac
else
	su="su -k"
fi

xml="/data/local/check.xml"

precondition
