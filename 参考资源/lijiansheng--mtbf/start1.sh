#!/bin/bash
IPADDRESS=$1
IPONLY=$1
BUILD_ID=$2
DEVICE=$3
ISUSB=0
#check avgs
if [ $# -eq 3 ];then
    case `echo $1|awk -F. '{print NF}'` in
        #usb connect
        1)
            IPADDRESS=$1
			ISUSB=1
        ;;
        #net connect
        4)
            IPADDRESS=$1":5555"
			ISUSB=0
        ;;
        #error device
        *)
            echo "$1 is wrong device!!!"
            exit
        ;;
    esac
    caselist="caselist.txt"
    if [ ! -f $caselist ];then
        echo "No $caselist!!! exit!!!"
        exit
    fi
    case $# in
        2)
            m_avg=15
        ;;
        3)
            m_avg=$5
        ;;
    esac
else
    echo "Avgs is $#, it should be device BUILD_ID"
    echo "device: IP or devices name"
    echo "BUILD_ID: Test result root folder"
    echo "DEVICE: Test result root folder"
    exit
fi
#connect device before run case
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
# check uiautomator process exist or not
waitUI()
{
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
            if [ `adb -s ${IPADDRESS} shell ps | grep -c uiautomator` -eq 0 ];then
                echo "There is no uiautomator!!! continue!!!"
                break
            else
                sleep 10
            fi
        ;;
        *)
            echo "date:"`adb -s ${IPADDRESS} shell ls|grep -c -w data`
        ;;
    esac
    local a=$((a+1))
    if [ $a -eq 10 ];then
        echo "reconnect 10 times, failed!!! exit!!!"
		adb -s ${IPADDRESS} wait-for-devices
        #exit
    fi
done
}
pullDropbox(){
	adb -s ${IPADDRESS} pull /sdcard/sems $result_folder/'LOOP'$i/$current_case_folder/sems
	adb -s ${IPADDRESS} pull /sdcard/logs $result_folder/'LOOP'$i/$current_case_folder/logs
	mkdir -p $result_folder/'LOOP'$i/$current_case_folder/dropbox
	adb -s ${IPADDRESS} root
	adb -s ${IPADDRESS} pull /data/system/dropbox $result_folder/'LOOP'$i/$current_case_folder/dropbox
	adb -s ${IPADDRESS} pull /data/tombstones $result_folder/'LOOP'$i/$current_case_folder
	adb -s ${IPADDRESS} pull /data/anr $result_folder/'LOOP'$i/$current_case_folder
}

reconnect 5
adb -s ${IPADDRESS} root
sleep 5
reconnect 5
if [ `adb -s ${IPADDRESS} shell id|grep -c root` -eq 0 ];then
    echo "No root!!!"
    exit
fi
adb -s ${IPADDRESS} remount
adb -s ${IPADDRESS} push smoke.jar /data/local/tmp/
adb -s ${IPADDRESS} push shell/PullLog.sh /data/local/tmp/
adb -s ${IPADDRESS} push Resource/musicandvideo /sdcard/musicandvideo
adb -s ${IPADDRESS} push Resource/musicandvideo/testmusic/testmuiscamr.amr /sdcard/musicandvideo/
adb -s ${IPADDRESS} push Resource/musicandvideo/testmusic/testmuiscmp3.mp3 /sdcard/musicandvideo/
adb -s ${IPADDRESS} push Resource/musicandvideo/testmusic/testmuiscwma.wma /sdcard/musicandvideo/
adb -s ${IPADDRESS} push Resource/MMS/PythonCoder.png /sdcard/Pictures/
adb -s ${IPADDRESS} push shell/get_memcpu.sh /data/local/tmp/
adb -s ${IPADDRESS} push Resource /sdcard/Resource/
adb -s ${IPADDRESS} shell chmod 0777 /data/local/tmp/PullLog.sh
adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
adb -s ${IPADDRESS} push apk/Utf7Ime.apk /data/local/tmp
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/Utf7Ime.apk
adb -s ${IPADDRESS} push apk/filemanager.apk /data/local/tmp
adb -s ${IPADDRESS} shell pm install -r /data/local/tmp/filemanager.apk
adb -s ${IPADDRESS} push MCM/mcm.sh /data/local/tmp
adb -s ${IPADDRESS} shell setprop persist.sys.enable_live false
#adb -s ${IPADDRESS} shell sh /data/local/tmp/mcm.sh 10 1440 &
echo "sh /data/local/tmp/mcm.sh 10 1440 &" >test.txt
echo "exit" >>test.txt
adb -s ${IPADDRESS} shell <test.txt &
adb -s ${IPADDRESS} remount
result_folder=$2/Phone1
mkdir -p $result_folder
buildVersion="buildVersion=="`adb -s $IPADDRESS shell getprop ro.build.description`
buildDate="buildDate=="`adb -s $IPADDRESS shell getprop ro.build.date`
echo $buildVersion > $result_folder/phoneInfo.txt
echo $buildDate >> $result_folder/phoneInfo.txt
testStartTime="testStartTime=="`date '+%Y-%m-%d %H:%M:%S'`
testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
echo $testStartTime >> $result_folder/phoneInfo.txt
echo $testEndTime >> $result_folder/phoneInfo.txt
list=""
ci=0
globalvars=`awk -F ":" '{if(NF==2) a=a " -e " $1 " " $2 fi}END{print a}' ${DEVICE} `
case_no=0
echo "CASENO,CASENAME,TIME,BATTERY" >$result_folder/BatteryStatus.csv
for ((i=1;i<2;i++))
do
	
	for line in `cat caselist.txt`
	do
		case_no=$((case_no+1))
		testCase=`echo $line| awk -F "," '{print $1}'`
		case_name=`echo $line|awk -F# '{print $2}'|awk -F "," '{print $1}'`
		#case avgs
		case_avg=`echo $line|awk -F "," '{for(i=2;i<=NF;i++)a=a " -e " $i;print a}'|tr ":" " "`	
		current_case_folder=${case_name}_`date '+%Y%m%d_%H%M%S'`		
		adb -s ${IPADDRESS} shell rm -r /sdcard/AutoSmoke_UI30/* > /dev/null
		mkdir -p $result_folder/'LOOP'$i/$current_case_folder
		adb -s ${IPADDRESS} shell busybox pkill uiautomator
		reconnect 5
		adb -s ${IPADDRESS} shell busybox mkdir -p /sdcard/AutoSmoke_UI30/$current_case_folder
		adb -s ${IPADDRESS} shell "echo INSTRUMENTATION_STATUS: class=$line > /sdcard/case.log"
		adb -s ${IPADDRESS} logcat -c &
		adb -s ${IPADDRESS} logcat -b all -v time > $result_folder/'LOOP'$i/$current_case_folder/logcat.log &
		#adb -s ${IPADDRESS} wait-for-device
		batteryValue=`adb -s ${IPADDRESS} shell cat /sys/class/power_supply/battery/capacity`
		echo $case_no,${case_name},`date '+%H:%M'`,$batteryValue >> $result_folder/BatteryStatus.csv
		adb -s ${IPADDRESS} shell "uiautomator runtest smoke.jar -c $testCase --nohup -e disable_ime true $globalvars $case_avg -e caseFolder $current_case_folder >> sdcard/case.log"
		adb -s ${IPADDRESS} shell "cat /sdcard/case.log"
		waitUI
		adb -s ${IPADDRESS} shell mv /sdcard/case.log /sdcard/AutoSmoke_UI30/$current_case_folder/case.log
		adb -s ${IPADDRESS} pull /sdcard/AutoSmoke_UI30/$current_case_folder $result_folder/'LOOP'$i/$current_case_folder
		ci=`expr $ci + 1`
		adb -s ${IPADDRESS} shell rm -rf /sdcard/AutoSmoke_UI30/*
		ps aux | grep ${IPADDRESS} | grep logcat | cut -c 9-15 | xargs kill
		echo ====================================== $line ends ======================================
		#echo ==========================================================end========================================================== >> $log.log
		if [ `grep -c "FATAL EXCEPTION" $result_folder/'LOOP'$i/$current_case_folder/logcat.log` -ne 0 ];then
			echo ==========FC happend========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
			pullDropbox
		elif [ `grep -c "ANR in" $result_folder/'LOOP'$i/$current_case_folder/logcat.log` -ne 0 ];then
			echo ==========ANR happend========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
			pullDropbox
		elif [ `grep -c "Build fingerprint:" $result_folder/'LOOP'$i/$current_case_folder/logcat.log` -ne 0 ];then
			echo ==========Tombstone happend========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log		
			pullDropbox
		elif [ `grep -c "FAILURES" $result_folder/'LOOP'$i/$current_case_folder/case.log` -ne 0 ];then
			pullDropbox
		else
			echo ==========There are no error happend========== >> $result_folder/'LOOP'$i/$current_case_folder/case.log
		fi
		testEndTime="testEndTime=="`date '+%Y-%m-%d %H:%M:%S'`
		sed -i '$d' $result_folder/phoneInfo.txt
		echo $testEndTime >> $result_folder/phoneInfo.txt
		adb -s ${IPADDRESS} shell rm -rf /data/tombstones
		adb -s ${IPADDRESS} shell rm -rf /data/anr
	done
done

adb -s ${IPADDRESS} shell touch /data/local/tmp/stop_monitor
python parse.py $2
adb -s ${IPADDRESS} pull /sdcard/mcm_result $result_folder/mcm_result
cp -R MCM/HTML/MCM_HTML $result_folder/mcm_result/
bash MCM/HTML/output_unix.sh $result_folder/mcm_result
sleep 3
echo "***************************************"
pid=`awk -F "," '{print $1}' $result_folder/mcm_result/state.txt`
print $pid
adb -s ${IPADDRESS} shell kill -9 $pid
