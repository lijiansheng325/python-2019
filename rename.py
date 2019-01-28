#RenameRand.py  
#Yanggd 2012/9/7  
#get file name, and then rename the file  
#after renamed, the name likes this:[a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][0-9]  
  
import random  
import os  
  
existName = []  
  
def renameRand(path):  
    fileList = os.listdir(path) #list the file name  
    rangeLetter=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')  
    for oldFileNameAndExt in fileList:  
        newFileName = random.choice(rangeLetter)+random.choice(rangeLetter)+ \
        str(random.randrange(10))+str(random.randrange(10))+random.choice(rangeLetter)+str(random.randrange(10))  
        while newFileName.upper() in existName:  
            newFileName = random.choice(rangeLetter) + random.choice(rangeLetter)+ \
            str(random.randrange(10))+str(random.randrange(10))+random.choice(rangeLetter)+str(random.randrange(10))  
        existName.append(newFileName.upper())  
        [oldFileName, fileExt] = oldFileNameAndExt.split('.', 1)  
        newFileNameAndExt = [newFileName, fileExt]  
        newFileNameAndExt = '.'.join(newFileNameAndExt)  
        path = os.path.abspath(path)  
        pathSrc = path + '\\' + oldFileNameAndExt  
        pathDst = path + '\\' + newFileNameAndExt  
        os.rename(pathSrc, pathDst)  
  
if __name__ == '__main__':  
    renameRand(r'D:\Test\rename')  