#coding=utf-8
#coding=GBK
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

#ctypes.windll.user32.MessageBoxA(0,'hello','some',0)

def helloCallBack():
	tkMessageBox.showinfo( "Hello Python", "The CPB file has been downloaded,\n extended press the power button and volume+ toggle,\
	let your IVVI phone into the FASTBOOT mode")
def messageCallBack():
	ctypes.windll.user32.MessageBoxW(0,u'CPB文件下载完成。\n手机关机,USB线连接电脑,长按开机键和音量上键进入FASTBOOT mode。\n\
使用酷派工具，根据提示完成刷机。 ', u' 完成提示 ', 0)

def all_files(root,patterns='*',single_level=False,yield_folders=False):
	patterns = patterns.split(';')
	for path,subdirs,files in os.walk(root):
		if yield_folders:
			files.extend(subdirs)
		files.sort()
		
		for name in files:
			for pattern in patterns:
				if fnmatch.fnmatch(name,pattern):
					yield os.path.join(path,name)
					break
		if single_level:
			break


def search_file(search_path=os.environ['PATH'], pathsep=os.pathsep):
	for path1 in search_path.split(os.pathsep):
		
		for source_path in all_files(path1,'*.CPB;'):
		#for source_path in all_files(path1,'*.txt;'):
			print source_path
			Y = source_path
			
			Y2 = Y.rsplit('\\',2)[2].rsplit('.',1)[0]
			
			target_path = Y2 + ".CPB"

			shutil.copyfile(Y, target_path)
def topGui():
	top = Tkinter.Tk()
	top.geometry('200x40')
	top.title(" Download IMAGE ")
	
	L1 = Label(top, text=p)
	L1.pack(fill = Y)
	
	
	
	top.mainloop()
# threads = []
# t1 = threading.Thread(target=topGui)
# threads.append(t1)
# t2 = threading.Thread(target=helloCallBack)
# threads.append(t2)

if __name__ == '__main__':

	# for t in threads:
	# 	t.setDaemon(True)
	# 	t.start()
	p = '\\\\10.1.11.53\\cpss1_03_eui'
	
	# topGui()
	t1 = threading.Thread(target=topGui)
	t1.start()

	# t1.join()
	
	
	
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
	
	# helloCallBack()   
	# search_file(filepath)
	# messageCallBack()
	
	# os.system('"D:\CoolpadDownloadAssistant\Coolpad Download Assistant\Coolpad Download Assistant.exe"')
	
	