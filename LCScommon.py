#!/usr/bin/env python
from pylab import *
pscale24=2.45#arcsec per pixel

pscalesdss=1.#arcsec per pixel
sdsspixelscale=0.396127#conversion for isophotal radii from pixels to arcseconds
mipspixelscale=pscale24
clusternames=['MKW11', 'MKW8', 'AWM4', 'A2063', 'A2052', 'NGC6107', 'Coma', 'A1367', 'Hercules']
clusterRA={'MKW11':202.3800, 'MKW8':220.1796, 'AWM4':241.2375, 'A2063':230.7578, 'A2052':229.1896, 'NGC6107':244.333750, 'Coma':194.9531, 'A1367':176.1231, 'Hercules':241.3125}
clusterDec={'MKW11':11.78861, 'MKW8':3.4530, 'AWM4':23.9206, 'A2063':8.6394, 'A2052':7.0003, 'NGC6107':34.901389, 'Coma':27.9807, 'A1367':19.8391, 'Hercules':17.7485}

clustervel={'MKW11':6854., 'MKW8':8100., 'AWM4':9526., 'A2063':10481., 'A2052':10647., 'NGC6107':9197., 'Coma':6900., 'A1367':8400., 'Hercules':11100.}

clustersigma={'MKW11':361, 'MKW8':325., 'AWM4':500., 'A2063':660., 'A2052':562., 'NGC6107':500., 'Coma':1000., 'A1367':745., 'Hercules':689.}

clusterz={'MKW11':.022849,'MKW8':.027,'AWM4':.031755,'A2063':.034937,'A2052':.035491,'NGC6107':.030658,'Coma':.023,'A1367':.028,'Hercules':.037}

xraycontourlevels={'MKW11':[.85,1.69,2.54],'MKW8':[.49,.99,1.48,1.98],'AWM4':[.8,1.6,2.4],'NGC6107':[1.43,2.85,4.27],'A2052':[.9,1.8,2.7,3.6],'A2063':[.9,1.8,2.7,3.6],'Hercules':[.9,1.92,2.9,3.8],'A1367':[.6,1.17,1.76,2.35],'Coma':[.88,1.76,2.63,3.51]}#used contour option in ds9 to derive these

#Group names
groupnames=['NRGb041','NRGb151','NRGb157','NRGb168','NRGb206','NRGb247','NRGb282','NRGb301','MKW8','NCG5846','NRGs076','NRGs272','NRGs385']
altgroupnames=['WBL226','MKW10','HCG59','WBL368','WBL404','MKW11test','Zw1400','WBL509','MKW8','NGC5846','WBL251','WBL477','NGC6107']
#location of Final images


#central biweight location as calculated from findbestbiweight code
clustercbi={'MKW11':6906,'MKW8':8098,'AWM4':9650,'A2063':10422,'A2052':10354.5,'NGC6107':9429,'Coma':6999,'A1367':6481,'Hercules':10957.5}

#sbi values output from +/- 4000km/s and 1 degree velocity cut from findbestbiweight code
clustersbi={'MKW11':392.37,'MKW8':491.32,'AWM4':476.67,'A2063':727.06,'A2052':626.32,'NGC6107':616.86,'Coma':937.03,'A1367':794.61,'Hercules':772.74}


# these correpond to area w/uniform 24um coverage
# center x,y,dx,dy,rotation E of N, all in degrees
cluster24Box={'MKW11':array([202.36239,11.752736,1.3138054,3.046197,27.0001],'f'), 'MKW8':array([220.18764,3.4955922,1.3188409,3.040413,13.5],'f'), 'AWM4':array([241.21434,23.872723,1.3441978,3.0241238,10],'f'), 'A2063':array([230.77172,8.6817732,1.3126447,3.0415136,13.5001],'f'), 'A2052':array([229.19761,7.0403283,1.3194664,3.0412907,13.25],'f'), 'NGC6107':array([244.30039,34.934184,1.3199655,3.0435265,322],'f'), 'Coma':array([194.86318,27.865896,1.5391027,1.976467,29.5002],'f'), 'A1367':array([176.1019,19.799614,.51080152,.90025557,31.5],'f'), 'Hercules':array([241.3065,17.771646,.51029561,.93431905,19.5001],'f')}


#solar magnitude in SDSS filters
SolarMag={'u':6.39,'g':5.07,'r':4.62,'i':4.52,'z':4.48}

#cosmology
H0=70
OmegaL=0.7
OmegaM=0.3
h=H0/100.

#bell stellar mass coefficients for sdss filters
bellug={'g':[-.221,0.485],'r':[-.099,0.345],'i':[-.053,0.268],'z':[-.105,0.226]}
bellur={'g':[-.390,0.417],'r':[-.223,0.229],'i':[-.151,0.233],'z':[-.178,0.192]}
bellui={'g':[-.375,0.359],'r':[-.212,0.257],'i':[-.144,0.201],'z':[-.171,0.165]}
belluz={'g':[-.400,0.332],'r':[-.232,0.239],'i':[-.161,0.187],'z':[-.179,0.151]}
bellgr={'g':[-.499,1.519],'r':[-.306,1.097],'i':[-.222,0.864],'z':[-.223,0.689]}
bellgi={'g':[-.379,0.914],'r':[-.220,0.661],'i':[-.152,0.518],'z':[-.175,0.421]}
bellgz={'g':[-.367,0.698],'r':[-.215,0.508],'i':[-.153,0.402],'z':[-.171,0.322]}
bellri={'g':[-.106,1.982],'r':[-.022,1.431],'i':[0.006,1.114],'z':[-.952,0.923]}
bellrz={'g':[-.124,1.067],'r':[-.041,0.780],'i':[-.018,0.623],'z':[-.041,0.463]}


deltaCutout=100.#width of cutouts in arcsec
ramin=170.#cuts for culling the ac
ramax=250.#cuts for culling the ac
decmin=0.
decmax=38.#cuts for culling the ac
zmin=0.01366#min z cut, z(coma)-3 sigma
zmax=0.04333#max z cut, z(A2052)+3 sigma
vmin=zmin*3.e5
vmax=zmax*3.e5
#cutoutpath='/home/rfinn/research/LocalClusters/cutouts/'
cutoutpath='/home/rfinn/research/LocalClusters/cutouts/'

Lsol=3.826e33#normalize by solar luminosity
bellconv=9.8e-11#converts Lir (in L_sun) to SFR/yr
bellconv=4.5e-44#Kenn 98 conversion fro erg/s to SFR/yr
