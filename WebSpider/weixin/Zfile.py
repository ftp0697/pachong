# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import zipfile
import os



class Zfile(object):
    def __init__(self,filename,mode='r',basedir=''):
        self.filename=filename
        self.mode=mode
        if self.mode in('w','a'):
            self.zfile=zipfile.ZipFile(filename,self.mode,compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile=zipfile.ZipFile(filename,self.mode)
        self.basedir=basedir
        if not self.basedir:
            self.basedir=os.path.dirname(filename)

    def addfile(self,path):
         if os.path.exists(path):
             if os.path.isfile(path):
                  self.zfile.write(path)
             else:
                 for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        self.zfile.write(os.path.join(dirpath,filename))



    def close(self):
        self.zfile.close()

    def extract_to(self,path):
        for p in self.zfile.namelist():
            self.extract(p,path)

    def extract(self,filename,path):
        if not filename.endswith('/'):
            f=os.path.join(path,filename)
            dir =os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f,'wb').write(self.zfile.read(filename))



def careate(zfile,files):
    z=Zfile(zfile,'w')
    z.addfile(files)
    z.close()

def extract(zfile,path):
    z=Zfile(zfile)
    z.extract_to(path)
    z.close()


