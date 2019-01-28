#!/usr/bin/python 
import os
import re
import csv
import subprocess  
import json
import sys
import shutil
#import matplotlib
#matplotlib.use('Agg')
#from matplotlib.pyplot import plot, savefig
#import matplotlib.pyplot as plt

def mem_analyzer(app_name, csv_file_name, csv_header, loop_num, 
                 ui_auto_cmd, adb_dump_mem_cmd, output_path):

    csv_file_path = os.path.join(output_path, csv_file_name)

    # csv file stored meminfo
    file = open(csv_file_path,'w')
    writer = csv.writer(file)
    writer.writerow(csv_header)

    free_id = []
    free_value = []

    # test loop
    for i in range(1, loop_num):
        print "mem_leak_analyzer test %s" %i
        s=subprocess.Popen(ui_auto_cmd)
        s.wait()

        # capature meminfo 
        output=os.popen(adb_dump_mem_cmd)
        # default value
        aa = 0 
        bb = 0
        cc = 0
        dd = 0
        ee = 0

        for line in output.readlines():
            if "Total RAM" in line :
                a = re.split(r"K",line)
                a1 = re.split(":",a[0])
                print a1[1]
                aa = a1[1]
            if "Free RAM" in line:
                b = re.split(r"K",line)
                b1 = re.split(":",b[0])
                print b1[1]
                bb = b1[1]
            if "Used RAM" in line:
                c = re.split(r"K",line)
                c1 = re.split(":",c[0])
                print c1[1]
                cc = c1[1]
            if "Lost RAM" in line:
                d = re.split(r"K",line)
                d1 = re.split(":",d[0])
                print d1[1]
                dd = d1[1]
            # check target appname in line  
            if app_name in line:
                e = re.split(r"K",line)
                print e[0]
                ee = e[0]

        free_id.append(i)
        free_value.append(bb)

        writer.writerow([i,aa, bb, cc,dd,ee,app_name])
    file.close()

#    plt.figure()    
#    plt.plot(free_id, free_value, '--ob')
#    plt.title("Free Memory Trends")
#    plt.ylabel('Free Mem')
#    plt.xlabel('Case Number')
#    plt.xticks(free_id)
#    plt.autoscale(enable=False, tight=False)
#    plt.ticklabel_format(style='plain')
#    plt.grid(True)
#   plt.savefig(csv_file_path+'.png', dpi=96)

    for line in open(csv_file_path):
        print (line)

try:
    if 2 <= len(sys.argv) <= 3: 
        print 'mem_leak_analyzer: Initializing' 
        OUTPUT_PATH = sys.argv[1:3][0]
        if os.path.exists(OUTPUT_PATH): 
            print 'mem_leak_analyzer: %s already exists? Cleaning' % OUTPUT_PATH
            shutil.rmtree(OUTPUT_PATH, ignore_errors=True)
        			
        os.makedirs(OUTPUT_PATH) 
        print 'mem_leak_analyzer: output directory %s' % OUTPUT_PATH

        json_file='mem_leak_analyzer.json'
        json_data=open(json_file)
        data = json.load(json_data)
        json_data.close()

        for key, value in data.items():
            if key.find("common") >= 0:            
                ADB_DUMP_MEM_CMD = str(data[key]["ADB_DUMP_MEM_CMD"])
                CSV_HEADER = str(data[key]["CSV_HEADER"]).split('_')

        for key, value in data.items():
            if key.find("case_list") >= 0:
                for case_key, case_value in value.items():
                    APP_NAME = str(data[key][case_key]["APP_NAME"])
                    CSV_FILE_NAME = str(data[key][case_key]["CSV_FILE_NAME"])
                    UI_AUTO_CMD = str(data[key][case_key]["UI_AUTO_CMD"]).split()
                    LOOP_NUM = data[key][case_key]["LOOP_NUM"]
                    print APP_NAME					
                    # memory analyzer
                    mem_analyzer(APP_NAME, CSV_FILE_NAME, CSV_HEADER, LOOP_NUM, 
                                 UI_AUTO_CMD, ADB_DUMP_MEM_CMD, OUTPUT_PATH)
    else:
        print 'Usage: %s <output_dir>' % sys.argv[0] 

except Exception, e:
    print str(e)
    sys.exit()
