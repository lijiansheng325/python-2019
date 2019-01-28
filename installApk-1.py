#coding=utf-8
#!/usr/bin/env python 

import os
import sys


doc = "d:\\apk\\apk"
apkInstall = "adb install "
txt = "apk.txt"

def findFile():
    apks = os.walk(doc)
    for root,dirs,files in apks:
        for dir in dirs:
#            print(os.path.join(root, dir))
            pass
        for file in files:
            apkFile = os.path.join(root, file)
            f = open(txt, "a")
            f.write(apkFile + '\n')
            f.close()

#            print apkFile

def installApk(file):
    apkTxt = open(file, "r")
    p = apkTxt.readlines()
    for apk1 in p:
        print "install " + apk1
        os.system(apkInstall + apk1)

if __name__ == "__main__":
	if os.path.exists(txt):
		os.remove(txt)
	else:
		pass
	findFile()
	installApk(txt)
	print "finish"

	os.system("pause")

 
