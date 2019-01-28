import os   
import sys 
from glob import glob 
import fnmatch

def all_files(root,patterns='*',single_level=False,yield_folders=False):
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
			
def search_file(pattern, search_path=os.environ['PATH'], pathsep=os.pathsep):
    for path1 in search_path.split(os.pathsep):
        for path in all_files(path1,'*image_files*.zip;'):
			print path
if __name__ == '__main__':
    import sys
    if len(sys.argv)<2  or sys.argv[1].startswith('-'):
        print 'Use: %s <pattern>' % sys.argv[0]
        sys.exit(1)
    if len(sys.argv)>2:
        search_file(sys.argv[1],sys.argv[2])
    else:
        search_file(sys.argv[1])
    
    
	


