import os,sys,time

def pathExists(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.exists(path):
            # We are nearly safe
            pass
        else:
            # There was an error on creation, so make sure we know about it
            raise
pathExists('.\\test\\screenshot')
t = 0
while 1:
    try:
        os.system('jietu.bat')
        time.sleep(5)
        t = t + 1
        if t > 123:
            break
    except KeyboardInterrupt:
        break
	
