# -*- encoding: utf-8 -*-
# Plain Text to Formatted Text
#
# Markdown
#    chapter (=========) 
#    section (---------)

import re
EMPTYLINE_PTN = re.compile(r'^\s*$',re.M|re.U)
PARAEND_PTN = re.compile(r'''([\.\?!'"=\)])$''',re.M|re.U)
INDENTSTART_PTN = re.compile(r'''^([ ]{2,}|\t)''',re.M|re.U)

# guessing chapter/section
CHAP_PTN1 = re.compile(r'\n\n([^\n]+)\n[ ]*={5,}\n')
CHAP_PTN2 = re.compile(ur'^\s*(제\s*\d+\s*장[ \.].{2,})$',re.M)
SECT_PTN1 = re.compile(r'\n\n([^\n]+)\n[ ]*-{5,}\n')
SECT_PTN2 = re.compile(r'^\s*([\dIVXivx]+\.?)\s*$',re.M)

class txt_cleaner:
    def __init__(self):
        self.ptn_sl_empty = re.compile(r'([^\n])\n\n([^\n])')
        self.ptn_sl_quote1 = re.compile(r"(\.\n)([ ]*'[^\n]*'\n)([ ]*[^'\n])")
        self.ptn_sl_quote2 = re.compile(r'(\.\n)([ ]*"[^\n]*"\n)([ ]*[^"\n])')
        self.ptn_quote_gap = re.compile(r'"\n\n([ ]*)"')
        self.cleaned = False

    def convert(self, txt, start=1):
        # preprocess
        txt = self.preprocess(txt, start)
        # paragraph
        txt = self.format_paragraph(txt)
        #if self.cleaned:
        #    txt = self.prettify_quote(txt)
        return txt

    def preprocess(self, txt, start=1):
        # line skip
        if start != 1:
            print "start from %d" % start
            txt = '\n'.join( txt.split('\n')[start-1:] )
        # remove spaces in line end
        txt = re.sub(r'[ \t\r]*\n', '\n', txt)
        # filter special character
        txt = txt.replace(u'”','"').replace(u'“','"')
        return txt

    def paragraph_analyze(self, txt):
        # extract patterns
        self.num_line = len( txt.split('\n') )
        self.num_emptyline = len( EMPTYLINE_PTN.findall(txt) )
        self.num_paraend = len( PARAEND_PTN.findall(txt) )
        self.num_indentline = len( INDENTSTART_PTN.findall(txt) )
        print "paragraph: %d %d %d %d" % (self.num_line, self.num_emptyline, self.num_paraend, self.num_indentline)

    def format_paragraph(self, txt):
        self.cleaned = False
        self.num_emptyline = len( EMPTYLINE_PTN.findall(txt) )
        self.num_paraend = len( PARAEND_PTN.findall(txt) )
        if self.num_emptyline > self.num_paraend:
            # Type-5: line separated with empty line
            print "detect all lines are separated by empty line"
            txt = self.ptn_sl_empty.sub(r'\g<1>\n\g<2>',txt)
            self.cleaned = True
        # merge multiple empty lines
        txt = re.sub(r'\n{2,}', r'\n\n', txt)
        # decide paragraph style
        self.paragraph_analyze(txt)
        if self.num_indentline > self.num_emptyline:
            # Type-2: paragraph by indentation
            print "detect paragraph indentation"
            txt = INDENTSTART_PTN.sub(r'\n\1',txt)
            self.cleaned = True
        elif self.num_emptyline < 0.4 * self.num_paraend:
            if self.num_paraend > 0.8 * self.num_line:
                # Type-3: paragraph in one line
                print "detect single line paragraph"
            else:
                # Type-4: not formatted
                print "detect not formatted paragraph"
            txt = PARAEND_PTN.sub(r'\1\n',txt)
            self.cleaned = True
        return txt

    def prettify_quote(self, txt):
        # wrap single quote block with empty lines
        #txt = self.ptn_sl_quote1.sub(r'\g<1>\n\g<2>\n\g<3>', txt)
        #txt = self.ptn_sl_quote2.sub(r'\g<1>\n\g<2>\n\g<3>', txt)
        # merge sequent single line quotes in one block
        txt = self.ptn_quote_gap.sub(r'"\n\1"', txt)
        return txt

def guess_format(txt):
    # chapter
    if len(CHAP_PTN1.findall(txt)) < 1:
        txt = CHAP_PTN2.sub(r'\n\1\n%s\n' % ('='*10), txt)
    # section
    if len(SECT_PTN1.findall(txt)) < 1:
        txt = SECT_PTN2.sub(r'\n\1\n%s\n' % ('-'*10), txt)
    return txt

def guess_coding(txt, filename=''):
    import codecs
    if txt[:3] == codecs.BOM_UTF8:
        return 'utf-8'
    if filename.find('.johab') > 0:
        return 'johab'
    return 'cp949'

#--------------------------------------
def load(fname):
    # load file
    try:
        text = open(fname,'r').read()
    except:
        import sys
        print >> sys.stderr, "fail to open"
        return None
    # guess text coding
    coding = guess_coding(text, fname)
    if coding == 'utf-8':
        text = unicode(text, coding)[1:]  # remove BOM
    else:
        text = unicode(text, coding, errors='replace')
    return text

def clean(text, start=1):
    # convert
    text = txt_cleaner().convert( text, start )
    return guess_format( text )

#--------------------------------------
def get_md_meta(text):
    lines = text.split('\n')
    info = {}
    meta_found = False
    for line in lines:
        if len(line.strip()) == 0:
            break   # empty line ends meta block
        pos = line.find(':')
        if pos >= 0:
            key = line[:pos].strip().lower()
            val = line[pos+1:].strip() 
            info[key] = val
            meta_found = True
        elif meta_found and line.startswith(' '*4):
            info[key] += ', ' + line.strip()
        else:
            break
    return info

def insert_md_meta(text, meta):
    # advance to first paragraph
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
    # insert meta
    nwlns = []
    nwlns.append(u"Language:  %s" % 'Korean')
    nwlns.append(u"Title:     %s" % meta['title'])
    nwlns.append(u"Author:    %s" % meta['author'])
    if 'publisher' in meta:
        nwlns.append(u"Publisher: %s" % meta['publisher'])
    if 'subject' in meta:
        nwlns.append(u"Subject:   %s" % meta['subject'])
    if 'isbn' in meta:
        nwlns.append(u"ISBN:      %s" % meta['isbn'])
    if 'description' in meta:
        nwlns.append(u"Summary:   %s" % meta['description'])
    if 'cover_url' in meta:
        nwlns.append(u"cover_url: %s" % meta['cover_url'])
    nwlns.append('')
    nwlns.extend( lines[cnt:] )
    return '\n'.join(nwlns)

#--------------------------------------
if __name__ == '__main__':
    import sys
    rslt = load(sys.argv[1])
    open(sys.argv[2],'w').write( rslt.encode('utf-8') )
# vim:sw=4:ts=8:et
