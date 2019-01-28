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
import threading

import ConfigParser

import subprocess
import re
#ctypes.windll.user32.MessageBoxA(0,'hello','some',0)

def helloCallBack():
	tkMessageBox.showinfo( "Hello Python", "The CPB file has been downloaded,\n extended press the power button and volume+ toggle,\
	let your IVVI phone into the FASTBOOT mode")
def messageCallBack():
	if m:
		ctypes.windll.user32.MessageBoxW(0,download_type.rsplit('.',1)[1].upper()+u'文件下载完成。\n手机关机,USB线连接电脑,长按开机键和音量上键进入FASTBOOT mode。\n\
使用酷派工具，根据提示完成刷机。 ', u' 完成提示 ', 0)
	else:
		ctypes.windll.user32.MessageBoxW(0,download_type.rsplit('.',1)[1].upper()+u'文件下载完成。', u' 完成提示 ', 0)
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
		
		for source_path in all_files(path1,download_feature):
		#for source_path in all_files(path1,'*.txt;'):
			
			Y = source_path
			
			Y2 = Y.rsplit('\\',2)[2].rsplit('.',1)[0]
			
			target_path = Y2 + download_type
			if not os.path.exists(target_path):
				print 'Start download  %s .....'%target_path
				shutil.copyfile(Y, target_path)
				print 'Finished '
			else:
				break 

def ensureAddress():			
	try:
		a = raw_input("Ensure?")+"\n"
		
	except KeyboardInterrupt:
		print '\nStop download'
		sys.exit()

coolpadTool = '"D:\CoolpadDownloadAssistant\Coolpad Download Assistant\Coolpad Download Assistant.exe"'
if os.path.exists('download.ini'):
	cf = ConfigParser.ConfigParser()
	 
	cf.read("download.ini")
	 	
	download_address_default = cf.get("download", "address1")
	download_type = cf.get("download", "type1")
	download_feature = cf.get("download", "feature1")
	print 'Address is: ', download_address_default +'\n','Type is: ', download_type.rsplit('.',1)[1].upper()
else:
	pass
# threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
# t2 = threading.Thread(target=move,args=(u'阿凡达',))
# threads.append(t2)

# for t in threads:
#         t.setDaemon(True)
#         t.start()

if __name__ == '__main__':
	
	p = download_address_default #'\\\\10.1.11.53\\cpss1_03_eui'
	l=os.listdir(p+os.sep)
	
	st = l.sort(key=lambda fn: os.path.getmtime(p+"\\"+fn) if not os.path.isdir(p+"\\"+fn) else 0) 
	
	lForm = []
	if  'cpss1_03_eui' in p:
		for fileIn in l:
			# print fileIn
			if 'SS1_03' in fileIn:
				lForm.append(fileIn)
	else:
		for fileIn in l:
			# print fileIn
			lForm.append(fileIn)
	# print lForm		
	d=datetime.datetime.fromtimestamp(os.path.getmtime(p+"\\"+lForm[-1]))
	print ('Last file is: '+lForm[-1])  
	time_end=time.mktime(d.timetuple())
	x = time.localtime(time_end)
	x_str = time.strftime('%Y-%m-%d %H:%M:%S',x)
	print 'Creat time is: ',x_str
	filepath = os.path.join(p + os.sep, lForm[-1])
	# print filepath
	
	th1 = threading.Thread(target = ensureAddress())
	th1.setDaemon(True)
	th1.start 
	
	
	# helloCallBack()   
	search_file(filepath)
	m=re.match('.cpb',download_type,re.I)
	if m:
		messageCallBack()
		subprocess.Popen(coolpadTool,stdout=subprocess.PIPE,shell=True)
		
	else:
		messageCallBack()