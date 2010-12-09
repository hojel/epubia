# -*- coding: utf-8 -*-
# ePUB generator with Cheetah template
#   input: {'title', 'author', 'isbn', 'cover_url', 'chapter'}

import sys
__program__ = sys.modules['__main__'].__program__
__version__ = sys.modules['__main__'].__version__

OPS_DIR = 'OPS'
IMG_FMT = 'png'
import re
IMG_PTN = re.compile('<img [^>]*src="(.*?)"',re.M)

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

def copy_image(url, fp, basedir='.'):
    try:
        if url.startswith('http://'):
            import urllib
            imgdata = urllib.urlopen(url).read()
        else:
            if url.startswith('file://'):
                url = url[7:]
            if url[1:2] != ':/':    # (eg. C:/ )
                url = os.path.join(basedir,url)
            imgdata = open(url,'rb').read()
    except:
        return False
    img = Image.open(StringIO(imgdata))
    sizelimit = (480, 640)
    if img.size[0] > sizelimit[0]:
        newsz = ( sizelimit[0], int(img.size[1]*sizelimit[0]/img.size[0]) )
        if newsz[1] > sizelimit[1]:
            img = img.resize([int(img.size[0]*sizelimit[1]/img.size[1]), sizelimit[1]], Image.ANTIALIAS)
        else:
            img = img.resize([sizelimit[0], int(img.size[1]*sizelimit[0]/im.size[0])], Image.ANTIALIAS)
    #img = ImageOps.grayscale(img)
    img.save(fp, format=IMG_FMT)
    return True

def epubgen(book, outfile, target_css, template_dir='./template', src_dir='.'):
    import time
    geninfo = {'name':__program__,
               'version':__version__,
               'timestamp':time.strftime("%Y-%m-%d"),
               'hascover':False,
              }

    epub = EPubFile(outfile)

    # cover image
    if 'cover_url' in book and book['cover_url']:
        buf = StringIO()
        if not copy_image( book['cover_url'], buf, basedir=src_dir ):
            return
        imgdata = buf.getvalue()
        # cover image
        epub.addData(imgdata, '', 'cover.'+IMG_FMT)
        # coverpage
        cvrpg_tmpl = open(os.path.join(template_dir, 'coverpage.xhtml'),'r').read()
        cvrpg = str( Template(cvrpg_tmpl, searchList=[ {'gen':geninfo} ]) )
        epub.addData(cvrpg, '', 'coverpage.xhtml')
        geninfo['hascover'] = True

    # title page
    titpg_tmpl = open(os.path.join(template_dir, 'titlepage.xhtml'),'r').read()
    titpg = str( Template(titpg_tmpl, searchList=[ {'book':book} ]) )
    epub.addData(titpg, OPS_DIR, 'titlepage.xhtml')

    # chapter files
    ch_tmpl = open(os.path.join(template_dir, 'chapter.xhtml'),'r').read()
    img_list = []
    imgcnt = 0
    for ch in book['chapter']:
        # extract images
        html = ch['html']
        for url in IMG_PTN.findall(html):
            imgcnt += 1
            buf = StringIO()
            if not copy_image( url, buf, basedir=src_dir ):
                print >> sys.stderr, "ERROR: can not read %s" % url
            imgdata = buf.getvalue()
            fname = "image%d.%s" % (imgcnt, IMG_FMT)
            epub.addData(imgdata, OPS_DIR+"/image", fname)
            html = html.replace(url, "image/"+fname)
            img_list.append( "image/"+fname )
        ch['html'] = html
        # store in ZIP
        html = str( Template(ch_tmpl, searchList=[ {'book':book, 'ch':ch} ]) )
        epub.addData(html, OPS_DIR, "chapter%d.xhtml" % ch['num'])
    book['image'] = img_list

    # OPF
    opf_tmpl = open(os.path.join(template_dir, 'content.opf'),'r').read()
    opf = str( Template(opf_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )
    epub.addData(opf, '', 'content.opf')

    # NCX
    ncx_tmpl = unicode(open(os.path.join(template_dir, 'toc.ncx'),'r').read(),'utf-8')
    ncx = str( Template(ncx_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )
    epub.addData(ncx, '', 'toc.ncx')

    # CSS
    epub.addFile(os.path.join(template_dir,'generic.css'), OPS_DIR, 'generic.css')
    epub.addFile(target_css, OPS_DIR, 'target.css')

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
    epubgen(book, outname, target_css=tgtcss)
# vim:ts=4:sw=4:et
