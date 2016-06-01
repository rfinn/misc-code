
#!/usr/bin/env -python
import atpy, os, pyfits
from pylab import *
from LCScommon import *
import numpy as np


class cluster:
           

     def __init__(self,clustername):
       infile= '/home/ioannis/lcs/'+clustername+'_lir_blue.fits.gz'
       fitstable=pyfits.open(infile)
       self.lirblue=fitstable[1].data
       self.ra=self.lirblue.RA
       self.dec=self.lirblue.DEC

       infile2='/home/ioannis/lcs/'+clustername+'_nsa_blue.fits.gz'
       fitstable2=pyfits.open(infile2)
       self.nsablue=fitstable2[1].data
       self.ra=self.nsablue.RA
       self.dec=self.nsablue.DEC

       
       self.clustername = clustername
     
     def lirfrac(self):
         figure(1)
         lircut = 10.50;
         lirbright_flag=self.lirblue.LIR_CHARY>lircut
                  
         #mass = log10(self.nsablue.MASS);
         #masscut= log10(self.nsablue.MASS[lirbright_flag]);
         mass = log10(self.nsablue.MASS);
         masscut= log10(self.nsablue.MASS[lirbright_flag]);
         mybins = arange(8,12,0.5)
         bincenters = 0.5*(mybins[1:]+mybins[:-1])
         
         #h1= hist(mass, bins=mybins, histtype='step',label='L(IR) All')
         #h2=hist(masscut,bins=mybins,histtype='step',color='r',label = 'L(IR)>10.5');
         
         (ybin1,xbin1,t)=hist(mass, bins=mybins, histtype='step',label='L(IR) All')
         (ybin2,xbin2,t)=hist(masscut,bins=mybins,histtype='step',color='r',label = 'L(IR)>10.5');
         legend(loc='best');
         
         figure(2)
         ratio = (1.0*ybin2)/(1.0*ybin1);
         plot(bincenters,ratio,label =self.clustername)
         legend(loc = 'best')
         
               
         
         xlabel ('log$_{10}(M/M_{\odot}$)(dex)');
         ylabel('[L(IR)>10.5]/[L(IR)all]')
         #title(self.clustername)
         #savefig(self.clustername+'_lumfrac_hist.png');
         savefig('lumfrac_all_clusters.png')
        
         

         


mkw11=cluster('mkw11')
mkw8 = cluster('mkw8')
awm4=cluster('awm4')
abell2063=cluster('abell2063')
abell2052=cluster('abell2052')
ngc6107=cluster('ngc6107')
coma = cluster('coma')
abell1367=cluster('abell1367')
hercules=cluster('hercules')
           

mkw11.lirfrac();
mkw8.lirfrac();
awm4.lirfrac();
abell2063.lirfrac();
abell2052.lirfrac();
ngc6107.lirfrac();
coma.lirfrac();
abell1367.lirfrac();
hercules.lirfrac();






show()
