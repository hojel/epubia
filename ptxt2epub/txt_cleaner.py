# -*- encoding: utf-8 -*-
# Plain Text to Formatted Text
#

import re
EMPTYLINE_PTN = re.compile(r'^\s*$',re.M|re.U)
PARAEND_PTN = re.compile(r'''([\.\?!'"=])$''',re.M|re.U)
INDENTSTART_PTN = re.compile(r'''^([[ ]{2,}\t])''',re.M|re.U)

# guessing chapter/section
CHAP_PTN1 = re.compile(ur'^\s*(제\s*\d+\s*장[ \.].{2,})$',re.M)
SECT_PTN1 = re.compile(r'^\s*([\dIVXivx]+\.?)\s*$',re.M)

class txt_cleaner:
    def __init__(self):
        self.filename = None
        self.ptn_sl_empty = re.compile(r'([^\n])\n\n([^\n])')
        self.ptn_sl_quote1 = re.compile(r"(\.\n)([ ]*'[^\n]*'\n)([ ]*[^'\n])")
        self.ptn_sl_quote2 = re.compile(r'(\.\n)([ ]*"[^\n]*"\n)([ ]*[^"\n])')
        self.ptn_quote_gap = re.compile(r'"\n\n([ ]*)"')

    def load(self, fname, start=1):
        self.filename = fname
        # load file
        try:
            txt = open(fname,'r').read()
        except:
            import sys
            print >> sys.stderr, "fail to open"
            return None
        # guess text coding
        coding = self.txt_coding(txt)
        if coding == 'utf-8':
            txt = unicode(txt[3:], coding)  # remove BOM
        else:
            txt = unicode(txt, coding, errors='replace')
        # convert
        return self.convert( txt, start=start )

    def convert(self, txt, start=1):
        # preprocess
        txt = self.preprocess(txt, start)
        # paragraph
        txt = self.clean_paragraph(txt)
        txt = self.beautify_quote(txt)
        # guess formatting
        txt = self.guess_format(txt)
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

    def clean_paragraph(self, txt):
        self.num_emptyline = len( EMPTYLINE_PTN.findall(txt) )
        self.num_paraend = len( PARAEND_PTN.findall(txt) )
        if self.num_emptyline > self.num_paraend:
            # Type-5: line separated with empty line
            print "detect all lines are separated by empty line"
            txt = self.ptn_sl_empty.sub(r'\g<1>\n\g<2>',txt)
        # merge multiple empty lines
        txt = re.sub(r'\n{2,}', r'\n\n', txt)
        # decide paragraph style
        self.paragraph_analyze(txt)
        if self.num_indentline > self.num_emptyline:
            # Type-2: paragraph by indentation
            print "detect paragraph indentation"
            txt = INDENTSTART_PTN.sub(r'\n\1',txt)
        elif self.num_emptyline < 0.4 * self.num_paraend:
            if self.num_paraend > 0.8 * self.num_line:
                # Type-3: paragraph in one line
                print "detect single line paragraph"
            else:
                # Type-4: not formatted
                print "detect not formatted paragraph"
            txt = PARAEND_PTN.sub(r'\1\n',txt)
        return txt

    def beautify_quote(self, txt):
        # wrap single quote block with empty lines
        #txt = self.ptn_sl_quote1.sub(r'\g<1>\n\g<2>\n\g<3>', txt)
        #txt = self.ptn_sl_quote2.sub(r'\g<1>\n\g<2>\n\g<3>', txt)
        # merge sequent single line quotes in one block
        txt = self.ptn_quote_gap.sub(r'"\n\1"', txt)
        return txt

    def guess_format(self, txt):
        # chapter
        if len(re.compile('^\s*=[^=].*=$',re.M).findall(txt)) < 1:
            txt = CHAP_PTN1.sub(r'= \1 =', txt)
        # section
        if len(re.compile('^\s*==[^=].*==$',re.M).findall(txt)) < 1:
            txt = SECT_PTN1.sub(r'== \1 ==', txt)
        return txt

    def txt_coding(self, txt):
        import codecs
        if txt[:3] == codecs.BOM_UTF8:
            return 'utf-8'
        if self.filename.find('johab.') > 0:
            return 'johab'
        return 'cp949'

if __name__ == '__main__':
    import sys
    rslt = txt_cleaner().load(sys.argv[1])
    import codecs
    codecs.open(sys.argv[2],'w').write( rslt.encode('utf-8') )
# vim:sw=4:ts=8:et
