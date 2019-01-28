#coding=utf-8
#coding=GBK
import os
import sys
import datetime
import time
import Tkinter
from Tkinter import *
import tkMessageBox
import subprocess
import shutil
import platform
# package = open("package.txt","r")
# #content1 = package.read(7)          
# for content2 in package.readlines(): 
# 	print content2     
# content3 = package.readlines()  
# #print content1
# # print content2
# # print content3

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
MONKEY_CMD_ZJ = 'adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions \
 --pkg-blacklist-file /data/local/tmp/WhiteBlack.txt -v -v  576000 > MONKEY_ZJ.log'
MONKEY_CMD_MD = 'adb shell monkey --throttle 500 -s 14041 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  \
--pkg-whitelist-file /data/local/tmp/WhiteBlack.txt -v -v 100 > MONKEY_MD.log'
KMSG_CMD = 'adb shell cat /proc/kmsg > KMSG.log'
PYTHON_other_CMD = 'python log_parser_runner.py -a 5 -b 5 -c 1 -o LOGPARSER_Report -s 10000'



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

def kmsg_cmd():
	subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)
def python_other_cmd():
	subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)
def kill_logcat():
    os.system('adb  shell busybox pkill logcat')
def kill_monkey():
    os.system('adb  shell busybox pkill com.android.commands.monkey')
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.exists(path):
            pass
        else:
            raise
def cur_file_dir():
    
    path = sys.path[0]
     
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
path_time = os.path.join(cur_file_dir(),'monkey_test',otherStyleTime)

def call_adb_pull_to_file(adb_shell_cmd, path, sub_path):
    path_name = os.path.join(path, sub_path)
    make_sure_path_exists(path_name)
    os.system(adb_shell_cmd + ' ' + path_name)
    time.sleep(2)

def get_device_info(path_t):
    try:
        
        call_adb_pull_to_file(ANR_CMD, path_t, ANR_PATH)
        call_adb_pull_to_file(SDCARD_SEMS_CMD, path_t, SDCARD_SEMS_PATH)
        call_adb_pull_to_file(SDCARD_LOGS_CMD, path_t, SDCARD_LOGS_PATH)
        call_adb_pull_to_file(DROPBOX_CMD, path_t, DROPBOX_PATH)
        call_adb_pull_to_file(TOMBSTONES_CMD, path_t, TOMBSTONES_PATH)
    
    except Exception,e:
        print str(e)

def end_test(path_t):
    kill_logcat()
    kill_monkey()
    get_device_info(path_t)
    os.system('adb kill-server')
    os.system('adb start-server')

    dirA="."
    dirB=path_t
    print dirB
    for i in os.listdir(dirA):
        if i.endswith('.log'):
            #print i
            shutil.move(dirA+os.sep+i, dirB+os.sep)
def monkey_cmd_md():
    starttime1 = datetime.datetime.now()
    StrTime1 = starttime1.strftime("%Y-%m-%d  %H:%M:%S")
    E1.insert (0, StrTime1 + '     ')
    fd_time=open('run_time.txt','w+')
    fd_time.write('开始名单测试' + '\n')
    fd_time.write('+'*70 + '\n')
    fd_time.write('Start time is '+ StrTime1 + '\n' )
    fd_time.close()

    otherStyleTime1 = starttime1.strftime("%Y-%m-%d-%H-%M-%S")
    path_t = os.path.join(cur_file_dir(),'monkey_test',otherStyleTime1)
    tkMessageBox.showinfo( "Start MONKEY", "开始名单测试%s"%StrTime1)
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_MD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)
    time.sleep(10)
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
    endtime = datetime.datetime.now()
    StrleTime2 = endtime.strftime("%Y-%m-%d  %H:%M:%S")
    E2.insert (0, StrleTime2 + '     ')
    fd_time=open('run_time.txt','a+')
    fd_time.write('End  time  is '+ StrleTime2 + '\n' )
    fd_time.write('Run  time  is %d'%(endtime - starttime1).seconds+'s' + '\n' )
    fd_time.write('+'*70)
    fd_time.close()

    end_test(path_t)
def monkey_cmd_zj():
    starttime1 = datetime.datetime.now()
    StrTime1 = starttime1.strftime("%Y-%m-%d  %H:%M:%S")
    E1.insert (1, StrTime1  + '     '   )
    fd_time=open('run_time.txt','w+')
    fd_time.write('开始整机测试' + '\n')
    fd_time.write('+'*70 + '\n')
    fd_time.write('Start time is '+ StrTime1 + '\n' )
    fd_time.close()

    otherStyleTime1 = starttime1.strftime("%Y-%m-%d-%H-%M-%S")
    path_t = os.path.join(cur_file_dir(),'monkey_test',otherStyleTime1)
    tkMessageBox.showinfo( "Start MONKEY", "开始整机测试%s"%StrTime1)
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_ZJ,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)
    time.sleep(10)
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
    endtime = datetime.datetime.now()
    StrleTime2 = endtime.strftime("%Y-%m-%d  %H:%M:%S")
    E2.insert (1, StrleTime2  + '     ' )
    fd_time=open('run_time.txt','a+')
    fd_time.write('End  time  is '+ StrleTime2 + '\n' )
    fd_time.write('Run  time  is %d'%(endtime - starttime1).seconds+'s' + '\n' )
    fd_time.write('+'*70)
    fd_time.close()

    end_test(path_t)


top = Tkinter.Tk()
top.title(" MONKEY TEST ")
print 'Please use the USB cable to connect testing machine and computer'
os.system('adb wait-for-device && adb root')
time.sleep(5)
os.system('adb wait-for-device && adb remount')
kill_logcat()
kill_monkey()

GET_PROP = 'adb shell getprop > getprop.txt'
subprocess.Popen(GET_PROP,stdout=subprocess.PIPE,shell=True)
time.sleep(5)
text = Text(top)
text.insert(INSERT, "+"*70+"\n")
package_text = open("getprop.txt","r")
for content2 in package_text.readlines(): 
	#print content2
    if 'build' in content2:
	   text.insert(INSERT, content2 + '\n')

text.insert(END, "+"*70+"\n")
text.pack(side = BOTTOM)     

text.tag_add("here", "1.0", "1.end")
text.tag_add("start", "5.0", "10.end" )
text.tag_add("mid", "13.0", "15.end" )
text.tag_add("mid_1", "20.0", "20.end" )
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="white", foreground="red")
text.tag_config("mid", background="white", foreground="blue")
text.tag_config("mid_1", background="white", foreground="red")



L2 = Label(top, text="   ")
L2.pack( side = TOP)

frame = Frame(top)
frame.pack()

bottomframe = Frame(top)
bottomframe.pack( side = BOTTOM  )

redbutton = Button(frame, text="名单测试", padx = 20 , pady = 1,fg="dark green",command = monkey_cmd_md)
redbutton.pack( side = LEFT)

L2 = Label(frame, text="   "*10)
L2.pack( side = LEFT)

redbutton = Button(frame, text="整机测试", fg="red",width = 20,command = monkey_cmd_zj)
redbutton.pack( side = LEFT)


bluebutton = Button(bottomframe, text="结束测试",width = 20, fg="blue",command = end_test)
bluebutton.pack( side = LEFT )

L2 = Label(top, text="   ")
L2.pack( side = TOP)



leftframe = Frame(top)
leftframe.pack( side = LEFT  )
L1 = Label(leftframe, text="   Start time:")
L1.pack( side = LEFT)
E1 = Entry(leftframe, bd =5)
E1.pack(side = LEFT)

L2 = Label(leftframe, text="        ")
L2.pack( side = LEFT)

L2 = Label(leftframe, text="End time:")
L2.pack(side = LEFT)
E2 = Entry(leftframe, bd =5)
E2.pack(side = LEFT)



top.mainloop()





