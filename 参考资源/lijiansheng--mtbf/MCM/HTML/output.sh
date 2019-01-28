if [ $# -eq 0 ];then
	echo "No file path!!!Please input the result path."
	exit
fi

getsleep(){
sleep_t=`awk -F, 'NR==1{printf substr($1,6,length($1)-5)+0}' $1`
}

cpu(){
if [ -d $1/tmp_cpu ];then rm -r $1/tmp_cpu;fi
mkdir $1/tmp_cpu
awk -F, -v f1="$1/tmp_cpu/loop" -v f2="$1/tmp_cpu/time" -v f3="$1/tmp_cpu/activity" -v f4="$1/tmp_cpu/usr" -v f5="$1/tmp_cpu/sys" -v f6="$1/tmp_cpu/nic" -v f7="$1/tmp_cpu/idle" -v f8="$1/tmp_cpu/io" -v f9="$1/tmp_cpu/irq" -v f10="$1/tmp_cpu/sirq" -v f11="$1/tmp_cpu/map_times" -v f12="$1/tmp_cpu/data" -v t1="\"" -v t2="\":[" -v t3="]" -v t4="{" -v t5="}" '{if(NR==1){i=-1;l=1;s=substr($1,6,length($1)-5)+0}else{i+=1;if(i*s>=3600){i=0;l+=1;print t3 >>f1;print t3 >>f2;print t3 t5 >>f3;print t3 >>f4;print t3 >>f5;print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print t3 t5 >>f12};if(i==0){print "cpu hour: "l;printf t1"loop"t2 >>f1;printf t1"time"t2 >>f2;printf t4 t1"act"t2 >>f3;printf t1"usr"t2 >>f4;printf t1"sys"t2 >>f5;printf t1"nic"t2 >>f6;printf t1"idle"t2 >>f7;printf t1"io"t2 >>f8;printf t1"irq"t2 >>f9;printf t1"sirq"t2 >>f10;printf t4 t1"data_time"t2 >>f12};if(i>0){printf "," >>f1;printf "," >>f2;printf "," >>f3;printf "," >>f4;printf "," >>f5;printf "," >>f6;printf "," >>f7;printf "," >>f8;printf "," >>f9;printf "," >>f10;printf "," >>f12};printf $1*s >>f1;printf $2 >>f2;printf t1 $3 t1 >>f3;printf $4 >>f4;printf $5 >>f5;printf $6 >>f6;printf $7 >>f7;printf $8 >>f8;printf $9 >>f9;printf $10 >>f10;printf t1 $11 t1 >>f12}}END{print t3 >>f1;print t3 >>f2;print t3 t5>>f3;print t3 >>f4;print t3 >>f5;print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print l>f11;print t3 t5>>f12}' $1/$2
echo "{\"sleep\":$sleep_t,\"map_times\":`cat $1/tmp_cpu/map_times`}">>$1/MCM_HTML/json/avg.json
local i=1
local loop=`awk 'END{print NR}' $1/tmp_cpu/loop`
while [ $i -le $loop ];do
	echo "cpu out json: hour"$i
	if [ ! -d $1/MCM_HTML/json/hour_$i ];then
		mkdir $1/MCM_HTML/json/hour_$i
	fi
	awk -v a=$i 'NR==a{print $0}' $1/tmp_cpu/activity >$1/MCM_HTML/json/hour_$i/activity.json
	awk -v a=$i 'NR==a{print $0}' $1/tmp_cpu/data >$1/MCM_HTML/json/hour_$i/data.json
	echo -n "{" >$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/loop >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/time >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/usr >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/sys >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/nic >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/idle >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/io >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_cpu/irq >>$1/MCM_HTML/json/hour_$i/cpu.json
	awk -v a=$i 'NR==a{printf $0}' $1/tmp_cpu/sirq >>$1/MCM_HTML/json/hour_$i/cpu.json
	echo -n "}" >>$1/MCM_HTML/json/hour_$i/cpu.json
	local i=$((i+1))
done
rm -r $1/tmp_cpu
}

cpuinfo_out(){
if [ ! -d $1/$2 ];then mkdir $1/$2 ;fi
grep ",$4," $6|awk -F, -v f1="$1/$2/loop" -v f2="$1/$2/time" -v f3="$1/$2/avg" -v f4="$1/$2/cpuinfo" -v f5="$1/tmp_cpuinfo/maxcpu" -v t1="\"" -v t2="\":[" -v t3="]" -v t4="[" -v s=$sleep_t -v c="$3" -v name="cpuinfo$5" '{if($6!=""){z=t1 $6 t1}else{z="null"};if(NR==1){i=0;b=$1;t=$2;p=$3;h=$4;r=$4;l=sprintf("%.0f",$1*s/3600+1);if(l*3600-$1*s>3600){l=l-1};y=z}else{i+=1;if($1*s>=l*3600){i=0;print t3 >>f1;print t3 >>f2;print t3 >>f3;print t3 >>f4;print l","c","h","name >>f5;l=sprintf("%.0f",$1*s/3600+1);if(l*3600-$1*s>3600){l=l-1};h=$4}else{if($4>h){h=$4}};if($1==b){r=t4 $4",2,"$3 t3}else{if($3==p){r=$4}else{r=t4 $4",1" t3};if($1>b+1&&i!=0){printf "," b*s+1 "," $1*s-1>>f1;printf "," t+1 "," $2-1>>f2;printf "," y "," z>>f3;printf ",0,0">>f4};b=$1;t=$2;p=$3;y=z}};if(i==0){print "cpuinfo comand: "c" hour: "l;printf l";"t1"loop"t2 >>f1;printf t1"time"t2 >>f2;printf t1"avg"t2 >>f3;printf t1"cpu"t2 >>f4};if(i>0){printf "," >>f1;printf "," >>f2;printf "," >>f3;printf "," >>f4};printf $1*s >>f1;printf $2 >>f2;printf z >>f3;printf r >>f4}END{print t3 >>f1;print t3 >>f2;print t3 >>f3;print t3 >>f4;print l","c","h","name >>f5}'
local i=1
local loop=`awk 'END{print NR}' $1/$2/loop`
while [ $i -le $loop ];do
	local l=`awk -F";" -v a=$i 'NR==a{print $1}' $1/$2/loop`
	if [ ! -d $1/MCM_HTML/json/hour_$l ];then
		mkdir $1/MCM_HTML/json/hour_$l
	fi
	echo -n "{\"name\":\"$line\"," >$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	awk -F";" -v a=$i 'NR==a{printf $2","}' $1/$2/loop >>$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	awk -v a=$i 'NR==a{printf $0","}' $1/$2/time >>$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	awk -v a=$i 'NR==a{printf $0","}' $1/$2/avg >>$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	awk -v a=$i 'NR==a{printf $0}' $1/$2/cpuinfo >>$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	echo -n "}" >>$1/MCM_HTML/json/hour_$l/cpuinfo$5.json
	local i=$((i+1))
done
rm $1/$2/loop $1/$2/time $1/$2/avg $1/$2/cpuinfo
touch $1/$2/finish
}

cpuinfo(){
if [ -d $1/tmp_cpuinfo ];then rm -r $1/tmp_cpuinfo;fi
mkdir $1/tmp_cpuinfo
awk -F, '{if(NR>1)print $5}' $1/$2 >$1/tmp_cpuinfo/tmp.log
local n=0
local thead=1
local check=0
sort -u $1/tmp_cpuinfo/tmp.log|while read line
do
	echo "cpuinfo: $line"
	local n=$((n+1))
	local tmp=`echo $line|sed 's/\\[/\\\\[/g;s/\\]/\\\\]/g'`
	cpuinfo_out "$1" "/tmp_cpuinfo/thead_$thead" "$line" "$tmp" $n $1/$2 &
	if [ $thead -eq $thead_number ];then
		local check=1
	fi
	if [ $check -eq 1 ];then
		local a=0
		while true;do
			local a=$((a+1))
			if [ -f $1/tmp_cpuinfo/thead_$a/finish ];then
				rm $1/tmp_cpuinfo/thead_$a/finish
				local thead=$a
				break
			fi
			if [ $a -eq $thead_number ];then
				local a=0
			fi
			sleep 1
		done
	else
		local thead=$((thead+1))
	fi
done
wait
local i=1
local map_times=`sort -t, -k1 -nr $1/tmp_cpuinfo/maxcpu|awk -F, 'NR==1{print $1}'`
echo "cpuline: maxcpu"
echo "Hours,Process_Name,cpu%,json Name" >$1/maxcpu.csv
while [ $i -le $map_times ];do
	awk -F, -v a=$i '{if($1==a)print $0}' $1/tmp_cpuinfo/maxcpu|sort -t, -k3 -nr >$1/tmp_cpuinfo/tmp0.log
	echo -n "{\"maxcpu\":[" >$1/MCM_HTML/json/hour_$i/cpuline.json
	awk -F, -v b="[" -v e="]" -v t="\"" -v f="$1/MCM_HTML/json/hour_$i/cpuline.json" '{if(NR>1){printf "," >>f};printf b t$2t","$3","t$4t e >>f}' $1/tmp_cpuinfo/tmp0.log
	echo -n "]}" >>$1/MCM_HTML/json/hour_$i/cpuline.json
	cat $1/tmp_cpuinfo/tmp0.log >>$1/maxcpu.csv
	local i=$((i+1))
done
}

mem(){
if [ -d $1/tmp_mem ];then rm -r $1/tmp_mem ;fi
mkdir $1/tmp_mem
awk -F, -v f1="$1/tmp_mem/loop" -v f2="$1/tmp_mem/time" -v f3="$1/tmp_mem/FBC" -v f4="$1/tmp_mem/io" -v f5="$1/tmp_mem/Active" -v f6="$1/tmp_mem/Inactive" -v f7="$1/tmp_mem/Mapped" -v f8="$1/tmp_mem/Slab" -v f9="$1/tmp_mem/MemFree" -v f10="$1/tmp_mem/Buffers" -v f11="$1/tmp_mem/Cached" -v f12="$1/tmp_mem/A_anon" -v f13="$1/tmp_mem/I_anon" -v f14="$1/tmp_mem/A_file" -v f15="$1/tmp_mem/I_file" -v f16="$1/tmp_mem/Dirty" -v f17="$1/tmp_mem/Writeback" -v f18="$1/tmp_mem/CMA" -v t1="\"" -v t2="\":[" -v t3="]" '{if(NR==1){s=substr($1,6,length($1)-5)+0;i=-1;l=1}else{i+=1;if(i*s>=3600){i=0;l+=1;print t3 >>f1;print t3 >>f2;print t3 >>f3;print t3 >>f4;print t3 >>f5;print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print t3 >>f11;print t3 >>f12;print t3 >>f13;print t3 >>f14;print t3 >>f15;print t3 >>f16;print t3 >>f17;if(NF==15)print t3 >>f18};if(i==0){print "mem hour: "l;printf t1"loop"t2 >>f1;printf t1"time"t2 >>f2;printf t1"free"t2 >>f3;printf t1"io"t2 >>f4;printf t1"active"t2 >>f5;printf t1"inactive"t2 >>f6;printf t1"mapped"t2 >>f7;printf t1"slab"t2 >>f8;printf t1"memfree"t2 >>f9;printf t1"buffers"t2 >>f10;printf t1"cached"t2 >>f11;printf t1"active_a"t2 >>f12;printf t1"inactive_a"t2 >>f13;printf t1"active_f"t2 >>f14;printf t1"inactive_f"t2 >>f15;printf t1"dirty"t2 >>f16;printf t1"writeback"t2 >>f17;if(NF==15)printf t1"CMAFree"t2 >>f18};if(i>0){printf "," >>f1;printf "," >>f2;printf "," >>f3;printf "," >>f4;printf "," >>f5;printf "," >>f6;printf "," >>f7;printf "," >>f8;printf "," >>f9;printf "," >>f10;printf "," >>f11;printf "," >>f12;printf "," >>f13;printf "," >>f14;printf "," >>f15;printf "," >>f16;printf "," >>f17;if(NF==15)printf "," >>f18};printf (NR-2)*s >>f1;printf $1 >>f2;printf("%.2f",($2+$3+$4)/1024) >>f3;printf("%.2f",($11+$12)/1024) >>f4;printf("%.2f",$5/1024) >>f5;printf("%.2f",$6/1024) >>f6;printf("%.2f",$13/1024) >>f7;printf("%.2f",$14/1024) >>f8;printf("%.2f",$2/1024) >>f9;printf("%.2f",$3/1024) >>f10;printf("%.2f",$4/1024) >>f11;printf("%.2f",$7/1024) >>f12;printf("%.2f",$8/1024) >>f13;printf("%.2f",$9/1024) >>f14;printf("%.2f",$10/1024) >>f15;printf("%.2f",$11/1024) >>f16;printf("%.2f",$12/1024) >>f17;if(NF==15)printf("%.2f",$15/1024) >>f18}}END{print t3 >>f1;print t3 >>f2;print t3 >>f3;print t3 >>f4;print t3 >>f5;print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print t3 >>f11;print t3 >>f12;print t3 >>f13;print t3 >>f14;print t3 >>f15;print t3 >>f16;print t3 >>f17;if(NF==15)print t3 >>f18}' $1/$2
local i=1
local loop=`awk 'END{print NR}' $1/tmp_mem/loop`
while [ $i -le $loop ];do
	echo "mem out json: hour"$i
	if [ ! -d $1/MCM_HTML/json/hour_$i ];then
		mkdir $1/MCM_HTML/json/hour_$i
	fi
	echo -n "{" >$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/loop >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/time >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/FBC >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/io >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Active >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Inactive >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Mapped >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Slab >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/MemFree >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Buffers >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Cached >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/A_anon >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/I_anon >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/A_file >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/I_file >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0","}' $1/tmp_mem/Dirty >>$1/MCM_HTML/json/hour_$i/mem.json
	awk -v a=$i 'NR==a{printf $0}' $1/tmp_mem/Writeback >>$1/MCM_HTML/json/hour_$i/mem.json
	if [ -f $1/tmp_mem/CMA ];then
		awk -v a=$i 'NR==a{printf ","$0}' $1/tmp_mem/CMA >>$1/MCM_HTML/json/hour_$i/mem.json
	else
		echo -n ",\"CMAFree\":[\"NA\"]" >>$1/MCM_HTML/json/hour_$i/mem.json
	fi
	echo -n "}" >>$1/MCM_HTML/json/hour_$i/mem.json
	local i=$((i+1))
done
rm -r $1/tmp_mem
}

meminfo_out(){
if [ ! -d $1/$2 ];then mkdir $1/$2 ;fi
grep ",$4," $6 >$1/$2/tmp0.log
local type=`awk -F, 'NR==1{if($6==""){printf 0}else{if($6==0&&$7==0&&$8==0&&$9==0&&$10==0&&$11==0&&$12==0){printf 0}else{printf 1}}}' $1/$2/tmp0.log`
awk -F, -v f1="$1/$2/loop" -v f2="$1/$2/time" -v f3="$1/$2/avg" -v f4="$1/tmp_meminfo/maxmem" -v f5="$1/$2/pss" -v f6="$1/$2/NHS" -v f7="$1/$2/NHA" -v f8="$1/$2/NHF" -v f9="$1/$2/DHP" -v f10="$1/$2/DHS" -v f11="$1/$2/DHA" -v f12="$1/$2/DHF" -v t1="\"" -v t2="\":[" -v t3="]" -v t4="[" -v s=$sleep_t -v c="$3" -v type=$type -v name="meminfo$5" '{if($NF=="null"){z="null"}else{z=t1 $NF t1};r=sprintf("%.2f",$5/1024);if(type==1){u=sprintf("%.2f",$6/1024);v=sprintf("%.2f",$7/1024);w=sprintf("%.2f",$8/1024);d=sprintf("%.2f",$9/1024);e=sprintf("%.2f",$10/1024);f=sprintf("%.2f",$11/1024);g=sprintf("%.2f",$12/1024)};if(NR==1){i=0;m=$5;n=$5;l=sprintf("%.0f",$1*s/3600+1);if(l*3600-$1*s>3600){l=l-1};b=$1;t=$2;p=$3;y=z}else{i+=1;if($1*s>=l*3600){i=0;print t3 >>f1;print t3 >>f2;print t3 >>f3;print l","t1 c t1","m","m-n","name >>f4;print t3 >>f5;l=sprintf("%.0f",$1*s/3600+1);if(l*3600-$1*s>3600){l=l-1};m=$5;n=$5;if(type==1){print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print t3 >>f11;print t3 >>f12}}else{if($5>m)m=$5;if($5<n)n=$5};if($1==b){r=t4 r",2,"$3 t3;if(type==1){u=t4 u",2,"$3 t3;v=t4 v",2,"$3 t3;w=t4 w",2,"$3 t3;d=t4 d",2,"$3 t3;e=t4 e",2,"$3 t3;f=t4 f",2,"$3 t3;g=t4 g",2,"$3 t3}}else{if($3!=p){r=t4 r",1" t3;if(type==1){u=t4 u",1" t3;v=t4 v",1" t3;w=t4 w",1" t3;d=t4 d",1" t3;e=t4 e",1" t3;f=t4 f",1" t3;g=t4 g",1" t3}};if($1>b+1&&i!=0){printf "," b*s+1 "," $1*s-1>>f1;printf "," t+1 "," $2-1>>f2;printf "," y "," z>>f3;printf ",0,0">>f5;if(type==1){printf ",0,0">>f6;printf ",0,0">>f7;printf ",0,0">>f8;printf ",0,0">>f9;printf ",0,0">>f10;printf ",0,0">>f11;printf ",0,0">>f12}};b=$1;t=$2;p=$3;y=z}};if(i==0){print "meminfo comand: "c" hour: "l;printf l";"t1"loop"t2 >>f1;printf t1"time"t2 >>f2;printf t1"avg"t2 >>f3;printf t1"pss"t2 >>f5;if(type==1){printf t1"NHS"t2 >>f6;printf t1"NHA"t2 >>f7;printf t1"NHF"t2 >>f8;printf t1"DHP"t2 >>f9;printf t1"DHS"t2 >>f10;printf t1"DHA"t2 >>f11;printf t1"DHF"t2 >>f12}};if(i>0){printf "," >>f1;printf "," >>f2;printf "," >>f3;printf "," >>f5;if(type==1){printf "," >>f6;printf "," >>f7;printf "," >>f8;printf "," >>f9;printf "," >>f10;printf "," >>f11;printf "," >>f12}};printf $1*s >>f1;printf $2 >>f2;printf z >>f3;printf r >>f5;if(type==1){printf u >>f6;printf v >>f7;printf w >>f8;printf d >>f9;printf e >>f10;printf f >>f11;printf g >>f12}}END{print t3 >>f1;print t3 >>f2;print t3 >>f3;print l","t1 c t1","m","m-n","name >>f4;print t3 >>f5;if(type==1){print t3 >>f6;print t3 >>f7;print t3 >>f8;print t3 >>f9;print t3 >>f10;print t3 >>f11;print t3 >>f12}}' $1/$2/tmp0.log
local i=1
local loop=`awk 'END{print NR}' $1/$2/loop`
while [ $i -le $loop ];do
	local l=`awk -F";" -v a=$i 'NR==a{print $1}' $1/$2/loop`
	if [ ! -d $1/MCM_HTML/json/hour_$l ];then
		mkdir $1/MCM_HTML/json/hour_$l
	fi
	echo -n "{\"name\":\"$line\"," >$1/MCM_HTML/json/hour_$l/meminfo$n.json
	echo -n "\"type\":$type," >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	awk -F";" -v a=$i 'NR==a{printf $2","}' $1/$2/loop >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	awk -v a=$i 'NR==a{printf $0","}' $1/$2/time >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	awk -v a=$i 'NR==a{printf $0","}' $1/$2/avg >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	awk -v a=$i 'NR==a{printf $0}' $1/$2/pss >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	if [ $type -eq 1 ];then
		echo -n "," >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/NHS >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/NHA >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/NHF >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/DHP >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/DHS >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0","}' $1/$2/DHA >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
		awk -v a=$i 'NR==a{printf $0}' $1/$2/DHF >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	fi
	echo -n "}" >>$1/MCM_HTML/json/hour_$l/meminfo$n.json
	local i=$((i+1))
done
rm $1/$2/loop $1/$2/time $1/$2/avg $1/$2/pss $1/$2/tmp0.log
if [ $type -eq 1 ];then
	rm $1/$2/NHS $1/$2/NHA $1/$2/NHF $1/$2/DHP $1/$2/DHS $1/$2/DHA $1/$2/DHF 
fi
touch $1/$2/finish
}

meminfo(){
if [ -d $1/tmp_meminfo ];then rm -r $1/tmp_meminfo ;fi
mkdir $1/tmp_meminfo
awk -F, '{if(NR>1)print $4}' $1/$2 >$1/tmp_meminfo/tmp.log
local n=0
local thead=1
local check=0
sort -u $1/tmp_meminfo/tmp.log|while read line
do
	echo "meminfo:$line"
	local n=$((n+1))
	local tmp=`echo $line|sed 's/\\[/\\\\[/g;s/\\]/\\\\]/g'`
	meminfo_out "$1" "/tmp_meminfo/thead_$thead" "$line" "$tmp" $n $1/$2 &
	if [ $thead -eq $thead_number ];then
		local check=1
	fi
	if [ $check -eq 1 ];then
		local a=0
		while true;do
			local a=$((a+1))
			if [ -f $1/tmp_meminfo/thead_$a/finish ];then
				rm $1/tmp_meminfo/thead_$a/finish
				local thead=$a
				break
			fi
			if [ $a -eq $thead_number ];then
				local a=0
			fi
			sleep 1
		done
	else
		local thead=$((thead+1))
	fi
done
wait
local i=1
local map_times=`sort -t, -k1 -nr $1/tmp_meminfo/maxmem|awk -F, 'NR==1{print $1}'`
echo "memline: maxmem"
echo "Hours,Process_Name,Pss(k),Pss Difference(k),json Name" >$1/maxmem.csv
while [ $i -le $map_times ];do
	echo "pssline: maxPss; hour$i"
	awk -F, -v a=$i '{if($1==a)print $0}' $1/tmp_meminfo/maxmem|sort -t, -k3 -nr >$1/tmp_meminfo/tmp0.log
	echo -n "{\"maxpss\":[" >$1/MCM_HTML/json/hour_$i/pssline.json
	awk -F, -v b="[" -v e="]" -v t="\"" -v f="$1/MCM_HTML/json/hour_$i/pssline.json" '{if(NR>1){printf "," >>f};printf b $2","sprintf("%.2f",$3/1024)","t$5t e >>f}' $1/tmp_meminfo/tmp0.log
	echo -n "]}" >>$1/MCM_HTML/json/hour_$i/pssline.json
	cat $1/tmp_meminfo/tmp0.log|tr -d "\"" >>$1/maxmem.csv
	echo "pdline: maxPD; hour$i"
	sort -t, -k4 -nr $1/tmp_meminfo/tmp0.log >$1/tmp_meminfo/tmp.log
	echo -n "{\"maxPD\":[" >$1/MCM_HTML/json/hour_$i/pdline.json
	awk -F, -v b="[" -v e="]" -v t="\"" -v f="$1/MCM_HTML/json/hour_$i/pdline.json" '{if(NR>1){printf "," >>f};printf b $2","sprintf("%.2f",$4/1024)","t$5t e >>f}' $1/tmp_meminfo/tmp.log
	echo -n "]}" >>$1/MCM_HTML/json/hour_$i/pdline.json
	local i=$((i+1))
done
rm $1/tmp_meminfo/maxmem $1/tmp_meminfo/tmp.log $1/tmp_meminfo/tmp0.log
}

#main
thead_number=10
if [ ! -d $1/MCM_HTML ];then
	cp -r MCM_HTML $1/
fi
if [ -d $1/MCM_HTML/json ];then
	rm -r $1/MCM_HTML/json
fi
mkdir $1/MCM_HTML/json
getsleep $1/cpu.csv
echo "!!!!!!!!!!cpuinfo!!!!!!!!!!"
cpuinfo "$1" "cpuinfo.csv"
echo "!!!!!!!!!!meminfo!!!!!!!!!!"
meminfo "$1" "meminfo.csv"
echo "!!!!!!!!!!cpu!!!!!!!!!!"
cpu "$1" "cpu.csv" &
echo "!!!!!!!!!!mem!!!!!!!!!!"
mem "$1" "mem.csv"
wait
rm -r $1/tmp_cpuinfo $1/tmp_meminfo
echo "Finish"