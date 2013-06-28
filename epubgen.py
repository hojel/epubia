# -*- coding: utf-8 -*-
# ePUB generator with Cheetah template
#   input: {'title', 'author', 'isbn', 'cover_url', 'chapter'}

import sys
__program__ = sys.modules['__main__'].__program__
__version__ = sys.modules['__main__'].__version__

OPS_DIR  = 'OPS'
IMG_SIZE = (600,800)

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
from PIL import Image
import os

class EPubFile:
    def __init__(self, name):
        self.epub = zipfile.ZipFile(name, 'w')
        self.addData('application/epub+zip', '', 'mimetype')
        self.saveData(CONTAINER, 'META-INF', 'container.xml')

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

    def saveData(self, data, subdir, relativeName):
        self.epub.writestr(os.path.join(subdir, relativeName), data, zipfile.ZIP_DEFLATED)

def copy_image(url, fp, basedir='.', maxsize=None, bw=False):
    pos = url.rfind('.',-5)
    if pos < 0:
        fmt = ''
    else:
        fmt = url[pos+1:].lower()
    try:
        if url.startswith('http://'):
            print 'download image from %s' % url
            import urllib
            imgdata = urllib.urlopen(url).read()
        else:
            if url.startswith('file://'):
                url = url[7:]
            url = os.path.join(basedir,url)
            imgdata = open(url,'rb').read()
    except:
        return None

    try:
        img = Image.open(StringIO(imgdata))
    except:
        return None
    
    # Scale
    if maxsize and (img.size[0] > maxsize[0] or img.size[1] > maxsize[1]):
        xscale = float(maxsize[0]) / img.size[0]
        yscale = float(maxsize[1]) / img.size[1]
        if xscale > yscale:
            img = img.resize([int(img.size[0]*yscale), maxsize[1]], Image.ANTIALIAS)
        else:
            img = img.resize([maxsize[0], int(img.size[1]*xscale)], Image.ANTIALIAS)
    if fmt=='png' or fmt=='jpeg':
        pass
    elif fmt=='gif':
        fmt = 'png'
    elif fmt=='jpg':
        fmt = 'jpeg'
    else:
        print "WARNING: image has unknown format, %s" % fmt
        img = img.convert('RGB')
        fmt = 'png'
    if bw:  # Dither
        img = img.convert('L')  # 'L'(gray)/'1'(1b)
    img.save(fp, format=fmt)
    return fmt

def epubgen(book, outfile, target_css, template_dir='./template', src_dir='.',
            fontfile='arial.ttf', toclevel=2):
    import time
    import uuid
    geninfo = {'name':__program__,
               'version':__version__,
               'timestamp':time.strftime("%Y-%m-%d"),
               'coverimage':None,
               'uuid':uuid.uuid4(),
               'toclevel':toclevel,
              }

    epub = EPubFile(outfile)

    # cover image
    if 'cover_url' in book and book['cover_url']:
        buf = StringIO()
        fmt = copy_image( book['cover_url'], buf, basedir=src_dir )
        if fmt:
            imgdata = buf.getvalue()
            imgfile = 'cover.'+fmt
            geninfo['coverimage'] = (imgfile, fmt)
            # cover image
            epub.addData(imgdata, '', imgfile)
            # coverpage
            cvrpg_tmpl = open(os.path.join(template_dir, 'coverpage.xhtml'),'r').read().decode('utf-8')
            cvrpg = str( Template(cvrpg_tmpl, searchList=[ {'gen':geninfo} ]) )
            epub.saveData(cvrpg, '', 'coverpage.xhtml')
        else:
            print >> sys.stderr, "ERROR: can not copy cover image, %s" % book['cover_url']

    # title page
    titpg_tmpl = open(os.path.join(template_dir, 'titlepage.xhtml'),'r').read().decode('utf-8')
    titpg = str( Template(titpg_tmpl, searchList=[ {'book':book} ]) )
    epub.saveData(titpg, OPS_DIR, 'titlepage.xhtml')

    # images from chapters
    img_list = []
    imgcnt = 0
    for ch in book['chapter']:
        # extract images
        html = ch['html']
        for url in IMG_PTN.findall(html):
            imgcnt += 1
            buf = StringIO()
            fmt = copy_image( url, buf, basedir=src_dir, maxsize=IMG_SIZE)
            if fmt:
                imgdata = buf.getvalue()
                fname = "image%d.%s" % (imgcnt, fmt)
                epub.addData(imgdata, OPS_DIR+"/image", fname)
                html = html.replace(url, "image/"+fname)
                img_list.append( ("image/"+fname, fmt) )
            else:
                print >> sys.stderr, "ERROR: can not read %s" % url
        ch['html'] = html
    book['image'] = img_list

    # chapter files
    ch_tmpl = open(os.path.join(template_dir, 'chapter.xhtml'),'r').read().decode('utf-8')
    for ch in book['chapter']:
        html = str( Template(ch_tmpl, searchList=[ {'book':book, 'ch':ch} ]) )
        epub.saveData(html, OPS_DIR, ch['filename'])

    # CSS
    epub.addFile(os.path.join(template_dir,'generic.css'), OPS_DIR, 'generic.css')
    epub.addFile(target_css, OPS_DIR, 'target.css')
    if os.path.basename(target_css).startswith('Embed') and fontfile:
        extname = os.path.splitext(fontfile)[1]
        epub.addFile(os.path.join('fonts',fontfile), OPS_DIR, 'embedded'+extname)

    # OPF
    opf_tmpl = open(os.path.join(template_dir, 'content.opf'),'r').read().decode('utf-8')
    opf = str( Template(opf_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )
    epub.saveData(opf, '', 'content.opf')

    # NCX
    ncx_tmpl = open(os.path.join(template_dir, 'toc.ncx'),'r').read().decode('utf-8')
    print "ePUB toc level: %d" %geninfo['toclevel']
    ncx = str( Template(ncx_tmpl, searchList=[ {'book':book, 'gen':geninfo} ]) )
    epub.saveData(ncx, '', 'toc.ncx')

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
