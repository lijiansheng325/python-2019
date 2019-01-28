import sys
import os

print "Hello World! \nThis is a\tPython program "

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

# x = int(raw_input("Enter x:"))
# y = int(raw_input("Enter y:"))
 
# sum = x + y
# print "He shi %s"%sum

# x1 = float(input("Enter x1:"))
# y1 = float(input("Enter y1:"))
 
# sum = x1 * y1
# print "Ji shi %f"%sum

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

personInfo = ("Diana", 32, "New York",6,999,'oooo')
name,age,country,career = ('Diana',32,'Canada','CompSci',)
print country
print personInfo
personInfo = personInfo + (1,2,3)
print personInfo
print personInfo[0]
print personInfo[5]

x = tuple(l)
print x

listNumbers = list(x)  
print listNumbers

x =  tuple(sorted(x))
print x