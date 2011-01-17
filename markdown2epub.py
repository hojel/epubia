# -*- coding: utf-8 -*-
# markdown to ePUB
#    - calls epubgen
__program__ = "epub test"
__version__ = "0.0.0"

import markdown
import epubgen
import re

LangAbbr = { 'English':'en', 'Korean':'ko' }

def markdown2epub(text, epubfile, target_css='target/None.css',
        template_dir='./template', src_dir='.',
        fontfile='arial.ttf', rmUntit1st=True):
    md = markdown.Markdown(extensions=['meta', 'def_list', 'footnotes'])
    html = md.convert(text)
    # book info
    book = {'title':'', 'author':'', 'lang':'ko', 'chapter':[],
            'publisher':'', 'summary':'', 'subject':'', 'isbn':'', 'cover_url':''}
    for key,val in md.Meta.items():
        if key == 'language':
            key,val = ('lang', [ LangAbbr[ val[0] ] ])
        book[ key ] = ', '.join(val)
    cnt = 0
    # Chapter by Chapter
    ch_list = html.replace('<h1 />','<h1></h1>').split('<h1>')
    if ch_list[0].strip() == '':
        ch_list.pop(0)
    for ch in ch_list:
        cnt += 1
        pos = ch.find('</h1>')
        if pos < 0:
            title = None
            chtm = ch
        else:
            title = ch[:pos]
            chtm = ch[pos+5:]
        book['chapter'].append( {'name':title,'num':cnt,'html':chtm} )
    # Remove 1st chapter if it has no title
    if rmUntit1st and len(book['chapter']) > 1 and book['chapter'][0]['name'] is None:
        print "Remove 1st chapter with no title"
        book['chapter'].pop(0)
        cnt = 0
        for ch in book['chapter']:
            cnt += 1
            ch['num'] = cnt     # renumber
    epubgen.epubgen(book, epubfile, target_css=target_css, template_dir=template_dir, src_dir=src_dir,
                    fontfile=fontfile)
    
if __name__ == "__main__":
    text = unicode(open("../txt/sung1.txt",'r').read(),'utf-8')[1:]
    markdown2epub(text, "../txt/sung1.epub")
# vim:ts=4:sw=4:et
