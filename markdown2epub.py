# -*- coding: utf-8 -*-
# markdown to ePUB
#    - calls epubgen
__program__ = "epub test"
__version__ = "0.0.0"

import markdown
import epubgen
import re

LangAbbr = { 'English':'en', 'Korean':'ko' }

xcmap = {}      # TOC reverse map
xcfilename = ''
def fix_toc_anchor(match):
    global xcfilename
    if match.group(1) and match.group(1) is not '':
        global xcmap
        chid = 'ch'+match.group(1)
        if chid in xcmap:
            xcfilename = xcmap[chid]
            return '"{0:s}"'.format(xcfilename)
        else:
            # section (using previous set xcfilename)
            return '"{0:s}#sec{1:s}"'.format(xcfilename, id)
    xcfilename = ''
    return '""'

xfmap = {}      # footnote reverse map
def fix_fnref_anchor(match):
    global xfmap
    return '"{0:s}#{1:s}"'.format(xfmap[match.group(1)], match.group(1))
    
def markdown2epub(text, epubfile, target_css='target/None.css',
        template_dir='./template', src_dir='.',
        fontfile='arial.ttf', tocLevel=2, skipTo1st=False):
    md = markdown.Markdown(
            extensions=['def_list', 'footnotes', 'tables', 'toc', 'meta'],
            #extension_configs={'footnotes' : ('PLACE_MARKER','====footnote====')},
            safe_mode="escape",
            output_format="xhtml1"
    )
    html = md.convert(text)
    # post-process unofficial markup
    #  1) <p>- - -</p> --> <p class="blankpara">&#160;</p>
    #  2) quotation mark
    html = html.replace('<p>- - -</p>', '<p class="blankpara">&#160;</p>')
    html = html.replace(u'“ ',"&#8220;").replace(u'”',"&#8221;")
    html = html.replace(u"‘ ","&#8216;").replace(u"’","&#8217;")
    # book info
    book = {'title':'', 'author':'', 'lang':'ko', 'chapter':[],
            'publisher':'', 'publishdate':'', 'summary':'', 'subject':'', 'isbn':'', 'cover_url':''}
    for key,val in md.Meta.items():
        if key == 'language':
            key,val = ('lang', [ LangAbbr[ val[0] ] ])
        book[ key ] = ', '.join(val)
    # Chapter by Chapter
    html = html.replace('<h1 />','<h1></h1>')
    html = html.replace('<h1>','<h1 id="">')
    html = html.replace('<div class="footnote">',u'<h1 id="footnote">주석</h1><div class="footnote">')
    html = html.replace('fn:','fn_').replace('fnref:','fnref_')
    html = html.replace('#fn_','footnote.xhtml#fn_')
    ch_list = html.split('<h1')
    if ch_list[0].strip() == '':
        ch_list.pop(0)
    chcnt = 0
    global xcmap, xfmap
    xcmap = {}
    xfmap = {}
    for ch in ch_list:
        chcnt += 1
        pos = ch.find('</h1>')
        sections = []
        if pos < 0:
            title = None
            chtm = ch
            chid = ''
        else:
            assert ch.startswith(' id="')
            title = ch[ch.find('>')+1:pos]
            chtm = ch[pos+5:]
            chid = ch[5:ch.find('"',5)]     # must start as ' id="'
            if chid == '':
                chid = "_%d" % chcnt
            else:
                chid = 'ch'+chid
            #chtm = chtm.replace('<code>','<blockquote>').replace('</code>','</blockquote>')
            chtm = re.compile('<h2 id="(.*?)">').sub(r'<h2 id="sec\g<1>">', chtm)
            chtm = re.compile('<h3 id="(.*?)">').sub(r'<h3 id="ssec\g<1>">', chtm)
            sections = [{'name':name, 'id':id} for id,name in re.compile('<h2 id="(.*?)">(.*?)</h2>').findall(chtm)]
        filename = 'chapter%d.xhtml' % chcnt
        if chid == 'footnote':
            filename = 'footnote.xhtml'
        book['chapter'].append( {'name':title,
                                 'id':chid,
                                 'num':chcnt,
                                 'html':chtm,
                                 'section':sections,
                                 'filename':filename} )
        print u"{0:d}({1:s}) {2:s}".format(chcnt,chid,title)
        # register in xref map
        xcmap[chid] = filename
        for xfref in re.compile('id="(fnref_.*?)"').findall(chtm):
            xfmap[xfref] = filename
    # Remove 1st chapter if it has no title
    if skipTo1st and len(book['chapter']) > 1 and book['chapter'][0]['name'] is None:
        print "Remove 1st chapter with no tag"
        book['chapter'].pop(0)
        chcnt = 0
        for ch in book['chapter']:
            chcnt += 1
            ch['num'] = chcnt     # renumber
            if ch['filename'].startswith('chapter'):
                ch['filename'] = 'chapter%d.xhtml' % chcnt
            xcmap[ch['id']] = filename
            for xfref in re.compile('id="(fnref_.*?)"').findall(ch['html']):
                xfmap[xfref] = filename
    # Fix anchor
    for ch in book['chapter']:
        # in TOC chapter
        if ch['html'].find('<div class="toc">') >= 0:
            ch['html'] = re.compile('"#(.*?)"').sub(fix_toc_anchor, ch['html'])
        # in Footnote chapter
        if ch['id'] == 'footnote':
            ch['html'] = re.compile('"#(fnref_.*?)"').sub(fix_fnref_anchor, ch['html'])
    # generate ePub
    epubgen.epubgen(book, epubfile, target_css=target_css, template_dir=template_dir, src_dir=src_dir,
                    fontfile=fontfile, toclevel=tocLevel)

if __name__ == "__main__":
    text = unicode(open("../txt/sung1.txt",'r').read(),'utf-8')[1:]
    markdown2epub(text, "../txt/sung1.epub")
# vim:ts=4:sw=4:et
