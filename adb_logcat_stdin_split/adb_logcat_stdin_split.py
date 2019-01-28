# -*- coding: cp936 -*-
## function: remove file 
## remark: python version 2-7-3

import os
import sys
from datetime import datetime


q = []

i = 0

context_size = 100

input = os.popen("adb logcat -c && adb logcat -v threadtime ")

while True:
    try:
        line = input.readline()
        q.append(line)
        i = i + 1
    except KeyboardInterrupt:
        sys.stdout.flush()
        break

    if (i == context_size):
        file_name_time_stamp = datetime.now()
        print 'Start writing file: ' +'logcat' + file_name_time_stamp.strftime('%Y-%m-%d-%H-%M-%S') + '.txt' 
        
        file_handler=open('logcat' + file_name_time_stamp.strftime('%Y-%m-%d-%H-%M-%S') + '.txt','w')
        for item in q:
            file_handler.write(item)
        file_handler.close()

        print 'End writing file' + '\n'
            
        i = 0        
        q[:] = []


