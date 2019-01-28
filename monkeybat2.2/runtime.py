import os
import sys
import datetime
import time
starttime = datetime.datetime.now()
StrTime = starttime.strftime("%Y-%m-%d  %H:%M:%S")
fd_time=open('run_time.txt','w+')
fd_time.write('+'*70 + '\n')
fd_time.write('Start time is '+ StrTime + '\n' )
fd_time.close()
print starttime

time.sleep(5)

endtime = datetime.datetime.now()
StrleTime = endtime.strftime("%Y-%m-%d  %H:%M:%S")
fd_time=open('run_time.txt','a+')
fd_time.write('End  time  is '+ StrleTime + '\n' )
fd_time.write('Run  time  is %d'%(endtime - starttime).seconds+'s' + '\n' )
fd_time.write('+'*70)
fd_time.close()
print endtime
#print "running time is " , (endtime - starttime).seconds,"s"