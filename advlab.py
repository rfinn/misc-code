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



##preliminary redshift vs. M_r plot
#figure(1)
#plot(nsa.ndat.ZDIST, nsa.ndat.ABSMAG[:,4],'k.')
#ylim(-10,-26,2)
#xlabel ('Redshift(zdist)')
#ylabel ('M_r (magnitude)')

## redshift vs. M_r using hexbin
figure(2)
hexbin(nsa.ndat.ZDIST, nsa.ndat.ABSMAG[:,4])
ylim(-10,-26,2)
xlabel ('Redshift(zdist)')
ylabel ('M${_r}$ (magnitude)')
savefig('absmag_redshift.png')




#############################################################

## MKW11_nsa.fits.gz file
class NSA:
    def __init__(self):
       # infile=homedir+'research/NSA/nsa_v0_1_2.fits'
        infile2= '/home/ioannis/lcs/mkw11_nsa.fits.gz'

        #nsa_dat=atpy.Table(infile)
        mkw11dat=pyfits.open(infile2)
        self.mkw11dat=mkw11dat[1].data
        #keepflag = ones(len(self.ndat))
        self.ra=self.mkw11dat.RA
        self.dec=self.mkw11dat.DEC
        self.redshift=self.mkw11dat.Z

        # cull for LCS
        keepflag=(self.redshift > zmin) & (self.redshift < zmax) & (self.ra > 170.) & (self.ra < ramax) & (self.dec > decmin) & (self.dec < decmax)
        #self.ra=self.ndat.RA[keepflag]
        #self.dec=self.ndat.DEC[keepflag]
        #self.redshift=self.ndat.Z[keepflag]
        
nsa=NSA()



class LIR:
    def __init__(self):
       # infile=homedir+'research/NSA/nsa_v0_1_2.fits'
        infile3= '/home/ioannis/lcs/mkw11_lir.fits.gz'

        #nsa_dat=atpy.Table(infile)
        mkw11lir=pyfits.open(infile3)
        self.mkw11lir=mkw11lir[1].data
        #keepflag = ones(len(self.ndat))
        self.ra=self.mkw11lir.RA
        self.dec=self.mkw11lir.DEC
        #self.redshift=self.mkw11lir.Z

        # cull for LCS
       # keepflag=(self.redshift > zmin) & (self.redshift < zmax) & (self.ra > 170.) & (self.ra < ramax) & (self.dec > decmin) & (self.dec < decmax)
        #self.ra=self.ndat.RA[keepflag]
        #self.dec=self.ndat.DEC[keepflag]
        #self.redshift=self.ndat.Z[keepflag]
        
lir=LIR()


color_mkw11 = nsa.mkw11dat.ABSMAG[:,1] - nsa.mkw11dat.ABSMAG[:,4];
mass_mkw11=nsa.mkw11dat.MASS;
z_mkw11=abs(lir.mkw11lir.LIR_CHARY);

## preliminary log(stellar mass) vs NUV-r plot
#figure(3)
#plot(log10(mass),color,'k.')
#ylim(0,8,1)
#xlim(7,12,1)
#title('MKW11')
#xlabel('log$_{10}$(M/M_o)')
#ylabel ('NUV-r')
###savefig('initial_colormass_plot.png')


## log(stellar mass) vs. NUV-r plot with cut at L(IR)=10
#figure(4)
#lircut = 10
#lirbright_flag = lir.mkw11lir.LIR_CHARY > lircut
#p1=plot(log10(mass_mkw11[lirbright_flag]),color_mkw11[lirbright_flag],'bo')
#p2 = plot (log10(mass_mkw11[~lirbright_flag]),color_mkw11[~lirbright_flag],'r.')
#ylim(0,7,1)
#xlim(7,12,1)
#fontsizeticks=10;
#size=17;
#yticks(fontsize =fontsizeticks)
#xticks(fontsize = fontsizeticks)
#title ('MKW11',fontsize=size)
#xlabel('log$_{10}(M/M_{\odot}$)',fontsize=size)
#ylabel ('NUV-r',fontsize=size)
#legend((p1,p2),('L(IR)>10','L(IR)<10'),loc='best')
#savefig('mkw11_colormass_initial.png')

#names=lir.mkw11lir.NSAID[lirbright_flag];
#print names


## log(stellar mass) vs. NUV-r plot where different color dots represent differing luminosities
figure(5)
sc=scatter(log10(mass_mkw11),color_mkw11,c=z_mkw11,vmin=9,vmax=11);
cb=colorbar(sc)
cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
ylim(0,7,1)
xlim(7,12,1)
fontsizeticks=10;
size=17;
yticks(fontsize =fontsizeticks)
xticks(fontsize = fontsizeticks)
title ('MKW11',fontsize=size)
xlabel('log$_{10}(M/M_{\odot}$)',fontsize=size)
ylabel ('NUV-r',fontsize=size)
savefig('mkw11_colormass_colorbar.png')

## RA vs. DEC plot where different color dots represent differing luminosities
#figure(6)
#x_mkw11=nsa.mkw11dat.RA;
#y_mkw11=nsa.mkw11dat.DEC;
##z_mkw11=abs(lir.mkw11lir.LIR_CHARY);
#sp=scatter(x_mkw11,y_mkw11,c=z_mkw11,vmin=9,vmax=11);
##cb=colorbar(sp)
#cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
#yticks(fontsize =fontsizeticks)
#xticks(fontsize = fontsizeticks)
#xlabel('RA(deg)',fontsize=size)
#ylabel('DEC(deg)',fontsize=size)
#title('MKW11',fontsize=size)
#savefig('mkw11_radec.png') 

# subtract out cluster center so that the axis are set at cluster center
figure(7)
x_mkw11=nsa.mkw11dat.RA;
y_mkw11=nsa.mkw11dat.DEC;
#z_mkw11=abs(lir.mkw11lir.LIR_CHARY);
deltara_mkw11= nsa.mkw11dat.RA-202.3800;
deltadec_mkw11 = nsa.mkw11dat.DEC-11.78861 ;
sp=scatter(deltara_mkw11,deltadec_mkw11,c=z_mkw11,vmin=9,vmax=11);
cb=colorbar(sp)
cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
yticks(fontsize =fontsizeticks)
xticks(fontsize = fontsizeticks)
xlabel('$\delta$ RA(deg)',fontsize=size)
ylabel('$\delta$ DEC(deg)',fontsize=size)
title('MKW11',fontsize=size)
savefig('mkw11_radec_new.png')

#############################################################################
class NSA:
    def __init__(self):
       # infile=homedir+'research/NSA/nsa_v0_1_2.fits'
        infile4= '/home/ioannis/lcs/coma_nsa.fits.gz'

        #nsa_dat=atpy.Table(infile)
        comadat=pyfits.open(infile4)
        self.comadat=comadat[1].data
        #keepflag = ones(len(self.ndat))
        self.ra=self.comadat.RA
        self.dec=self.comadat.DEC
        self.redshift=self.comadat.Z

        # cull for LCS
        keepflag=(self.redshift > zmin) & (self.redshift < zmax) & (self.ra > 170.) & (self.ra < ramax) & (self.dec > decmin) & (self.dec < decmax)
        #self.ra=self.ndat.RA[keepflag]
        #self.dec=self.ndat.DEC[keepflag]
        #self.redshift=self.ndat.Z[keepflag]
        
nsa=NSA()



class LIR:
    def __init__(self):
       # infile=homedir+'research/NSA/nsa_v0_1_2.fits'
        infile5= '/home/ioannis/lcs/coma_lir.fits.gz'

        #nsa_dat=atpy.Table(infile)
        comalir=pyfits.open(infile5)
        self.comalir=comalir[1].data
        #keepflag = ones(len(self.ndat))
        self.ra=self.comalir.RA
        self.dec=self.comalir.DEC
       
lir=LIR()

color_coma = nsa.comadat.ABSMAG[:,1] - nsa.comadat.ABSMAG[:,4];
mass_coma=nsa.comadat.MASS;
z_coma=abs(lir.comalir.LIR_CHARY);



figure(8)
sc=scatter(log10(mass_coma),color_coma,c=z_coma,vmin=9,vmax=11);
cb=colorbar(sc)
cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
ylim(0,7,1)
xlim(7,12,1)
fontsizeticks=10;
size=17;
yticks(fontsize =fontsizeticks)
xticks(fontsize = fontsizeticks)
title ('Coma',fontsize=size)
xlabel('log$_{10}(M/M_{\odot}$)',fontsize=size)
ylabel ('NUV-r',fontsize=size)
savefig('coma_colormass_colorbar.png')

## RA vs. DEC plot where different color dots represent differing luminosities
#figure(9)
#x_coma=nsa.comadat.RA;
#y_coma=nsa.comadat.DEC;
#z_coma=abs(lir.comalir.LIR_CHARY);
#sp=scatter(x_coma,y_coma,c=z_coma,vmin=9,vmax=11);
#cb=colorbar(sp)
#cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
#yticks(fontsize =fontsizeticks)
#xticks(fontsize = fontsizeticks)
#xlabel('RA(deg)',fontsize=size)
#ylabel('DEC(deg)',fontsize=size)
#title('Coma',fontsize=size)
#savefig('coma_radec.png') 

# subtract out cluster center so that the axis are set at cluster center
figure(10)
#x=nsa.mkw11dat.RA;
#y=nsa.mkw11dat.DEC;
#z=abs(lir.mkw11lir.LIR_CHARY);
deltara_coma= nsa.comadat.RA-194.9531 ;
deltadec_coma = nsa.comadat.DEC-27.9807 ;
sp=scatter(deltara_coma,deltadec_coma,c=z_coma,vmin=9,vmax=11);
cb=colorbar(sp)
cb.ax.set_ylabel('log$_{10}[L(IR)/L_{\odot}$]')
yticks(fontsize =fontsizeticks)
xticks(fontsize = fontsizeticks)
xlabel('$\delta$ RA(deg)',fontsize=size)
ylabel('$\delta$ DEC(deg)',fontsize=size)
title('Coma',fontsize=size)
savefig('coma_radec_new.png')


show()
