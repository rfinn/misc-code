#!/usr/bin/env -python
import atpy, os, pyfits
from pylab import *
from LCScommon import *

mypath=os.getcwd()
if mypath.find('Users') > -1:
    print "Running on Rose's mac pro"
    homedir='/Users/rfinn/'
elif mypath.find('home') > -1:
    print "Running on coma"
    homedir='/home/rfinn/'

class NSA:
    def __init__(self):
       # infile=homedir+'research/NSA/nsa_v0_1_2.fits'
        infile= '/home/astro4/Amy/NSA/nsa_v0_1_2.fits'

        #nsa_dat=atpy.Table(infile)
        ndat=pyfits.open(infile)
        self.ndat=ndat[1].data
        #keepflag = ones(len(self.ndat))
        self.ra=self.ndat.RA
        self.dec=self.ndat.DEC
        self.redshift=self.ndat.Z

        # cull for LCS
        keepflag=(self.redshift > zmin) & (self.redshift < zmax) & (self.ra > 170.) & (self.ra < ramax) & (self.dec > decmin) & (self.dec < decmax)
        #self.ra=self.ndat.RA[keepflag]
        #self.dec=self.ndat.DEC[keepflag]
        #self.redshift=self.ndat.Z[keepflag]
        
nsa=NSA()        



