#!/usr/bin/env python

from pylab import *
import glob
import os
import sys

print sys.argv
clustername=sys.argv[1]

cutoutdirectory='/home/alissa/LocalClusters/cutouts/'+clustername+'/Finished/'
os.chdir(cutoutdirectory)

#make directory to move rejected galaxies into
s='mkdir reject'
os.system(s)
#generate lists of galaxies
sdssFiles=glob.glob('*cutout-sdss.dat')
agcnameS=[]
for fil in sdssFiles:
    t=fil.split('-')
    clustername=t[0]
#    try:
#        agcnameS.append(str(t[1]))
#    except ValueError:
#        agcnameS.append(str(t[2]))
#        print('catch')
    if t[1]=='':
        agcnameS.append(str(t[2]))
    else:
        agcnameS.append(str(t[1]))       
agcnameS=array(agcnameS, 'S')
mipsFiles=glob.glob('*cutout-24-rot.dat')
agcnameM=[]
for fil in mipsFiles:
    t=fil.split('-')
    if t[1]=='':
        agcnameM.append(str(t[2]))
    else:
        agcnameM.append(str(t[1])) 
agcnameM=array(agcnameM, 'S')

#create file to make final list
filepath='/home/alissa/LocalClusters/cutouts/'+clustername+'/Finished/'+clustername+'FinalList.dat'#edit this line based on which user is using it and where you want the files to end up
outfile1=open(filepath,'w')
#compare lists
for mfile in agcnameM:
    for sfile in agcnameS:
        check=1
        if mfile.find(sfile)>-1:
            s=mfile+'\n'
            outfile1.write(s)
            check=2
            break
    if check<2:
        #s='mv *'+mfile+'* /home/alissa/LocalClusters/cutouts/'+clustername+'/Finished/reject'
        s='mv *'+mfile+'* reject'
        print mfile
        os.system(s)
for sfile in agcnameS:
    for mfile in agcnameM:
        check=1
        if sfile.find(mfile)>-1:
            check=2
            break
    if check<2:
        #s='mv *'+sfile+'* /home/alissa/LocalClusters/cutouts/'+clustername+'/Finished/reject'
        s='mv *'+sfile+'* reject'
        print sfile
        os.system(s)           
outfile1.close()            
