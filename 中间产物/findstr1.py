#coding =gbk
#coding=GBK
import os
import sys
import zipfile
def flash_img():
	#os.system('adb wait-for-device')
	#os.system('adb reboot bootloader')
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
			search(fp, word)

os.system('rm *.img')
file_find_end = search_file_zip('.'+os.sep, sys.argv[2])
print file_find_end
print '*'*70
print 'Please unzip %s'%file_find_end
print 'continue Input ok\n'
print '*'*70
IMG_READY = raw_input() 
if IMG_READY == str('ok'):
	print 'IMG is ok'
else:
	print 'Input error'
	sys.exit()
flash_img()