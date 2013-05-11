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

CHAP_PTN1 = re.compile(r'\n\n([^\n]+)\n[ ]*={5,}[ \t]*\n')
CHAP_PTN2 = re.compile(r'\n#[ \t]*')
CHAP_PTN3 = re.compile(ur'^\s*(제\s*\d+\s*장[ \.].{2,})$',re.M)
SECT_PTN1 = re.compile(r'\n##[ \t]*')
SECT_PTN2 = re.compile(r'^\s*([\dIVXivx]+\.?)\s*$',re.M)

def ftxt2markdown(txt):
    #txt = find_header_from_toc(txt)
    txt2 = guess_header(txt)
    return txt2

#--------------------------------------
def guess_header(txt):
    # chapter
    numch = 0
    numch += len(CHAP_PTN1.findall(txt))
    numch += len(CHAP_PTN2.findall(txt))
    if numch < 1:
        txt = CHAP_PTN3.sub(r'\n# \1\n\n', txt)
        # section
        numsec = 0
        numsec += len(SECT_PTN1.findall(txt))
        if numsec < 1:
            txt = SECT_PTN2.sub(r'\n## \1\n\n', txt)
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
