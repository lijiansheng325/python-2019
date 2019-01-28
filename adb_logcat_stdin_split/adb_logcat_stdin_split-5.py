# -*- coding: cp936 -*-
## function: remove file 
## remark: python version 2-7-3

import os
import sys
from datetime import datetime

import signal
import getopt
import glob

from xml.etree import ElementTree
from xml.dom import minidom

from xml.etree.ElementTree import Element, SubElement, Comment
#from ElementTree_pretty import prettify



TAG_DICT = {
    "CRASH_TAG": "CRASH",
    "ANR_0": "Application is not responding",
    "ANR_1": "ANR in",
    "FC": "FATAL EXCEPTION",
    "TC": "Tombstone written to: /data/tombstones"   
}

CRASH_DICT = dict()
ANR_DICT = dict()
FC_DICT = dict()
TC_DICT = dict()


def insert_result_to_dict(dict_name, log_key, log_result):
    if dict_name == 'CRASH_TAG':
        CRASH_DICT[log_key] = log_result
    elif dict_name == 'ANR_0':
        ANR_DICT[log_key] = log_result
    elif dict_name == 'ANR_1':
        ANR_DICT[log_key] = log_result
    elif dict_name == 'FC':
        FC_DICT[log_key] = log_result
    elif dict_name == 'TC':
        TC_DICT[log_key] = log_result

def parse_logcat_file(filename, log_key, log_tag, context_size):
    line_num = 0
    fd = open(filename)  
    content_list = fd.readlines()  
    fd.close()

    i = 0    
    q = []
    q_bk = []
    found_tag = 0
    tag_result = ''
    tag_key = ''
        
    for line in content_list:  
        q.append(line.rstrip())
        line_num = line_num + 1
        i = i + 1

        if (i == context_size):
            for item in q:
                if (item.find(log_tag) >= 0 ):
                    found_tag = 1

            if (found_tag == 1):
                #print log_tag
                for item_previous in q_bk:
                    tag_result = tag_result + item_previous + '\n'
                for item in q:
                    if (item.find(log_tag) >= 0 ):
                        #sys.stdout.write('=========================\''+ log_tag +'\' found in '+ filename +'::'+ str(line_num) + '===========================\n')
                        tag_key = filename +'::'+ str(line_num)
                        tag_result = tag_result + '=========================\n'+ item + '\n=========================\n'
                    else:
                        tag_result = tag_result + item + '\n'
                insert_result_to_dict(log_key, tag_key, tag_result)
                #sys.stdout.write(tag_result + '\n')                
            else:
                q_bk[:] = []
                q_bk = list(q)

            found_tag = 0
            i = 0
            q[:] = []
            tag_key = ''
            tag_result = ''

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def dump_dict_to_xml(xml_node, dict):
    for key in dict:
        SubElement(xml_node, "log", name=key).text = dict[key]

def GenerateXML():
    top = Element('top')
    comment = Comment('Generated for LogParser')
    top.append(comment)

    dump_dict_to_xml(SubElement(top, 'anr'), ANR_DICT)
    dump_dict_to_xml(SubElement(top, 'fc'), FC_DICT)
    dump_dict_to_xml(SubElement(top, 'crash'), CRASH_DICT)
    dump_dict_to_xml(SubElement(top, 'tc'), TC_DICT)
    #print prettify(top)

    xml_lines = prettify(top)

    if (len(str(xml_lines)) > 90):
        file_handler=open('report.txt','a')
        for key in ANR_DICT:
            file_handler.write(ANR_DICT[key])
        
        for key in FC_DICT:
            file_handler.write(FC_DICT[key])

        for key in CRASH_DICT:
            file_handler.write(CRASH_DICT[key])

        for key in TC_DICT:
            file_handler.write(TC_DICT[key])
        
        file_handler.close()
    
q = []
i = 0
split_size = 1000
context_size = 10

input = os.popen("adb logcat -c && adb logcat -v threadtime ")

while True:
    try:
        line = input.readline()
        q.append(line)
        i = i + 1
    except KeyboardInterrupt:
        sys.stdout.flush()
        break

    if (i == split_size):
        file_name_time_stamp = datetime.now()
        log_filename = file_name_time_stamp.strftime('%Y-%m-%d-%H-%M-%S')
        print 'Start writing file: \n' + log_filename
        
        file_handler=open(log_filename,'w')
        for item in q:
            file_handler.write(item)
        file_handler.close()

        print 'End writing file\n'


        print 'Start parsing file: \n ' + log_filename
        
        for key in TAG_DICT:
            parse_logcat_file(log_filename, key, TAG_DICT[key], context_size)
            
        print 'End parsing\n'

        GenerateXML()
        
        i = 0        
        q[:] = []


