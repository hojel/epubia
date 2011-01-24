# -*- coding: utf-8 -*-
# markdown to ePUB
#    - calls epubgen
__program__ = "epub test"
__version__ = "0.0.0"

import markdown
import epubgen
import re

LangAbbr = { 'English':'en', 'Korean':'ko' }

seccnt = 0
def insert_section_id(obj):
    global seccnt
    seccnt += 1
    return '<h2 id="idsec%03d">' % seccnt

def markdown2epub(text, epubfile, target_css='target/None.css',
        template_dir='./template', src_dir='.',
        fontfile='arial.ttf', skipTo1st=False):
    md = markdown.Markdown(extensions=['meta', 'def_list', 'footnotes'])
    html = md.convert(text)
    # book info
    book = {'title':'', 'author':'', 'lang':'ko', 'chapter':[],
            'publisher':'', 'summary':'', 'subject':'', 'isbn':'', 'cover_url':''}
    for key,val in md.Meta.items():
        if key == 'language':
            key,val = ('lang', [ LangAbbr[ val[0] ] ])
        book[ key ] = ', '.join(val)
    # Chapter by Chapter
    ch_list = html.replace('<h1 />','<h1></h1>').split('<h1>')
    if ch_list[0].strip() == '':
        ch_list.pop(0)
    chcnt = 0
    for ch in ch_list:
        chcnt += 1
        pos = ch.find('</h1>')
        sections = []
        if pos < 0:
            title = None
            chtm = ch
        else:
            title = ch[:pos]
            chtm = ch[pos+5:]
            #chtm = chtm.replace('<code>','<blockquote>').replace('</code>','</blockquote>')
            # extract section and attach id to each of them
            global seccnt
            seccnt = 0
            chtm = re.compile("<h2>").sub(insert_section_id, chtm)
            sections = [{'name':name, 'id':id} for id,name in re.compile('<h2 id="(.*?)">(.*?)</h2>').findall(chtm)]
        book['chapter'].append( {'name':title,'num':chcnt,'html':chtm,'section':sections} )
    # Remove 1st chapter if it has no title
    if skipTo1st and len(book['chapter']) > 1 and book['chapter'][0]['name'] is None:
        print "Remove 1st chapter with no tag"
        book['chapter'].pop(0)
        chcnt = 0
        for ch in book['chapter']:
            chcnt += 1
            ch['num'] = chcnt     # renumber
    epubgen.epubgen(book, epubfile, target_css=target_css, template_dir=template_dir, src_dir=src_dir,
                    fontfile=fontfile)
    
if __name__ == "__main__":
    text = unicode(open("../txt/sung1.txt",'r').read(),'utf-8')[1:]
    markdown2epub(text, "../txt/sung1.epub")
# vim:ts=4:sw=4:et
