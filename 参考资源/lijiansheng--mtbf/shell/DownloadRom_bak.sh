#!/bin/bash
HOST=10.150.140.91/share
FOLDER=dailybuild/mtk-s1
findSubFolder(){
	if [ -n "$2" ];then
		echo "$1"|awk -v a=$2 'BEFIN{r=0;b=0}{if(NF==8&&$2!="blocks"&&$1==a){print $1;b=1;exit};if(NF==8&&$2!="blocks"&&$1!=a&&$1~/^.*([0-9])+$/&&$1>r)r=$1}END{if(b==0)print r}'
	else
		echo "$1"|awk 'BEFIN{r=0;b=0}{if(NF==8&&$2!="blocks"&&$1~/^.*([0-9])+$/&&$1>r)r=$1}END{print r}'
	fi
}

findSubFolderEndswith(){
	echo "$1"|awk -v a=$2 '$1 ~ /a$/ { print $1 }'
}

help(){
	echo "Usage:"
	echo "	-s: specify which release will be download"
	echo "	    if not provide this option, the latest one will be choiced."
	exit -1
}
# parse all args
while echo $1 | grep -q ^-; do
    eval $( echo $1 | sed 's/^-//' )=$2
    shift
    shift
done

#To get the latest release folder, we need to access this block twice.
#in the first loop, $FOLDER became dailybuild/max1/20141211
#second loop, $FOLDER became dailybuild/max1/20141211/max1_20141211_114332
i=0
while ((i<1))
do
	# get the latest release root folder
	RESULT=`smbclient //${HOST} -c "ls ${FOLDER}/*" -N 2>&1`
	if [[ $! -ne 0 ]];then
		echo "Error: Unreachable location, can't fetch release list.";
		exit -1
	fi

	if [ -n "$s" ];then
		
		SUBFOLDER=`findSubFolder "$RESULT" "$s"`
	else
		SUBFOLDER=`findSubFolder "$RESULT"`
	fi
	FOLDER=$FOLDER/$SUBFOLDER/full_x600
	echo $SUBFOLDER
	let ++i
	
done

SUBFOLDER=`smbclient //${HOST} -c "ls ${FOLDER}/*" -N 2>&1|awk '$1 ~ /open_userdebug$/ { print $1 }'`
echo $SUBFOLDER

mkdir $SUBFOLDER
cd $SUBFOLDER
FOLDER=$FOLDER/$SUBFOLDER/img
smbclient //10.150.140.91/share -c "cd ${FOLDER};recurse;prompt;mget *" -N
cd ..



