#!/bin/bash

ERR_LOG_FILE=err_log.txt							# File to save the err logs

CHECK_LOG_V='============Log Compliance Analysis Tool v3==========='

line=''
date=''
time=''
pid=''
tid=''
pri=''

cur_line_no=0

regex_rule="[0-9][0-9]\-[0-9][0-9]\s\{1,\}[0-9][0-9]\:[0-9][0-9]:[0-9][0-9].[0-9]\{1,4\}\s\{1,\}[0-9]\{1,5\}\s\{1,\}[0-9]\{1,5\}\s\{1,\}[VDIWFE]"

function Help ()
{
	echo $CHECK_LOG_V
	echo 'Examples:                        '
	echo -e "\t$0 xxx.log     							"
	echo -e "\t$0 ./                       "
	echo -e "\t$0 dir                    "
	echo -e "Notes:\n\tLogs not compliant will be saved to err_log.txt"
	echo '==================================================='
}

function handle_err_log()
{
	line_msg=$cur_line_no":\t"$line
	echo -e $line_msg >> $ERR_LOG_FILE
}

#0 : Success
#1 : Failures
function check_log_file_name()
{
		file_full_name=$1
		
		ext=${file_full_name##*.}
		file_name=${file_full_name%.*}
		
		#echo "====$file_full_name, $file_name, $ext, ===="
		
		if [[ $ext == log ]]; then
				return 0
		fi
		
		return 1
}

function analyze_one_file_log()
{
			if [ $# -eq 0 ]; then
					echo -e "Please input log file.\n"
					exit 1
			fi
			
			if [ ! -f $1 ]; then
					echo -e "$1 is not a valid log file.\n"
					exit 1
			fi
	
			check_log_file_name $1			
			ret=$?
			
			if [[ $ret -ne 0 ]]; then
					echo -e "$1 is not a valid log file, a valid log file looks like xxx.log.\n"
					exit 1
			fi			
			
			###Now Start to analyze the log file
			
			echo -e "Start to analyze log file: $1"
			
			echo -e "Start to analyze log file: $1" >> $ERR_LOG_FILE
			
			cat $1 | grep -n -v -e "$regex_rule" >> $ERR_LOG_FILE
			
			echo -e "End of analyzing log file: $1\n" >> $ERR_LOG_FILE
			
			echo -e "End of analyzing log file: $1\n"
}


#Must have dir as input argument, the function
#will analyze the log files under this dir
function analyze_dir()
{
		if [ $# -eq 0 ]; then
				echo -e "Please input a direcoty.\n"
				exit 1
		fi
		
		if [ ! -d $1 ]; then
				echo -e "$1 is not a directory.\n"
				exit 1
		fi
		
		dir_name=$1
		
		#echo "dir_name: $dir_name"
		
		ls $dir_name"/"*.log >/dev/null 2>&1
		
		if [ $? -eq 0 ]; then
				for i in `ls $dir_name"/"*.log`	
				do							
							analyze_one_file_log $i							
				done				
		else
				echo -e "Can not find log file in $dir_name, nothing to do.\n"
		fi		
}

#####################Now Start#########################
if [ $# -eq 0 ]; then
		Help					
		exit 0
fi

echo -e "" > $ERR_LOG_FILE

echo $CHECK_LOG_V

echo -e "\n==================Analyze Logs for $1===============\n"

if [ -f $1 ]; then	
		analyze_one_file_log $1	
elif [ -d $1 ]; then
		analyze_dir $1		
else	
		echo "Error: $1 is not a directory or regular file"		
		exit 1
fi 	

echo -e "==================Finished Analyzing Logs for $1===============\n"




