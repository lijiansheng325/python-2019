import os

MONKEY_CMD = 'adb shell monkey --throttle 500  -s 500  --hprof  --ignore-crashes  --ignore-timeouts --kill-process-after-error --monitor-native-crashes -v -v -v  20000000'

os.system(MONKEY_CMD)
