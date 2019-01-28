#!/usr/bin/python 
import os
import time
import re
import shutil
import os.path
import datetime
import subprocess
import commands
import sys
import datetime
import getopt

server = "//imgrepo-cnbj-iov.devops.letv.com/dailybuild/"
mmu = "IOV/df91/mmu/imx6dl/daily/"
ihub_evt01 = "IOV/df91/ihub/evt01/bsp_daily/"
ihub_820 = "IOV/df91/ihub/820/ncar/ces/"
#ihub_820 = "IOV/df91/ihub/820/betacar_daily"
ihub_820a = "IOV/df91/ihub/820a/bsp_daily/"
ihub_j6 = "IOV/df91/ihub/tij6/ces/"
#ihub_j6 = "IOV/df91/ihub/tij6/bringup/"
rdc_820 = "IOV/df91/rdc/820/ncar/ces/"
rdc_820a = "IOV/df91/rdc/820a/bsp_daily/"
#HPC = "IOV/df91/hu_hpc/820a/ncar_bsp/"
#MPC = "IOV/df91/hu_mpc/820a/ncar_bsp/"
#HPC = "IOV/df91/hu_hpc/820a/ncar_daily/visteon_display/"
HPC = "IOV/df91/hu_hpc/820a/ncar_daily/"
MPC = "IOV/df91/hu_mpc/820a/ncar_daily/"
adaptor = "IOV/df91/adaptor/imx6dl/"

bmw = "IOV/df91/bmw_rse/820a/ncar_daily/"
if len(sys.argv) > 1:
    today = sys.argv[1]
else:
    today = time.strftime("%Y%m%d",time.localtime(time.time()))

currtime = time.time()
delta_Local = 3600*24*3

now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y%m%d')

HPC_smb_path = os.path.join(HPC, yes_time_nyr)
MPC_smb_path = os.path.join(MPC, yes_time_nyr)
bmw_smb_path = os.path.join(bmw, today)
mmu_smb_path = os.path.join(mmu,today)
adaptor_smb_path = os.path.join(adaptor, today)

HPC_local = "/home/ljs/df91/hpc-yes/"
MPC_local = "/home/ljs/df91/mpc-yes/"
bmw_local = "/home/ljs/df91/bmw/"
mmu_local = "/home/ljs/df91/mmu/"
adaptor_local = "/home/ljs/df91/adaptor/"

mypath=os.getcwd()



def run_sh_command(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT):
    """run linux shell command, return result or error"""
    p = subprocess.Popen(cmd, stdout=stdout,stderr=stderr, shell=True)
    result = p.communicate()
    return result[0]



def scandir(startdir, target):

    os.chdir(startdir)
#    print os.listdir(os.curdir)


    for obj in os.listdir(os.curdir):
        m = re.search(target, obj)

        if m:

            print obj
            run_sh_command('unzip '+obj )
            run_sh_command('sudo chmod -R 777 *' )


        if os.path.isdir(obj):

            scandir(obj, target)

            os.chdir(os.pardir) #!!!



def downloaDBuild(smb_path,local_path):

    run_sh_command('rm -rf '+local_path+'*')
    os.chdir(local_path)
    run_sh_command('mkdir ' + today)
    local_path = os.path.join(local_path, today)
    os.chdir(local_path)
    #download SW
    print 'smbclient ' + server + ' -N -D ' + smb_path + ' -c "recurse;prompt;mget *"'
    run_sh_command('smbclient ' + server + ' -N -D ' + smb_path + ' -c "recurse;prompt;mget *"')
    scandir(local_path, 'fastboot\w*.zip')
    
def confirmStart():
    try:
        a = raw_input("\nSure -- press 'Enter' ; Not -- press 'Ctrl + c'")
    except KeyboardInterrupt:
        print '\nStop!!!!!!'
        sys.exit()


if __name__=="__main__":

    
    print "\nFor example :'python get_FlashPacckage_bmw.py 20170803 mmu'\n"
#    time.sleep(5)
    p1 = ""
    p2 = ""
    if len(sys.argv) > 2:
        if sys.argv[2] == "mmu":
            p1 = mmu_smb_path
            p2 = mmu_local
        elif sys.argv[2] == "hpc":
            p1 = HPC_smb_path
            p2 = HPC_local
        elif sys.argv[2] == "mpc":
            p1 = MPC_smb_path
            p2 = MPC_local
        elif sys.argv[2] == "adaptor":
            p1 = adaptor_smb_path 
            p2 = adaptor_local


    else:
        p1 = bmw_smb_path
        p2 = bmw_local
    print p1 , p2
    confirmStart()
    print "ok"
    downloaDBuild(p1,p2)
    os.chdir(mypath)
