# -*- coding: utf-8 -*-
# ePUB generator with Cheetah template

import sys
__program__ = sys.modules['__main__'].__program__
__version__ = sys.modules['__main__'].__version__

OPS_DIR = 'OPS'

CONTAINER = '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
'''

from Cheetah.Template import Template
from StringIO import StringIO
import zipfile
import Image
import os

class EPubFile:
    def __init__(self, name):
        self.epub = zipfile.ZipFile(name, 'w')
        self.addData('application/epub+zip', '', 'mimetype')
        self.addData(CONTAINER, 'META-INF', 'container.xml')

    def __del__(self):
        self.close()

    def close(self):
        if self.epub is not None:
            self.epub.close()
            self.epub = None

    def addFile(self, fullname, subdir, relativeName):
        self.epub.write(fullname, os.path.join(subdir, relativeName))

    def addData(self, data, subdir, relativeName):
        self.epub.writestr(os.path.join(subdir, relativeName), data)

def epub_gen(book, chhtm, coverimg, tmpldir, targetcss, outfile):
    # cover image
    if coverimg:
        if coverimg.startswith('http'):
            import urllib
            imgdata = urllib.urlopen(coverimg).read()
        else:
            imgdata = open(coverimg,'rb').read()
        img = Image.open(StringIO(imgdata))
        sizelimit = (570, 650)
        if img.size[0] > sizelimit[0]:
            img = img.resize([sizelimit[0], int(img.size[1]*sizelimit[0]/img.size[0])], Image.ANTIALIAS)
        if img.size[1] > sizelimit[1]:
            img = img.resize([int(img.size[0]*sizelimit[1]/img.size[1]), sizelimit[1]], Image.ANTIALIAS)
        #img = ImageOps.grayscale(img)
        coverfmt = 'png'
        buf = StringIO()
        img.save(buf, format=coverfmt)
        imgdata = buf.getvalue()
    else:
        coverfmt = ''

    # OPF
    opf_tmpl = open(os.path.join(tmpldir, 'content.opf'),'r').read()
    import time
    geninfo = {'name':__program__,
               'version':__version__,
               'timestamp':time.strftime("%Y-%m-%d"),
               'coverfmt':coverfmt,
              }
    opf = str( Template(opf_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )

    # NCX
    ncx_tmpl = unicode(open(os.path.join(tmpldir, 'toc.ncx'),'r').read(),'utf-8')
    ncx = str( Template(ncx_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )

    # title page
    titpg_tmpl = open(os.path.join(tmpldir, 'titlepage.xhtml'),'r').read()
    titpg = str( Template(titpg_tmpl, searchList=[ {'book':book} ]) )

    # chapter files
    ch_tmpl = open(os.path.join(tmpldir, 'chapter.xhtml'),'r').read()
    ch_list = []
    num = 0
    for ch in chhtm:
        num += 1
        html = str( Template(ch_tmpl, searchList=[ {'book':book, 'ch':ch} ]) )
        ch_list.append( ("chapter%d.xhtml" % num, html) )

    epub = EPubFile(outfile)
    if coverfmt:
        # cover image
        epub.addData(imgdata, '', 'cover.'+coverfmt)
        # coverpage
        cvrpg_tmpl = open(os.path.join(tmpldir, 'coverpage.xhtml'),'r').read()
        cvrpg = str( Template(cvrpg_tmpl, searchList=[ {'gen':geninfo} ]) )
        epub.addData(cvrpg, '', 'coverpage.xhtml')
    epub.addFile(os.path.join(tmpldir,'generic.css'), OPS_DIR, 'generic.css')
    epub.addFile(targetcss, OPS_DIR, 'target.css')
    epub.addData(titpg, OPS_DIR, 'titlepage.xhtml')
    for fname,html in ch_list:
        epub.addData(html, OPS_DIR, fname)
    epub.addData(opf, '', 'content.opf')
    epub.addData(ncx, '', 'toc.ncx')

    epub.close()
    epub = None

if __name__ == "__main__":
    outname = "test.epub"
    cover   = "cover.jpeg"
    mainhtm = "html_test.htm"
    tgtcss  = "test.css"

    from txt_parser import _book, _chapter
    book = _book(title='Test Book',author='Anonymous')
    book.chapter = [ _chapter(id='1',title='Chapter 1',anchor='id_ch001'),
                     _chapter(id='2',title='Chapter 2',anchor='id_ch002') ]

    htm = open(mainhtm, 'r').read()
    print htm
    epub_gen(book, htm, cover, "../ptxt2epub/template", tgtcss, outname)
# vim:ts=4:sw=4:et
