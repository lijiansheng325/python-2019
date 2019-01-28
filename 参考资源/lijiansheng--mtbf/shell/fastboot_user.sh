#!/bin/bash
IPADDRESS=$1
#check avgs
if [ $# -eq 1 ];then
	case `echo $1|awk -F. '{print NF}'` in
		#usb connect
		1)
			IPADDRESS=$1
		;;
		#net connect
		4)
			IPADDRESS=$1":5555"
		;;
		#error device
		*)
			echo "$1 is wrong device!!!"
			exit
		;;
	esac
else
	echo "Avgs is $#"
	echo "device: IP or devices name"
	exit
fi
reconnect()
{
if [ $ISUSB -eq 1 ];then
	adb -s ${IPADDRESS} wait-for-devices
	return
fi
adb disconnect ${IPADDRESS}
local a=0
while true;do
	sleep 5
    case `adb -s ${IPADDRESS} shell ls|grep -c -w data` in
        0)
            adb connect ${IPADDRESS}
			sleep 2
			adb -s ${IPADDRESS} root
			sleep 5
        ;;
        1)
            echo "reconnect $a times, connected!!! continue!!!"
            break
        ;;
        *)
            echo "date:"`adb -s ${IPADDRESS} shell ls|grep -c -w data`
        ;;
    esac
    local a=$((a+1))
    if [ $a -eq $1 ];then
        echo "reconnect $1 times, failed!!! exit!!!"
		adb -s ${IPADDRESS} wait-for-devices
        #exit
    fi
done
}

flash_phone()
{
	adb -s ${IPADDRESS} wait-for-device
	rm -r temp.log
	adb -s ${IPADDRESS} reboot bootloader
	wait
	sleep 20
	fastboot -w
	sleep 5
	fastboot devices
	fastboot flash preloader_x600 preloader_x600.bin
	wait
	sleep 5
	fastboot flash lk lk.bin
	wait
	sleep 5
	fastboot flash boot boot.img
	wait
	sleep 5
	fastboot flash recovery recovery.img
	wait
	sleep 5
	fastboot flash secro secro.img
	wait
	sleep 5
	fastboot flash logo logo.bin
	wait
	sleep 5
	fastboot flash video video.img
	wait
	sleep 5
	fastboot flash tee1 trustzone.bin
	wait
	sleep 5
	fastboot flash tee2 trustzone.bin
	wait
	sleep 5
	fastboot flash system system.img
	wait
	sleep 5
	fastboot flash cache cache.img > temp.log 2>&1
	wait
	sleep 5
	fastboot flash userdata userdata.img
	wait
	sleep 5
	fastboot flash aboot emmc_appsboot.mbn
	wait
	sleep 5
	fastboot flash abootbak emmc_appsboot.mbn
	wait
	sleep 5
	fastboot flash persist persist.img
	wait
	sleep 5
	fastboot reboot
	sleep 20
}

flash_phone

int=1
while(( $int<=10 ))
do
	line=`awk 'NR==3 { print $0 }' temp.log`
	echo "**************************"
	echo $line
	echo "**************************"
	if [ "$line" == "FAILED (remote: unknown command)" ];then
		echo "检测到刷机失败，正在启动新一次的刷机"
		flash_phone
	else
		echo "flash success"
		break		
	fi
	let "int++"
done
sleep 100
