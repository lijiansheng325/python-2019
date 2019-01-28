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
MONKEY_CMD_ZJ = 'adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-blacklist-file /data/local/tmp/WhiteBlack.txt -v -v  576000 > MONKEY_ZJ.log'
MONKEY_CMD_MD = 'adb shell monkey --throttle 500 -s 14041 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-whitelist-file /data/local/tmp/WhiteBlack.txt -v -v 1000 > MONKEY_MD.log'
KMSG_CMD = 'adb shell cat /proc/kmsg > KMSG.log'
PYTHON_other_CMD = 'python log_parser_runner.py -a 5 -b 5 -c 1 -o LOGPARSER_Report -s 10000'



def monkey_cmd_md():
    tkMessageBox.showinfo( "Start MONKEY", "开始名单测试")
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_MD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)
def monkey_cmd_zj():
    tkMessageBox.showinfo( "Start MONKEY", "开始整机测试")
    os.system(PUSH_WHITHBLACK)
    subprocess.Popen(MONKEY_CMD_ZJ,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(KMSG_CMD,stdout=subprocess.PIPE,shell=True)
    subprocess.Popen(PYTHON_other_CMD,stdout=subprocess.PIPE,shell=True)
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
def call_adb_pull_to_file(adb_shell_cmd, path, sub_path):
    path_name = os.path.join(path, sub_path)
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
def end_test():
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

now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
path_time = os.path.join(cur_file_dir(),'monkey_test',otherStyleTime)

top = Tkinter.Tk()
top.title(" MONKEY TEST ")
os.system('adb wait-for-device && adb root')
time.sleep(5)
os.system('adb wait-for-device && adb remount')
kill_logcat()
kill_monkey()

def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")
   
B = Tkinter.Button(top, text ="Hello button", command = helloCallBack )
C = Tkinter.Canvas(top, bg="Dark blue", height=250, width=300,highlightcolor="green")
D = Tkinter.Canvas(top, bg="white", height=200, width=300,highlightcolor="green",cursor="circle")
E = Tkinter.Canvas(top, bg="white", height=400, width=300,highlightcolor="green",cursor="circle")
F = Tkinter.Canvas(top, bg="white", height=300, width=300,highlightcolor="green",cursor="circle")
G = Tkinter.Canvas(top, bg="white", height=100, width=300,highlightcolor="green",cursor="circle")

coord = 10, 50, 240, 210
arc = C.create_arc(coord, start=0, extent=150, fill="red")

line = D.create_line(50, 50, 150,200,250,50,50,50,fill="red",width=10 )

oval = D.create_oval(125, 125, 150,150, fill="light blue")

oval = C.create_polygon(10,10, 100,120, 20,100, 200,200,fill="pink",width=10)

d = {1:'error',2:'info',3:'question',4:'hourglass'}
for i in d:
    E.create_bitmap((30*i,20),bitmap = d[i])
img = PhotoImage(file = 'c:\\woniu.gif')
F.create_image((150,150),image = img)
filename = PhotoImage(file = "E:\\work\\suchai\\woniu.gif")
image = E.create_image(150, 100,  image=filename)

# C.pack()
# B.pack()
#D.pack()
# F.pack()
# text = Text(top,)
# text.pack(expand=YES, fill='both')

CheckVar1 = IntVar()
CheckVar2 = IntVar()
C1 = Checkbutton(top, text = "Music", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 activebackground = "black",width = 20)
C2 = Checkbutton(top, text = "Video", fg = "green",variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5,  \
                 selectcolor="red" , \
                 width = 30)
# C1.pack()
# C2.select()
# C1.invoke()
# #C1.toggle()
# C2.pack()

starttime = datetime.datetime.now()
StrTime = starttime.strftime("%Y-%m-%d  %H:%M:%S")
text1 = Text(top,)
text1.insert(INSERT, 'Start time is '+ StrTime + '\n')
text1.insert(INSERT, "1" + '\n')
text1.insert(END, "22")
text1.insert(INSERT, "1" + '\n')

text1.pack(side = LEFT) 

# L1 = Label(top, text="User Name:")
# L1.pack( side = LEFT)
# E1 = Entry(top, bd =5)
# E1.pack(side = LEFT)
# E1.insert (1, "0" )

text = Text(top)
text.insert(INSERT, "+"*70+"\n")
package_text = open("package.txt","r")
for content2 in package_text.readlines(): 
	#print content2
	text.insert(INSERT, content2)
text.insert(END, "+"*70+"\n")
text.pack(side = BOTTOM)     

text.tag_add("here", "1.0", "1.end")
text.tag_add("start", "2.0", "10.end" )
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="white", foreground="blue")

# top.mainloop()

#root = Tk()
frame = Frame(top)
frame.pack()

bottomframe = Frame(top)
bottomframe.pack( side = BOTTOM  )

redbutton = Button(frame, text="名单测试", padx = 1 , pady = 1,fg="red",command = monkey_cmd_md)
redbutton.pack( side = LEFT)

L2 = Label(frame, text="   ")
L2.pack( side = LEFT)

redbutton = Button(frame, text="整机测试", fg="red",width = 8,command = monkey_cmd_zj)
redbutton.pack( side = LEFT)

L2 = Label(frame, text="   ")
L2.pack( side = LEFT)

bluebutton = Button(frame, text="KMSG-LOG", fg="blue",height = 1,highlightcolor = "red",command = kmsg_cmd)
bluebutton.pack( side = LEFT )

L2 = Label(frame, text="   ")
L2.pack( side = LEFT)
greenbutton = Button(bottomframe, text="中断MONKEY", fg="brown",command = kill_monkey)
greenbutton.pack( side = LEFT )

L2 = Label(bottomframe, text="   ")
L2.pack( side = LEFT)

blackbutton = Button(bottomframe, text="中断LOGCAT", fg="black",command = kill_logcat)
blackbutton.pack(side = LEFT  )

L2 = Label(bottomframe, text="   ")
L2.pack( side = LEFT)

bluebutton = Button(bottomframe, text="结束测试", fg="blue",command = end_test)
bluebutton.pack( side = LEFT )

blackbutton = Button(frame, text="启动LOG_parser", fg="black",command = python_other_cmd)
blackbutton.pack(side = LEFT)
#blackbutton.pack( side = BOTTOM)

 

top.mainloop()

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

end_test()

