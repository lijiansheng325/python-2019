#!/usr/bin/env python 
# 
# Copyright (c) 2012 The Chromium Authors. All rights reserved. 
# Use of this source code is governed by a BSD-style license that can be 
# found in the LICENSE file. 

import os
import sys
import time
import datetime

device_log = {}
report_result = {}
log_parser_output_path = ''
event_log_file = 'eventlog'
log_parser_report_path = 'reports'
log_parser_report_file = 'reports.txt'

if 2 <= len(sys.argv) <= 3: 
    print 'log_parser_reporter: Initializing' 
    log_parser_output_path = sys.argv[1:3][0]
else: 
    print 'Usage: %s <log_parser_ouput_dir>' % sys.argv[0] 
    sys.exit(0)

event_file = file(os.path.join(log_parser_output_path, event_log_file), 'r')
lines = event_file.readlines()
event_file.close()

mark = 0
numLines = len(lines)

while mark < numLines:
    line = lines[mark]
    if line.find("started") > 0:
        items = line.rstrip().split(' ')
        device_log[(items[7], items[11])] = items[0:2]
    elif line.find("died") > 0:
        items = line.rstrip().split(' ')
        device_log[(items[7], items[11])] = items[0:2]
    mark += 1

for key in device_log:
    if key[1].find('started') >= 0:
        report_result[key[0]] = device_log[key][0] + " " + device_log[key][1]


for key in device_log:
    if key[1].find('died') >= 0:
        start_string = report_result[key[0]]
        end_string = device_log[key][0] + " " + device_log[key][1]

        print '\n\nDone:'        
        print 'test name: ' + key[0]
        print 'start: ' + start_string.split(',')[0]
        print 'end: ' + end_string.split(',')[0]

        start_datetime = time.mktime(time.strptime(start_string.split(',')[0], 
                                                   "%Y-%m-%d %H:%M:%S"))
        end_datetime = time.mktime(time.strptime(end_string.split(',')[0], 
                                                 "%Y-%m-%d %H:%M:%S"))
        print 'Duration: ' + str(datetime.timedelta(seconds=end_datetime - start_datetime))
        report_result[key[0]] = 'Duration: ' + str(datetime.timedelta(seconds=end_datetime - start_datetime))

        print 'Result:'
        try:
            log_parser_path = os.path.join(log_parser_output_path, key[0])
            report_path = os.path.join(log_parser_report_path, log_parser_report_file)
            #fh = open('./temp/'+key[0]+'/reports/reports.txt', 'r')
            fh = open(os.path.join(log_parser_path, report_path), 'r')
            lines = fh.readlines()
            fh.close()

            for line in lines:
                print line.rstrip()            
        except Exception,e:
            print str(e)
            pass
        print ''
  
for key in report_result:
    if report_result[key].find('Duration') < 0:        
        start_datetime = time.mktime(time.strptime(report_result[key].split(',')[0], "%Y-%m-%d %H:%M:%S"))
        local_datetime = time.mktime(time.localtime())          
        print 'Still running:'
        print 'test name: ' + key
        print 'start: ' + report_result[key].split(',')[0]        
        print 'Duration: ' + str(datetime.timedelta(seconds=local_datetime - start_datetime))      
        print 'Result:'
        try:
            log_parser_path = os.path.join(log_parser_output_path, key)
            report_path = os.path.join(log_parser_report_path, log_parser_report_file)
            fh = open(os.path.join(log_parser_path, report_path), 'r')
            lines = fh.readlines()
            fh.close()

            for line in lines:
                print '    ' + line.rstrip()            
        except Exception,e:
            print str(e)
            pass
        print ''

