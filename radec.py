#!/usr/bin/env -python
import atpy, os, pyfits
from pylab import *
from LCScommon import *


class cluster:
     #def __init__(self,clustername):
       #infile= '/home/ioannis/lcs/'+clustername+'_nsa.fits.gz'
       #fitstable=pyfits.open(infile)
       #self.nsa=fitstable[1].data
       #self.ra=self.nsa.RA
       #self.dec=self.nsa.DEC

       

     def __init__(self,clustername):
       infile= '/home/ioannis/lcs/'+clustername+'_lir.fits.gz'
       fitstable=pyfits.open(infile)
       self.lir=fitstable[1].data
       self.ra=self.lir.RA
       self.dec=self.lir.DEC

       infile2='/home/ioannis/lcs/'+clustername+'_nsa.fits.gz'
       fitstable2=pyfits.open(infile2)
       self.nsa=fitstable2[1].data
       self.ra=self.nsa.RA
       self.dec=self.nsa.DEC

       self.clustername = clustername

     def plotradeclir(self):
         figure()
         x=self.nsa.RA;
         y=self.nsa.DEC;
         z=abs(self.lir.LIR_CHARY);
         sp=scatter(x,y,c=z,vmin=9,vmax=11);
         cb=colorbar(sp)
         fontsizeticks=10;
         size=17;
         cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
         yticks(fontsize =fontsizeticks)
         xticks(fontsize = fontsizeticks)
         xlabel('RA(deg)',fontsize=size)
         ylabel('DEC(deg)',fontsize=size)
         title(self.clustername,fontsize=size)
           
     
     def colormass(self):
         figure()
         color = self.nsa.ABSMAG[:,1] -self.nsa.ABSMAG[:,4];
         mass=self.nsa.MASS;
         z=abs(self.lir.LIR_CHARY);
         sc=scatter(log10(mass),color,c=z,vmin=9,vmax=11);
         cb=colorbar(sc)
         cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
         ylim(0,7,1)
         xlim(7,12,1)
         fontsizeticks=10;
         size=17;
         yticks(fontsize =fontsizeticks)
         xticks(fontsize = fontsizeticks)
         title (self.clustername,fontsize=size)
         xlabel('log$_{10}(M/M_{\odot}$)',fontsize=size)
         ylabel ('NUV-r',fontsize=size)

         
mkw11=cluster('mkw11')
coma = cluster('coma')




mkw11. plotradeclir()
coma.plotradeclir()
