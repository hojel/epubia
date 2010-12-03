# -*- encoding: utf-8 -*-
# Write Text/HTML from Object
#
# Object:
#  {'book':
#    {'title',''}
#    {'chapter':
#      {'title',''}
#      {'section':
#        {'title',''}
#        {'paragraph',''}[]
#      }[]
#    }[]
#  }

import cgi

class text_writer:
    def __init__(self, book):
        self.book = book

    def one_file(self):
        lines = []
        lines.append( u"#title: %s" % self.book.title )
        lines.append( u"#author: %s" % self.book.author )
        for ch in self.per_chapter():
            lines.append( u"= %s =" % ch['name'] )
            lines.append( u"%s" % ch['text'] )
        return '\n'.join(lines).encode('utf-8')

    def per_chapter(self):
        chlist = []
        num = 0
        for ch in self.book.chapter:
            num += 1
            p = {'name':ch.title, 'num':num}
            lines = []
            for sec in ch.section:
                if sec.title:
                    lines.append( u"%s" % sec.title )
                    lines.append( u"----------" )
                for para in sec.paragraph:
                    lines.append( '\n'.join(para.text) )
            p['text'] = '\n\n'.join(lines)
            chlist.append(p)
        return chlist

class html_writer:
    def __init__(self, book):
        self.book = book

    def one_file(self):
        lines = []
        lines.append( u"<html>\n<head>" )
        lines.append( u"  <title>%s</title>" % cgi.escape(self.book.title) )
        lines.append( u'  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>' )
        lines.append( u"</head>\n<body>" )
        for ch in self.per_chapter():
            lines.append( u"  <h2>%s</h2>" % cgi.escape(ch['name']) )
            lines.append( u"%s" % ch['html'] )
            lines.append( "" )
        lines.append( u"</body>\n</html>" )
        return '\n'.join(lines).encode('utf-8')

    def per_chapter(self):
        chlist = []
        num = 0
        for ch in self.book.chapter:
            num += 1
            p = {'name':ch.title, 'num':num}
            lines = []
            for sec in ch.section:
                if sec.title:
                    lines.append( u"  <h3>%s</h3>" % cgi.escape(sec.title) )
                for para in sec.paragraph:
                    ll = '  <p>'
                    for txt in para.text:
                        ll += cgi.escape(txt)
                        if txt[0] == '"' and txt[-1] == '"':
                            ll += '<br/>\n'
                    ll += '</p>'
                    lines.append( ll.replace('<br/>\n</p>','</p>') )
            p['html'] = '\n'.join(lines)
            chlist.append(p)
        return chlist

if __name__ == '__main__':
    import sys
    import codecs
    from txt_parser import txt_parser
    text = codecs.open(sys.argv[1],'r','utf-8').read()[1:]
    #-------------------
    dom = txt_parser().parse(text)
    out = html_writer().one_file(dom)
    open(sys.argv[2],'w').write( out.encode('utf-8') )
# vim: sw=4 ts=8 expandtab
