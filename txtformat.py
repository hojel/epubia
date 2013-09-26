# -*- encoding: utf-8 -*-
# Plain Text to Formatted Text

import codecs

def guess_coding(txt, filename=''):
    if filename.find('.utf8') > 0:
        return 'utf-8'
    if filename.find('.cp949') > 0:
        return 'cp949'
    if filename.find('.euckr') > 0:
        return 'euc-kr'
    if filename.find('.johab') > 0:
        return 'johab'
    if txt[:3] == codecs.BOM_UTF8:
        return 'utf-8'
    import chardet
    detsz = min(10000, len(txt))
    coding = chardet.detect(txt[:detsz])['encoding']
    print "coding %s is detected" % coding
    if coding is None or coding == 'EUC-KR':
        coding = 'cp949'
    return coding

def load(fname):
    # load file
    try:
        text = open(fname,'r').read()
    except:
        import sys
        print >> sys.stderr, "fail to open"
        return None
    # convert to unicode
    coding = guess_coding(text, filename=fname)
    text = unicode(text, coding, errors='replace')
    if ord(text[0]) == 0xfeff:  # utf-8 BOM
        return text[1:]
    return text

def clean(txt, startline=1, pretty_quote=True, correct_word_break=None, guess_chapter=True, guess_parasep=False):
    from ptxt2ftxt import ptxt2ftxt, ftxtclean
    from ftxt2markdown import ftxt2markdown
    txt = ptxt2ftxt(txt, startline)
    txt = ftxtclean(txt, pretty_quote, correct_word_break)
    txt = ftxt2markdown(txt, guess_chapter, guess_parasep)
    return txt

#--------------------------------------
if __name__ == '__main__':
    import sys
    txt = load(sys.argv[1])
    rslt = clean(txt)
    open(sys.argv[2],'w').write( rslt.encode('utf-8') )
# vim:sw=4:ts=8:et
