#coding=utf-8

import os
import sys
import datetime
import time

from glob import glob 
import fnmatch
import shutil
import tkMessageBox
import ctypes
import Tkinter
from Tkinter import *
import threading

#resize函数是用来改变文字大小的，当进度条改变时调用
def resize(ev=None):
	# label.config(font='Helvetica -%d bold' % scale.get())
	print(scale.get())
	p = E1.get()
	
	
	
	l=os.listdir(p+os.sep)
	# print l
	st = l.sort(key=lambda fn: os.path.getmtime(p+"\\"+fn) if not os.path.isdir(p+"\\"+fn) else 0) 
	lForm = []
	for fileIn in l:
		if 'SS1_03' in fileIn:
			lForm.append(fileIn)
	# print lForm		
	d=datetime.datetime.fromtimestamp(os.path.getmtime(p+"\\"+lForm[-1]))
	print ('last file is '+lForm[-1])  
	time_end=time.mktime(d.timetuple())
	x = time.localtime(time_end)
	x_str = time.strftime('%Y-%m-%d %H:%M:%S',x)
	print 'time_end:',x_str
	filepath = os.path.join(p + os.sep, lForm[-1])
	print filepath
#config函数就是通过设置组件的参数来改变组件的，这里改变的是font字体大小
top=Tk()   #主窗口
top.geometry('600x400')  #设置了主窗口的初始大小600x400
label=Label(top,text='Hello world!',font='Helvetica -12 bold')  #设置标签字体的初始大小
label.pack(fill=Y,expand=1)

p1 = '\\\\10.1.11.53\\cpss1_03_eui'

L1 = Label(top, text="User Name:")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)
E1.pack(side = LEFT)
E1.insert(1, p1)
#scale创建进度条，设置
scale=Scale(top,from_=10,to=40,orient=HORIZONTAL,command=resize)
scale.set(12)  #设置起始位置
scale.pack(fill=X,expand=1)
quit = Button(top,text='QUIT',command=top.quit,activeforeground='white',activebackground='red')
quit.pack()
mainloop()