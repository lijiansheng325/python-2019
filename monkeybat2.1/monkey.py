#coding=GBK
## function: remove file 
## remark: python version 2-7-3
import os
import sys
import datetime
import time
import platform
import subprocess
import shutil
ANR_PATH = "ANR"
SDCARD_SEMS_PATH = "SDCARD_SEM"
SDCARD_LOGS_PATH = "SDCARD_LOG"
DROPBOX_PATH = "DROP_BOX"
TOMBSTONES_PATH = "TOMB_STONE"

ANR_CMD = "adb pull /data/anr "
SDCARD_SEMS_CMD = "adb pull /sdcard/sems "
SDCARD_LOGS_CMD = "adb pull /sdcard/logs "
DROPBOX_CMD = "adb pull /data/system/dropbox "
TOMBSTONES_CMD = "adb pull /data/tombstones "


PUSH_WHITHBLACK = 'adb push WhiteBlack.txt /data/local/tmp/'
MONKEY_CMD_ZJ = 'adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-blacklist-file /data/local/tmp/WhiteBlack.txt -v -v  576000 > MONKEY_ZJ.log'
MONKEY_CMD_MD = 'adb shell monkey --throttle 1000 -s 14041 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-whitelist-file /data/local/tmp/WhiteBlack.txt -v -v 1000 > MONKEY_MD.log'
KMSG_CMD = 'adb shell cat /proc/kmsg > KMSG.log'
PYTHON_other_CMD = 'python log_parser_runner.py -a 5 -b 5 -c 1 -o LOGPARSER_Report -s 10000'

def LOG_creat(cmd,txtname):
    data=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    txtname = txtname
    for line in data.stdout.readline():
        filepath = os.path.join('.' + os.sep, txtname)
        fd = open(filepath,'a')
        fd.write(line)
        fd.close()
def file_exist(filename):
    if os.path.exists(filename):
        message = 'OK, the "%s" file exists.'
        os.remove(filename)
    else:
        return 0

cmd1 = "adb shell pm list packages -f" 
cmd2 = "adb shell pm list packages"
txtname1 = "package&apk.txt"
txtname2 = "package.txt"
sep1 = '/'
sep2 = ':'
def package(cmd,txtname,sep):
    data=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    for line in data.stdout.readlines():
        line_list = line.rsplit(sep,1)
        fd=open(txtname,"a")
        fd.write(line_list[1])
        fd.close()
 

def TestPlatform():
    print ("----------Operation System--------------------------")
    #Windows will be : (32bit, WindowsPE)
    #Linux will be : (32bit, ELF)
    print(platform.architecture())

    #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
    #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
    print(platform.platform())

    #Windows will be : Windows
    #Linux will be : Linux
    print(platform.system())

    print ("--------------Python Version-------------------------")
    #Windows and Linux will be : 3.1.1 or 3.1.3
    print(platform.python_version())

def UsePlatform():
    sysstr = platform.system()
    if(sysstr == "Windows"):
        print "Call Windows tasks"
    elif(sysstr == "Linux"):
        print "Call Linux tasks"
    else:
        print "Other System tasks"
    

def cur_file_dir():
    
    path = sys.path[0]
     
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)



def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.exists(path):
            # We are nearly safe
            pass
        else:
            # There was an error on creation, so make sure we know about it
            raise

def call_adb_pull_to_file(adb_shell_cmd, path, sub_path):
    path_name = os.path.join(path, sub_path)
    #print path_name
    make_sure_path_exists(path_name)
    os.system(adb_shell_cmd + ' ' + path_name)
    time.sleep(2)

def get_device_info():
    try:
        
        call_adb_pull_to_file(ANR_CMD, path_time, ANR_PATH)
        call_adb_pull_to_file(SDCARD_SEMS_CMD, path_time, SDCARD_SEMS_PATH)
        call_adb_pull_to_file(SDCARD_LOGS_CMD, path_time, SDCARD_LOGS_PATH)
        call_adb_pull_to_file(DROPBOX_CMD, path_time, DROPBOX_PATH)
        call_adb_pull_to_file(TOMBSTONES_CMD, path_time, TOMBSTONES_PATH)
    
    except Exception,e:
        print str(e)


def kill_logcat():
    os.system('adb  shell busybox pkill logcat')
# kill monkey
def kill_monkey():
    os.system('adb  shell busybox pkill com.android.commands.monkey')
#get_device_info()

UsePlatform()
print("Python Version is " + platform.python_version())

os.system('adb wait-for-device && adb root')
time.sleep(5)
os.system('adb wait-for-device && adb remount')

kill_logcat()
kill_monkey()
file_exist('package&apk.txt')
file_exist('package.txt')
package(cmd1,txtname1,sep1)
package(cmd2,txtname2,sep2) 

print '*'*70
print ' Package list have been generated in package.txt\n To run a partial test based on whitelist, please add package names into WhiteBlack.txt'
print ' To run a full test, please add excluding package names into WhiteBlack.txt.WhiteBlack.txt can be empty by default.\n Monkey can identify Black and white list by  parameter'
print ' WhiteBlack.txt is  ready, please input < ok > to continue\n'
print '*'*70
LIST_PACKAGE = raw_input() 
if LIST_PACKAGE == str('ok'):
    pass
else:
    print 'Input error'
    sys.exit()
print '='*70
print ' Input < z > to start full test of Monkey:\n Input < m > to start partial test of Monkey:\n'
print '='*70

CHOICE = raw_input()
if CHOICE == str('z'):
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_ZJ,stdout=subprocess.PIPE,shell=True)
    print 'Start full test' 
elif CHOICE == str('m'):
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_MD,stdout=subprocess.PIPE,shell=True)
    print 'Start partial test'
else:
    print 'Input Error'
    sys.exit()

subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)

starttime = datetime.datetime.now()
StrTime = starttime.strftime("%Y-%m-%d  %H:%M:%S")
fd_time=open('run_time.txt','w+')
fd_time.write('+'*70 + '\n')
fd_time.write('Start time is '+ StrTime + '\n' )
fd_time.close()

now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
path_time = os.path.join(cur_file_dir(),'monkey_test',otherStyleTime)
#print path_time
make_sure_path_exists(path_time)
subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)

time.sleep(5)  

def M_ID():
    MONKEY_ID = os.popen('adb shell ps')
    q = MONKEY_ID.read()
    #print q
    if "com.android.commands.monkey" in q:
        #print 'monkey_run'
        return 1
    else:
        #print 'monkey_stop'
        return 0
    


print '+'*70
print 'Please waiting for the test end ...... '
print '\n'
print 'But if you want to interrupt the test now,press Ctrl + C and enter \'q\''
print '+'*70


while 1:
	try:		
		I = M_ID()
        
		if (I == 0):
			#print "step1"
			break
		else:
			#print "step 2"
            
			continue
	except KeyboardInterrupt:
		print "Test interruped,please input \'q\':"
		INPUT_interrupt = raw_input()
		if INPUT_interrupt == str('q'):
			break
        
        
kill_logcat()
kill_monkey()
get_device_info()
os.system('adb kill-server')
os.system('adb start-server')

dirA="."
dirB=path_time
print dirB
for i in os.listdir(dirA):
	if i.endswith('.log'):
		#print i
		shutil.move(dirA+os.sep+i, dirB+os.sep)

endtime = datetime.datetime.now()
StrleTime = endtime.strftime("%Y-%m-%d  %H:%M:%S")
fd_time=open('run_time.txt','a+')
fd_time.write('End  time  is '+ StrleTime + '\n' )
fd_time.write('Run  time  is %d'%(endtime - starttime).seconds + 's' + '\n' )
fd_time.write('+'*70 + '\n')
fd_time.close()