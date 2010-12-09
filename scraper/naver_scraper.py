# -*- encoding: utf-8 -*-
# Book Info using Naver OpenAPI

import urllib
from xml.dom.minidom import parseString

import re
MARKUP_PTN = re.compile(r'</?[a-z]+>')

class book_scraper:
    key = '46f179fdde77da5c56e24c842ee802c8'    # my key
    srch_url = 'http://openapi.naver.com/search?key=%s&query=%s&display=1&target=book'
    isbn_url = 'http://openapi.naver.com/search?key=%s&query=%s&display=1&target=book_adv&d_isbn=%s'
    kyobo_img = 'http://image.kyobobook.co.kr/images/book/large/%s/l%s.jpg'
    #kyobo_img = 'http://image.kyobobook.co.kr/images/book/xlarge/%s/x%s.jpg'

    default_value = {'author':'','isbn':'',
                     'cover_url':'',
                     'publisher':'','description':'','subject':''}

    def __init__(self):
        pass
    def search(self,qstr):
        return self.parse( urllib.urlopen(self.srch_url % (self.key, urllib.quote_plus(qstr))).read() )
    def fetch(self,isbn):
        return self.parse( urllib.urlopen(self.isbn_url % (self.key, isbn)).read() )[0]
    def parse(self,xml):
        info = []
        dom = parseString(xml)
        assert dom.childNodes[0].childNodes[0].nodeName == 'channel'
        for node in dom.childNodes[0].childNodes[0].childNodes:
            pkt = self.default_value
            if node.nodeName == 'item':
                for e in node.childNodes:
                    if e.nodeName == 'title':
                        pkt['title'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'author':
                        pkt['author'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'cover_url':
                        pkt['cover_url'] = e.childNodes[0].nodeValue.replace('=m1','=m5')
                    elif e.nodeName == 'publisher':
                        pkt['publisher'] = e.childNodes[0].nodeValue
                    elif e.nodeName == 'description':
                        pkt['description'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'isbn':
                        pkt['isbn'] = e.childNodes[0].nodeValue.split(' ')[-1]
                if pkt['cover_url'] == '' and len(pkt['isbn']) == 13:
                    pkt['cover_url'] = self.kyobo_img % (pkt['isbn'][-3:-1], pkt['isbn'])
                info.append( pkt )
        return info
    def cleanup(self,str):
        return MARKUP_PTN.sub('',str).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

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
