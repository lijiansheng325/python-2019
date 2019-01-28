import urllib 

print "downloading with urllib" 
url = 'http://www.pythontab.com/test/demo.zip'  
print "downloading with urllib"
urllib.urlretrieve(url, "demo.zip")