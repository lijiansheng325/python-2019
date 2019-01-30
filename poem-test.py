#coding=utf-8
#!/usr/bin/env python

import os
import sys
import random
from random import choice
import urllib.request
import re
from bs4 import BeautifulSoup
from distutils.filelist import findall
#读取拼音的方法
import xpinyin

p =xpinyin.Pinyin()
#定义全局变量，为每句关键词在网页匹配
keyword1=str("href");
keyword2=str();
sencha11=str();sencha12=str();sencha13=str();sencha14=str();sencha15=str();
sencha21=str();sencha22=str();sencha23=str();sencha24=str();sencha25=str();
sencha31=str();sencha32=str();sencha33=str();sencha34=str();sencha35=str();
sencha41=str();sencha42=str();sencha43=str();sencha44=str();sencha45=str();

value=str();value1=str();value2=str();value3=str();value4=str();

#定义题目词库
lst0 = ['风','花','雪','月','云','日','水'];
#定义所有词库
lst = ['风','花','雪','月','天','地','水','楼','烟'];
#定义地点词库
lst1 = ['长安','北平','苏杭','临安','天水','苍空','大漠','沧海','平兆','洛阳','大江','苍穹','京都','开封','邯郸','泰山','黄山','五岳','华山','楚天','长沙','五台'];
#定义初始动词库，'出','升','落','降','满','映','华','探','照',
lst2= ['射','起','悲','出','升','落','降','满','映','探','照','轻','凋','落'];
#定义初始形容词库和后续词库
lst3= ['晚','浅','清','圆','南','明','远','白'];

lst4= ['人生','岁月','年华','红粉','相思','故乡','夕阳','美人','家园','父老','亲人'];

lst5= ['似','如','若','比'];

lst6= ['落花','流水','红豆','埃尘'];

lst7= ['昨夜','今朝','明朝','何日'];

lst8= ['复又','又重','复还','再还'];

lst9= ['来','开','生','看','梦','暖','轮'];

#定义list来承接选出来的词组
keypin11=[];


print("请输入一个字如风花雪月");
for line in sys.stdin:
        for value in line.split():

                print ('--------------'+''+''+''+''+''+''+'');



        break;

sencha12=choice(lst2);sencha13=choice(lst1);sencha15=choice(lst3);
print(value+sencha12+sencha13+sencha15+',');



while True:
 value2=choice(lst);sencha22=choice(lst2);sencha23=choice(lst1);sencha25=choice(lst3);
 if value2 !=value1 and sencha22 != sencha12 and sencha23 != sencha13 and sencha25 != sencha15:
    print(value2+sencha22+sencha23+sencha25+',');
    break

'''
for i in range(2):
    while True:
     value2=choice(lst);sencha22=choice(lst2);sencha23=choice(lst1);sencha25=choice(lst3);
     if value2 !=value1 and sencha22 != sencha12 and sencha23 != sencha13 and sencha25 != sencha15:
        print(value2+sencha22+sencha23+sencha25+',');
        break
'''
# 打印第三句
value3=choice(lst4);sencha32=choice(lst5);sencha33=choice(lst6);
print(value3+sencha32+sencha33+',');
# 打印第四句，并判断和第二句押韵
value4=choice(lst7);sencha42=choice(lst8);
s=p.get_pinyin(sencha25);
tt=(s[-2:]);
while True:
 sencha43=choice(lst9);
 s1=p.get_pinyin(sencha43);
 tt1=(s1[-2:]);
 if tt1==tt:
    print(value4+sencha42+sencha43+'。');
    break;
