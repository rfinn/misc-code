#!/usr/bin/env python
from pylab import *

figure(1)
clf()
axes()
cir=Circle((0,0),radius=.75,alpha=.2, ec='g', lw=5, fill=False)
gca().add_patch(cir)
axis('scaled')
show()


