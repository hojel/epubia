# -*- encoding: utf-8 -*-
# Formatted Text to Markdown
#
# Added markup
#    *          null paragraph
# Disabled markup
#    -          list item
# Changed markup
#    ---        horizontal line -> predefined paragraph separator
#    * * *      horizontal line -> predefined paragraph separator

import re

PTN_CHAP1 = re.compile(r'^\s*(\d+)\s*$',re.M)
PTN_CHAP2 = re.compile(ur'^\s*(제\s*\d+\s*장(?:\..*|\s*))$',re.M)
PTN_CHAP3 = re.compile(ur'^\s*(第\s*[一二三四五六七八九十]+\s*章)',re.M)
PTN_CHAP4 = re.compile(r'^\s*(chapter\s+\d+\.?|prologue|epilogue)\s*$',re.M|re.I)

def ftxt2markdown(txt, guessChapter=True, guessParaSep=False):
    # (1) guess chapter
    if guessChapter:
    	print "Guess Chapter"
    	txt = guess_header(txt)
        #txt = find_header_from_toc(txt)
    # (2) consider sequence of empty lines as empty paragraph
    if guessParaSep:
    	print "Guess Paragraph Separation"
        txt = re.compile('\n{6,}([^#\*\t\n!])').sub(r'\n\n*\n\n\g<1>', txt)
    txt2 = re.compile('\n{3,}').sub(r'\n\n', txt)
    # (3) filter unwanted markdown syntax
    txt2 = re.compile('^( {0,3})-([^-])',re.M|re.U).sub(r'\g<1>\\-\g<2>', txt2)
    return txt2

#--------------------------------------
PTN_MD_CH1 = re.compile(r'^#($|[^#])',re.M)
PTN_MD_CH2 = re.compile(r'\n\n([^\n]+)\n[ ]*={5,}[ \t]*\n')

def guess_header(txt):
    # chapter
    numch = 0
    numch += len(PTN_MD_CH1.findall(txt))
    numch += len(PTN_MD_CH2.findall(txt))
    if numch == 0:
        txt = PTN_CHAP1.sub(r'\n# \g<1>\n', txt)
        txt = PTN_CHAP2.sub(r'\n# \g<1>\n', txt)
        txt = PTN_CHAP3.sub(r'\n# \g<1>', txt)
        txt = PTN_CHAP4.sub(r'\n# \g<1>\n', txt)
    return txt

#--------------------------------------
# (EXPERIMENTAL)
def find_header_from_toc(text, toc_hdr=u"차례"):
    start = False
    inTOC = False
    cnt = 0
    for line in text.split('\n'):
    	if start:
            cname = re.compile('\d*\s*$').sub('',line).strip()
            if cname:
                inTOC = True
                #print (u"chapter: %s" % cname).encode('utf-8')
                text = re.compile('^%s$' % cname,re.M).sub('%s\n%s' % (cname,'='*2*len(cname)),text)
                cnt += 1
            elif inTOC:
                break
    	elif line.find(toc_hdr) >= 0:
            start = True
            inTOC = False
    print "%d chapters found" % cnt
    return text

#--------------------------------------
def extract_meta(text):
    lines = text.split('\n')
    info = {}
    meta_found = False
    for line in lines:
        if len(line.strip()) == 0:
            break   # empty line ends meta block
        pos = line.find(':')
        if pos >= 0:
            key = line[:pos].lower()
            if key[0] == ' ' or key[-1] == ' ':
                break
            val = line[pos+1:].strip() 
            info[key] = val
            meta_found = True
        elif meta_found and line.startswith(' '*4):
            info[key] += ', ' + line.strip()
        else:
            break
    return info

def insert_meta(text, meta):
    # remove existing meta block
    lines = text.split('\n')
    cnt = 0
    meta_found = False
    for line in lines:
        if len(line.strip()) == 0:
            break   # empty line ends meta block
        pos = line.find(':')
        if pos >= 0:
            meta_found = True
        elif meta_found and line.startswith(' '*4):
            pass    # continued block
        else:
            break
        cnt += 1
    # insert new meta block
    nwlns = []
    for key, val in meta.items():
        if key == 'isbn':
            key = key.upper()
        elif key.find('_') < 0:     # not cover_url
            key = key.title()
        nwlns.append( u"{0:15} {1}".format(key+':', val.replace('\n','')) )
    nwlns.append('')
    nwlns.extend( lines[cnt:] )
    return '\n'.join(nwlns)

#--------------------------------------
if __name__ == '__main__':
    import sys
    txt = open(sys.argv[1],'r').read().decode('euc-kr')
    rslt = ftxt2markdown(txt)
    open(sys.argv[2],'w').write( rslt.encode('utf-8') )
# vim:sw=4:ts=8:et
