# -*- coding: utf-8 -*-
import markdown
import ho.pisa as pisa
import StringIO
import os
import re

debug = False

def md2pdf(text, pdffile, cssfile='xhtml2pdf-hangul.css', src_dir='.'):
    global debug
    md = markdown.Markdown(extensions=['meta','footnotes'])
    html = md.convert(text)
    if debug:
        open('test.html','w').write(html.encode('utf-8'))
    htmline = []
    # Cover Page
    tempcover = './cover.jpg'
    if 'cover_url' in md.Meta:
        import urllib
        url = md.Meta['cover_url'][0]
        open(tempcover,'wb').write( urllib.urlopen(url).read() )
        htmline.append("""\
  <div style="text-align: center; vertical-align: middle; page-break-after: always;">
    <img class="bookcover" alt="Cover" src="%s" />
  </div>
""" % tempcover)
    # Title Page
    if 'title' in md.Meta:
        title = md.Meta['title'][0].replace(', ','<br />')
        author = ''
        if 'author' in md.Meta:
            author = md.Meta['author'][0].replace(', ','<br />')
        htmline.append("""\
  <div style="text-align: center; vertical-align: middle; page-break-after: always;">
    <div class="booktitle">%s</div>
    <div class="bookauthor">%s</div>
  </div>
""" % (title, author) )
    # correct image path
    for url in re.compile('<img [^>]*src="(.*?)"').findall(html):
        if url.startswith('http://') or os.path.isabs(url):
            pass
        else:
            html = html.replace(url, os.path.normpath(src_dir+'/'+url))
    htmline.append(html)
    # PDF generation
    target_css = open(cssfile, 'r').read()
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
    #if os.path.exists(tempcover):
    #    os.remove(tempcover)
    #if debug and not pdf.err:
    #	pisa.startViewer(pdffile)

if __name__ == "__main__":
    debug = True
    import os, sys
    outfile = os.path.splitext(sys.argv[1])[0] + ".pdf"
    text = unicode(open(sys.argv[1],'r'),'utf-8')[1:]
    md2pdf(text, outfile)
# vim:sw=4:ts=4:et
