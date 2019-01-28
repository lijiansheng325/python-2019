 
import ConfigParser
import string, os, sys
import subprocess
import re
MONKEY_CMD = 'adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-blacklist-file /data/local/tmp/WhiteBlack.txt -v -v  576000 > '

# if os.path.exists('monkeycfg.ini'):
# 	cf = ConfigParser.ConfigParser()
	 
# 	cf.read("monkeycfg.ini")
	 
# 	#return all section
# 	secs = cf.sections()
# 	print 'sections:', secs
	 
# 	opts = cf.options("Monkey")
# 	print 'options:', opts
	 
# 	kvs = cf.items("Monkey")
# 	print 'Monkey:', kvs
	 
# 	#read by type
# 	Monkey_throttle = cf.get("Monkey", "throttle")
# 	Monkey_s = cf.get("Monkey", "Seed")
# 	Monkey_command = cf.get("Monkey", "command")
# 	Monkey_aimhour = cf.getint("Monkey", "aimhour")
# 	Monkey_timeout = cf.getint("Monkey", "timeout")
# 	Monkey_securityexception = cf.getint("Monkey", "securityexception")
# 	Monkey_exception = cf.getint("Monkey", "exception")
	 

# else:
# 	pass
# monkeyList = MONKEY_CMD.split(" ")

# monkeyStr = ' '.join(monkeyList)	
# # monkeyStr1 = str(monkeyList)	
# print monkeyStr
# print monkeyList
# print len(monkeyList)
if not os.path.exists('WhiteBlack.txt'):
    print 'Please edit WhiteBlack.txt '
    whiteBlack = raw_input('input ok:\n') 
    if whiteBlack == "ok":
    	pass
    else:
    	sys.exit()
def  monkeyCmd(monkeyType):
	if os.path.exists('monkeycfg.ini'):
		cf = ConfigParser.ConfigParser()
		 
		cf.read("monkeycfg.ini")
		 	
		Monkey_throttle = cf.get("Monkey", "throttle")
		Monkey_s = cf.get("Monkey", "Seed")
		Monkey_command = cf.get("Monkey", "command")
		Monkey_aimhour = cf.getint("Monkey", "aimhour")
		Monkey_timeout = cf.getint("Monkey", "timeout")
		Monkey_securityexception = cf.getint("Monkey", "securityexception")
		Monkey_exception = cf.getint("Monkey", "exception")
		
	else:
		pass
	monkeyList = MONKEY_CMD.split(" ")

	
	m=re.match('md',monkeyType,re.IGNORECASE)
	if m:
		monkeyList1 = ['--pkg-whitelist-file' if x == '--pkg-blacklist-file' else x for x in monkeyList]
	else:
		monkeyList1 = monkeyList

	isExists=os.path.exists('monkeycfg.ini')
	if not isExists:
		monkeyList1.append('MONKEY_' + monkeyType.upper()+'.log')
		MONKEY_CMD_type = ' '.join(monkeyList1)	
	else:
		
		if Monkey_timeout == 0:
			monkeyList1.remove('--ignore-timeouts')
		if Monkey_securityexception == 0:
			monkeyList1.remove('--ignore-security-exceptions')
			
		
		monkeyList1.append('MONKEY_' + monkeyType.upper()+'.log')
		MONKEY_CMD_type = ' '.join(monkeyList1)
		MONKEY_CMD_type = MONKEY_CMD_type.replace('500',Monkey_throttle).replace('576000',Monkey_command).replace('1000',Monkey_s)
	return MONKEY_CMD_type

print monkeyCmd('md')
# subprocess.Popen(monkeyCmd('md'),stdout=subprocess.PIPE,shell=True) 
# subprocess.Popen(monkeyZj(),stdout=subprocess.PIPE,shell=True) 
# print "thread:", threads
# print "processor:", processors
 
 
# #modify one value and write to file
# cf.set("Monkey", "Monkey_pass", "xgmtest")
# cf.write(open("test.conf", "w"))