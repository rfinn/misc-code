#!/usr/bin/env python
"""


"""

from pylab import *
from pyraf import iraf
import pyfits
import sqlcl
import glob
import os
import ReadAGCsav
from matplotlib.backends.backend_pdf import PdfFile

delta=100.#width of cutouts in arcsec
ramin=170.
ramax=250.
decmax=38.
zmin=0.01366#min z cut, z(coma)-3 sigma
zmax=0.04333#max z cut, z(A2052)+3 sigma
vmin=zmin*3.e5
vmax=zmax*3.e5

#cutoutpath='/home/rfinn/research/LocalClusters/cutouts/'
cutoutpath='/home/rfinn/research/LocalClusters/cutouts/'


class cluster:
    def __init__(self):
	self.prefix=names[ncl]
        self.cra=clusterRA[ncl]
        self.cdec=clusterDec[ncl]
        self.cz=clusterz[ncl]
        self.dr=3.#get galaxies w/in 3 degrees
	self.cutoutpath=cutoutpath+self.prefix+'/'
        #if self.prefix.find('A2063')>-1:
        #    self.dr=5.

#mipsimage=['/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits','/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits','/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits','/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits','/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits','/home/rfinn/research/LocalClusters/cutouts/MKW11/FullMKW11ch1rf_mosaic_minus_median_extract.fits']
        self.image24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/Full'+self.prefix+'ch1rf_mosaic_minus_median_extract.fits'
	self.noise24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/Full'+self.prefix+'ch1rf_mosaic_unc.fits'
        self.sdssrim1='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'R1.fits'
        self.sdssrim2='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'R2.fits'
        self.sdssrim1skysub='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'R1s.fits'
        self.sdssrim2skysub='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'R2s.fits'
        self.rotatedimage24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24umWCS/'+self.prefix+'-WCS-mosaic_minus_median_extract.fits'
#	self.rotatedimage24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/'+'r'+self.prefix+'-rotated-24.fits'
	if ncl > 6:#for Abell 1367 and Hercules cluster
		self.image24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/'+self.prefix+'ch1r1_mosaic_minus_median_extract.fits'
		self.noise24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/'+self.prefix+'ch1r1_mosaic_unc.fits'
		self.sdssrim1='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'_SDSSr_mosaic.fits'
		self.sdssrim2='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'_SDSSr_mosaic.fits'
		self.sdssrim1skysub='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'_SDSSr_mosaics.fits'
		self.sdssrim2skysub='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'+self.prefix+'_SDSSr_mosaics.fits'

	self.imagepath24='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/24um/'
	self.sdssimagepath='/home/rfinn/research/LocalClusters/Images/'+self.prefix+'/SDSS/'

	t=self.sdssrim1.split('.')
	self.sdsstestcat1=t[0]+'-test.cat'

    	t=self.sdssrim2.split('.')
	self.sdsstestcat2=t[0]+'-test.cat'
	self.testcat24=self.imagepath24+self.prefix+'-24um-test.cat'
	


    def getsdssspeccat(self):
        print 'Getting SDSS spec cat for ',self.prefix
        drsearch=3.*60.#search radius in arcmin for sdss query
        #zmin=self.cz-.005
        #zmax=self.cz+.005
        #from this, we will make a field sample and a cluster sample
        query="select n.distance,g.ra,g.dec, g.u, g.g, g.r, g.i, g.z, s.z,l.ew,l.ewErr, s.plate, s.fiberID, s.tile from galaxy g, specobj s, specline l, dbo.fGetNearbyObjEq(%12.8f,%12.8f,%8.3f) n where g.objid = s.bestobjid and g.objID = n.objID and l.specobjid = s.specobjid and s.z < %5.4f and s.z > %5.4f and (g.PrimTarget & 0x00000040) > 0 and l.LineId = 6565 order by distance" % (self.cra,self.cdec,drsearch,zmax,zmin)
        try:
            lines=sqlcl.query(query).readlines()
        except IOError:
            print "IOError for cluster",self.prefix," trying spec query again"
            lines=sqlcl.query(query).readlines()
        print self.prefix,": got number + 1 of spec objects = ",len(lines)
        n='/home/rfinn/research/LocalClusters/SDSSCatalogs/'+str(self.prefix)+'galaxy.dat'
        outfile=open(n,'w')
        j=0
        if (len(lines) > 1.):
            for line in lines[1:]:
                if j < 0:
                    print line
                    j=j+1
                outfile.write(line)
        outfile.close()

    def getsdssphotcat(self):

	print "getting phot cat for cluster",self.prefix
	drsearch=3.*60.#search radius in arcmin for sdss query
	#Vg=0.3556-0.7614*((self.avegr)-0.6148)#(V-g) from Blanton et al 2003
	#query="select g.ra, g.dec, g.u, g.g, g.r, g.i, g.z, g.plate_ID, g.MJD,  from galaxy g, dbo.fGetNearbyObjEq(%12.8f,%12.8f,%8.3f) n where g.objID = n.objID and (g.g < %5.2f) and ((0.384*g.g + 0.716*g.r)< %5.2f)" % (self.ra[i],self.dec[i],drsearch,(mr+1.5),mr)
	query="select g.ra, g.dec, g.u, g.g, g.r, g.i, g.z, g.objid, g.specObjID,g.extinction_u, g.extinction_g, g.extinction_r, g.extinction_i, g.extinction_z from galaxy g, dbo.fGetNearbyObjEq(%12.8f,%12.8f,%8.3f) n where g.objID = n.objID and  (g.PrimTarget & 0x00000040) > 0 " % (self.cra,self.cdec,drsearch)
        try:
            lines=sqlcl.query(query).readlines()
        except IOError:
            print "IOError for cluster",self.prefix," trying phot query again"
            lines=sqlcl.query(query).readlines()

#	lines=sqlcl.query(query).readlines()
	#print query
	print "got number+1 phot objects = ",len(lines)
	#print lines

        n='/home/rfinn/research/LocalClusters/SDSSCatalogs/'+str(self.prefix)+'galaxy.photcat.dat'
        outfile=open(n,'w')
        j=0
        if (len(lines) > 1.):
            for line in lines[1:]:
                if j < 0:
                    print line
                    j=j+1
                outfile.write(line)
        outfile.close()


 

 


ncl=0
names=['MKW11','MKW8','AWM4', 'A2063','A2052','NGC6107', 'Coma','A1367','Hercules']
#names=['NGC6107', 'Coma','A1367','Hercules']

clusterRA=[202.38000,220.1796,241.2375, 230.7578, 229.1896, 244.333750,194.9531, 176.1231, 241.3125]
clusterDec=[11.78861,3.4530, 23.9206, 8.6394, 7.0003, 34.901389, 27.9807, 19.8391, 17.7485]
clusterz=[.022849,.027,.031755,.034937,.035491,.030658,.023,.028,.037]

for ncl in range(8,len(names)):
#for ncl in range(len(names)):
#these=array([0,3,4,5,7,8],'i')
#for ncl in these:
#for ncl in range(1,len(names)):
#for ncl in range(6,7):#coma only
#for ncl in range(6,len(names)):
    if ncl == 0:
        mkw11=cluster()
        cl=mkw11
    if ncl == 1:
        mkw8=cluster()
        cl=mkw8
    if ncl == 2:
        awm4=cluster()
        cl=awm4
    if ncl == 3:
        a2063=cluster()
        cl=a2063
    if ncl == 4:
        a2052=cluster()
        cl=a2052
    if ncl == 5:
        ngc6107=cluster()
        cl=ngc6107
    if ncl == 6:
        coma=cluster()
        cl=coma
    if ncl == 7:
        a1367=cluster()
        cl=a1367
    if ncl == 8:
        hercules=cluster()
        cl=hercules

    print '%8s RA  range = %12.8f %12.8f'%(cl.prefix,clusterRA[ncl]-3.3/2.,clusterRA[ncl]+3.3/2.)
    print '%8s Dec range = %12.8f %12.8f'%(cl.prefix,clusterDec[ncl]-3.3/2.,clusterDec[ncl]+3.3/2.)
    
#    cl.getsdssspeccat()
    cl.getsdssphotcat()

