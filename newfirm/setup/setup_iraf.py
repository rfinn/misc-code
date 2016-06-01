#!/usr/bin/env python
# $Id: setup_iraf.py 9 2008-08/26 12:52:58Z nmbs $
# TODO: if rerun on same log file, dont make new directories
#
#Chun Ly: Made some modifications starting with Ivo's script
#and changing the input files since they are not label with a prefix of 'raw'
#Also change the header keyword for OBJECT
#

import os
import sys
import shutil
import string
from math import *
from numarray import *
import string, commands

debug=0
verbose = 1
o = os.system
dbadpix = 'calib/badpix/'
ddark = 'calib/dark'
dflat = 'calib/flat/'
draw = 'raw'  
dref = 'calib/refimage/'
log = '00NIGHT_LOG.cat'
fields = 'setup/00FIELDS.cat'

radeg=180/pi
distance_lim=5.0/60.0 # [degrees] if pointing within some angle, assume we are on the right field

if not os.access(fields,os.F_OK):
   print('NOTE: no fields file found, please provide a file ',fields,' containing 3 columns: fieldname, ra, dec')
   sys.exit()

# ------------------------------------------------------------ begin class cat 
class cat:
   """Simple catalog class.""" 

   def __init__(self,catfile=None):
      if catfile is None:
         self.data = []
         self.hdr = []
         self.datatype=[]
      else: self.load(catfile)
  
   # load catalog, give filename
   def load(self,catfile):
      f = open(catfile)
      lines = f.readlines()
      f.close()
      self.hdr = string.split(lines[0].lower().replace('#',''))
      self.data = []
      for line in lines[1:]: self.data.append(string.split(line))
   #end load
   
   # select columns given list of header keywords
   def col(self,keylis):
      """Select columns keylis from catalog"""
      
      keylis = keylis.lower().split()
      
      ikeys=[]
      for key in keylis:
         ikeys.append(self.hdr.index(key))
         cols=[]
         
      # in each row, select one or more columns
      for row in self.data:
         c=[]
         if debug: print row
         for i in ikeys:
            if i > len(row): 
               print "WARNING: too few elements in row "+row
               continue
            try: # if cannot eval to float or int, use string
               c.append(eval(row[i]))
            except (SyntaxError,TypeError,NameError):
               c.append(row[i]) 
               
         # if only one key, write plain list i.s.o. nested  
         if len(ikeys) == 1: 
            cols.append(c[0])
         else: cols.append(c)
          
      return cols
   #end col

# --------------------------------------- end class cat 
 
# from skyangles to degrees
def todeg(angle):
   a = angle.split(':')
   return int(a[0])+int(a[1])/60.+float(a[2])/3600. 
#end todeg

# find first field within distance_lim of ra,dec
def resolvefield(ra,dec,fl,verbose):
   a1 = todeg(ra)*15.
   d1 = todeg(dec)
   # loop fields
   for name,ra2,dec2 in zip(fl.col('name'),fl.col('ra'),fl.col('dec')):
      a2 = todeg(ra2)*15.
      d2 = todeg(dec2)
      dist = sqrt((d1-d2)**2 + ((a1-a2)*cos(d1*pi/180))**2)
      if dist < distance_lim:
         if verbose == 1: print 'resolved field ',a1,d1, ' = ', name, ' (distance ',dist, 'deg)' 
         return name
#      else:
#         if verbose == 1: print a1,d1
      
   # we found no matching field
   return 'UNKNOWN'
#end resolvefield

# ---------------------------------------------------------- script starts here
if len(sys.argv) != 3 :
   print 'usage: $ setup/setup_iraf.py [path_to_raw_data/night] [code dir]'
   print 'e.g.: $ setup/setup_iraf.py /Volumes/NEWFIRM1/20080325 /codes'
   sys.exit()

if not os.access('calib',os.F_OK):
   os.mkdir('calib')
   os.mkdir(ddark)
   os.mkdir(dflat)
   os.mkdir(dbadpix)
   os.mkdir(dref)
   print 'note: calibration files in the following directories are required: '
   print './calib ./calib/dark ./calib/flat ./calib/badpix ./calib/refimage'
   
dsrc = sys.argv[1] ; print dsrc
codes = sys.argv[2] ; print codes

# assume night dir the deepest subdir in the provided path
#dsrc = dsrc.replace('/raw','')
for dir in dsrc.split('/'):
   if len(dir) > 0: dnight = dir

if not os.access(dnight,os.F_OK):
   os.mkdir(dnight)

#create common psf_contours.csh and linking to samir's stuff
o('cp -af setup/keyword_flag.txt '+dnight)
o('ln -s ../setup/normzpt.fits '+dnight)
o('ln -s '+codes+'/newfirm/run_nfextern.py '+dnight+'/run_nfextern.py')
o('ln -s ~/login.cl '+dnight)

# change to the night dir
os.chdir(dnight)

#make field_stack.dat
f0=open('field_stack.dat','w')
f0.write('#prefix \tlist.sci.all \t\tlist.sci.stack                flat 		               bpm 		              2MASS_image  MP_sigma\n')

# in the night directory: link the raw and calib directory
if os.access(dsrc,os.F_OK):
   if os.access(draw,os.F_OK):
      os.system('rm raw')
   os.system('ln -s '+dsrc+' '+draw)
   if verbose: print('linking '+dsrc+' to '+draw)

if not os.access('calib',os.F_OK):
   os.system('ln -s ../calib')

# get summary of vital keywords 
# note: wcstools need to be installed
if verbose: print('getting header keywords of all fits files: this may take a minute...')
hkey="FILENAME OBSTYPE TELRA TELDEC OBJECT EXPCOADD NCOADD EXPTIME  NOCNO NOCTOT TIME-OBS FILTER FSAMPLE DIGAVGS"
if not os.access(log,os.F_OK):
   o('echo "# '+hkey+' " | sed s/-//g > '+log)
#   o('gethead -bf '+hkey+' raw/S*.fits | sed s/\.fits// >> '+log) #do not have *.fits.gz
   o('gethead -bf '+hkey+' raw/raw*.fits | sed s/\.fits// >> '+log) #do not have *.fits.gz
#   o('gethead -bf '+hkey+' raw/c*.fits | sed s/\.fits// >> '+log) #do not have *.fits.gz
   dir_make = 1
else:
   print "File "+log+" exists. Might need to delete if you want to recreate."
   dir_make = 0

# night log
nl = cat(log)
nl_frame = nl.col('filename')
nl_obj = nl.col('object') 
nl_ditnr = nl.col('nocno')
nl_filt = nl.col('filter')
nl_ncoadd = nl.col('ncoadd') 
nl_expcoadd = nl.col('expcoadd') 
nl_fsample = nl.col('fsample')
nl_digavgs = nl.col('digavgs')
# this is wrong: use crval1,2
nl_ra = nl.col('telra') 
nl_dec = nl.col('teldec') 

#field centers
fl = cat('../'+fields)

print 'extracting skysub sequences'
filt0=''; mark=0 # ='' marks the start of a new filter+field sequence
if len(nl_frame) > 0:
   f2=open('list.raw.all', 'w')

for i in range(len(nl_frame)):
   if nl_obj[i] == 'Object_Dither' or 'DitherStare_Field' or 'Standard_Obs':
      # if dither follow number drops: signals a new sequence
      # print i, filt0, str(nl_filt[i])
      if filt0 == '': # or str(nl_filt[i]) != filt0:
         if i != 0:
            i=i-1; mark=1

         #print i, nl_frame[i]
         # start new sequence
         print '\nfound new dither sequence: filter='+str(nl_filt[i])
         field0 =  resolvefield(nl_ra[i],nl_dec[i],fl,1)
         outfile0 = field0+'_'+str(nl_filt[i])+'-0'
         refimage0 = dref+'2mass_'+field0+'_0.4.fits' #updated on 08/08/08

         # make unique filenames a la iraf if already exists
         #if dir_make:
         while os.access(outfile0,os.F_OK): # and filt0 != '':
            tmpout = outfile0.split('-')
            if len(tmpout) == 1:  # this is the second FIELD_FILTER -> so make FIELD_FILTER.1
               outfile0=outfile0+'-1'
            else: outfile0=tmpout[0]+'-'+str(int(tmpout[1])+1) # make FIELD_FILTER.[N] -> FIELD_FILTER.[N+1]
         else: os.mkdir(outfile0)
         if not os.access(outfile0,os.F_OK): os.mkdir(outfile0)

         txt = '%s %15s.raw.lis %15s.raw.stack.lis %s %s %s 10 \n' % (str.ljust(outfile0,15), outfile0, outfile0,
                                                                      dflat+dnight+'_'+outfile0+'_'+'skyflat.fits',
                                                                      dbadpix+dnight+'_bpm.fits', refimage0)
         f0.write(txt)

         #else:
            #tmpout = outfile0.split('.')
            #print tmpout
            #if len(tmpout) == 1:  # this is the second FIELD_FILTER -> so make FIELD_FILTER.1
            #   outfile0=outfile0+'.1'
            #else: outfile0=tmpout[0]+'.'+str(int(tmpout[1])+1) # make FIELD_FILTER.[N] -> FIELD_FILTER.[N+1]
         #endelse

         f=open(outfile0+'.raw.lis','w') #open file if it is new
         f.write('T_'+nl_frame[i]+'.fits\n') #format is just filename. No raw/ part
         f2.write(nl_frame[i]+'.fits\n') #format is just filename. No raw/ part

         if mark:
            f.write('T_'+nl_frame[i+1]+'.fits\n') #format is just filename. No raw/ part
            f2.write(nl_frame[i+1]+'.fits\n') #format is just filename. No raw/ part
            mark = 0
         
         filt0 = str(nl_filt[i])
      else:
         #endif write frame to current sequence
         #print nl_frame[i], filt0, nl_filt[i]
         field = resolvefield(nl_ra[i],nl_dec[i],fl,0)
         if field == field0 and str(nl_filt[i]) == filt0:
            f.write('T_'+nl_frame[i]+'.fits\n')
            f2.write(nl_frame[i]+'.fits\n')
            filt0=str(nl_filt[i])
         else:
            filt0 = '' #; print nl_frame[i], i
            f.close()
            o('cp '+outfile0+'.raw.lis '+outfile0+'.raw.stack.lis')
            #o("awk '{print \"T_\" $0}' < test.lis > "+outfile0+"/raw.stack.lis") #format is T_*.fits
            #o("awk '{sub(/raw\//, \"T_\"); print }' < test.lis > "+outfile0+"/raw.stack.lis")

            fsize = commands.getstatusoutput('wc '+outfile0+'.raw.lis'); print fsize[1]
      #endelse
   #endif
#endfor
f.close()  # close last sequence
o('cp '+outfile0+'.raw.lis '+outfile0+".raw.stack.lis")
#o("awk '{print \"T_\" $0}' < test.lis > "+outfile0+"/raw.stack.lis") #format is T_*.fits
fsize = commands.getstatusoutput('wc '+outfile0+'.raw.lis'); print fsize[1]
commands.getstatusoutput('rm test.lis')
f0.close() #field_stack
f2.close() #full_list
sys.exit()
