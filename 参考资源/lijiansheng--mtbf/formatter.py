import csv
import os,sys
import time
import string
try:
	from django.template.loader import get_template
except Exception, e:
	print "It appears that Django is not installed. Please install Django"
	print "from the included file Django-1.2.3.tar.gz. The version of "
	print "Django available with your Linux distribution, if you are "
	print "using one, may not be suitable. Unzip and untar the zip "
	print "into any directory, cd into the folder, and, as "
	print "administrator, run:"
	print "python setup.py install"
	sys.exit()
from django.template import Context
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
reload(sys)
sys.setdefaultencoding('utf-8')

class PssCsvReader():
	def __init__(self, soureFolder,resultFolder,totalMemNum):
		self.csvFile = csv.DictReader(file(soureFolder+"/procrank.csv", 'rb'))
		self.plist = []#cmdline names
		self.tempdict = {}
		for row in self.csvFile:
			timestamp = row['Second']
			if not self.tempdict.has_key(timestamp):
				self.tempdict[timestamp] = {}
			pname = row['cmdline']
			if not pname in self.plist:
				self.plist.append(pname)
			pss = row['Pss']
			self.tempdict[timestamp].update({pname:pss})
                totalMemFile = csv.DictReader(file(soureFolder+"/freemem.csv", 'rb'))
                pnameUsedMem = "TotalUsedMem"
                self.plist.append(pnameUsedMem)
                for row in totalMemFile:
			timestamp = row['Second']
                        freeMem = row['freemem']
                        usedMem = int(totalMemNum) - int(freeMem)
                        if not self.tempdict.has_key(timestamp):
				self.tempdict[timestamp] = {}
                        self.tempdict[timestamp].update({pnameUsedMem:usedMem})
			
	def getProcessList(self):
		if self.plist[0] != 'Second':
			self.plist.insert(0, 'Second')
		return self.plist

        def getTop5ProcessList(self,sourceFolder):
		topFile = open(sourceFolder+"/cmdline.txt","r") 
		self.toplist = []#top 5 cmdline names
		for line in topFile.readlines():
			line=line.strip('\n')
                        self.toplist.append(line)
                self.toplist.append("TotalUsedMem")
                return self.toplist
	
	def getRowData(self):
		data = []
		for key, value in self.tempdict.items():
			value.update({'Second':key})
			data.append(value)
		data.sort(key=lambda data : int(data['Second']))
		return data			
	
class PssCsvWriter():
	def __init__(self, path, fieldname):
		self.writer = csv.DictWriter(file(path+"/out.csv", 'wb'), fieldnames=fieldname,restval="0")
	
	def generateCsvFile(self, rowData):
		self.writer.writerows(rowData)

class CpuCsvReader():
	def __init__(self, sourceFolder):
		self.csvFile = csv.DictReader(file(sourceFolder+"/top.csv", 'rb'))
		self.plist = []#cmdline names
		self.tempdict = {}
		for row in self.csvFile:
			timestamp = row['Second']
			if not self.tempdict.has_key(timestamp):
				self.tempdict[timestamp] = {}
			pname = row['cmdline']
			if not pname in self.plist:
				self.plist.append(pname)
			cpu = row['CPU%']
			self.tempdict[timestamp].update({pname:cpu})
			
	def getProcessList(self):
		if self.plist[0] != 'Second':
			self.plist.insert(0, 'Second')
		return self.plist

        def getTop5ProcessList(self,sourceFolder):
		topFile = open(sourceFolder+"/name.txt","r") 
		self.toplist = []#top 5 cmdline names
		for line in topFile.readlines():
			line=line.strip('\n')
                        self.toplist.append(line)
                return self.toplist
	
	def getRowData(self):
		data = []
		for key, value in self.tempdict.items():
			value.update({'Second':key})
			data.append(value)
		data.sort(key=lambda data : int(data['Second']))
		return data			
	
class CpuCsvWriter():
	def __init__(self, path, fieldname):
		self.writer = csv.DictWriter(file(path+"/topout.csv", 'wb'), fieldnames=fieldname,restval="0")
	
	def generateCsvFile(self, rowData):
		self.writer.writerows(rowData)
		
def main(argv):
	time1= time.time()
	if len(argv) != 4:
		print "Letv Csv format convert for chart Ver 0.3"
		print "Usage:"
		print "python formatter.py <sourceFolder> <outFolder> <allMemNumInThisDevice>"
		sys.exit()
	cr = PssCsvReader(argv[1],argv[2],argv[3])
	pl = cr.getProcessList()
        tl = cr.getTop5ProcessList(argv[1])
	cw = PssCsvWriter(argv[2], pl)
	cw.generateCsvFile(cr.getRowData())
	from django.conf import settings
	settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
 			TEMPLATE_DIRS=(os.path.dirname(os.path.abspath(__file__)),))
	djangoVersion = django.get_version()[0:3]
	if djangoVersion == '1.7':
 		django.setup()
        tmp = get_template("htmlTemplate/pssPicTemp.htm")
	rd = {'datafields':pl}        
        top = {'top5processes':tl}
        rd.update(top)
        html = tmp.render(Context(rd))
	with open(argv[2]+"/pssPic.htm", 'w') as fp:
		fp.write(html)
	time2= time.time()
	print "pss convert finished. Cost time:"+str(time2-time1)+ " sec."
        
	cr = CpuCsvReader(argv[1])
	pl = cr.getProcessList()
        tl = cr.getTop5ProcessList(argv[1])
	cw = CpuCsvWriter(argv[2], pl)
	cw.generateCsvFile(cr.getRowData())
        tmp = get_template("htmlTemplate/topPicTemp.htm")
	rd = {'datafields':pl}        
        top = {'top5processes':tl}
        rd.update(top)
        html = tmp.render(Context(rd))
	with open(argv[2]+"/topPic.htm", 'w') as fp:
		fp.write(html)
	time2= time.time()
	print "cpu convert file finished. Cost time:"+str(time2-time1)+ " sec."

if __name__ == '__main__':
	main(sys.argv)
