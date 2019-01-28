#!/bin/bash

# Version: 2017.04.14

############ BEGIN Adjustable Parameters ############
# How many seconds you refresh data
SLEEP_SECONDS=3
# ADB Device Serial Number
ADB_SN=""
# How many seconds you check for /proc/stat change
CPU_STAT_SECONDS=1
#QCOM S820A CPU Temp Sensors
TSENSOR_LIST="0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19"
############ END Adjustable Parameters ############

DATE_CMD="date +%Y.%m.%d.%k.%M.%S"
DATE_CMD_NS="date +%Y.%m.%d.%k.%M.%S.%N"
ADB_CMD="adb ${ADB_SN}"
ADB_ROOT_SHELL_CMD="adb ${ADB_SN} shell"
STR=""
MEM_TOTAL=`${ADB_ROOT_SHELL_CMD} cat /proc/meminfo |grep MemTotal |awk '{ print $2*0.01 }'`

function lockCpuGpuFreq()
{
    local TMP_FILE=_tmp_lock_freq_file
    echo performance>${TMP_FILE}
    sh -c "${ADB_CMD} push ${TMP_FILE} /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor" 1>&2
    sh -c "${ADB_CMD} push ${TMP_FILE} /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor" 1>&2
    sh -c "${ADB_CMD} push ${TMP_FILE} /sys/devices/system/cpu/cpu2/cpufreq/scaling_governor" 1>&2
    sh -c "${ADB_CMD} push ${TMP_FILE} /sys/devices/system/cpu/cpu3/cpufreq/scaling_governor" 1>&2
    sh -c "${ADB_CMD} push ${TMP_FILE} /sys/kernel/gpu/gpu_governor" 1>&2
    rm ${TMP_FILE}
}

function calcTemperature()
{
    local TCNT=$#
    local TSUM=0
    local TVAL=0
    while [ ! -z "${1}" ]; do
        TVAL=`${ADB_ROOT_SHELL_CMD} cat /sys/devices/virtual/thermal/thermal_zone${1}/temp`
        TSUM=`echo ${TSUM} ${TVAL} | awk '{ print (($1+$2)) }'`
        shift 1
    done
    STR+=,`echo ${TSUM} ${TCNT} |awk '{ print (($1*0.1/$2)) }'`
}

function calcCpuRateObsoleted()
{
    STR+=,`${ADB_ROOT_SHELL_CMD} top -n 2| grep -w IOW | tail -2 | head -1 | sed 's/%/ /g' |awk '{ print (($2+$5+$8+$11)) }'`
}

function calcCpuRate()
{
    local T_STR=`${ADB_ROOT_SHELL_CMD} "head -1 /proc/stat && sleep ${CPU_STAT_SECONDS} && head -1 /proc/stat"`
    local IDLE_HZ=`echo ${T_STR} |awk '{ print (($16-$5))}'`
    local BUSY_HZ=`echo ${T_STR} |awk '{ print (($13-$2+$14-$3+$15-$4+$17-$6+$18-$7+$19-$8)) }'`
    STR+=,`echo ${BUSY_HZ} ${IDLE_HZ} |awk '{ print (($1*100/(($1+$2)))) }'`
}

function calcGpuRate()
{
    STR+=,`${ADB_ROOT_SHELL_CMD} cat /sys/kernel/gpu/gpu_busy |awk '{ print $1 }'`
}

function calcMemAvailable()
{
    local MEM_AVAILABLE=`${ADB_ROOT_SHELL_CMD} cat /proc/meminfo |grep MemAvailable |awk '{ print $2 }'`
    STR+=,`echo ${MEM_AVAILABLE} ${MEM_TOTAL} | awk '{ print ((100-$1/$2)) }'`
}

function calcRunningProcessesAndLastMinLoadAvg()
{
    STR+=,`${ADB_ROOT_SHELL_CMD} cat /proc/loadavg |sed 's/\// /g' |awk '{ print $4 "," $1 }'`
}

function loopOnce()
{
    STR=`${DATE_CMD}`
    calcTemperature ${TSENSOR_LIST}
    calcCpuRate
    calcGpuRate
    calcMemAvailable
    calcRunningProcessesAndLastMinLoadAvg
    echo $STR
}

function calcCpuRateUbuntu()
{
    STR+=`top -n 1 |grep -w "%Cpu" |awk '{ print (($2+$4+$6+$10+$12+$14)) }'`
}

function mainFunction()
{
    ${ADB_CMD} root 2>&1 >/dev/null
    if [ -z "`date +%N | grep N`" ]; then
        DATE_CMD=${DATE_CMD_NS}
    fi
    lockCpuGpuFreq 2>/dev/null
    echo "Check Point,Board Temperature,CPU%,GPU%,Memory%,Running processes,Last Minute LoadAvg"
    while true;
    do
        loopOnce 2>/dev/null &
        sleep ${SLEEP_SECONDS}
        wait
    done
}

mainFunction
