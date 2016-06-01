#!/usr/bin/env -python
import atpy, os, pyfits
from pylab import *
from LCScommon import *

clustercenterra={'mkw11':202.3800, 'mkw8':220.1796, 'awm4':241.2375, 'abell2063':230.7578,'abell2052':229.1896, 'ngc6107':244.333750, 'coma':194.9531, 'abell1367':176.1231, 'hercules':241.3125}
clustercenterdec={'mkw11':11.78861, 'mkw8':3.4530, 'awm4':23.9206, 'abell2063':8.6394, 'abell2052':7.0003, 'ngc6107':34.901389, 'coma':27.9807, 'abell1367':19.8391, 'hercules':17.7485}

clusterscale={'mkw11':0.46169232, 'mkw8':0.54289997, 'awm4':0.63484109, 'abell2063':0.69582570, 'abell2052':0.70637835,'ngc6107':0.61372271,'coma':0.46470493,'abell1367':0.44470904,'hercules':0.73510397}

class cluster:
           

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
       self.clustercenterra=clustercenterra[clustername]
       self.clustercenterdec = clustercenterdec[clustername]
       self.clusterscale = clusterscale[clustername]

     def radec(self):
         figure()
         x=(self.nsa.RA-self.clustercenterra);
         y=(self.nsa.DEC-self.clustercenterdec);
         scale = ((60)*(60)*(self.clusterscale))/(1000);
         
         xmpc = x*scale;
         ympc = y*scale;

         #print xmpc
         
         z=abs(self.lir.LIR_CHARY);
         sp=scatter(xmpc,ympc,c=z,vmin=9,vmax=11);
         cb=colorbar(sp)
         fontsizeticks=10;
         size=17;
         cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]',fontsize=17)
         yticks(fontsize =fontsizeticks)
         xticks(fontsize = fontsizeticks)
         xlabel('RA (Mpc)',fontsize=size)
         ylabel('DEC (Mpc)',fontsize=size)
         title(self.clustername,fontsize=size)
         savefig(self.clustername+'_radec.png')
           
     
     def colormass(self):
         figure()
         color = self.nsa.ABSMAG[:,1] -self.nsa.ABSMAG[:,4];
         mass=self.nsa.MASS;
         z=abs(self.lir.LIR_CHARY);
         sc=scatter(log10(mass),color,c=z,vmin=9,vmax=11);
         cb=colorbar(sc)
         cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]',fontsize=17)

         ## plot lines which separate the red sequence from the green valley and the green valley
         ## from fthe blue sequence
         xred = arange(7,13,1)
         yred= 0.6*xred -0.5;     
         plot(xred,yred);
         xupperlim = arange(7,13,1);
         yupperlim = 0.6*xupperlim-1.0;
         plot(xupperlim,yupperlim,'--')
         xlowerlim = arange(7,13,1);
         ylowerlim = 0.6*xlowerlim-2.10;
         plot(xlowerlim,ylowerlim,'--')
         
         ylim(0,7,1)
         xlim(7,12,1)
         fontsizeticks=10;
         size=17;
         yticks(fontsize =fontsizeticks)
         xticks(fontsize = fontsizeticks)
         title (self.clustername,fontsize=size)
         xlabel('log$_{10}(M/M_{\odot}$)',fontsize=size)
         ylabel ('NUV-r',fontsize=size)
         savefig(self.clustername+'colorMass.png')

     def luminosity(self):
          lircut = 11.0;
          lirbright_flag=self.lir.LIR_CHARY>lircut
          names=self.lir.NSAID[lirbright_flag]
          print names

         
mkw11=cluster('mkw11')
mkw8 = cluster('mkw8')
awm4=cluster('awm4')
abell2063=cluster('abell2063')
abell2052=cluster('abell2052')
ngc6107=cluster('ngc6107')
coma = cluster('coma')
abell1367=cluster('abell1367')
hercules=cluster('hercules')



mkw11.radec()
mkw11.colormass()

mkw8.radec()
#mkw8.colormass()

awm4.radec()
#awm4.colormass()

abell2063.radec()
#abell2063.colormass()

abell2052.radec()
#abell2052.colormass()

ngc6107.radec()
#ngc6107.colormass()

coma.radec()
#coma.colormass()

abell1367.radec()
#abell1367.colormass()

hercules.radec()
#hercules.colormass()

show()


