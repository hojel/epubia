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

ptn_h2tag = re.compile('<h2 id="(.*?)">')
ptn_h2tag0 = re.compile('<h2>')
ptn_h3tag = re.compile('<h3 id="(.*?)">')
ptn_sect  = re.compile('<h2 id="(.*?)">(.*?)</h2>')
ptn_fnref = re.compile('id="(fnref_.*?)"')

def markdown2epub(text, epubfile, target_css='target/None.css',
        template_dir='./template', src_dir='.',
        fontfile='arial.ttf', tocLevel=2, skipTo1st=False, splitLargeText=True):
    ext_list=['def_list', 'footnotes', 'tables', 'meta']
    if '[TOC]' in text:
        ext_list.append('toc')
    md = markdown.Markdown(
            extensions=ext_list,
            #extension_configs={'footnotes' : ('PLACE_MARKER','====footnote====')},
            safe_mode="escape",
            output_format="xhtml1"
    )
    html = md.convert(text)
    # post-process unofficial markup
    #  1) <p>*</p> --> <p class="blankpara">&#160;</p>
    #       - &nbsp; is not accepted in XHTML
    #  2) quotation mark
    #       - &ldquo;, &rdquo; are not accepted in XHTML
    html = html.replace('<p>*</p>', '<p class="blankpara">&#160;</p>')
    html = re.sub(u'“ ?', "&#8220;", html)
    html = html.replace(u'”',"&#8221;")
    html = re.sub(u"‘ ?", "&#8216;", html)
    html = html.replace(u"’","&#8217;")
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
        seccnt = 0
        sections = []
        pos = ch.find('</h1>')
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
            if True:
                chtm = chtm.replace('<pre><code>','<pre>').replace('</code></pre>','</pre>')
            chtm = ptn_h2tag.sub(r'<h2 id="sec\g<1>">', chtm)
            chtm = ptn_h2tag0.sub(match_add_h2_id, chtm)
            chtm = ptn_h3tag.sub(r'<h3 id="ssec\g<1>">', chtm)
            sections = [{'name':name, 'id':id} for id,name in ptn_sect.findall(chtm)]
        filename = 'chapter%d.xhtml' % chcnt
        if chid == 'chfootnote':
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
        for xfref in ptn_fnref.findall(chtm):
            print "register anchor {0:s}#{1:s}".format(filename, xfref)
            xfmap[xfref] = filename
    # Remove 1st chapter if it has no title
    if skipTo1st:
        remove_1st_chapter(book)
    # Split chapter if it exceeds 290 KB
    if splitLargeText:
        split_large_chapter(book)
    # Fix anchor
    for ch in book['chapter']:
        # in TOC chapter
        if '<div class="toc">' in ch['html']:
            ch['html'] = re.compile('"#(.*?)"').sub(fix_toc_anchor, ch['html'])
        # in Footnote chapter
        if ch['id'] == 'chfootnote':
            ch['html'] = re.compile('"#(fnref_.*?)"').sub(fix_fnref_anchor, ch['html'])
    # generate ePub
    epubgen.epubgen(book, epubfile, target_css=target_css, template_dir=template_dir, src_dir=src_dir,
                    fontfile=fontfile, toclevel=tocLevel)

def match_add_h2_id(match):
    global seccnt
    if match.group(0) not in [None, '']:
        ss = '<h2 id="_sec{0:d}">'.format(seccnt)
        seccnt += 1
        return ss

#--------------------------------------------------
def remove_1st_chapter(book):
    if len(book['chapter']) > 1 and book['chapter'][0]['name'] is None:
        print "Remove 1st chapter with no tag"
        global xcmap, xfmap
        book['chapter'].pop(0)
        chcnt = 0
        for ch in book['chapter']:
            chcnt += 1
            ch['num'] = chcnt     # renumber
            if ch['filename'].startswith('chapter'):
                ch['filename'] = 'chapter%d.xhtml' % chcnt
                xcmap[ch['id']] = ch['filename']
                for xfref in ptn_fnref.findall(ch['html']):
                    xfmap[xfref] = ch['filename']

def split_large_chapter(book):
    chcnt = 0
    ptn_fnref = re.compile('id="(fnref_.*?)"')
    newpos = 0
    for ch in book['chapter']:
        chcnt += 1
        newpos += 1
        # limit: xhtml < 300 KB
        html = ch['html']
        if len(html) > 110*1024:
            print "long chapter detected, "+ch['id']
            htmls = []
            pos_s = 0
            pos_e = 100*1024
            while True:
            	pos_e = html.find('<p>', pos_e)
            	htmls.append( html[pos_s : pos_e] )
            	if pos_e < 0:
            		break
            	pos_s = pos_e
            	pos_e = pos_s + 100*1024
            print "Split to %d files" %len(htmls)
            ch['html'] = htmls[0]
            if not ch['id']:
                ch['id'] = '__ch_%d' %chcnt
            idx = 0
            for html in htmls[1:]:
                idx += 1
                filename = 'split_ch%d_%d.html' %(ch['num'], idx)
                ch2 = {'name':None,
                       'id':ch['id']+'_%d' %idx,
                       'num':ch['num'],
                       'html':html,
                       'section':None,
                       'filename':filename}
                book['chapter'].insert(newpos, ch2)
                newpos += 1

if __name__ == "__main__":
    text = unicode(open("../txt/sung1.txt",'r').read(),'utf-8')[1:]
    markdown2epub(text, "../txt/sung1.epub")

    """
    # test split large file
    html = markdown.Markdown(safe_mode="escape", output_format="xhtml1").convert(text)
    book = {'chapter': [
                {'name':'Whole',
                 'id':'ch1',
                 'num':1,
                 'html':html,
                 'section':None,
                 'filename':'chapter1.xhtml'}]
    }
    print len(book['chapter'])
    split_large_chapter(book)
    print len(book['chapter'])
    """
# vim:ts=4:sw=4:et
