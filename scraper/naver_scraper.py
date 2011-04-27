# -*- encoding: utf-8 -*-
# Book Info using Naver OpenAPI

import urllib
from xml.dom.minidom import parseString

import re
MARKUP_PTN = re.compile(r'</?[a-z]+>')

class book_scraper:
    key = ''    # my key
    srch_url = 'http://openapi.naver.com/search?key={0:s}&query={1:s}&display=1&target=book'
    isbn_url = 'http://openapi.naver.com/search?key={0:s}&query={1:s}&display=1&target=book_adv&d_isbn={1:s}'
    img_url  = 'http://book.daum-img.net/image/KOR{0:s}'

    default_value = {'title':'','author':'','isbn':'',
                     'cover_url':'',
                     'publisher':'','description':'','subject':''}

    def __init__(self):
        pass
    def search(self,qstr):
        return self.parse( urllib.urlopen(self.srch_url.format(self.key, urllib.quote_plus(qstr))).read() )
    def fetch(self,isbn):
        return self.parse( urllib.urlopen(self.isbn_url.format(self.key, isbn)).read() )[0]
    def parse(self,xml):
        info = []
        dom = parseString(xml)
        assert dom.childNodes[0].childNodes[0].nodeName == 'channel'
        for node in dom.childNodes[0].childNodes[0].childNodes:
            if node.nodeName == 'item':
                pkt = self.default_value
                for e in node.childNodes:
                    if e.nodeName == 'title':
                        pkt['title'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'author':
                        pkt['author'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'image':
                        pkt['cover_url'] = e.childNodes[0].nodeValue.replace('=m1','=m5')
                    elif e.nodeName == 'publisher':
                        pkt['publisher'] = e.childNodes[0].nodeValue
                    elif e.nodeName == 'description':
                        if e.childNodes:
                            pkt['description'] = self.cleanup(e.childNodes[0].nodeValue)
                    elif e.nodeName == 'isbn':
                        if e.childNodes:
                            pkt['isbn'] = self.cleanup(e.childNodes[0].nodeValue.split(' ')[-1])
                if pkt['cover_url'] == '' and len(pkt['isbn']) == 13:
                    pkt['cover_url'] = self.img_url.format(pkt['isbn'], pkt['isbn'][-3:-1])
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
