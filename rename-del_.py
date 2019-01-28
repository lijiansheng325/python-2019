import os;
def rename():
	path='.';
	filelist=os.listdir(path) 
	for files in filelist:
		Olddir=os.path.join(path,files);
		if os.path.isdir(Olddir):
			continue;
		filename=os.path.splitext(files)[0];
		filetype=os.path.splitext(files)[1];
		if filename.find('_')>=0:
			Newdir=os.path.join(path,filename.split('_', 1)[0]+filename.split('_', 1)[1]+filetype);

			if not os.path.isfile(Newdir):
				os.rename(Olddir,Newdir);
rename();