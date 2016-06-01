#!/usr/bin/env python

from pylab import *
#from pyraf import iraf
import os
#import numpy
import glob
import pyfits
import sys

prefix=sys.argv[1]

analyzer={'MKW11':'astro4', 'MKW8':'astro4', 'AWM4':'astro4', 'A2063':'alissa', 'A2052':'alissa', 'NGC6107':'alissa', 'Coma':'alissa', 'A1367':176.1231, 'Hercules':241.3125}
path='/home/'+analyzer[prefix]+'/LocalClusters/cutouts/'+prefix+'/


# Retrieve galaxy data
#generate list-create array and arange numbers sm to lg
sdssList=glob.glob('*cutout-sdss.dat')
agcname=[]
for fil in sdssList:
    t=fil.split('-')
    try:
        agcname.append(float(t[1]))
    except ValueError:
        agcname.append(float(t[2]))
agcname=array(agcname,'f')
sortedindex=agcname.argsort()
#set up arrays for file names
dat24=[]
datSDSS=[]
im24=[]
imSDSS=[]
mask24=[]
maskSDSS=[]
for i in range(len(sdssList)):
    sortedi=sortedindex[i]
    datfilesdss=sdssList[sortedi]
    n=datfilesdss.split('sdss')
    datfile24=n[0]+'24-rot.dat'
    fits24=n[0]+'24-rot.fits'
    fitsSDSS=n[0]+'sdss.fits'
    p=n[0].split('/')
    mfits24='m'+n[0]+'24-rot.fits'
    mfitsSDSS='m'+n[0]+'sdss.fits'
    #add files to arrays
    dat24.append(datfile24)
    datSDSS.append(datfilesdss)
    im24.append(fits24)
    imSDSS.append(fitsSDSS)
    mask24.append(mfits24)
    maskSDSS.append(mfitsSDSS)
dat24=array(dat24, 'S')
datSDSS=array(datSDSS, 'S')
im24=array(im24, 'S')
imSDSS=array(imSDSS, 'S')
mask24=array(mask24, 'S')
maskSDSS=array(maskSDSS, 'S')
clusterSplit=sdssList[0].split('-')
cluster=clusterSplit[0]

print cluster
print len(dat24)
print len(datSDSS)
print len(im24)
print len(imSDSS)
print len(mask24)
print len(maskSDSS)

pages = ceil(len(dat24)/6.)
print pages

#skyval = input("What is the sky value for this cluster?")
skyval=0 #for skysub images

# Create figures
for j in range(pages):
#for j in range(1): #used for testing    
    i = 0
    n = j+1
    s = str(n)
    name = cluster + '_implot' + s + '.eps'

    figure(j+1, figsize=(10,10))
    clf()
    subplots_adjust(left=0.1, right=0.9, bottom=0.1,wspace=0.01, hspace=0.01)
    # Create subplots - sdss, sdss mask, 24, 24 mask, profile
    while i<6:
        frame = i*5
        if (j*6)+i >=len(dat24):
            break
        else:
            #read data into arrays(24 mircon)
            read24=open(dat24[(j*6)+i], 'r')
            lines=read24.readlines()
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
            read24.close()
            #read data into arrays(sdss)
            readSDSS=open(datSDSS[(j*6)+i], 'r')
            linesS=readSDSS.readlines()
            row_numS=[]
            smaS=[]
            intensS=[]
            intens_errS=[]
            for line in linesS:
                t=line.split()
                row_numS.append(t[0])
                smaS.append(t[1])
                intensS.append(t[2])
                intens_errS.append(t[3])
            row_numS=array(row_numS, 'f')
            readSDSS.close()
            smaS=array(smaS, 'f')
            intensS=array(intensS, 'f')
            intens_errS=array(intens_errS, 'f')
            #Create Subplots
            #load SDSS image
            subplot(6,5,frame+1)
            fits=pyfits.open(imSDSS[(j*6)+i])
            im=fits[0].data.copy()
            fits.close()
            sky=median(im[im<950])
            sky=sky-19 ##############This line may need to be adjusted if images aren't showing up
            imshow(log10(sqrt(im-sky)),cmap=cm.binary,vmax=1.4)
            ax=gca()
            ax.set_yticklabels(([]))
            ax.set_xticklabels(([]))
            gal_split = imSDSS[(j*6)+i].split('-')
            if gal_split[1]=='':
                galname = gal_split[2]
            else:
                galname = gal_split[1]
            text(.9, .5, galname, horizontalalignment='center', verticalalignment='center',rotation=90, transform=ax.transAxes)
            axis('equal')
            #load masked SDSS image
            subplot(6,5,frame+2)
            fits=pyfits.open(maskSDSS[(j*6)+i])
            im=fits[0].data.copy()
            fits.close()
            sky=median(im[im<950])
            sky=sky-19 ##############This line may need to be adjusted if masked images aren't showing up
            axis('equal')
            imshow(log10(sqrt(im-sky)),cmap=cm.binary,vmax=1.4)
            ax=gca()
            ax.set_yticklabels(([]))
            ax.set_xticklabels(([]))
            gal_split = maskSDSS[(j*6)+i].split('-')
            if gal_split[1]=='':
                galname = gal_split[2]
            else:
                galname = gal_split[1]
            text(.9, .5, galname, horizontalalignment='center', verticalalignment='center',rotation=90, transform=ax.transAxes)
            axis('equal')
            #load MIPS(24 micron) image
            subplot(6,5,frame+3)
            fits=pyfits.open(im24[(j*6)+i])
            im=fits[0].data.copy()
            fits.close()
            axis('equal')
            imshow(log10(sqrt(im+5)),cmap=cm.binary,vmax=.37)
            ax=gca()
            ax.set_yticklabels(([]))
            ax.set_xticklabels(([]))
            gal_split = im24[(j*6)+i].split('-')
            if gal_split[1]=='':
                galname = gal_split[2]
            else:
                galname = gal_split[1]
            text(.9, .5, galname, horizontalalignment='center', verticalalignment='center',rotation=90, transform=ax.transAxes)
            axis('equal')
            #load masked MIPS(24 micron) image
            subplot(6,5,frame+4)
            fits=pyfits.open(mask24[(j*6)+i])
            im=fits[0].data.copy()
            fits.close()
            axis('equal')
            imshow(log10(sqrt(im+5)),cmap=cm.binary,vmax=.37)
            ax=gca()
            ax.set_yticklabels(([]))
            ax.set_xticklabels(([]))
            gal_split = mask24[(j*6)+i].split('-')
            if gal_split[1]=='':
                galname = gal_split[2]
            else:
                galname = gal_split[1]
            text(.9, .5, galname, horizontalalignment='center', verticalalignment='center',rotation=90, transform=ax.transAxes)
            axis('equal')
            #plot SMA and Intensity
            gal_split = dat24[(j*6)+i].split('-')
            if gal_split[1]=='':
                galname = gal_split[2]
            else:
                galname = gal_split[1]
            ###data24 = numpy.genfromtxt(dat24[(j*6)+i], unpack=True)
            ###dataSDSS = numpy.genfromtxt(datSDSS[(j*6)+i], unpack=True)
            row_num24 = row_num24
            row_nunS = row_numS
            sma24= sma24 * 2.450016
            smaS = smaS *1.15

            intens24 = intens24 * 141
            intensS =(intensS-skyval) * 0.02229

            intens_err24 = intens_err24 * 141
            intens_errS = intens_errS * 0.02229
            axis('equal')
            subplot(6,5,frame+5)
            plot(sma24, intens24, 'r.')
            try:
                errorbar(sma24, intens24, yerr=intens_err24,fmt=None,ecolor='r')
            except ValueError:
                print('24m')
                print i, galname
                print sma24,intens24, intens_err24
            plot(smaS, intensS, 'b+')
            try:
                errorbar(smaS, intensS, yerr=intens_errS, fmt=None, ecolor='b')
            except ValueError:
                print('sdss')
                print i, galname
                print smaS,intensS,intens_errS
            ##errorbar(smaS, intensS, yerr=intens_errS,fmt=None,ecolor='b')
            axhline(y=1,color='r',ls=':')
            axhline(y=.2,color='b',ls=':')
            ax=gca()
            ax.set_yscale('log')
            frame=(i+1)*1.
            #axis([0.,60.,0.01,1200.])
            ax=gca()
            if (frame <  30):
                ax.set_xticklabels(([]))
                ax.set_yticklabels(([]))           
            i = i+1
            ax=gca()
            text(.6, .9, galname, horizontalalignment='left', verticalalignment='center',transform=ax.transAxes)
    savefig(name)
