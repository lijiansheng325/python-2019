#!/bin/bash

DATE_CMD_NS="date +%Y.%m.%d.%k.%M.%S.%N"

function mainFunction()
{
    echo `${DATE_CMD_NS}`
    echo "Time,  core_temperature, Board Temperature, Fan-speed"
    while true;
    do
        STR=`${DATE_CMD_NS}`
		STR+=/`adb shell mcu_client core_temperature |awk '{ print "Core " $2 "℃ " }'`
		STR+=/`adb shell mcu_client board_temperature |awk '{ print "Board " $2 "℃ " }'`
		STR+=/`adb shell mcu_client fan1_speed |awk '{ print $2 " " $3 }'`
		echo $STR 2>/dev/null &
        sleep 2
        wait
    done
}

mainFunction
