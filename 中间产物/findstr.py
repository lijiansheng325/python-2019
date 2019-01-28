#coding =gbk
import os
from glob import glob 
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