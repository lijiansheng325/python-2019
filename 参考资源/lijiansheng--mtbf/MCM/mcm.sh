#!/system/bin/sh

date_now(){
day=`date +%Y/%m/%d`
time=`date +%H:%M:%S`
time_name=`date +%Y%m%d_%H%M%S`
}

getmem_pid(){
if [ -d /proc/$1 ];then
	local pss=`$su dumpsys meminfo $1|busybox awk 'BEGIN{t=0}{if($1=="Native"){n=n+$(NF-2);o=o+$(NF-1);p=p+$NF}else{if($1=="Dalvik"&&NF>6){d=d+$(NF-2);e=e+$(NF-1);f=f+$NF;g=g+$(NF-6)}else{if($1=="TOTAL"){t=$2;print $2","n","o","p","d","e","f","g;exit}}}}END{if(t==0)print "no"}'`
	if [ "$pss" == "no" ];then
		local pss=`$su cat /proc/$1/smaps|grep Pss|busybox awk 'BEGIN{a=0}{a=a+$2}END{if(a!=0) print a",,,,,,,";else print a}'`
	fi
	if [ $pss"a" != "0a" ];then
		local get_t=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
		echo "$3,$get_t,$1,$2,$pss,$4" >>$testresult/meminfo.csv
	fi
fi
}
get_package(){
local check=`/system/bin/ps|grep -E "$packages"`
if [ ! -z "$check" ];then
	echo "$p_check"|while read p;do
		echo "$check"|busybox awk -v package="$p" '{if($NF==package)print $2" "$NF}END{print 0" "0}'|while read l;do
			local pid=`echo $l|busybox awk '{print $1}'`
			local command=`echo $l|busybox awk '{print $2}'`
			if [ $pid -ne 0 ];then
				if [ -f /proc/$pid/cmdline ];then
					local avg=`cat /proc/$pid/cmdline|busybox awk 'BEGIN{r="null"}{if(NR>1){if(NR==2)r=$0;else r=r" "$0}}END{print r}'`
					if [ -z `echo $avg|busybox tr -d " "` ];then
						local avg="null"
					fi
					getmem_pid $pid $command $1 "$avg" &
				fi
				t=$((t+1))
				if [ $t -eq $2 ];then
					wait
					t=0
				fi
			else
				wait
			fi
		done
	done
fi
}
get_meminfo(){
/system/bin/ps|busybox awk '{if(NR>1&&$5>0&&$NF!="ps"&&$NF!="grep"&&$NF!="busybox"&&$NF!="sh"&&$NF!="dumpsys")print $2" "$NF}END{print 0" "0}'|while read l;do
	local pid=`echo $l|busybox awk '{print $1}'`
	local command=`echo $l|busybox awk '{print $2}'`
	if [ $pid -ne 0 ];then
		if [ -f /proc/$pid/cmdline ];then
			local avg=`cat /proc/$pid/cmdline|busybox awk 'BEGIN{r="null"}{if(NR>1){if(NR==2)r=$0;else r=r" "$0}}END{print r}'`
			if [ -z `echo $avg|busybox tr -d " "` ];then
				local avg="null"
			fi
			getmem_pid $pid $command $1 "$avg" &
		fi
		t=$((t+1))
		if [ $t -eq $2 ];then
			wait
			t=0
		fi
	else
		wait
	fi
done
}

getmem(){
local get_t=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
local info=`cat /proc/meminfo|busybox awk 'BEGIN{r=0}{if($1=="MemFree:"){a=$2};if($1=="Buffers:"){b=$2};if($1=="Cached:"){c=$2};if($1=="Active:"){e=$2};if($1=="Inactive:"){f=$2};if($1=="Active(anon):"){g=$2};if($1=="Inactive(anon):"){h=$2};if($1=="Active(file):"){i=$2};if($1=="Inactive(file):"){j=$2};if($1=="Dirty:"){k=$2};if($1=="Writeback:"){l=$2};if($1=="Mapped:"){m=$2};if($1=="Slab:"){n=$2};if($1=="CMA"&&$2=="Free:"){r=1;a=a-$3;o=$3}}END{if(r==0) print a","b","c","e","f","g","h","i","j","k","l","m","n;else print a","b","c","e","f","g","h","i","j","k","l","m","n","o}'`
echo "$get_t,$info" >>$testresult/mem.csv
}

getcpu(){
local get_t=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
local activity=`$su dumpsys window w|grep mFocusedApp|busybox awk '{print $NF}'|busybox tr -d '}'`
local data_t=`date +%Y/%m/%d" "%H:%M:%S`
busybox top -b -n 1 >/data/local/tmp/busybox_top.log &
wait
local tmp=`busybox sed 's/%//g;s/\.0//g;s/S </S</g;s/R </R</g;s/D </D</g;s/{main}//g;s/[0-9]m[0-9]/m /g;s/}//g;s/ th\\]/_th\\]/g;s/\\[mtk /\\[mtk_/g' /data/local/tmp/busybox_top.log|busybox awk -v data="$data_t" -v loop=$1 -v time=$get_t -v act=$activity -v csv="$testresult/cpu.csv" -v cpu=$2 '{if(NR==2) print loop","time","act","$2","$4","$6","$8","$10","$12","$14","data >>csv;if(NR>4&&$(cpu+1)!="busybox"&&$(cpu+1)!="/system/bin/sh"){if($cpu=="0") exit;if(NF==cpu+1){r=$(cpu+1)}else{r=$(cpu+1)"{"$(cpu+2);if(NF>(cpu+2))for(i=(cpu+3);i<=NF;i++)r=r" "$i};print loop","time","$1","$cpu","r}}'`
echo "$tmp"|busybox awk -F"{" '{if(NF==3)print $1 $3","$2;else if(NF==2){print $1","$2}else{if($0!="")print $0","}}' >>$testresult/cpuinfo.csv
}

if [ $# -lt 2 ];then
	packages="All"
    exit
elif [ $# -eq 3 ];then
	packages="$3"
	p_check=`echo "$3"|busybox sed 's/|/\n/g'`
fi
testresult="$EXTERNAL_STORAGE/mcm_result"
if [ -f $testresult/state.txt ];then
	pid=`busybox awk -F "," '{print $1}' $testresult/state.txt`
	if [ -f /proc/$pid/cmdline ];then
		if [ `cat /proc/$pid/cmdline|busybox awk 'NR==1{print $1}'`"a" == "sha" ];then
			exit
		fi
	fi
fi
if [ ! -d $testresult ];then
	mkdir $testresult
else
    rm -r $testresult
	mkdir $testresult
fi
check_su=`su -c id|grep -c root`
if [ $check_su -eq 0 ];then
	su=""
	check_su=`id|grep -c root`
	if [ $check_su -eq 0 ];then
		touch $testresult/no_su_exit
		exit
	fi
else
	su="su -k"
fi

date_now
mac=`cat /sys/class/net/*/address|busybox sed -n '1p'|busybox tr -d ':'`
model=`getprop ro.product.model|busybox sed 's/ /_/g'`
build=`getprop ro.build.fingerprint`
if [ -z $build ];then
	build=`getprop ro.build.description`
fi
start_time="$day $time"
start_s=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
echo "$$,$1,0/$2,$model-$mac,$start_time,$start_s,$start_s,$build,$packages" >$testresult/state.txt
echo "Loop:$1,Time,Activity,usr,sys,nic,idle,io,irq,sirq,Data Time" >$testresult/cpu.csv
echo "Loop:$1,Time,PID,%CPU,Command,Thread/avgs" >$testresult/cpuinfo.csv
if [ `cat /proc/meminfo|grep -c "CMA Free"` -eq 0 ];then
	echo "Time:$1,MemFree,Buffers,Cached,Active,Inactive,Active(anon),Inactive(anon),Active(file),Inactive(file),Dirty,Writeback,Mapped,Slab" >$testresult/mem.csv
else
	echo "Time:$1,MemFree,Buffers,Cached,Active,Inactive,Active(anon),Inactive(anon),Active(file),Inactive(file),Dirty,Writeback,Mapped,Slab,CMA Free" >$testresult/mem.csv
fi
echo "Loop:$1,Time,PID,Process_Name,Pss,Native_Heap(Size),Native_Heap(Alloc),Native_Heap(Free),Dalvik_Heap(Size),Dalvik_Heap(Alloc),Dalvik_Heap(Free),Dalvik_Pss,Avgs" >$testresult/meminfo.csv
busybox top -b -n 1 >/data/local/tmp/busybox_top.log &
wait
cpu_p=`busybox awk 'NR==4{print NF-1}' /data/local/tmp/busybox_top.log`
loop=0
while [ $loop != $2 ]
do
	start_second=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
	getcpu $loop $cpu_p
	getmem $loop
	if [ $# -eq 2 ];then
		get_meminfo $loop 5
	elif [ $# -eq 3 ];then
		get_package $loop 5
	fi
	end_second=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
	use_second=$((end_second-start_second))
	echo Use second: $use_second
	if [ $use_second -lt $1 ];then
		sleep $(($1-use_second))
	fi
	loop=$((loop+1))
	end_second=`busybox awk -F. 'NR==1{print $1}' /proc/uptime`
	echo "$$,$1,$loop/$2,$model-$mac,$start_time,$start_s,$end_second,$build,$packages" >$testresult/state.txt
done
