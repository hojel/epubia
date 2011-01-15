# -*- coding: utf-8 -*-
import markdown
import ho.pisa as pisa
import StringIO
import os
import re
from Cheetah.Template import Template

debug = False

def markdown2pdf(text, pdffile, cssfile='xhtml2pdf.css', src_dir='.',
        fontfile='arial.ttf', rmUntit1st=True):
    global debug
    md = markdown.Markdown(extensions=['meta','footnotes'])
    html = md.convert(text)
    if debug:
        open('test.html','w').write(html.encode('utf-8'))
    htmline = []
    #-- Cover & Title Page
    cover_file = None
    title = None
    author = None

    import tempfile
    tempcover = None
    if 'cover_url' in md.Meta:
        import urllib
        cover_url = md.Meta['cover_url'][0]
        if cover_url.startswith('http://'):
            extname = cover_url[ cover_url.rfind('.'): ]
            fd,tempcover = tempfile.mkstemp(suffix=extname)
            os.write(fd, urllib.urlopen(cover_url).read())
            os.close(fd)
            cover_file = tempcover
        else:
            cover_file = cover_url
            if cover_url.startswith('file://'):
                cover_file = cover_url[7:]
    if 'title' in md.Meta:
        title = md.Meta['title'][0].replace(', ','<br />')
    if 'author' in md.Meta:
        author = md.Meta['author'][0].replace(', ','<br />')
    cover_tmpl = open(os.path.join('template','pdf_coverpage.html'), 'r').read()
    coverpg_htm = str( Template(cover_tmpl, searchList=[ {'cover_url':cover_file,'title':title,'author':author} ]) )
    htmline.append( unicode(coverpg_htm,'utf-8') )
    #-- Body
    # correct image path
    for url in re.compile('<img [^>]*src="(.*?)"').findall(html):
        if url.startswith('http://') or os.path.isabs(url):
            pass
        else:
            html = html.replace(url, os.path.normpath(src_dir+'/'+url))
    if rmUntit1st:
        html = html[ html.find('<h1'): ]
    html = html.replace('<h1 />','<h1></h1>')
    htmline.append(html)
    #-- PDF generation
    css_tmpl = open(os.path.join('template',cssfile), 'r').read()
    target_css = str( Template(css_tmpl, searchList=[ {'font':'fonts/'+fontfile} ]) )
    fp = file(pdffile,'wb')
    pdf = pisa.pisaDocument(
                StringIO.StringIO('\n'.join(htmline).encode('utf-8')),
                fp,
                #path=src_dir,  # not working!
                #link_callback=fetch_resources,
                default_css=target_css,
                #xhtml=True,
                encoding='utf-8')
    fp.close()
    if tempcover and os.path.exists(tempcover):
        os.remove(tempcover)
    #if debug and not pdf.err:
    #	pisa.startViewer(pdffile)

if __name__ == "__main__":
    debug = True
    import os, sys
    outfile = os.path.splitext(sys.argv[1])[0] + ".pdf"
    text = unicode(open(sys.argv[1],'r'),'utf-8')[1:]
    markdown2pdf(text, outfile, fontfile='SeoulHangang.ttf')
# vim:sw=4:ts=4:et
