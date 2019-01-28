#! /usr/bin/python
# Filename: pickling.py
import cPickle as p
import sys,os
#import pickle as p
shoplistfile = 'shoplist.data'
# the name of the file where we will store the object
shoplist = [' apple' , ' mango' , ' carrot ' ]
# Write to the file
f = file(shoplistfile, 'w' )
p.dump(shoplist , f ) # dump the object to a file
f.close()
del shoplist # remove the shoplist
# Read back from the storage
f = file(shoplistfile)
storedlist = p.load(f )
print storedlist

listone = [2, 3, 4,1,5,34]
listtwo = [2*i for i in listone if 10 > i > 2]
print listtwo

def powersum(power, *args):
	'''Return the sum of each argument raised to specified power.'''
	total = 0
	for i in args:
		total += pow(i, power)
	return total
	
print powersum(2,3,4,5,6)#args=[3,4] total=pow(3,2)+pow(4,2)+pow(5,2)+pow(6,2)=86