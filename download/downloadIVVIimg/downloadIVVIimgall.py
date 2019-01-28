#coding=GBK
import os   
import sys 
from glob import glob 
import fnmatch
import shutil

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


def search_file(search_path=os.environ['PATH'], pathsep=os.pathsep):
	for path1 in search_path.split(os.pathsep):
		
		for source_path in all_files(path1,'*image_files*.zip;'):
		#for source_path in all_files(path1,'*.txt;'):
			#print source_path
			Y = source_path
			#print Y
			Y1 = Y.rsplit('\\',2)[1].rsplit('_',1)[1]
			Y2 = Y.rsplit('\\',2)[2].rsplit('.',1)[0]
			target_path = Y2 + "_" + Y1 + ".zip"
			shutil.copyfile(source_path, target_path)


		

if __name__ == '__main__':
    
    if len(sys.argv)<2  or sys.argv[1].startswith('-'):
        print 'Use: %s <work_path>' % sys.argv[0]
        sys.exit(1)
    else:
        search_file(sys.argv[1])