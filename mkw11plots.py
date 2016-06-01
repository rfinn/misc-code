#!/usr/bin/env python

from pylab import *
import numpy
import pyfits

#import cluster data
data=numpy.genfromtxt("MKW11galaxy.csv", delimiter=',')
dist, ra,dec, redshift=data[:,0], data[:,1], data[:,2], data[:,8]
print dist
