#!/usr/bin/env python

from pylab import *
import pyfits

figure()
clf()
images=['252428','space','252438']
images=array(images,'S')
fig=1
while fig<4:
    subplot(2,2,fig)
    name=('A2052-'+images[fig-1]+'-cutout-sdss.fits')
    fits=pyfits.open(name)
    im=fits[0].data.copy()
    fits.close()
    sky=median(im[im<950])
    sky=sky-19  # tweak this(9 makes NGC show up, 19 for A2052)
    axis('equal')
    imshow(log10(sqrt(im-sky)),cmap=cm.binary,vmax=1.4)#tweak this
    subplot(2,2,(fig+1))
    name=('mA2052-'+images[fig-1]+'-cutout-sdss.fits')
    fits=pyfits.open(name)
    im=fits[0].data.copy()
    fits.close()
    sky=median(im[im<950])
    sky=sky-19  # tweak this(9makes NGC show up, 19 for A2052)
    axis('equal')
    imshow(log10(sqrt(im-sky)),cmap=cm.binary,vmax=1.4)#tweak this

    fig=fig+2
show()
