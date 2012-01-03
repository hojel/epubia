# -*- encoding: utf-8 -*-
# Book Info using Daum OpenAPI

import urllib
from xml.dom.minidom import parseString

import re
MARKUP_PTN = re.compile(r'</?[a-z]+>')

class book_scraper:
    key = 'DAUM_SEARCH_DEMO_APIKEY'    # my key
    srch_url = 'http://apis.daum.net/search/book?q={0:s}&result=1&apikey={1:s}&output=xml'
    isbn_url = 'http://apis.daum.net/search/book?q={0:s}&result=1&searchType=isbn&apikey={1:s}&output=xml'

    default_value = {'title':'','author':'','isbn':'',
                     'cover_url':'',
                     'publisher':'','publishdate':'',
                     'description':'','subject':''}

    def __init__(self):
        pass
    def search(self,qstr):
        return self.parse( urllib.urlopen(self.srch_url.format(urllib.quote_plus(qstr), self.key)).read() )
    def fetch(self,isbn):
        isbn = self.parse( urllib.urlopen(self.isbn_url.format(isbn, self.key)).read() )
        if isbn:
            return isbn[0]
        return None
    def parse(self,xml):
        info = []
        dom = parseString(xml)
        assert dom.childNodes[0].nodeName == 'channel'
        for node in dom.childNodes[0].childNodes:
            if node.nodeName == 'item':
                pkt = self.default_value
                for e in node.childNodes:
                    if e.nodeName == 'title':
                        if e.childNodes:
                            pkt['title'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'author':
                        if e.childNodes:
                            pkt['author'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'cover_s_url':
                        if e.childNodes:
                            pkt['cover_url'] = e.childNodes[0].nodeValue.replace('R72x100','image')
                    elif e.nodeName == 'pub_nm':
                        if e.childNodes:
                            pkt['publisher'] = e.childNodes[0].nodeValue
                    elif e.nodeName == 'pub_date':
                        if e.childNodes:
                            ss = e.childNodes[0].nodeValue
                            pkt['publishdate'] = "%s-%s-%s" % (ss[0:4],ss[4:6],ss[6:8])
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
                newimg = self.get_yes24_cover(pkt['isbn'])
                if newimg:
                    pkt['cover_url'] = newimg
                info.append( pkt )
        return info
    def cleanup(self,str):
        return MARKUP_PTN.sub('',str).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    # cover image from other sites
    def get_kyobo_cover(self,isbn):
        img_url = 'http://image.kyobobook.co.kr/images/book/large/{1:s}/l{0:s}.jpg'
        #img_url = 'http://image.kyobobook.co.kr/images/book/xlarge/{1:s}/l{0:s}.jpg'
        return img_url.format(isbn, isbn[-3:-1])
    def get_yes24_cover(self,isbn):
        srch_url = "http://www.yes24.com/SEARCHCORNER/Result?domain=BOOK&query={0:s}&detail_yn=Y&title_yn=N&author_yn=N&company_yn=N&isbn={0:s}&sort_gb=POPULAR"
        doc = urllib.urlopen(srch_url.format(isbn)).read()
        match = re.search("http://image.yes24.com/goods/(\d*)/S",doc)
        if match:
            return "http://image.yes24.com/goods/{0:s}/L".format(match.group(1))
        return None

if __name__ == "__main__":
    info = book_scraper().search( "은하영웅전설 1" )[0]
    print info['title']
    print info['author']
    print info['cover_url']

    info = book_scraper().search( "[이광수]무정" )[0]
    print info['title']
    print info['author']
    print info['cover_url']
# vim:ts=4:sw=4:et
