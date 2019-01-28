#coding = utf-8
import os
import sys
import datetime
import time
#coding=GBK
from glob import glob 
import fnmatch
import shutil

p = '\\\\10.1.11.51\\cpss1_03_eui\\Rel_Version'
l=os.listdir(p+os.sep)
st = l.sort(key=lambda fn: os.path.getmtime(p+"\\"+fn) if not os.path.isdir(p+"\\"+fn) else 0) 
d=datetime.datetime.fromtimestamp(os.path.getmtime(p+"\\"+l[-1]))
print ('last file is '+l[-1])  
time_end=time.mktime(d.timetuple())
print 'time_end:',time_end
filepath = os.path.join(p + os.sep, l[-1])
print filepath

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
			
def flash_img():

	os.system('adb reboot bootloader')
	os.system('fastboot -i 0x1ebf flash  boot boot.img')
	os.system('fastboot -i 0x1ebf flash cache cache.img')
	os.system('fastboot -i 0x1ebf flash system system.img')
	os.system('fastboot -i 0x1ebf flash userdata userdata.img') 
	os.system('fastboot -i 0x1ebf flash recovery recovery.img')
	os.system('fastboot -i 0x1ebf reboot')

def search_file_zip(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
			print fp
			return fp
        elif os.path.isdir(fp):
			search_file_zip(fp, word)			

if __name__ == '__main__':
    
    
    search_file(filepath)
	
	# os.system('rm *.img')
	# file_find_end = search_file_zip('.'+os.sep, sys.argv[2])
	
	
	#flash_img()

 

