#!/system/bin/sh

#检测su
check_su=`ls /system/xbin/|busybox grep -c -w su`
if [ $check_su -eq 0 ];then
	su=""
else
	su="su -k"
fi
if [ $# -ne 1 ];then
    echo "No avg!!!"
    exit
fi

if [ -f $EXTERNAL_STORAGE/Pss_Cpu/State.txt ];then
	pid=`busybox awk -F "," '{print $1}' $EXTERNAL_STORAGE/Pss_Cpu/State.txt`
	name=`/system/bin/ps $((pid))|busybox awk 'END{print $NF}'`
	if [ $name"a" == "sha" ];then
		kill $((pid))
		echo "Killed the running script."
	fi
fi
if [ -f /data/local/tmp/stop_monitor ];then
	rm /data/local/tmp/stop_monitor
fi
#结果保存文件夹根据需求调整
testresult="$EXTERNAL_STORAGE/Pss_Cpu"
if [ ! -d $testresult ];then
	mkdir $testresult
else
    rm -r $testresult
	mkdir $testresult
fi

echo "$$,0,0,0,0,0" >$testresult/State.txt

date_now(){
day=`date +%Y/%m/%d`
time=`date +%H:%M:%S`
time_name=`date +%Y%m%d_%H%M%S`
}

#需要一个参数，second：第一列序列时间
get_meminfo(){
date_now
fg=`$su dumpsys activity|grep "Recent #0"|busybox awk '{print $7}'|busybox tr -d "}"`
tmp=`$su procrank`
local a=1
while [ $a -ne 0 ];do
	local w=`echo "$tmp"|grep -c "warning"`
	if [ $w -ne 0 ];then
		local w_pid=`echo "$tmp"|grep "warning"|busybox awk '{print $7";"}'`
		local w_pid=`echo $w_pid`
		date_now
		fg=`$su dumpsys activity|grep "Recent #0"|busybox awk '{print $7}'|busybox tr -d "}"`
		tmp=`$su procrank`
		local a=$((a+1))
		echo "$day $time procrank获取结果中有warning(进程：$w_pid时间点：$1;当前前台进程：$fg)" >>$testresult/procrank_error.log
		if [ $a -eq 3 ];then
			echo "$day $time 重试3次仍旧存在warning，停止重试)" >>$testresult/procrank_error.log
			local a=0
		fi
	else
		local a=0
	fi
done
if [ ! -f $testresult/procrank.csv ];then
	echo "Second,PID,Pss,cmdline,Process_state" >$testresult/procrank.csv
fi
if [ ! -f $testresult/freemem.csv ];then
	echo "Second,Time,free,buffers,cached,freemem,case" >$testresult/freemem.csv
fi
if [ -d /sdcard/AutoSmoke_UI30 ];then
	local case=`ls /sdcard/AutoSmoke_UI30/`
else
	local case="NA"
fi
echo "$tmp"|busybox awk -v s=$1 -v t="$day $time" -v f=$fg -v z=$case -v csv1="$testresult/procrank.csv" -v csv2="$testresult/freemem.csv" -v txt="$testresult/cmdline.txt" '{if(NF==8&&$1!="PID"){l=l+1;if(l<6){print $8>>txt};if($8==f){c="fp"}else{c="bp"};print s","$1","substr($4,1,length($4)-1)","$8","c >>csv1}else{if(NF==13){print s","t","substr($4,1,length($4)-1)","substr($6,1,length($6)-1)","substr($8,1,length($8)-1)","substr($4,1,length($4)-1)+substr($6,1,length($6)-1)+substr($8,1,length($8)-1)+0","z >>csv2}}}' 
local txt=`cat $testresult/cmdline.txt|busybox sort|busybox uniq`
echo "$txt" >$testresult/cmdline.txt
}

#需要一个参数，second：第一列序列时间
get_cpuinfo(){
if [ ! -f $testresult/cpu.csv ];then
	echo "Second,User,System,IOW,IRQ" >$testresult/cpu.csv
fi
if [ ! -f $testresult/top.csv ];then
	echo "Second,PID,CPU%,cmdline" >$testresult/top.csv
fi
/system/bin/top -m 5 -n 1|busybox awk -v s=$1 -v csv1="$testresult/cpu.csv" -v csv2="$testresult/top.csv" -v txt="$testresult/name.txt" '{if(NF==8){print s","$2$4$6$8 >>csv1}else{if(NF!=0&&NF!=22&&$1!="PID"){print s","$1","$3","$NF >>csv2;print $NF >>txt}}}'
local txt=`cat $testresult/name.txt|busybox sort|busybox uniq`
echo "$txt" >$testresult/name.txt
}

a=0
date_now
monitor_start_time="$day $time"
start_s=`date +%s`
while true;do
	start_second=`date +%s`
	Second=$(($1*$a))
	date_now
	get_meminfo $Second
	get_cpuinfo $Second
	end_second=`date +%s`
	use_second=$((end_second-start_second))
	if [ -f /data/local/tmp/stop_monitor ];then
		exit
	fi
	if [ $use_second -lt $1 ];then
		sleep $(($1-use_second))
	fi
	a=$((a+1))
	echo "$$,$monitor_start_time,$start_s,$1,$a,$end_second" >$testresult/State.txt
done
