#! /bin/env python

import sys
__program__ = sys.modules['__main__'].__program__
__version__ = sys.modules['__main__'].__version__

CONTAINER = '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
'''

import zipfile
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
    from Cheetah.Template import Template

    if coverimg: coverfmt = 'jpeg'
    else:        coverfmt = ''

    # OPF
    f = open(os.path.join(tmpldir, 'content.opf'),'r')
    opf_tmpl = f.read(); f.close()
    import time
    geninfo = {'name':__program__,
               'version':__version__,
               'timestamp':time.strftime("%Y-%m-%d"),
               'coverfmt':coverfmt,
              }
    opf = str( Template(opf_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )

    # NCX
    f = open(os.path.join(tmpldir, 'toc.ncx'),'r')
    ncx_tmpl = unicode(f.read(),'utf-8'); f.close()
    ncx = str( Template(ncx_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )

    # title page
    f = open(os.path.join(tmpldir, 'titlepage.xhtml'),'r')
    titpg_tmpl = f.read(); f.close()
    titpg = str( Template(titpg_tmpl, searchList=[ {'book':book} ]) )

    # chapter files
    f = open(os.path.join(tmpldir, 'chapter.xhtml'),'r')
    ch_tmpl = f.read(); f.close()
    ch_list = []
    num = 0
    for ch in chhtm:
        num += 1
        html = str( Template(ch_tmpl, searchList=[ {'book':book, 'ch':ch} ]) )
        ch_list.append( ("chapter%d.xhtml" % num, html) )

    epub = EPubFile(outfile)
    if coverfmt:
        if coverimg.startswith('http'):
            import urllib
            imgdata = urllib.urlopen(coverimg).read()
            epub.addData(imgdata, '', 'cover.'+coverfmt)
        else:
            epub.addFile(coverimg, '', 'cover.'+coverfmt)
        # coverpage
        f = open(os.path.join(tmpldir, 'coverpage.xhtml'),'r')
        cvrpg_tmpl = f.read(); f.close()
        cvrpg = str( Template(cvrpg_tmpl, searchList=[ {'gen':geninfo} ]) )
        epub.addData(cvrpg, '', 'coverpage.xhtml')
    epub.addFile(os.path.join(tmpldir,'generic.css'), 'OPS', 'generic.css')
    epub.addFile(targetcss, 'OPS', 'target.css')
    epub.addData(titpg, 'OPS', 'titlepage.xhtml')
    for fname,html in ch_list:
        epub.addData(html, 'OPS', fname)
    epub.addData(opf, '', 'content.opf')
    epub.addData(ncx, '', 'toc.ncx')

    epub.close()
    epub = None

if __name__ == "__main__":
    outname = "test.epub"
    cover   = "cover.jpeg"
    mainhtm = "html_test.htm"
    tgtcss  = "test.css"

    from Cheetah.Template import Template
    from txt_parser import _book, _chapter
    book = _book(title='Test Book',author='Anonymous')
    book.chapter = [ _chapter(id='1',title='Chapter 1',anchor='id_ch001'),
                     _chapter(id='2',title='Chapter 2',anchor='id_ch002') ]

    f = open(mainhtm, 'r')
    htm = f.read(); f.close()
    print htm
    epub_gen(book, htm, cover, "../ptxt2epub/template", tgtcss, outname)
# vim:ts=4:sw=4:et
