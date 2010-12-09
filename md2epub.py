# -*- coding: utf-8 -*-
# markdown to ePUB
#    - calls epubgen
__program__ = "epub test"
__version__ = "0.0.0"

import markdown
import epubgen
import re

LangAbbr = { 'English':'en', 'Korean':'ko' }

def md2epub(text, epubfile, target_css='target/None.css', template_dir='./template', src_dir='.'):
    md = markdown.Markdown(extensions=['meta','footnotes'])
    html = md.convert(text)
    # book info
    book = {'title':'', 'author':'', 'lang':'ko', 'chapter':[],
            'publisher':'', 'summary':'', 'subject':'', 'isbn':'', 'cover_url':''}
    for key,val in md.Meta.items():
        if key == 'language':
            key = 'lang'
            val = [ LangAbbr[ val[0] ] ]
        book[ key ] = ', '.join(val)
    cnt = 0
    # Chapter by Chapter
    ch_list = html.split('<h1>')
    if len(ch_list) > 1:
        ch_list.pop(0)
    for ch in ch_list:
        cnt += 1
        pos = ch.find('</h1>')
        if pos < 0:
            title = ''
            chtm = ch
        else:
            title = ch[:pos]
            chtm = ch[pos+5:]
        book['chapter'].append( {'name':title,'num':cnt,'html':chtm} )
    epubgen.epubgen(book, epubfile, target_css=target_css, template_dir=template_dir, src_dir=src_dir)
    
if __name__ == "__main__":
    text = unicode(open("../txt/sung1.txt",'r').read(),'utf-8')[1:]
    md2epub(text, "../txt/sung1.epub")
# vim:ts=4:sw=4:et
