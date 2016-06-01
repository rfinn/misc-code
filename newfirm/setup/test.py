import os
import sys
import shutil
import string
from math import *
from numarray import *
import string

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

dirfile="dir.dat"
os.system('ls -l | grep drw | grep "\.1" > test')
os.system("awk 'BEGIN{print \"# DIRECTORY\"} {test=NF; print $test}' < test > "+dirfile)
n2=cat(dirfile)
n2_dir = n2.col('directory')
n2_dir.replace('.1', '')
print, n2_dir
for i in range(len(n2_dir)):
   if not os.access(n2_dir[i]+'.0',os.F_OK):
      os.mkdir(n2_dir[i]+'.0')
#      n2_dir[i].replace('.0', '')
      cmd = "cat "+n2_dir[i]+"*/raw.lis > "+n2_dir[i]+'.0/raw.lis'
      os.system(cmd)
   #endif
#endfor

