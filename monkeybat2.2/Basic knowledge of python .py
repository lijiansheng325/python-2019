#coding=utf-8
# -*- coding:cp936 -*-
import sys
import os

print "Hello World! \nThis is a\tPython program "

#数学运算
x = 3              # an integer stored (in variable x)
f = 3.1415926      # a floating real point (in variable f)
name = "Python"    # a string
big = 358315791L   # long, a very large number
z = complex(2,3)   # (2+3i)  a complex number. consists of real and imaginary part.
 
print x ,f,"\t",name," ", big, "/", z
sum1 = x + f
sum2 = f - x
sum3 = x * big
sum4 = z / x
sum5 = name + " 2.7" 
print sum1,sum2,sum3,sum4,sum5
print "\n"

##获取键盘输入
# x = int(raw_input("Enter x:"))
# y = int(raw_input("Enter y:"))
 
# sum = x + y
# print "He shi %d"%sum

# x1 = float(input("Enter x1:"))
# y1 = float(input("Enter y1:"))
 
# sum = x1 * y1
# print "Ji shi %f"%sum

#字符串
s = "Hello Python"
print s      # prints whole string
print s[0]   # prints "H"
print s[1] # prints "e"
print s[0:2] # prints "He"
print s[2:4] # prints "ll"
print s[6:]  # prints "Python"
print s + ' ' + s # print concatenated string.
print s.replace('Hello','Thanks') # print a string with a replaced word
 
# convert string to uppercase
s = s.upper()
print s
 
# convert to lowercase
s = s.lower()
print s

q = "ll"
 
if q == s:
    print 'strings equal'
else:
	print q + " not equal " + s
if q in s:
    print q + " found in " + s

#列表
l = [ "arake", "Derp", "Derek", "Dominique" ]
 
print l                # prints all elements
l.append("Victoria")   # add element.
print l                # print all elements
l.remove("Derp")       # remove element.
l.remove("arake")      # remove element.
print l                # print all elements.
l.sort() 
print l
l.reverse()
print l

#字典
dict = {}
dict['Ford'] = "Car"
dict['Python'] = "The Python Programming Language"
dict[2] = "This sentence is stored here."
 
print dict['Ford']
print dict['Python']
print dict[2]
print dict
del dict[2]
print dict
dict[3] = 2
print dict

#元组
personInfo = ("Diana", 32, "New York",6,999,'oooo')
name,age,country,career = ('Diana',32,'Canada','CompSci',)
print country
print personInfo
personInfo = personInfo + (1,2,3)
print personInfo
print personInfo[0]
print personInfo[5]

#列表转化成元组
x = tuple(l)
print x

#元组转化为列表
listNumbers = list(x)  
print listNumbers

#元组排序
x =  tuple(sorted(x))
print x

#1、字典
dict = {'name': 'Zara', 'age': 7, 'class': 'First'}
#字典转为字符串，返回：<type 'str'> {'age': 7, 'name': 'Zara', 'class': 'First'}
print type(str(dict)), str(dict)
#字典可以转为元组，返回：('age', 'name', 'class')
print tuple(dict)
#字典可以转为元组，返回：(7, 'Zara', 'First')
print tuple(dict.values())
#字典转为列表，返回：['age', 'name', 'class']
print list(dict)
#字典转为列表
print dict.values()
#2、元组
tup=(1, 2, 3, 4, 5)
#元组转为字符串，返回：(1, 2, 3, 4, 5)
print tup.__str__()
#元组转为列表，返回：[1, 2, 3, 4, 5]
print list(tup)
#元组不可以转为字典
#3、列表
nums=[1, 3, 5, 7, 8, 13, 20];
#列表转为字符串，返回：[1, 3, 5, 7, 8, 13, 20]
print str(nums)
#列表转为元组，返回：(1, 3, 5, 7, 8, 13, 20)
print tuple(nums)
#列表不可以转为字典
#4、字符串
#字符串转为元组，返回：(1, 2, 3)
print tuple(eval("(1,2,3)"))
#字符串转为列表，返回：[1, 2, 3]
print list(eval("(1,2,3)"))
#字符串转为字典，返回：<type 'dict'>
print type(eval("{'name':'ljq', 'age':24}"))