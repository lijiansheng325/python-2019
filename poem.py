#coding=utf-8



import sys
import random
from random import choice
import urllib.request
import re
from bs4 import BeautifulSoup
from distutils.filelist import findall
import os

#读取拼音的方法
import xpinyin

p =xpinyin.Pinyin()

# 验证xpinyin方法
#s=p.get_pinyin(u"上海");
#print(s);

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

lst4= ['人生','岁月','年华','红粉','相思','故乡','夕阳','美人'];

lst5= ['似','如','若','比'];

lst6= ['落花','流水','红豆','埃尘'];

lst7= ['昨夜','今朝','明朝','何日'];

lst8= ['复又','又重','复还','再还'];

lst9= ['来','开','生','看','梦','暖','轮'];

#定义list来承接选出来的词组
keypin11=[];

print("请输入一个字如风花雪月，小弟为你做首五言诗，前两句对仗，二四句押韵，有情有景哦！");
for line in sys.stdin:
        for value in line.split():

                print (''+''+''+''+''+''+''+'');



        break;


                #调用网页内容
with urllib.request.urlopen('https://so.gushiwen.org/mingju/') as response:
    html = response.read()



#搜索前55页的内容：思考为何55页就报错，需要加headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
def getall():
    for i in range(1,8,1):
       getalldoc(i);

#定义取网页的方法
def getalldoc(ii):
    #字符串拼接成目标网址
    #https://so.gushiwen.org/mingju/default.aspx?p=2&c=&t=
    testurl = "https://so.gushiwen.org/mingju/default.aspx?p="+str(ii)+"&c=&t=.html"
    #使用request去get目标网址
    with urllib.request.urlopen(testurl) as response:
      res = response.read();

    #创建一个BeautifulSoup对象
    soup = BeautifulSoup(res, "html.parser", from_encoding="utf-8")
    #找出目标网址中所有的a标签，函数返回的是一个list

    for ans in soup.find_all('a',href = re.compile('mingju')):

           #考虑如何读取网站的词库了，名词库

           #从list中随机获取1个元素，作为一个值返回

        for inum in range(1,500,1):
          sencha11=str();sencha12=choice(lst2);sencha13=str();sencha14=str();sencha15=str();
          keyword1=value+sencha12;


        #如果匹配成功，打印
          ansstr=str(ans);#注意返回变量不是字串，所以要转换
          if re.search(keyword1,ansstr):
            #print(keyword1);
            #把匹配好的词放入词库以备打印候选
            keypin11.append(keyword1);
            #print(keypin11);
            return


#执行定义好的方法，选出来待定的词库
getall();

#最终打印
 # 打印第一句
while keypin11:
 value=choice(keypin11);
 value1=value[0:1];
 sencha12=value[1:2];
 #print(value1);

 sencha13=choice(lst1);sencha15=choice(lst3);
 print(value+sencha13+sencha15+',');
 # 打印第二句，并判断不重复
 while True:
  value2=choice(lst);sencha22=choice(lst2);sencha23=choice(lst1);sencha25=choice(lst3);
  if value2 !=value1 and sencha22 != sencha12 and sencha23 != sencha13 and sencha25 != sencha15:
     print(value2+sencha22+sencha23+sencha25+',');
     break

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
 break;
else:
  print("小弟词穷了！");
