#!/usr/bin/env python

from pylab import *
from pyraf import iraf
import pylab
import os
import numpy
import glob
import pyfits

# Retrieve galaxy data
dat24 = glob.glob('*cutout-24.dat')
datSDSS = glob.glob('*cutout-sdss.dat')

cluster_split = dat24[0].split('-')
cluster = cluster_split[0]

print cluster
print len(dat24)
print len(datSDSS)

pages = ceil(len(dat24)/16.)
print pages

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
        if (j*16)+i >= len(dat24):
            break
        else:
            gal_split = dat24[(j*16)+i].split('-')
            galname = gal_split[1]
            data24 = numpy.genfromtxt(dat24[(j*16)+i], unpack=True)
            dataSDSS = numpy.genfromtxt(datSDSS[(j*16)+i], unpack=True)
            row_num24, row_numS = data24[0,:], dataSDSS[0,:]
            sma24, smaS = data24[1,:] * 2.450016, dataSDSS[1,:] * 1.15
            intens24, intensS =data24[2,:] * 141, (dataSDSS[2,:]-919) * 0.02229
            intens_err24, intens_errS = data24[3,:] * 141, (dataSDSS[3,:]) * 0.02229
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
