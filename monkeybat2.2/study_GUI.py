#coding=utf-8
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

MONKEY_CMD_ZJ = 'adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions   -v -v  576000 '
MONKEY_CMD_MD = 'adb shell monkey --throttle 1000 -s 14041 -p com.android.calculator2 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions   -v -v 100 '

md = 'md'
zj = 'zj'

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


def monkey_cmd_md():
    
    os.popen(MONKEY_CMD_MD)
def monkey_cmd_zj():
    subprocess.Popen(MONKEY_CMD_ZJ)
  


def kill_logcat():
    os.system('adb  shell busybox pkill logcat')
def kill_monkey():
    os.system('adb  shell busybox pkill com.android.commands.monkey')

def end_test():
    kill_logcat()
    kill_monkey()
    print 'work end'
    # get_device_info()
    os.system('adb kill-server')
    os.system('adb start-server')
    os.system('adb reboot')

    

now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d-%H-%M-%S")
path_time = os.path.join('.','monkey_test',otherStyleTime)


def donothing():
   filewin = Toplevel(top)
   button = Button(filewin, text="Do nothing button",command = monkey_cmd_md)
   button.pack()


print os.getpid()
top = Tkinter.Tk()
top.title(" MONKEY TEST ")
# os.system('adb wait-for-device && adb root')
# time.sleep(5)
# os.system('adb wait-for-device && adb remount')
root = Toplevel(top)
root.title('xxxxx')  
x = Entry(root,width = 30)
x.insert(1,'MONKEY_CMD_MD')
x.pack()

y = Button(top,text="名单测试", fg="red",command = donothing )

y1 = Button(top,text="结束测试", fg="red",command = end_test )
y1.pack()
y.pack()

# y.invoke()
# root = Tk()
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=top.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
L1 = Label(top, text="User Name:")
top.config(menu=menubar)

# L1.pack( side = LEFT)

# top = Tkinter.Tk()
# top.title(" MONKEY TEST ")
# os.system('adb wait-for-device && adb root')
# time.sleep(5)
# os.system('adb wait-for-device && adb remount')
def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Hello button", command = helloCallBack)
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

# starttime = datetime.datetime.now()
# StrTime = starttime.strftime("%Y-%m-%d  %H:%M:%S")
# text = Text(top,)
# text.insert(INSERT, 'Start time is '+ StrTime + '\n')

# text.insert(END, "Bye Bye.....")
# text.pack(side = LEFT) 

L1 = Label(top, text="User Name:")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)
E1.pack(side = LEFT)
E1.insert (1, "0" )

# text = Text(top)
# text.insert(INSERT, "Start......\n")
# package_text = open("package.txt","r")
# for content2 in package_text.readlines(): 
# 	#print content2
# 	text.insert(INSERT, content2)
# text.insert(END, "Bye Bye.....")
# text.pack() 



# scrollbar = Scrollbar(top)
# scrollbar.pack( side = RIGHT, fill=Y )

# mylist = Listbox(top )
# for line in range(100):
#    mylist.insert(END, "This is line number " + str(line))

# mylist.pack( side = RIGHT, fill = BOTH )

# scrollbar.config( command = mylist.yview )



# labelframe = LabelFrame(top, text="This is a LabelFrame")
# labelframe.pack(fill="both", expand="yes")
 
# left = Label(labelframe, text="Inside the LabelFrame")
# left.pack()

m1 = PanedWindow()
m1.pack(fill=BOTH, expand=1)

left = Label(m1, text="left pane")
m1.add(left)

m2 = PanedWindow(m1, orient=VERTICAL)
m1.add(m2)

top = Label(m2, text="top pane")
m2.add(top)

bottom = Label(m2, text="bottom pane")
m2.add(bottom)

# scrollbar = Scrollbar(m1)
# scrollbar.pack( side = RIGHT, fill=Y )


# text = Text(m1,yscrollcommand = scrollbar.set)
# text.insert(INSERT, "Start......\n")
# package_text = open("package.txt","r")
# for content2 in package_text.readlines(): 
#     #print content2
#     text.insert(INSERT, content2)
# text.insert(END, "Bye Bye.....")
# text.pack() 

# scrollbar.config( command = text.yview )


# text.tag_add("here", "1.0", "1.end")
# text.tag_add("start", "2.0", "8.end")
# text.tag_config("here", background="yellow", foreground="blue")
# text.tag_config("start", background="black", foreground="green")

# top.mainloop()

#root = Tk()
# frame = Frame(top)
# frame.pack()

# bottomframe = Frame(top)
# bottomframe.pack( side = BOTTOM )

# redbutton = Button(frame, text="名单测试", fg="red", )
# redbutton.pack( side = LEFT)

# redbutton = Button(frame, text="整机测试", fg="red", )
# redbutton.pack( side = LEFT)

# greenbutton = Button(frame, text="中断MONKEY", fg="brown", )
# greenbutton.pack( side = LEFT )

# bluebutton = Button(frame, text="KMSG-LOG", fg="blue", )
# bluebutton.pack( side = LEFT )

# blackbutton = Button(bottomframe, text="中断LOGCAT", fg="black", )
# blackbutton.pack( )

# bluebutton = Button(frame, text="结束测试", fg="blue", )
# bluebutton.pack( side = LEFT )

# blackbutton = Button(bottomframe, text="启动LOG_parser", fg="black", )
# blackbutton.pack()
#blackbutton.pack( side = BOTTOM)

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)


var = IntVar()
R1 = Radiobutton(m1, text="Option 1", variable=var, value=1,command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(m1, text="Option 2", variable=var, value=2,command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(m1, text="Option 3", variable=var, value=3,command=sel)
R3.pack( anchor = W)

label = Label(m1)
label.pack()
 



top.mainloop()

# while 1:
#     try:        
#         I = M_ID()
        
#         if (I == 0):
#             #print "step1"
#             break
#         else:
#             #print "step 2"
            
#             continue
#     except KeyboardInterrupt:
#         print "Test interruped,please input \'q\':"
#         INPUT_interrupt = raw_input()
#         if INPUT_interrupt == str('q'):
#             break
# end_test()