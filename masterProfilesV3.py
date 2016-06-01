#!/usr/bin/env python

from pylab import *
#from pyraf import iraf
import os
#import numpy
import glob
import pyfits

# Retrieve galaxy data
##dat24 = glob.glob('*cutout-24-rot.dat')
##datSDSS = glob.glob('*cutout-sdss.dat')

#skyVal=input('what is the sky value?')
skyVal=0

sdssList=glob.glob('*cutout-sdss.dat')
agcname=[]
for fil in sdssList:
    t=fil.split('-')
    try:
        agcname.append(float(t[1]))
    except ValueError:
        agcname.append(float(t[2]))
agcname=array(agcname, 'f')
sortedindex=agcname.argsort()
datfile24=[]
for i in range(len(sdssList)):
    sortedi=sortedindex[i]
    datfilesdss=sdssList[sortedi]
    n=datfilesdss.split('sdss')
    datfile24=n[0]+'24-rot.dat'
datfile24=array(datfile24, 'S')
#datfile24=append(datfile24,datfile24)
print datfile24
###cluster_split = dat24[0].split('-')
###cluster = cluster_split[0]

clusterSplit=sdssList[0].split('-')
cluster=clusterSplit[0]

print cluster
##print len(datfile24)
print len(sdssList)

pages = ceil(len(sdssList)/16.)
print pages
galnum=0
# Create figures
for j in range(pages):
    i = 0
    n = j+1
    s = str(n)
    name = cluster + '_plot' + s + '.eps'

    figure(j+1, figsize=(10,10))
    clf()
    subplots_adjust(left=0.1, right=0.9, bottom=0.1,wspace=0.01, hspace=0.01)
    # Create subplots - sdss, sdss mask, 24, 24 mask, 
    while i < 16:
        if (j*16)+i >= len(sdssList):
            break
        else:
            #test
            #read data into arrays(24 mircon)
            print(galnum)
            lines=datfile24[galnum].readlines()
            row_num24=[]
            sma24=[]
            intens24=[]
            intens_err24=[]
            for line in lines:
                 t=line.split()
                 row_num24.append(t[0])
                 sma24.append(t[1])
                 intens24.append(t[2])
                 intens_err24.append(t[3])
            row_num24=array(row_num24, 'f')
            sma24=array(sma24, 'f')
            intens24=array(intens24, 'f')
            intens_err24=array(intens_err24, 'f')
            #convert (24 micron)
            sma24=sma24*2.450016 #check
            intens24=intens24*141 #check
            intens_err24=intens_err24*141 #check
            #read data into arrays(sdss)
            linesS=dataSDSS.readlines()
            row_numS=[]
            smaS=[]
            intensS=[]
            intens_errS=[]
            for line in lines:
                 t=line.split()
                 row_numS.append(t[0])
                 smaS.append(t[1])
                 intensS.append(t[2])
                 intens_errS.append(t[3])
            row_numS=array(row_numS, 'f')
            smaS=array(smaS, 'f')
            intensS=array(intensS, 'f')
            intens_errS=array(intens_errS, 'f')
            
            galname = agcname[agcname.argsort()][j]
            row_num24, row_numS = row24, row
            sma24, smaS = sma24 * 2.450016, sma * 1.15
            intens24, intensS =intens24 * 141, (intens-skyVal) * 0.02229#changeSV
            intens_err24, intens_errS = intens24err * 141, intenserr * 0.02229           
            subplot(4,4,i+1)
            plot(sma24, intens24, 'r.')
            errorbar(sma24, intens24, yerr=intens_err24,fmt=None,ecolor='r')
            plot(smaS, intensS, 'b+')
            errorbar(smaS, intensS, yerr=intens_errS,fmt=None,ecolor='b')
            axhline(y=1,color='r',ls=':')
            axhline(y=.2,color='b',ls=':')
            ax=gca()
            ax.set_yscale('log')
            frame=(i+1)
            axis([0.,70.,0.01,5000.])
            ax=gca()
            if (frame <  10):
                ax.set_xticklabels(([]))
            else:
                xticks(arange(0, 70, 20), fontsize=10)
            test=(i/4.-floor(i/4.))
            if (test > .2):
                ax.set_yticklabels(([]))
            else:
                yticks(fontsize=10)            
            i = i+1
            galnum=galnum+1
        ax=gca()
        text(.6, .9, galname, horizontalalignment='left', verticalalignment='center',transform=ax.transAxes)
    if i==16:
        ax=gca()
        text(-1, -0.25, 'SMA (arcsec)', horizontalalignment='center', verticalalignment='center', weight='bold', transform=ax.transAxes)
        text(-3.3, 2, 'Intensity (microJy)', horizontalalignment='center', verticalalignment='center', weight='bold',rotation=90, transform=ax.transAxes)
        text(-1, 4.25, 'Intensity vs. Semi-major Axis', horizontalalignment='center', verticalalignment='center', weight='bold', transform=ax.transAxes)
        savefig(name)
    else:
        savefig(name)
        continue
