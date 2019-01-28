import os   
import sys 
from glob import glob 
import fnmatch
def all_files(root,patterns='*',single_level=false,yield_folders=false):
	patterns = patterns.split(';')
	for path,subdirs,files in os.walk(root):
		if yield_folders:
			files.extend(subdirs)
		files.sort()
		
		for name in files:
			for pattern in patterns:
				if fnmatch.fnmatch(name,pattern):
					yield os.path.join(path,name)
					break
		if single_level:
			break
for path in all_files('\\10.140.60.134\ivvi\20160122','*image_files*.zip'):
print path
def search_file(pattern, search_path=os.environ['PATH'], pathsep=os.pathsep):
    for path in search_path.split(os.pathsep):
        for match in glob(os.path.join(path, pattern)):
            yield match
if __name__ == '__main__':
    import sys
    if len(sys.argv)<2  or sys.argv[1].startswith('-'):
        print 'Use: %s <pattern>' % sys.argv[0]
        sys.exit(1)
    if len(sys.argv)>2:
        matchs = list(search_file(sys.argv[1],sys.argv[2]))
    else:
        matchs = list(search_file(sys.argv[1]))
    print '%d match' % len(matchs)
    for match in matchs:
        print match
 
OriginalPath = match
DestPath ="." 
print (" Original path is :" + OriginalPath )   
print (" DestPath path is :" + DestPath )  
flag =os.system("xcopy.exe"+ " " + OriginalPath + " " 
+DestPath + " " + "/y")  
print(flag) 