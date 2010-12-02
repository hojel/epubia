# -*- encoding: utf-8 -*-
# Book Info using Daum OpenAPI

import urllib
from xml.dom.minidom import parseString

import re
MARKUP_PTN = re.compile(r'</?[a-z]+>')

class book_scraper:
    key = 'DAUM_SEARCH_DEMO_APIKEY'    # my key
    srch_url = 'http://apis.daum.net/search/book?q=%s&result=1&apikey=%s'
    isbn_url = 'http://apis.daum.net/search/book?q=%s&result=1&searchType=isbn&apikey=%s'
    kyobo_img = 'http://image.kyobobook.co.kr/images/book/large/%s/l%s.jpg'
    #kyobo_img = 'http://image.kyobobook.co.kr/images/book/xlarge/%s/x%s.jpg'

    def __init__(self):
        pass
    def search(self,qstr):
        return self.parse( urllib.urlopen(self.srch_url % (urllib.quote_plus(qstr), self.key)).read() )
    def fetch(self,isbn):
        return self.parse( urllib.urlopen(self.isbn_url % (isbn, self.key)).read() )[0]
    def parse(self,xml):
        info = []
        dom = parseString(xml)
        assert dom.childNodes[0].nodeName == 'channel'
        for node in dom.childNodes[0].childNodes:
            pkt = {'title':'', 'author':'', 'image':'', 'isbn':'',
                   'publisher':'', 'subject':'', 'description':''}
            if node.nodeName == 'item':
                for e in node.childNodes:
                    if e.nodeName == 'title':
                        if e.childNodes:
                            pkt['title'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'author':
                        if e.childNodes:
                            pkt['author'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'cover_s_url':
                        if e.childNodes:
                            pkt['image'] = e.childNodes[0].nodeValue.replace('R72x100','image')
                    elif e.nodeName == 'pub_nm':
                        if e.childNodes:
                            pkt['publisher'] = e.childNodes[0].nodeValue
                    elif e.nodeName == 'category':
                        if e.childNodes:
                            pkt['subject'] = e.childNodes[0].nodeValue
                    elif e.nodeName == 'description':
                        if e.childNodes:
                            pkt['description'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'isbn':  # ISBN-10
                        if e.childNodes:
                            pkt['isbn'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'barcode':  # ISBN-13
                        if e.childNodes:
                            pkt['isbn'] = self.cleanup(e.childNodes[0].nodeValue)[3:]
                if pkt['image'] == '' and len(pkt['isbn']) == 13:
                    pkt['image'] = self.kyobo_img % (pkt['isbn'][-3:-1], pkt['isbn'])
                info.append( pkt )
        return info
    def cleanup(self,str):
        return MARKUP_PTN.sub('',str).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

if __name__ == "__main__":
    info = book_scraper().search( "은하영웅전설 1" )[0]
    print info['title']
    print info['author']
    print info['image']

    info = book_scraper().search( "[이광수]무정" )[0]
    print info['title']
    print info['author']
    print info['image']
# vim:ts=4:sw=4:et
