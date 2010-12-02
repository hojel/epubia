# -*- encoding: utf-8 -*-
# Text to ePUB converter

import sys
__program__ = "ptxt2epub"
__version__ = "0.1.0"

tmpldir = "../ptxt2epub/template"
targetcss = "../target/NookColor.css"

from txt_cleaner import txt_cleaner
from book_scraper_daum import book_scraper
from txt_parser import txt_parser
from book_writer import html_writer
from epub_gen import epub_gen

def ptxt2epub(txtfile, isbn, epubfile, start=1):
    # parsing
    txt  = txt_cleaner().load( txtfile, start=start )
    book = txt_parser().parse(txt)
    if isbn:
        # search with isbn
        info = book_scraper().fetch(isbn)
    else:
        # search with file name
        import os
        srch = unicode(os.path.splitext( os.path.basename(txtfile) )[0], 'cp949')
        print "searching %s" % srch
        info = book_scraper().search( srch.encode('utf-8') )[0]
    print "title: %s" % info['title']
    print "author: %s" % info['author']
    book.title = info['title']
    book.author = info['author']
    book.isbn = info['isbn']
    book.publisher = info['publisher']
    book.description = info['description']
    book.subject = [ info['subject'] ]
    # generating
    htm = html_writer(book).per_chapter()
    epub_gen(book, htm, info['image'], tmpldir, targetcss, epubfile)
    print "%s is generated" % epubfile

if __name__ == "__main__":
    import sys, os
    from optparse import OptionParser

    parser = OptionParser(usage = '%prog [options] txt')
    parser.add_option("-o", "--output", dest="outfile",
                      help="output ePub name", metavar="FILE")
    parser.add_option("-n", "--isbn", dest="isbn",
                      help="ISBN-13 of input", metavar="ISBN")
    parser.add_option("-s", "--start", dest="start",
                      help="input start line", metavar="INT")
    options, args = parser.parse_args()

    if len(args) < 1 or not os.path.isfile(args[0]):
        parser.print_help()
        sys.exit(1)

    if options.outfile:
        outname = options.outfile
    else:
        outname = os.path.splitext(args[0])[0] + '.epub'

    start = 1       # start from first line
    if options.start:
        start = int(options.start)

    ptxt2epub(args[0], options.isbn, outname, start=start)

# vim:ts=4:sw=4:et
