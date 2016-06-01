#!/usr/bin/env python

'''
usage

galTablesV4.py *cutout-24-rot.tab

this will find all table files matching your string and convert them to text files
'''

print('This version of galTables works for *cutout-24-rot.tab files and *cutout-sdss.tab files. If you are not using rotated 24m files then use galTablesv2.py')

from pylab import *
import glob
from pyraf import iraf
import os,sys

iraf.stsdas()
iraf.analysis()
iraf.toolbox()
iraf.ttools()

matchstring=sys.argv[1]
#flag = str(raw_input('Which files? a=24  b=sdss '))
#flag = str(flag)
#if flag.find('a') > -1:
#    tabfiles = glob.glob('*cutout-24-rot.tab')
#if flag.find('b') > -1:
#    tabfiles = glob.glob('*cutout-sdss.tab')

tabfiles = glob.glob(matchstring)
#tabfiles=glob.glob('*.tab')
print tabfiles
for i in range(len(tabfiles)):
    tfile = tabfiles[i]

    nfile = tfile.split('.')
    dfile = nfile[0]+'.dat'
    print tfile,' -> ',dfile
    iraf.tprint(table=tfile,pwidth='INDEF',showhdr='no',showunits='no',Stdout=dfile)
