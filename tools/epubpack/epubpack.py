#!/bin/env python
# ePUB packaging
# (part of epubia.googlecode.com)

import os
import zipfile

def epub_archive(arg, dir, files):
    root,epub = arg
    rdir = os.path.relpath(dir,root)
    if dir is root and 'mimetype' in files:
        epub.write(os.path.join(dir,'mimetype'), 'mimetype')
        files.remove('mimetype')
    for file in files:
        #print rdir+' -> '+file
        file2 = file.decode('euc-kr')
        if file.endswith('.xhtml') or file.endswith('.css') or file.endswith('xpgt'):
            epub.write(os.path.join(dir,file), os.path.join(rdir,file2), zipfile.ZIP_DEFLATED)
        else:
            epub.write(os.path.join(dir,file), os.path.join(rdir,file2))

def epubpack(dir, outfile):
    epub = zipfile.ZipFile(outfile,'w')
    os.path.walk(dir, epub_archive, (dir,epub))
    epub.close()

if __name__=="__main__":
    epubpack('epub','out.epub')

# vim:ts=4:sw=4:et
