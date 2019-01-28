#!/usr/bin/env python

import multiprocessing as mp
import os
import time

MONKEY_CMD = 'adb shell monkey --throttle 500  -s 500  --hprof  --ignore-crashes  --ignore-timeouts --kill-process-after-error --monitor-native-crashes -v -v -v  20000000'

LOGCAT_CMD = 'adb logcat -c && adb logcat -v threadtime > temp.txt'

REBOOT_CMD = 'adb reboot'

def foo():
    print 'start fetching log  here'
    os.system(LOGCAT_CMD)
    pass

def bar():
    print 'start MONKEY  here'
    os.system(MONKEY_CMD)
    pass

p1 = mp.Process(target=foo, args=())
p2 = mp.Process(target=bar, args=())

try:
    p1.start()
    p2.start()
    time.sleep(1)
    p1.join()
    time.sleep(1)
    p2.join()
except KeyboardInterrupt:
    print "Ending..."
    time.sleep(1)
    p1.terminate()
    time.sleep(1)
    p2.terminate()
    time.sleep(1)
    os.system(REBOOT_CMD)
    print "Quit done."
