# -*- coding: utf-8 -*-
import os
import sys
import threading
import time
import zipfile

import datetime as dt
import pandas as pd


reload(sys)
sys.setdefaultencoding( "utf-8" )

def copyFiles(sourceDir, targetDir):
    copyFileCounts = 0
    print sourceDir
    print '%s copy %s the %sth file'%(dt.datetime.now(), sourceDir,copyFileCounts)
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        
        if os.path.isfile(sourceF):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print '%s %s finish copying'%(dt.datetime.now(), targetF)
            else:
                print '%s %s exist'%(dt.datetime.now(), targetF)
           
        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)

def dirtozip(startdir,zipPath):
    f=zipfile.ZipFile(zipPath,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename),os.path.join(dirpath,filename).replace(startdir,""))
    f.close()
    
class csvtojsonthread(threading.Thread):
    def __init__(self, csvtojson):
        threading.Thread.__init__(self, name = 'mcmtojson')
        self.csvtojson=csvtojson
    def run(self):
        self.csvtojson

class mcmtojson():
    def main(self,csvPath,resultPath):
        if len(open('%s/cpu.csv'%csvPath).readlines()) > 1:
            thread = csvtojsonthread(self.cpu('%s/cpu.csv'%csvPath,resultPath))
            thread.setDaemon(True)
            thread.start()
        if len(open('%s/cpuinfo.csv'%csvPath).readlines()) > 1:
            thread = csvtojsonthread(self.cpuinfo('%s/cpuinfo.csv'%csvPath,resultPath))
            thread.setDaemon(True)
            thread.start()
        if len(open('%s/mem.csv'%csvPath).readlines()) > 1:
            thread = csvtojsonthread(self.mem('%s/mem.csv'%csvPath,resultPath))
            thread.setDaemon(True)
            thread.start()
        if len(open('%s/meminfo.csv'%csvPath).readlines()) > 1:
            thread = csvtojsonthread(self.meminfo('%s/meminfo.csv'%csvPath,resultPath))
            thread.setDaemon(True)
            thread.start()
        
    def json_w(self,filePath,json_data):
        import json
        with open(filePath, 'w') as f:
            f.write(json.dumps(json_data))
            
    def cpu(self,csvPath,resultPath):
        data=pd.read_csv(r'%s'%csvPath,warn_bad_lines=False,error_bad_lines=False).fillna(value='null')
        sleep_time=int(data.columns[0].replace('Loop:',''))
        if sleep_time == 1 :
            unit_time=300
        elif sleep_time == 2 :
            unit_time=600
        elif sleep_time < 5 :
            unit_time=900
        elif sleep_time < 10 :
            unit_time=1800
        else:
            unit_time=3600
        sleep_loop=unit_time/sleep_time
        hours=int(data.index[-1])*sleep_time/unit_time
        if int(data.index[-1])*sleep_time%unit_time > 0:
            hours=hours+1
        json_avg={"sleep":sleep_time,"map_times":hours}
        self.json_w(r'%s/avg.json'%resultPath, json_avg)
        print 'cpu.csv'
        print '%s cpu Hours=%s'%(dt.datetime.now(),hours)
        for i in range(1,hours+1):
            print '%s cpu hour: %s/%s'%(dt.datetime.now(),i,hours)
            if not os.path.exists(r'%s/hour_%s'%(resultPath,i)):
                os.mkdir(r'%s/hour_%s'%(resultPath,i))
            data_hour=data[(data.index<i*sleep_loop)&(data.index>=(i-1)*sleep_loop)]
            json_activity={'act':data_hour['Activity'].values.tolist()}
            json_date={'data_time':data_hour['Data Time'].values.tolist()}
            Loops=(data_hour[data.columns[0]]*sleep_time).values.tolist()
            Time=data_hour['Time'].values.tolist()
            usr=data_hour['usr'].values.tolist()
            sys=data_hour['sys'].values.tolist()
            nic=data_hour['nic'].values.tolist()
            idle=data_hour['idle'].values.tolist()
            io=data_hour['io'].values.tolist()
            irq=data_hour['irq'].values.tolist()
            sirq=data_hour['sirq'].values.tolist()
            json_cpu={'loop':Loops,'time':Time,'usr':usr,'sys':sys,'nic':nic,'idle':idle,'io':io,'irq':irq,'sirq':sirq}
            self.json_w(r'%s/hour_%s/activity.json'%(resultPath,i), json_activity)
            self.json_w(r'%s/hour_%s/data.json'%(resultPath,i), json_date)
            self.json_w(r'%s/hour_%s/cpu.json'%(resultPath,i), json_cpu)
        print '%s cpu Finish'%dt.datetime.now()
        
    def cpuinfo(self,csvPath,resultPath):
        data=pd.read_csv(r'%s'%csvPath,warn_bad_lines=False,error_bad_lines=False).fillna(value='null')
        sleep_time=int(data.columns[0].replace('Loop:',''))
        if sleep_time == 1 :
            unit_time=300
        elif sleep_time == 2 :
            unit_time=600
        elif sleep_time < 5 :
            unit_time=900
        elif sleep_time < 10 :
            unit_time=1800
        else:
            unit_time=3600
        sleep_loop=unit_time/sleep_time
        hours=data[data.columns[0]].tail(1).values[0]*sleep_time/unit_time
        if data.index[-1]*sleep_time%unit_time > 0:
            hours=hours+1
        if os.path.exists(r'%s/maxcpu.csv'%csvPath):
            os.remove(r'%s/maxcpu.csv'%csvPath)
        f=open(r'%s/maxcpu.csv'%os.path.dirname(csvPath),'w')
        f.write('Hours,Process_Name,cpu%,json Name')
        f.close()
        print 'cpuinfo.csv'
        for i in range(1,hours+1):
            h=0
            if not os.path.exists(r'%s/hour_%s'%(resultPath,i)):
                os.mkdir(r'%s/hour_%s'%(resultPath,i))
            data_hour=data[(data[data.columns[0]].values<i*sleep_loop)&(data[data.columns[0]].values>=(i-1)*sleep_loop)]
            Command=data_hour['Command'].unique().tolist()
            print '%s cpuinfo hour: %s/%s'%(dt.datetime.now(),i,hours)
            maxcpu=[]
            for c in Command:
                #print '%s cpuinfo Command: %s'%(dt.datetime.now(),c)
                h=h+1
                data_command=data_hour[data_hour['Command'].values==c]
                Loops=(data_command[data_command.columns[0]]*sleep_time).values.tolist()
                Tims=data_command['Time'].values.tolist()
                Pid=data_command['PID'].values.tolist()
                CPU=data_command['%CPU'].values.tolist()
                CPU_max=max(CPU)
                AVG=data_command['Thread/avgs'].values.tolist()
                tmp=len(Loops)
                p=0
                l=0
                for l in range(1,tmp):
                    p=p+1
                    if Loops[p] == Loops[p-1]:
                        CPU[p]=[CPU[p],2,Pid[p]]
                    else:
                        if Pid[p] != Pid[p-1]:
                            CPU[p]=[CPU[p],1]
                        if Loops[p] > Loops[p-1]+sleep_time:
                            Loops.insert(p,Loops[p]-1)
                            Loops.insert(p,Loops[p-1]+1)
                            Tims.insert(p,Tims[p]-1)
                            Tims.insert(p,Tims[p-1]+1)
                            Pid.insert(p,0)
                            Pid.insert(p,0)
                            CPU.insert(p,0)
                            CPU.insert(p,0)
                            AVG.insert(p,AVG[p-1])
                            AVG.insert(p,AVG[p-1])
                            p=p+2
                json_cpuinfo={"name":c,"loop":Loops,"time":Tims,"avg":AVG,"cpu":CPU}
                self.json_w(r'%s/hour_%s/cpuinfo%s.json'%(resultPath,i,h), json_cpuinfo)
                maxcpu.append(['%s'%c,CPU_max,'cpuinfo%s'%h])
            maxcpu.sort(key=lambda a_tuple:a_tuple[1],reverse=True)
            json_cpuline={"maxcpu":maxcpu}
            self.json_w(r'%s/hour_%s/cpuline.json'%(resultPath,i), json_cpuline)
            l=0
            f=open(r'%s/maxcpu.csv'%os.path.dirname(csvPath),'a')
            for l in range(1,len(maxcpu)):
                f.write('/n%s,%s,%s,%s'%(i,maxcpu[l][0],maxcpu[l][1],maxcpu[l][2]))
            f.close()
        print '%s cpuinfo Finish'%dt.datetime.now()
            
    def mem(self,csvPath,resultPath):
        data=pd.read_csv(r'%s'%csvPath,warn_bad_lines=False,error_bad_lines=False).fillna(value='null')
        sleep_time=int(data.columns[0].replace('Time:',''))
        if sleep_time == 1 :
            unit_time=300
        elif sleep_time == 2 :
            unit_time=600
        elif sleep_time < 5 :
            unit_time=900
        elif sleep_time < 10 :
            unit_time=1800
        else:
            unit_time=3600
        sleep_loop=unit_time/sleep_time
        hours=data.index[-1]*sleep_time/unit_time
        if data.index[-1]*sleep_time%unit_time > 0:
            hours=hours+1
        print 'mem.csv'
        for i in range(1,hours+1):
            print '%s mem hour: %s/%s'%(dt.datetime.now(),i,hours)
            if not os.path.exists(r'%s/hour_%s'%(resultPath,i)):
                os.mkdir(r'%s/hour_%s'%(resultPath,i))
            data_hour=data[(data.index<i*sleep_loop)&(data.index>=(i-1)*sleep_loop)]
            Loops=(data_hour.index*sleep_time).values.tolist()
            Time=data_hour[data.columns[0]].values.tolist()
            MemFree=(data['MemFree']/1024).values.tolist()
            Buffers=(data['Buffers']/1024).values.tolist()
            Cached=(data['Cached']/1024).values.tolist()
            Active=(data['Active']/1024).values.tolist()
            Inactive=(data['Inactive']/1024).values.tolist()
            Active_a=(data['Active(anon)']/1024).values.tolist()
            Inactive_a=(data['Inactive(anon)']/1024).values.tolist()
            Active_f=(data['Active(file)']/1024).values.tolist()
            Inactive_f=(data['Inactive(file)']/1024).values.tolist()
            Dirty=(data['Dirty']/1024).values.tolist()
            Writeback=(data['Writeback']/1024).values.tolist()
            Mapped=(data['Mapped']/1024).values.tolist()
            Slab=(data['Slab']/1024).values.tolist()
            IO=((data['Dirty']+data['Writeback'])/1024).values.tolist()
            if len(data.columns) == 15:
                CMAFree=(data['CMA Free']/1024).values.tolist()
                Free=((data['MemFree']+data['Buffers']+data['Cached']-data['CMA Free'])/1024).values.tolist()
            else:
                Free=((data['MemFree']+data['Buffers']+data['Cached'])/1024).values.tolist()
            for l in range(len(Loops)):
                MemFree[l]=round(MemFree[l],2)
                Buffers[l]=round(Buffers[l],2)
                Cached[l]=round(Cached[l],2)
                Active[l]=round(Active[l],2)
                Inactive[l]=round(Inactive[l],2)
                Active_a[l]=round(Active_a[l],2)
                Inactive_a[l]=round(Inactive_a[l],2)
                Active_f[l]=round(Active_f[l],2)
                Inactive_f[l]=round(Inactive_f[l],2)
                Dirty[l]=round(Dirty[l],2)
                Writeback[l]=round(Writeback[l],2)
                Mapped[l]=round(Mapped[l],2)
                Slab[l]=round(Slab[l],2)
                IO[l]=round(IO[l],2)
                if len(data.columns) == 15:
                    CMAFree[l]=round(CMAFree[l],2)
                Free[l]=round(Free[l],2)
            if len(data.columns) == 15:
                json_mem={'loop':Loops,'time':Time,'free':Free,'io':IO,'active':Active,'inactive':Inactive,'mapped':Mapped,'slab':Slab,'memfree':MemFree,'buffers':Buffers,'cached':Cached,'active_a':Active_a,'inactive_a':Inactive_a,'active_f':Active_f,'inactive_f':Inactive_f,'dirty':Dirty,'writeback':Writeback,'CMAFree':CMAFree}
            else:
                json_mem={'loop':Loops,'time':Time,'free':Free,'io':IO,'active':Active,'inactive':Inactive,'mapped':Mapped,'slab':Slab,'memfree':MemFree,'buffers':Buffers,'cached':Cached,'active_a':Active_a,'inactive_a':Inactive_a,'active_f':Active_f,'inactive_f':Inactive_f,'dirty':Dirty,'writeback':Writeback}
            self.json_w(r'%s/hour_%s/mem.json'%(resultPath,i), json_mem)
        print '%s mem Finish'%dt.datetime.now()
        
    def meminfo(self,csvPath,resultPath):
        data=pd.read_csv(r'%s'%csvPath,warn_bad_lines=False,error_bad_lines=False).fillna(value='null')
        sleep_time=int(data.columns[0].replace('Loop:',''))
        if sleep_time == 1 :
            unit_time=300
        elif sleep_time == 2 :
            unit_time=600
        elif sleep_time < 5 :
            unit_time=900
        elif sleep_time < 10 :
            unit_time=1800
        else:
            unit_time=3600
        sleep_loop=unit_time/sleep_time
        hours=data[data.columns[0]].tail(1).values[0]*sleep_time/unit_time
        if data.index[-1]*sleep_time%unit_time > 0:
            hours=hours+1
        if os.path.exists(r'%s/maxmem.csv'%csvPath):
            os.remove(r'%s/maxmem.csv'%csvPath)
        f=open(r'%s/maxmem.csv'%os.path.dirname(csvPath),'w')
        f.write('Hours,Process_Name,Pss(k),Pss Difference(k),json Name')
        f.close()
        print 'meminfo.csv'
        for i in range(1,hours+1):
            print '%s meminfo hour: %s/%s'%(dt.datetime.now(),i,hours)
            h=0
            if not os.path.exists(r'%s/hour_%s'%(resultPath,i)):
                os.mkdir(r'%s/hour_%s'%(resultPath,i))
            data_hour=data[(data[data.columns[0]].values<i*sleep_loop)&(data[data.columns[0]].values>=(i-1)*sleep_loop)]
            Command=data_hour['Process_Name'].unique().tolist()
            maxpss=[]
            maxpd=[]
            maxcsv=[]
            for c in Command:
                #print '%s meminfo Command: %s'%(dt.datetime.now(),c)
                h=h+1
                data_command=data_hour[data_hour['Process_Name'].values==c]
                Loops=(data_command[data_command.columns[0]]*sleep_time).values.tolist()
                Tims=data_command['Time'].values.tolist()
                Pid=data_command['PID'].values.tolist()
                Pss=(data_command['Pss']/1024).values.tolist()
                Pss_max=max(data_command['Pss'])
                Pss_min=min(data_command['Pss'])
                AVG=data_command['Avgs'].values.tolist()
                if data_command['Native_Heap(Size)'].head(1).values[0] == 'null':
                    meminfo_type=0
                else:
                    if int(data_command['Native_Heap(Size)'].head(1).values[0]) == 0:
                        meminfo_type=0
                    else:
                        meminfo_type=1
                        NHS=(data_command['Native_Heap(Size)']/1024).values.tolist()
                        NHA=(data_command['Native_Heap(Alloc)']/1024).values.tolist()
                        NHF=(data_command['Native_Heap(Free)']/1024).values.tolist()
                        DHP=(data_command['Dalvik_Pss']/1024).values.tolist()
                        DHS=(data_command['Dalvik_Heap(Size)']/1024).values.tolist()
                        DHA=(data_command['Dalvik_Heap(Alloc)']/1024).values.tolist()
                        DHF=(data_command['Dalvik_Heap(Free)']/1024).values.tolist()
                tmp=len(Loops)
                p=0
                Pss[0]=round(Pss[0],2)
                if meminfo_type == 1:
                    NHS[0]=round(NHS[0],2)
                    NHA[0]=round(NHA[0],2)
                    NHF[0]=round(NHF[0],2)
                    DHP[0]=round(DHP[0],2)
                    DHS[0]=round(DHS[0],2)
                    DHA[0]=round(DHA[0],2)
                    DHF[0]=round(DHF[0],2)
                for l in range(1,tmp):
                    p=p+1
                    Pss[p]=round(Pss[p],2)
                    if meminfo_type == 1:
                        NHS[p]=round(NHS[p],2)
                        NHA[p]=round(NHA[p],2)
                        NHF[p]=round(NHF[p],2)
                        DHP[p]=round(DHP[p],2)
                        DHS[p]=round(DHS[p],2)
                        DHA[p]=round(DHA[p],2)
                        DHF[p]=round(DHF[p],2)
                    if Loops[p] == Loops[p-1]:
                        Pss[p]=[Pss[p],2,Pid[p]]
                        if meminfo_type == 1:
                            NHS[p]=[NHS[p],2,Pid[p]]
                            NHA[p]=[NHA[p],2,Pid[p]]
                            NHF[p]=[NHF[p],2,Pid[p]]
                            DHP[p]=[DHP[p],2,Pid[p]]
                            DHS[p]=[DHS[p],2,Pid[p]]
                            DHA[p]=[DHA[p],2,Pid[p]]
                            DHF[p]=[DHF[p],2,Pid[p]]
                    else:
                        if Pid[p] != Pid[p-1]:
                            Pss[p]=[Pss[p],1]
                            if meminfo_type == 1:
                                NHS[p]=[NHS[p],1]
                                NHA[p]=[NHA[p],1]
                                NHF[p]=[NHF[p],1]
                                DHP[p]=[DHP[p],1]
                                DHS[p]=[DHS[p],1]
                                DHA[p]=[DHA[p],1]
                                DHF[p]=[DHF[p],1]
                        if Loops[p] > Loops[p-1]+sleep_time:
                            Loops.insert(p,Loops[p]-1)
                            Loops.insert(p,Loops[p-1]+1)
                            Tims.insert(p,Tims[p]-1)
                            Tims.insert(p,Tims[p-1]+1)
                            Pid.insert(p,0)
                            Pid.insert(p,0)
                            Pss.insert(p,0)
                            Pss.insert(p,0)
                            AVG.insert(p,AVG[p-1])
                            AVG.insert(p,AVG[p-1])
                            if meminfo_type == 1:
                                NHS.insert(p,0)
                                NHS.insert(p,0)
                                NHA.insert(p,0)
                                NHA.insert(p,0)
                                NHF.insert(p,0)
                                NHF.insert(p,0)
                                DHP.insert(p,0)
                                DHP.insert(p,0)
                                DHS.insert(p,0)
                                DHS.insert(p,0)
                                DHA.insert(p,0)
                                DHA.insert(p,0)
                                DHF.insert(p,0)
                                DHF.insert(p,0)
                            p=p+2
                if meminfo_type == 0:
                    json_meminfo={"name":c,"type":meminfo_type,"loop":Loops,"time":Tims,"avg":AVG,"pss":Pss}
                else:
                    json_meminfo={"name":c,"type":meminfo_type,"loop":Loops,"time":Tims,"avg":AVG,"pss":Pss,"NHS":NHS,"NHA":NHA,"NHF":NHF,"DHP":DHP,"DHS":DHS,"DHA":DHA,"DHF":DHF}
                self.json_w(r'%s/hour_%s/meminfo%s.json'%(resultPath,i,h), json_meminfo)
                maxpss.append(['%s'%c,round(Pss_max*1.0/1024,2),'meminfo%s'%h])
                maxpd.append(['%s'%c,round((Pss_max-Pss_min)*1.0/1024,2),'meminfo%s'%h])
                maxcsv.append(['%s'%c,Pss_max,(Pss_max-Pss_min),'meminfo%s'%h])
            maxpss.sort(key=lambda a_tuple:a_tuple[1],reverse=True)
            maxpd.sort(key=lambda a_tuple:a_tuple[1],reverse=True)
            maxcsv.sort(key=lambda a_tuple:a_tuple[1],reverse=True)
            json_pssline={"maxpss":maxpss}
            json_pdline={"maxPD":maxpd}
            self.json_w(r'%s/hour_%s/pssline.json'%(resultPath,i), json_pssline)
            self.json_w(r'%s/hour_%s/pdline.json'%(resultPath,i), json_pdline)
            l=0
            f=open(r'%s/maxmem.csv'%os.path.dirname(csvPath),'a')
            for l in range(1,len(maxcsv)):
                f.write('/n%s,%s,%s,%s,%s'%(i,maxcsv[l][0],maxcsv[l][1],maxcsv[l][2],maxcsv[l][3]))
            f.close()
        print '%s meminfo Finish'%dt.datetime.now()
                
if __name__ == '__main__':
    csvPath=sys.argv[1]
    nocsv=0
    if not os.path.exists('%s/cpu.csv'%csvPath):
        print 'There is no cpu.csv in %s'%csvPath
        nocsv=nocsv+1
    if not os.path.exists('%s/cpuinfo.csv'%csvPath):
        print 'There is no cpuinfo.csv in %s'%csvPath
        nocsv=nocsv+1
    if not os.path.exists('%s/mem.csv'%csvPath):
        print 'There is no mem.csv in %s'%csvPath
        nocsv=nocsv+1
    if not os.path.exists('%s/meminfo.csv'%csvPath):
        print 'There is no meminfo.csv in %s'%csvPath
        nocsv=nocsv+1
    if nocsv != 0:
        sys.exit()
    import shutil
    test=mcmtojson()
    if os.path.exists(r'%s/MCM_HTML'%csvPath):
        try:
            shutil.rmtree(r'%s/MCM_HTML/json'%csvPath)
        except os.error, err:
            time.sleep(0.5)
            try:
                shutil.rmtree(r'%s/MCM_HTML/json'%csvPath)
            except os.error, err:
                print "Delete MCM_HTML Error!!!"
    else:
        os.mkdir(r'%s/MCM_HTML'%csvPath)
    copyFiles('%s/MCM_HTML'%os.path.dirname(sys.argv[0]), '%s/MCM_HTML'%csvPath)
    time.sleep(0.5)
    os.mkdir(r'%s/MCM_HTML/json'%csvPath)
    test.main(r'%s'%csvPath, r'%s/MCM_HTML/json'%csvPath)
    if os.path.exists('%s/MCM_HTML.zip'%csvPath):
        os.remove('%s/MCM_HTML.zip'%csvPath)
    dirtozip('%s/MCM_HTML'%csvPath,'%s/MCM_HTML.zip'%csvPath)
    shutil.rmtree(r'%s/MCM_HTML'%csvPath)
            