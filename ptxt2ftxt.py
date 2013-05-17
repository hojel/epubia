# -*- encoding: utf-8 -*-
# Plain Text to Formatted Text
#   1) guess text format type
#   2) formatting based on the given type

import re

QOpenChr  = u'''“‘『「<'"'''
QCloseChr = u'''”’』」>'"'''
SEndChr   = u'\.!\?,'

EMPTYLINE_PTN = re.compile(r'^\s*$',re.M|re.U)
PARAEND_PTN = re.compile(r'''([%s%s])\s*$''' %(SEndChr,QCloseChr),re.M|re.U)
INDENTSTART_PTN = re.compile(r'''^([ ]{1,3})''',re.M|re.U)      # preserve Markdown block (4 spaces or tab)

#------------------------------------------------------
def ptxt2ftxt(txt, startline=1, pretty_quote=False):
    # preprocess
    txt = preprocess(txt, startline)
    # decide paragraph style
    pfmt = analyze_paragraph(txt)
    print "guessed format: %d" %pfmt
    # paragraph
    txt2 = format_paragraph(txt, pfmt)
    # preprocess
    txt3 = postprocess(txt2, pretty_quote)
    return txt3

def ftxtclean(txt, pretty_quote=True, correct_word_break=None):
    txt2 = correct_keyword(txt)
    if pretty_quote:
        txt2 = change_quotechar(txt2)
    if correct_word_break is not None:
    	if correct_word_break == "naver_autospacing":
            print "INFO: correct word break with Naver Autospacing"
            txt2 = correct_word_by_naver(txt2)
        else:
            txt2 = correct_word_by_pattern(txt2)
    return txt2

#------------------------------------------------------
def preprocess(txt, startline=1):
    # line skip
    if startline != 1:
        print "start from %d" % startline
        txt = '\n'.join( txt.split('\n')[startline-1:] )
    # remove spaces in line end
    # --> space in tail can be used as line break directive
    #txt = re.compile(r'[ \r]*$',re.M).sub('', txt)
    # clean empty line
    txt = re.compile(r'^\s*$',re.M|re.U).sub('', txt)
    # filter special character
    #txt = txt.replace(u'“ ','"').replace(u'”','"')
    #txt = txt.replace(u"‘ ","'").replace(u"’","'")
    return txt

def analyze_paragraph(txt):
    # extract patterns
    num_line = len( txt.split('\n') )
    num_emptyline = len( EMPTYLINE_PTN.findall(txt) )
    num_paraend = len( PARAEND_PTN.findall(txt) )
    num_indentline = len( INDENTSTART_PTN.findall(txt) )
    print "paragraph: %d %d %d %d" % (num_line, num_emptyline, num_paraend, num_indentline)
    # guess format
    if num_emptyline > 0.45*num_line and num_paraend < 0.8*num_emptyline:
        # line separated with empty line
        print "detect all lines are separated by empty line"
        num_removed = num_line/2
        num_line -= num_removed
        num_emptyline -= num_removed
        num_paraend -= num_removed
    if num_indentline > num_emptyline:
        # Type-2: paragraph by indent
        pfmt_type = 2;
    elif num_emptyline < 0.3 * num_paraend:
        if num_paraend > 0.8 * num_line:
            # Type-3: paragraph in one line
            print "detect single line paragraph"
            pfmt_type = 3;
        else:
            # Type-4: not formatted
            print "detect non formatted paragraph"
            pfmt_type = 4;
    else:
        pfmt_type = 1;
    return pfmt_type

# formatting all paragraph to type-1 format
def format_paragraph(txt, pfmt_type=1):
    if pfmt_type == 2:
        txt = INDENTSTART_PTN.sub(r'\n',txt)
    elif pfmt_type == 3 or pfmt_type == 4:
        txt = PARAEND_PTN.sub(r'\1\n',txt)
    return txt

def postprocess(txt, pretty_quote):
    # insert line before quote start
    txt2 = re.compile(r"([%s%s])\s*\n([%s])" %(SEndChr, QCloseChr, QOpenChr)).sub(r"\1\n\n\2", txt)
    # insert line after quote ends
    txt2 = re.compile(r"([%s])\s*\n(\S)" %QCloseChr).sub(r"\1\n\n\2", txt2)
    return txt2

#----------------------------------------------------------
def change_quotechar(txt):
    txt = re.compile('^(.[^"]*)"$', re.M).sub(ur"\1”", txt)
    txt = re.compile('^"([^"]*\S)$', re.M).sub(ur"“\1", txt)
    txt = re.compile("^(.[^']*)'$", re.M).sub(ur"\1’", txt)
    txt = re.compile("^'([^']*\S)$", re.M).sub(ur"‘\1", txt)
    return txt

def correct_word_by_pattern(txt):
    txt = re.compile('(\w)\n([다자까아][\.\?!])',re.U).sub(r'\1\2\n',txt)
    txt = re.compile('(\w)\n([이가을를은는도]) ',re.U).sub(r'\1\2\n',txt)
    return txt

# using Naver auto-spacing site
def correct_word_by_naver(txt):
    # separate a line to two lines
    ll1 = []
    for l in txt.split('\n'):
    	ll1.append(l)
    	ll1.append('')
    txt1 = '\n'.join(ll1)
    txt2 = re.compile(r'(\S+)\n\n(\S+) *\n{0,2}').sub(r'\n\1 \2\n', txt1)
    ll2 = txt2.split('\n')
    if len(ll2) % 2:
    	txt2 += '\n'
    	ll2.append('')
    # access external site
    from naver_autospacing import naver_autospacing
    try:
        txt3 = naver_autospacing(txt2)
    except:
        print "ERROR: fail to access Naver Autospacing site"
        return txt
    # merge
    ll3 = txt3.split('\n')
    for i in range(len(ll2)-len(ll3)):
        ll3.append('')
    ll4 = [(ll2[i]+ll3[i+1]).rstrip() for i in range(0, len(ll2), 2)]
    return '\n'.join(ll4)

def correct_keyword(txt):
    # Disable some markdown markers for better output
    #    1) horizontal line drawing by '* * *'
    #    2) list starting with '-' 
    #         use alternative way starting with '*' 
    txt = re.compile('(\* *\* *\*)',re.M|re.U).sub(r'\t\g<1>', txt)
    txt = re.compile('^( *)-([^-])',re.M|re.U).sub(r'\g<1>\\-\g<2>', txt)
    #txt = re.compile('^ *--- *$',re.M).sub(r'- - -', txt)
    return txt

#--------------------------------------
if __name__ == '__main__':
    import sys
    txt = open(sys.argv[1],'r').read().decode('euc-kr')
    txt2 = ptxt2ftxt(txt, pretty_quote=True)
    txt3 = ftxtclean(txt2, pretty_quote=True)
    open(sys.argv[2],'w').write( txt3.encode('utf-8') )
# vim:sw=4:ts=8:et
