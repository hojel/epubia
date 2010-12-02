# -*- encoding: utf-8 -*-
# Parsing Formatted Text
#
#     [Supported Markup]
#     = Chapter =              ->  <h2>Chapter</h2>
#     == Section ==            ->  <h3>Section</h3>
#     ------                   ->  <hr/>
#     #                        ->  comment
#     #title:                  ->  book title
#     #author:                 ->  author
#     #isbn:                   ->  ISBN code
#
#     [TO DO]
#     {{{
#        something             ->  <div class="blockquote"></div>
#     }}}
#
#     _italic_                 ->  <em></em>
#     *bold*                   ->  <strong></strong>
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

import re
CHAPTER_PTN = re.compile('=([^=].*)=')
SECTION_PTN = re.compile('==([^=].*)==')
DIRECTIVE_PTN = re.compile('^#(title|author|isbn):(.*)')

class _book:
    def __init__(self, title=None, author=None, isbn=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.lang = 'ko'
        self.subject = []
        self.pubdate = None
        self.publisher = None
        self.description = None
        self.chapter = []
class _chapter:
    def __init__(self, id='0', title=None, anchor=None):
        self.id = id
        self.title = title
        self.anchor = anchor
        self.section = []
class _section:
    def __init__(self):
        self.title = None
        self.paragraph = []
class _paragraph:
    def __init__(self):
        self.indented = False
        self.text = []

class txt_parser:
    def __init__(self):
        self.book = _book()
        self.rm_1st_nontitled_ch = True

    def parse(self, txt):
        self.chap = _chapter()
        self.sec = _section()
        self.para = _paragraph()
        for line in self.preprocess(txt).split('\n'):
            cline = line.strip()
            # comment
            if line.startswith('#'):
                query = DIRECTIVE_PTN.match(line)
                if query:
                    keyword = query.group(1)
                    value = query.group(2).strip()
                    if keyword == 'title':
                        self.title = value
                    elif keyword == 'author':
                        self.author = value
                    elif keyword == 'isbn':
                        self.isbn = value
                continue
            # chapter
            query = CHAPTER_PTN.match(cline)
            if query:
                self.close_chapter()
                self.chap.title = query.group(1).strip()
                continue
            # section
            query = SECTION_PTN.match(cline)
            if query:
                self.close_section()
                self.sec.title = query.group(1).strip()
                continue
            # paragraph end with empty line
            if len(cline) == 0:
                self.close_paragraph()
            elif line.startswith('{{{'):
                # indented paragraph
                if not self.para.indented:
                    self.close_paragraph()
                    self.para.indented = True
                self.para.text.append(cline)
            elif line.startswith('}}}'):
                self.close_paragraph()
                self.para.indented = False
            else:
                self.para.text.append(cline)
        self.close_chapter()
        self.postprocess()
        return self.book

    def preprocess(self,txt):
        return txt

    def postprocess(self):
        if self.rm_1st_nontitled_ch:
            if self.book.chapter[0].title is None and len(self.book.chapter) > 2:
                self.book.chapter.pop(0)

    def close_paragraph(self):
        if len(self.para.text) > 0:
            if self.sec.title is None:
                self.sec.title = ''
            self.sec.paragraph.append( self.para )
            self.para = _paragraph()

    def close_section(self):
        self.close_paragraph()
        if len(self.sec.paragraph) > 0:
            self.chap.section.append( self.sec )
            self.sec = _section()

    def close_chapter(self):
        self.close_section()
        if len(self.chap.section) > 0:
            self.book.chapter.append( self.chap )
            self.chap = _chapter()

if __name__ == '__main__':
    import sys
    import codecs
    f1 = codecs.open(sys.argv[1],'r','utf-8')
    text = f1.read()[1:]
    f1.close()
    #-------------------
    from book_writer import book_writer
    dom = txt_parser().parse(text)
    out = book_writer().tohtml(dom)
    f2 = open(sys.argv[2],'w')
    f2.write( out.encode('utf-8') )
    f2.close()
# vim: sw=4 ts=8 expandtab
