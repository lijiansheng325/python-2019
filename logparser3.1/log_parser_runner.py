# -*- coding: cp936 -*-
## function: log_parser_runner 
## remark: python version 2-7-3

import os
import sys
import shutil
import datetime
import time
import errno
import getopt
import re
import subprocess
import json

# fixed variables
REPORTS_PATH = 'reports'
REPORT_NAME = 'report_name'
TOP_RESULT_FILE = 'reports.txt'
CRASH_FILE = 'crash.txt'
ANR_FILE = 'anr.txt'
FC_FILE = 'fc.txt'
TC_FILE = 'tc.txt'
LOGCAT_FILE = 'logcat_snipest.txt'

# fixed variables
ANR_PATH = "ANR"
SDCARD_SEMS_PATH = "SDCARD_SEM"
SDCARD_LOGS_PATH = "SDCARD_LOG"
DROPBOX_PATH = "DROP_BOX"
TOMBSTONES_PATH = "TOMB_STONE"

TAG_DICT = {}
ADB_CMD_DICT = {}
PARSER_ARGS_DICT = {}

# get values of variables from json data file
try:
    json_file='log_parser_runner.json'
    json_data=open(json_file)
    data = json.load(json_data)
    json_data.close()

    for key, value in data.items():
        if key.find("TAG_DICT") >= 0:
            TAG_DICT = value
        elif key.find("ADB_CMD") >=0:
            ADB_CMD_DICT = value
        elif key.find("PARSER_ARGS") >=0:
            PARSER_ARGS_DICT = value

    ADB_FETCH_LOGS_CMD = str(ADB_CMD_DICT["ADB_FETCH_LOGS_CMD"])

    ADB_WAIT_CMD = str(ADB_CMD_DICT["ADB_WAIT_CMD"]).split()
    ADB_ROOT_CMD = str(ADB_CMD_DICT["ADB_ROOT_CMD"]).split()
    ADB_REMOUNT_CMD = str(ADB_CMD_DICT["ADB_REMOUNT_CMD"]).split()

    ANR_PULL_CMD = str(ADB_CMD_DICT["ANR_PULL_CMD"]).split()
    DROPBOX_PULL_CMD = str(ADB_CMD_DICT["DROPBOX_PULL_CMD"]).split()
    SDCARD_SEMS_PULL_CMD = str(ADB_CMD_DICT["SDCARD_SEMS_PULL_CMD"]).split()
    SDCARD_LOGS_PULL_CMD = str(ADB_CMD_DICT["SDCARD_LOGS_PULL_CMD"]).split()
    TOMBSTONES_PULL_CMD = str(ADB_CMD_DICT["TOMBSTONES_PULL_CMD"]).split()

    ANR_CLEAN_CMD = str(ADB_CMD_DICT["ANR_CLEAN_CMD"]).split()
    DROPBOX_CLEAN_CMD = str(ADB_CMD_DICT["DROPBOX_CLEAN_CMD"]).split()
    SDCARD_SEMS_CLEAN_CMD = str(ADB_CMD_DICT["SDCARD_SEMS_CLEAN_CMD"]).split()
    SDCARD_LOGS_CLEAN_CMD = str(ADB_CMD_DICT["SDCARD_LOGS_CLEAN_CMD"]).split()
    TOMBSTONES_CLEAN_CMD = str(ADB_CMD_DICT["TOMBSTONES_CLEAN_CMD"]).split()

    # parser step
    PARSER_STEP = PARSER_ARGS_DICT["STEP"]

    # a size, b size is similar as 'grep -a5 -b5...'
    A_SIZE = PARSER_ARGS_DICT["A_SIZE"]
    B_SIZE = PARSER_ARGS_DICT["B_SIZE"]
except Exception, e:
    print(str(e))
    sys.exit()

q = []
A_LIST=[]
B_LIST=[] 

# total result of current test
TOTAL_DICT = dict()

# catagorzied result of each kind of test
CRASH_SPLIT_DICT = dict()
ANR_SPLIT_DICT = dict()
FC_SPLIT_DICT = dict()
TC_SPLIT_DICT = dict()

# detailed result of each kind of test
CRASH_DICT = dict()
ANR_DICT = dict()
FC_DICT = dict()
TC_DICT = dict()

# parser count of current test
parser_count = 0

def dump_dict(dict):
    for key in dict:
        print key + ':\n' + str(dict[key])

def increase_dict_value(dict, key):
    if (key in dict):
        dict[key] += 1
    else:
        dict[key] = 1

def append_dict_value(dict, key, value):
    if (key in dict):
        dict[key] += '\n\n'
        dict[key] += value
    else:
        dict[key] = value

def insert_result_to_detail_dict(tag_key, package_key, log_result):
    if tag_key == 'CRASH':
        append_dict_value(CRASH_DICT, package_key, log_result)
    elif tag_key =='ANR_0' or tag_key == 'ANR_1':
        append_dict_value(ANR_DICT, package_key, log_result)
    elif tag_key == 'FC':
        append_dict_value(FC_DICT, package_key, log_result)
    elif tag_key == 'TC':
        append_dict_value(TC_DICT, package_key, log_result)

def insert_result_to_split_dict(tag_key, package_key):
    if tag_key == 'CRASH':
        increase_dict_value(CRASH_SPLIT_DICT, package_key)        
    elif tag_key =='ANR_0' or tag_key == 'ANR_1':
        increase_dict_value(ANR_SPLIT_DICT, package_key)        
    elif tag_key == 'FC':
        increase_dict_value(FC_SPLIT_DICT, package_key)        
    elif tag_key == 'TC':
        increase_dict_value(TC_SPLIT_DICT, package_key)        

def insert_result_to_total_dict(tag_key):
    if tag_key == 'CRASH':
        increase_dict_value(TOTAL_DICT, 'CRASH')        
    elif tag_key =='ANR_0' or tag_key == 'ANR_1':
        increase_dict_value(TOTAL_DICT, 'ANR')        
    elif tag_key == 'FC':
        increase_dict_value(TOTAL_DICT, 'FC')        
    elif tag_key == 'TC':
        increase_dict_value(TOTAL_DICT, 'TC')        

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.exists(path):
            # We are nearly safe
            pass
        else:
            # There was an error on creation, so make sure we know about it
            raise

def dump_detail_dict_to_file(test_name, file_name, dict):
    path_name = test_name
    filepath = os.path.join(path_name, file_name)
    make_sure_path_exists(path_name)

    file_handler=open(filepath,'w+')
    for key in dict:
        file_handler.write(key)
        file_handler.write(':\n')
        file_handler.write(str(dict[key]))
        file_handler.write('\n\n')    
    file_handler.close()

def DumpDetailResult(test_name):
    dump_detail_dict_to_file(test_name, CRASH_FILE, CRASH_DICT)    
    dump_detail_dict_to_file(test_name, ANR_FILE, ANR_DICT)    
    dump_detail_dict_to_file(test_name, FC_FILE, FC_DICT)    
    dump_detail_dict_to_file(test_name, TC_FILE, TC_DICT)    

def dump_dict_to_file2(file_handler, dict):
    for key in dict:
        file_handler.write(key)
        file_handler.write(':')
        file_handler.write(str(dict[key]))
        file_handler.write('\n')

def DumpTopResult2(test_name):
    path_name = test_name
    filepath = os.path.join(path_name, TOP_RESULT_FILE)
    make_sure_path_exists(path_name)

    file_handler=open(filepath,'w+')
    file_handler.write('='*10 + '\n')    
    dump_dict_to_file2(file_handler, TOTAL_DICT)

    file_handler.write('CRASH' + '>'*10 + '\n')    
    dump_dict_to_file2(file_handler, CRASH_SPLIT_DICT)    

    file_handler.write('ANR' + '>'*10 + '\n')    
    dump_dict_to_file2(file_handler, ANR_SPLIT_DICT)    

    file_handler.write('FC' + '>'*10 + '\n')    
    dump_dict_to_file2(file_handler, FC_SPLIT_DICT)    

    file_handler.write('TC' + '>'*10 + '\n')    
    dump_dict_to_file2(file_handler, TC_SPLIT_DICT)    
    
    file_handler.close()

badchars= re.compile(r'[^A-Za-z0-9_. ]+|^\.|\.$|^ | $|^$')
badnames= re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')

def makeName(s):
    name= badchars.sub('_', s)
    if badnames.match(name):
        name= '_'+name
    return name

def get_root_of_device():
    try:
        s0=subprocess.Popen(ADB_WAIT_CMD)
        s0.wait() 
        s1=subprocess.Popen(ADB_ROOT_CMD)
        s1.wait() 
        s2=subprocess.Popen(ADB_REMOUNT_CMD)
        s2.wait() 
        
        #os.system('adb wait-for-device && adb root')
        #time.sleep(2)
        #os.system('adb wait-for-device && adb remount')
    except Exception, e:
        print(str(e))
        pass

def clean_device_log():
    call_adb_clean_log(ANR_CLEAN_CMD)
    call_adb_clean_log(SDCARD_SEMS_CLEAN_CMD)
    call_adb_clean_log(SDCARD_LOGS_CLEAN_CMD)
    call_adb_clean_log(DROPBOX_CLEAN_CMD)
    call_adb_clean_log(TOMBSTONES_CLEAN_CMD)
    
def get_device_log(test_name, time_stamp, package, tag, logcat_result):
    try:
        package = makeName(package)
        tag = makeName(tag)       
        part_path_name = time_stamp+'_'+package+'_'+tag
                
        path_name = os.path.join(test_name, part_path_name)
        make_sure_path_exists(path_name)

        call_adb_pull_to_file(ANR_PULL_CMD, path_name, ANR_PATH)
        call_adb_pull_to_file(SDCARD_SEMS_PULL_CMD, path_name, SDCARD_SEMS_PATH)
        call_adb_pull_to_file(SDCARD_LOGS_PULL_CMD, path_name, SDCARD_LOGS_PATH)
        call_adb_pull_to_file(DROPBOX_PULL_CMD, path_name, DROPBOX_PATH)
        call_adb_pull_to_file(TOMBSTONES_PULL_CMD, path_name, TOMBSTONES_PATH)

        logcat_file = os.path.join(path_name, LOGCAT_FILE)
        file_handler=open(logcat_file,'w+')
        file_handler.write(logcat_result)
        file_handler.close()
    except Exception,e:
        print str(e)
        pass

def call_adb_pull_to_file(adb_shell_cmd, path, sub_path):
    try:
        path_name = os.path.join(path, sub_path)
        make_sure_path_exists(path_name)

        adb_shell_cmd.append(path_name)

        subprocess.call(adb_shell_cmd)
        time.sleep(2)      

        #s=subprocess.Popen(adb_shell_cmd + ' ' + path_name)
        #s.wait() 

        #os.system(adb_shell_cmd + ' ' + path_name)
        #time.sleep(2)
    except Exception, e:
        print str(e)
        pass

def call_adb_clean_log(adb_shell_cmd):
    try:
        subprocess.call(adb_shell_cmd)
        time.sleep(2)      
        #s=subprocess.Popen(adb_shell_cmd)
        #s.wait() 
        #os.system(adb_shell_cmd)
        #time.sleep(2)        
    except Exception, e:
        print str(e)
        pass

def usage():  
    print '''  
    Usage: log_parser_runner [options...]  
    Options:   
    -o : Report output directory name
    Example:
    python log_parser_runner.py -o 'Report_Folder'
    '''

############################################################################
# main process start
############################################################################
    
try:
    opts, args = getopt.getopt(sys.argv[1:],'o:')
except getopt.GetoptError:
    usage()  
    sys.exit()
   
if len(opts) == 0:  
    usage()  
    sys.exit()
else:
    try:
        #A_SIZE = (-1)*(int(opts[0][1])+1)
        REPORT_NAME = opts[0][1]        
    except IndexError:
        usage()  
        sys.exit()    

# Get root access of devices
get_root_of_device()

# Clean android device logs
clean_device_log()

test_name = os.path.join(REPORT_NAME, REPORTS_PATH)
print test_name + ' is starting'

# main pipeline
input = os.popen(ADB_FETCH_LOGS_CMD)

while True:
    try:
        line = input.readline()
        q.append(line.rstrip())
        parser_count += 1

        # 100K lines parsed and create phrased report
        if ((len(line) > 0) and (parser_count % PARSER_STEP == 0)):
            DumpTopResult2(test_name) 
            #DumpTopResult(test_name) 
            DumpDetailResult(test_name)
            sys.stdout.write("=")
            sys.stdout.flush()

        # pipe line is empty, so create final report and quit
        if (len(line) == 0):
            print '\n' + test_name + ' is ending ...'
            DumpTopResult2(test_name)
            #DumpTopResult(test_name) 
            DumpDetailResult(test_name)
            break

        # verify each tag_key for each line
        for key in TAG_DICT:
            if (line.find(str(TAG_DICT[key])) >= 0):
                ############################################
                ### update total result dict with tag key
                ############################################
                insert_result_to_total_dict(key)

                # package name 
                package = None
                package_found = 0
                    
                # next line to  
                line2 = ''

                ### A part
                A_LIST = q[A_SIZE:-1]
                log_result = '>'*100
                log_result += '\n'
                log_result += '\n'.join(A_LIST)
                log_result += '\n'

                ### TAG line START
                log_result += '+'*100
                log_result += '\n'

                # TAG line
                log_result += line.rstrip()
                log_result += '\n'
                
                # parse the tag line 
                tag_list = line.rstrip().split(' ')
                for tag_item in tag_list:
                    if (tag_item.find('com.')==0):
                        if (tag_item.find('/')>0):
                            char_pos = tag_item.find('/')
                            package = tag_item[0:char_pos]
                        elif (tag_item.find(',')>0):
                            char_pos = tag_item.find(',')
                            package = tag_item[0:char_pos]
                        else:
                            package = tag_item
                        insert_result_to_split_dict(key, package)
                        package_found = 1
                        break

                #####################
                # FC is one exception
                #####################
                if ((key == 'FC') and (package_found == 0)):
                    # read the next line to find package name
                    line2 = input.readline()
                    tag_list2 = line2.rstrip().split(' ')
                    for tag_item2 in tag_list2:
                        if ( tag_item2.find('com.')==0 or tag_item2.find('java.')==0):
                            if (tag_item2.find(',')>0):
                                char_pos = tag_item2.find(',')
                                package = tag_item2[0:char_pos]
                            elif (tag_item2.find(':')>0):
                                char_pos = tag_item2.find(':')
                                package = tag_item2[0:char_pos]
                            else:
                                package = tag_item2
                            insert_result_to_split_dict(key, package)
                            package_found == 1
                            break

                # not package name found
                if ( (package is None) and (package_found == 0)):                
                    # default package name
                    now3= datetime.datetime.now()
                    otherStyleTime3 = now3.strftime("%H-%M-%S")
                    package = key
                    package += '_no_package_'
                    package += otherStyleTime3
                    insert_result_to_split_dict(key, package)
                                            
                #########################################################
                ### update split result dict with tag key and packagename
                #########################################################
                #insert_result_to_split_dict(key, package)
                        
                if ((key == 'FC') and (len(line2) > 0)):
                    log_result += line2.rstrip()
                    log_result += '\n'

                ### TAG line END
                log_result += '+'*100
                log_result += '\n'

                ### B part (PIPE:readline B_SIZE times more)
                for i in range(B_SIZE):
                    B_LIST.append(input.readline().rstrip())
                log_result += '\n'.join(B_LIST)
                log_result += '\n'
                log_result += '<'*100
                log_result += '\n'
                
                #########################################################
                ### insert detailed log info detailed dict
                #########################################################
                insert_result_to_detail_dict(key, package, log_result)

                #########################################################
                # create milisec to avoid directory overwiting
                #########################################################
                now2 = datetime.datetime.now()
                otherStyleTime2 = now2.strftime("%H-%M-%S")
                milisec = time.time() * 1000
                otherStyleTime2 += '_'
                otherStyleTime2 += str(int(milisec))

                ########################################
                # dump log file for current running case
                ########################################
                get_device_log(test_name, otherStyleTime2, package, key, log_result)

                # refresh report file 
                DumpTopResult2(test_name) 
                DumpDetailResult(test_name)
                            
                A_LIST=[]
                B_LIST=[] 

    except KeyboardInterrupt, e:
        print(str(e))
        sys.exit()
        #raise

###############################################################################
# main process end
###############################################################################
