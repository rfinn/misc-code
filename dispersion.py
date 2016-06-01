#!/usr/bin/env python 

import pyfits
from pylab import *
import numpy


clusterSigma={'MKW11':361, 'MKW8':325, 'AWM4':500, 'A2063':660, 'A2052':562, 'NGC6107':410, 'Coma':1000, 'A1367':745, 'Hercules':689}

clustercentralvelocity={'MKW11':6854, 'MKW8':8100, 'AWM4':9526, 'A2063':10481, 'A2052':10647, 'NGC6107':9197, 'Coma':6900, 'A1367':8400, 'Hercules':11100}

##clusterlow={'MKW11':3854, 'MKW8':5100,'AWM4':6526,'A2063':7481,'A2052':7647,'NGC6107':6197, 'Coma':3900,'A1367':5400,'Hercules':8100}

##clusterhigh={'MKW11':9854, 'MKW8':11100,'AWM4':12526,'A2063':13481,'A2052':13647,'NGC6107':12197, 'Coma':9900,'A1367':11400,'Hercules':14100}

##clusterlow2={'MKW11':4006, 'MKW8':4956,'AWM4':7137,'A2063':5312,'A2052':8978,'NGC6107':6015, 'Coma':4631,'A1367':5833,'Hercules':8621}

##clusterhigh2={'MKW11':9701, 'MKW8':11244,'AWM4':11914,'A2063':15650,'A2052':12316,'NGC6107':12379, 'Coma':9169,'A1367':10967,'Hercules':13579}

##clusterlow3={'MKW11':5327.75, 'MKW8':5585.73,'AWM4':7120.42,'A2063':7336.58,'A2052':8550.66,'NGC6107':6868.46, 'Coma':4541.88,'A1367':4393.8,'Hercules':8642.4}

##clusterhigh3={'MKW11':8380.25, 'MKW8':10614.27,'AWM4':11931.58,'A2063':13625.42,'A2052':12743.34,'NGC6107':11525.54, 'Coma':9258.12,'A1367':12406.2,'Hercules':13557.6}

##clusterlow4={'MKW11':5651.53, 'MKW8':5742.44,'AWM4':7097.01,'A2063':8532.77,'A2052':8514.45,'NGC6107':7062.29, 'Coma':4534.67,'A1367':3231.03,'Hercules':8648.51}

##clusterhigh4={'MKW11':8056.47, 'MKW8':10457.56,'AWM4':11954.99,'A2063':12429.23,'A2052':12779.55,'NGC6107':11331.71, 'Coma':9265.33,'A1367':13568.97,'Hercules':13551.49}

##clusterlow5={'MKW11':5747.3, 'MKW8':5758.61,'AWM4':7028.35,'A2063':8551,'A2052':8514.45,'NGC6107':7154.74, 'Coma':4534.67,'A1367':3231.03,'Hercules':8648.51}

##clusterhigh5={'MKW11':7960.7, 'MKW8':10441.39,'AWM4':12023.65,'A2063':12411,'A2052':12779.55,'NGC6107':11239.26, 'Coma':9265.33,'A1367':13568.97,'Hercules':13551.49}

##clusterlow6={'MKW11':5791.22, 'MKW8':5758.61,'AWM4':6879.19,'A2063':8551,'A2052':8514.45,'NGC6107':7190.49, 'Coma':4534.67,'A1367':3231.03,'Hercules':8648.51}

##clusterhigh6={'MKW11':7916.78, 'MKW8':10441.39,'AWM4':12172.81,'A2063':12411,'A2052':12779.55,'NGC6107':11203.51, 'Coma':9265.33,'A1367':13568.97,'Hercules':13551.49}

##clusterlow7={'MKW11':5816.85, 'MKW8':5758.61,'AWM4':6752.57,'A2063':8551,'A2052':8514.45,'NGC6107':7224.44, 'Coma':4534.67,'A1367':3231.03,'Hercules':8648.51}

##clusterhigh7={'MKW11':7891.15, 'MKW8':10441.39,'AWM4':12299.43,'A2063':12411,'A2052':12779.55,'NGC6107':11169.56, 'Coma':9265.33,'A1367':13568.97,'Hercules':13551.49}

clusterlow8={'MKW11':5816.85, 'MKW8':5758.61,'AWM4':6344.15,'A2063':8551,'A2052':8514.45,'NGC6107':7269.02, 'Coma':4534.67,'A1367':3231.03,'Hercules':8648.51}

clusterhigh8={'MKW11':7891.15, 'MKW8':10441.39,'AWM4':12707.85,'A2063':12411,'A2052':12779.55,'NGC6107':11124.989, 'Coma':9265.33,'A1367':13568.97,'Hercules':13551.49}

clustercbimin={'MKW11':2854,'MKW8':4100,'AWM4':5526,'A2063':6481,'A2052':6647,'NGC6107':5197,'Coma':2900,'A1367':4400,'Hercules':7100}

clustercbimax={'MKW11':10854,'MKW8':12100,'AWM4':13526,'A2063':14481,'A2052':14647,'NGC6107':13197,'Coma':10900,'A1367':12400,'Hercules':15100}

class cluster:
   def __init__(self,clustername):
       self.clustername=clustername
       infile='/home/rfinn/research/LocalClusters/MasterTables/'+clustername+'mastertable.fits'
       #infile='/home/astro4/LocalClusters/'+clustername+'mastertable.fits'
       tb=pyfits.open(infile)
       tbdata=tb[1].data
       tb.close()
       self.agcflag=tbdata.field('AGCflag')
       self.sdssflag=tbdata.field('SDSSflag')
       self.sexsdssflag=tbdata.field('SEXSDSSflag')
       self.sex24flag=tbdata.field('SEX24FLAG')
       self.agcnumber=tbdata.field('AGCNUMBER')
       self.ra=tbdata.field('AGC-RA')
       self.dec=tbdata.field('AGC-DEC')
       self.a100=tbdata.field('A100')
       self.b100=tbdata.field('B100')
       self.mag10=tbdata.field('MAG10')
       self.posang=tbdata.field('POSANG')
       self.bsteintype=tbdata.field('BSTEINTYPE')
       self.vopt=tbdata.field('VOPT')#optical velocity
       self.verr=tbdata.field('VERR')
       self.vsource=tbdata.field('VSOURCE')#HI velocity
       self.flux100=tbdata.field('FLUX100')
       self.rms100=tbdata.field('RMS100')
       self.v21=tbdata.field('V21')
       self.width=tbdata.field('WIDTH')
       self.widtherr=tbdata.field('WIDTHERR')
       self.sdssra=tbdata.field('SDSSRA')
       self.sdssdec=tbdata.field('SDSSDEC')
       self.sdssu=tbdata.field('SDSSU')
       self.sdssg=tbdata.field('SDSSG')
       self.sdssr=tbdata.field('SDSSR')
       self.sdssi=tbdata.field('SDSSI')
       self.sdssz=tbdata.field('SDSSZ')
       self.sdssspecz=tbdata.field('SDSSSPECZ')
       self.sdsshaew=tbdata.field('SDSSHAEW')
       self.sdsshaewerr=tbdata.field('SDSSHAEWERR')
       self.numberser=tbdata.field('NUMBERSER')
       self.ximageser=tbdata.field('XIMAGESER')
       self.yimageser=tbdata.field('YIMAGESER')
       self.xminimageser=tbdata.field('XMINIMAGESER')
       self.xmaximageser=tbdata.field('XMAXIMAGESER')
       self.yminimageser=tbdata.field('YMINIMAGESER')
       self.raser=tbdata.field('RASER')
       self.decser=tbdata.field('DECSER')
       self.fluxisoser=tbdata.field('FLUXISOSER')
       self.fluxerrisoser=tbdata.field('FLUXERRISOSER')
       self.magisoser=tbdata.field('MAGISOSER')
       self.magerrisoser=tbdata.field('MAGERRISOSER')
       self.fluxautoser=tbdata.field('FLUXAUTOSER')
       self.fluxerrautoser=tbdata.field('FLUXERRAUTOSER')
       self.magautoser=tbdata.field('MAGAUTOSER')
       self.magerrautoser=tbdata.field('MAGERRAUTOSER')
       self.fluxpetroser=tbdata.field('FLUXPETROSER')
       self.fluxerrpetroser=tbdata.field('FLUXERRPETROSER')
       self.magpetroser=tbdata.field('MAGPETROSER')
       self.magerrpetroser=tbdata.field('MAGERRPETROSER')
       self.kronradser=tbdata.field('KRONRADSER')#kron radius
       self.petroradser=tbdata.field('PETRORADSER')#petrosian radius
       self.fluxradser=tbdata.field('FLUXRADSER')#1/2 light radius
       self.isoareaser=tbdata.field('ISOAREASER')
       self.aworldser=tbdata.field('AWORLDSER')
       self.bworldser=tbdata.field('BWORLDSER')
       self.thetaser=tbdata.field('THETASER')
       self.errthetaser=tbdata.field('ERRTHETASER')
       self.thetaj2000ser=tbdata.field('THETAJ2000SER')
       self.errthetaj2000ser=tbdata.field('ERRTHETAJ2000SER')
       self.elongser=tbdata.field('ELONGATIONSER')
       self.elliptser=tbdata.field('ELLIPTICITYSER')
       self.fwhmser=tbdata.field('FWHMSER')
       self.flagsser=tbdata.field('FLAGSSER')
       self.classstarser=tbdata.field('CLASSSTARSER')
       self.numberse24=tbdata.field('NUMBERSE24')
       self.ximagese24=tbdata.field('XIMAGESE24')
       self.yimagese24=tbdata.field('YIMAGESE24')
       self.xminimagese24=tbdata.field('XMINIMAGESE24')
       self.xmaximagese24=tbdata.field('XMAXIMAGESE24')
       self.xminimagese24=tbdata.field('YMINIMAGESE24')
       self.rase24=tbdata.field('RASE24')
       self.decse24=tbdata.field('DECSE24')
       self.fluxisose24=tbdata.field('FLUXISOSE24')
       self.fluxerrisose24=tbdata.field('FLUXERRISOSE24')
       self.magisose24=tbdata.field('MAGISOSE24')
       self.magerrisose24=tbdata.field('MAGERRISOSE24')
       self.fluxautose24=tbdata.field('FLUXAUTOSE24')
       self.fluxerrautose24=tbdata.field('FLUXERRAUTOSE24')
       self.magautose24=tbdata.field('MAGAUTOSE24')
       self.magerrautose24=tbdata.field('MAGERRAUTOSE24')
       self.fluxpetrose24=tbdata.field('FLUXPETROSE24')
       self.fluxerrpetrose24=tbdata.field('FLUXERRPETROSE24')
       self.magpetrose24=tbdata.field('MAGPETROSE24')
       self.magerrpetrose24=tbdata.field('MAGERRPETROSE24')
       self.kronradse24=tbdata.field('KRONRADSE24')
       self.petroradse24=tbdata.field('PETRORADSE24')
       self.fluxradse24=tbdata.field('FLUXRADSE24')
       self.isoarease24=tbdata.field('ISOAREASE24')
       self.aworldse24=tbdata.field('AWORLDSE24')
       self.bworldse24=tbdata.field('BWORLDSE24')
       self.thetase24=tbdata.field('THETASE24')
       self.errthetase24=tbdata.field('ERRTHETASE24')
       self.thetaj2000se24=tbdata.field('THETAJ2000SE24')
       self.errthetaj2000se24=tbdata.field('ERRTHETAJ2000SE24')
       self.elongse24=tbdata.field('ELONGATIONSE24')
       self.elliptse24=tbdata.field('ELLIPTICITYSE24')
       self.fwhmse24=tbdata.field('FWHMSE24')
       self.flagsse24=tbdata.field('FLAGSSE24')
       self.classstarse24=tbdata.field('CLASSSTARSE24')
       self.f24dist=self.fluxautose24[self.sex24flag]
       ##self.highv=[]
##        self.highv2=[]
##        self.highv3=[]
##        self.highv4=[]
##        self.highv5=[]
##        self.highv6=[]
##        self.highv7=[]
       self.highv8=[]
       self.cbi=[]
       self.sigma=clusterSigma[clustername]
       self.cv=clustercentralvelocity[clustername]
      ## self.low=clusterlow[clustername]
##        self.high=clusterhigh[clustername]
##        self.low2=clusterlow2[clustername]
##        self.high2=clusterhigh2[clustername]
##        self.low3=clusterlow3[clustername]
##        self.high3=clusterhigh3[clustername]
##        self.low4=clusterlow4[clustername]
##        self.high4=clusterhigh4[clustername]
##        self.low5=clusterlow5[clustername]
##        self.high5=clusterhigh5[clustername]
##        self.low6=clusterlow6[clustername]
##        self.high6=clusterhigh6[clustername]
##        self.low7=clusterlow7[clustername]
##        self.high7=clusterhigh7[clustername]
       self.low8=clusterlow8[clustername]
       self.high8=clusterhigh8[clustername]
       self.cbiMin=clustercbimin[clustername]
       self.cbiMax=clustercbimax[clustername]
       # Use sdss redshift for galaxies with SDSSflag>0, then v21, then vopt
       self.allvelocity=(3e5)*self.sdssspecz
       self.r=size(self.vopt)
       a=0
       while a<self.r:
           if self.sdssflag[a]<=0 and self.v21[a]>0:
               self.allvelocity[a]=self.v21[a]
               a=a+1
           elif self.sdssflag[a]<=0 and self.v21[a]<=0:
               self.allvelocity[a]=self.vopt[a]
              # print(self.agcnumber[a])
               a=a+1
           else:
               a=a+1









   #function used to plot histograms of  velocity disperion
   def plotvelhist(self):
       bins=30
       x1=self.allvelocity
       (yhist,xhist,patches)=hist(x1,bins)
       xhist=xhist[0:len(xhist)-1]+0.5*(xhist[1]-xhist[0])
       #plots gaussian fit to histograms for each cluster
       mean= average(x1)
       std=numpy.std(x1)
      # print std
       norm=max(yhist)
       xmin=3000
       xmax=15000
       xplot=arange(xmin,xmax,500)
       y1=norm*exp(-((xplot -mean)**2)/(2*std**2))
       plot(xplot,y1,'g-')
       xlabel('velocity dispersion')
       xlim(xmin,xmax)

       #plots the central velocity of each cluster
       axvline(self.cv,ymin=0,ymax=60,color='r')


       #calculate chi-squared
       yfit=norm*exp(-((xhist -mean)**2)/(2*std**2))
       errorysquared=(yhist)
        #print len(yhist),len(yfit),len(xhist),len(errorysquared)
       chisq=sum(((yhist-yfit)**2)/errorysquared)
       #print chisq

       chisqmin=1.e32
       sigmabest=std
       for vsigma in range(200,1500,100):
           yfit=norm*exp(-((xhist -mean)**2)/(2*vsigma**2))
           errorysquared=(yhist)
           chisq=sum(((yhist-yfit)**2)/errorysquared)/len(yfit)
           if chisq < chisqmin:
               sigmabest=vsigma
               chiqsmin=chisq

       s1='$ \sigma = %5.0f$'%(sigmabest)

       y1=norm*exp(-((xplot -mean)**2)/(2*sigmabest**2))
       plot(xplot,y1,'r:')

       y2=norm*exp(-((xplot -self.cv)**2)/(2*self.sigma**2))
       plot(xplot,y2,'m-')

       s=self.clustername+s1
       title(s)



   #only plots velocities within a  +/- 3000km/s  range of central velocity in order to get rid of the outliers
      ## i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low and self.allvelocity[i] < self.high:
##                self.highv.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew(self):
##        bins=30
##        x1=self.highv
##        (yhist,xhist,patches)=hist(x1,bins)
##        stdnew=numpy.std(x1)
##        #print stdnew
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew= average(x1)
##        normnew=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y1=normnew*exp(-((xplot -meannew)**2)/(2*stdnew**2))
##        plot(xplot,y1,'g-')



##        #Reajust velocity cut,+/-3 times standard deviation?
##        i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low2 and self.allvelocity[i] < self.high2:
##                self.highv2.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew2(self):
##        bins=30
##        x2=self.highv2
##        (yhist,xhist,patches)=hist(x2,bins)
##        stdnew2=numpy.std(x2)
##        #print stdnew2
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew2= average(x2)
##        normnew2=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y2=normnew2*exp(-((xplot -meannew2)**2)/(2*stdnew2**2))
##        plot(xplot,y2,'g-')



      ## #Reajust velocity cut2
##        i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low3 and self.allvelocity[i] < self.high3:
##                self.highv3.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew3(self):
##        bins=30
##        x3=self.highv3
##        (yhist,xhist,patches)=hist(x3,bins)
##        stdnew3=numpy.std(x3)
##       # print stdnew3
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew3= average(x3)
##        normnew3=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y3=normnew3*exp(-((xplot -meannew3)**2)/(2*stdnew3**2))
##        plot(xplot,y3,'g-')



       ###Reajust velocity cut3
##        i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low4 and self.allvelocity[i] < self.high4:
##                self.highv4.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew4(self):
##        bins=30
##        x4=self.highv4
##        (yhist,xhist,patches)=hist(x4,bins)
##        stdnew4=numpy.std(x4)
##        #print stdnew4*3
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew4= average(x4)
##        normnew4=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y4=normnew4*exp(-((xplot -meannew4)**2)/(2*stdnew4**2))
##        plot(xplot,y4,'g-')


       ## #Reajust velocity cut4

##        i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low5 and self.allvelocity[i] < self.high5:
##                self.highv5.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew5(self):
##        bins=30
##        x5=self.highv5
##        (yhist,xhist,patches)=hist(x5,bins)
##        stdnew5=numpy.std(x5)
##        #print stdnew4*3
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew5= average(x5)
##        normnew5=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y5=normnew5*exp(-((xplot -meannew5)**2)/(2*stdnew5**2))
##        plot(xplot,y5,'g-')


      ## #Reajust velocity cut5
##        i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low6 and self.allvelocity[i] < self.high6:
##                self.highv6.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew6(self):
##        bins=30
##        x6=self.highv6
##        (yhist,xhist,patches)=hist(x6,bins)
##        stdnew6=numpy.std(x6)
##      # print stdnew6
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew6= average(x6)
##        normnew6=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y6=normnew6*exp(-((xplot -meannew6)**2)/(2*stdnew6**2))
##        plot(xplot,y6,'g-')



       #Reajust velocity cut6
      ## i=0
##        while i< len(self.allvelocity):
##            if self.allvelocity[i] > self.low7 and self.allvelocity[i] < self.high7:
##                self.highv7.append(self.allvelocity[i])
##                i=i+1
##            else:
##                i=i+1


##    def plotvelhistnew7(self):
##        bins=30
##        x7=self.highv7
##        (yhist,xhist,patches)=hist(x7,bins)
##        stdnew7=numpy.std(x7)
##        #print stdnew7
##        xmin=3000
##        xmax=15000
##        xlim(xmin,xmax)
##        xlabel('velocity dispersion')
##        meannew7= average(x7)
##        normnew7=max(yhist)

##        xplot=arange(xmin,xmax,500)
##        y7=normnew7*exp(-((xplot -meannew7)**2)/(2*stdnew7**2))
##        plot(xplot,y7,'g-')


        #Reajust velocity cut7
       i=0
       while i< len(self.allvelocity):
           if self.allvelocity[i] > self.low8 and self.allvelocity[i] < self.high8:
               self.highv8.append(self.allvelocity[i])
               i=i+1
           else:
               i=i+1


   def plotvelhistnew8(self):
       bins=30
       x8=self.highv8
       (yhist,xhist,patches)=hist(x8,bins)
       stdnew8=numpy.std(x8)
      # print stdnew8
       xmin=3000
       xmax=15000
       xlim(xmin,xmax)
       xlabel('velocity dispersion')
       meannew8= average(x8)
       normnew8=max(yhist)

       xplot=arange(xmin,xmax,500)
       y8=normnew8*exp(-((xplot -meannew8)**2)/(2*stdnew8**2))
       plot(xplot,y8,'g-')



############## Finds the biweight central location
       i=0
       while i<len(self.allvelocity):
          if self.allvelocity[i]>self.cbiMin and self.allvelocity[i]<self.cbiMax:
             self.cbi.append(self.allvelocity[i])
             i+=1
          else:
             i+=1

   def centralbi(self):
       stuff=self.cbi #with cut off
      # stuff=self.allvelocity #without cutoff
       print("Cbi")

       stuff=array(stuff,'f')
       medStuff=median(stuff)

       MAD=median(stuff-medStuff)

       ui=((stuff-medStuff)/6*MAD)

       top=sum((stuff-medStuff)*((1-(ui**2))**2))
       bottom=sum((1-ui**2)**2)

       CBI=medStuff + (top/bottom)
       print(CBI)
   
       #Find the biweight scale
       n=len(stuff)
       usbi=((stuff-medStuff)/9*MAD)
       upper1=sum(((stuff-medStuff)**2)*((1-usbi**2)**4))
       lower1=sum((1-usbi**2)*(1-5*usbi**2))
       sbi=(sqrt(n)*((sqrt(upper1))/(abs(lower1))))
       print("Sbi")
       print sbi




mkw11=cluster('MKW11')
coma=cluster('Coma')
herc=cluster('Hercules')
awm4=cluster('AWM4')
a1367=cluster('A1367')
a2052=cluster('A2052')
a2063=cluster('A2063')
ngc=cluster('NGC6107')
mkw8=cluster('MKW8')

#plot histogram
figure(1,figsize=(16,14))
subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
clf()

subplot(3,3,1)
mkw11.plotvelhist()

subplot(3,3,2)
mkw8.plotvelhist()

subplot(3,3,3)
awm4.plotvelhist()

subplot(3,3,4)
a2063.plotvelhist()

subplot(3,3,5)
a2052.plotvelhist()

subplot(3,3,6)
ngc.plotvelhist()

subplot(3,3,7)
coma.plotvelhist()

subplot(3,3,8)
a1367.plotvelhist()

subplot(3,3,9)
herc.plotvelhist()

show()




##figure(2,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew()

##subplot(3,3,2)
##mkw8.plotvelhistnew()

##subplot(3,3,3)
##awm4.plotvelhistnew()

##subplot(3,3,4)
##a2063.plotvelhistnew()

##subplot(3,3,5)
##a2052.plotvelhistnew()

##subplot(3,3,6)
##ngc.plotvelhistnew()

##subplot(3,3,7)
##coma.plotvelhistnew()

##subplot(3,3,8)
##a1367.plotvelhistnew()

##subplot(3,3,9)
##herc.plotvelhistnew()




##figure(3,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew2()

##subplot(3,3,2)
##mkw8.plotvelhistnew2()

##subplot(3,3,3)
##awm4.plotvelhistnew2()

##subplot(3,3,4)
##a2063.plotvelhistnew2()

##subplot(3,3,5)
##a2052.plotvelhistnew2()

##subplot(3,3,6)
##ngc.plotvelhistnew2()

##subplot(3,3,7)
##coma.plotvelhistnew2()

##subplot(3,3,8)
##a1367.plotvelhistnew2()

##subplot(3,3,9)
##herc.plotvelhistnew2()

##figure(4,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew3()

##subplot(3,3,2)
##mkw8.plotvelhistnew3()

##subplot(3,3,3)
##awm4.plotvelhistnew3()

##subplot(3,3,4)
##a2063.plotvelhistnew3()

##subplot(3,3,5)
##a2052.plotvelhistnew3()

##subplot(3,3,6)
##ngc.plotvelhistnew3()

##subplot(3,3,7)
##coma.plotvelhistnew3()

##subplot(3,3,8)
##a1367.plotvelhistnew3()

##subplot(3,3,9)
##herc.plotvelhistnew3()


##figure(5,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew4()

##subplot(3,3,2)
##mkw8.plotvelhistnew4()

##subplot(3,3,3)
##awm4.plotvelhistnew4()

##subplot(3,3,4)
##a2063.plotvelhistnew4()

##subplot(3,3,5)
##a2052.plotvelhistnew4()

##subplot(3,3,6)
##ngc.plotvelhistnew4()

##subplot(3,3,7)
##coma.plotvelhistnew4()

##subplot(3,3,8)
##a1367.plotvelhistnew4()

##subplot(3,3,9)
##herc.plotvelhistnew4()



##figure(6,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew5()

##subplot(3,3,2)
##mkw8.plotvelhistnew5()

##subplot(3,3,3)
##awm4.plotvelhistnew5()

##subplot(3,3,4)
##a2063.plotvelhistnew5()

##subplot(3,3,5)
##a2052.plotvelhistnew5()

##subplot(3,3,6)
##ngc.plotvelhistnew5()

##subplot(3,3,7)
##coma.plotvelhistnew5()

##subplot(3,3,8)
##a1367.plotvelhistnew5()

##subplot(3,3,9)
##herc.plotvelhistnew5()


##figure(7,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew6()

##subplot(3,3,2)
##mkw8.plotvelhistnew6()

##subplot(3,3,3)
##awm4.plotvelhistnew6()

##subplot(3,3,4)
##a2063.plotvelhistnew6()

##subplot(3,3,5)
##a2052.plotvelhistnew6()

##subplot(3,3,6)
##ngc.plotvelhistnew6()

##subplot(3,3,7)
##coma.plotvelhistnew6()

##subplot(3,3,8)
##a1367.plotvelhistnew6()

##subplot(3,3,9)
##herc.plotvelhistnew6()



##figure(8,figsize=(16,14))
##subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
##clf()

##subplot(3,3,1)
##mkw11.plotvelhistnew7()

##subplot(3,3,2)
##mkw8.plotvelhistnew7()

##subplot(3,3,3)
##awm4.plotvelhistnew7()

##subplot(3,3,4)
##a2063.plotvelhistnew7()

##subplot(3,3,5)
##a2052.plotvelhistnew7()

##subplot(3,3,6)
##ngc.plotvelhistnew7()

##subplot(3,3,7)
##coma.plotvelhistnew7()

##subplot(3,3,8)
##a1367.plotvelhistnew7()

##subplot(3,3,9)
##herc.plotvelhistnew7()



figure(9,figsize=(16,14))
subplots_adjust(left=0.1, right=.9, bottom=.1, wspace=.27, hspace=.22)
clf()

subplot(3,3,1)
mkw11.plotvelhistnew8()


subplot(3,3,2)
mkw8.plotvelhistnew8()

subplot(3,3,3)
awm4.plotvelhistnew8()

subplot(3,3,4)
a2063.plotvelhistnew8()

subplot(3,3,5)
a2052.plotvelhistnew8()

subplot(3,3,6)
ngc.plotvelhistnew8()

subplot(3,3,7)
coma.plotvelhistnew8()

subplot(3,3,8)
a1367.plotvelhistnew8()

subplot(3,3,9)
herc.plotvelhistnew8()

show()


print ("MKW11")
mkw11.centralbi()
print ("MKW8")
mkw8.centralbi()
print ("AWM4")
awm4.centralbi()
print ("A2063")
a2063.centralbi()
print ("A2052")
a2052.centralbi()
print ("NGC6107")
ngc.centralbi()
print ("Coma")
coma.centralbi()
print ("A1367")
a1367.centralbi()
print ("Hercules")
herc.centralbi()
