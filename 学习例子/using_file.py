#! /usr/bin/python
# Filename: using_file.py
poem = ''' \
Programming is fun
When the work is done
if you wanna make your work also fun:
use Python!
'''
f = file('poem.txt' , 'w' ) # open for ' w'riting
f.write(poem) # wri t e t ext t o f i l e
f.close() # cl ose t he f i l e
f = file('poem.txt' )
# if no mode is specified, ' r'ead m ode is assumed by default
while True:
	line = f.readline()
	if len(line) == 0: # Zero length indicates EOF
		break
	print line,
# Notice comma to avoid automatic newline added by Python
f.close() # close the file