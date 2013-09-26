# -*- encoding: utf-8 -*-
# Book Info using Aladin

import urllib
from lxml.html import fromstring, tostring
import re

class book_scraper:
    search_url = 'http://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={0:s}'
    browse_url = 'http://www.aladin.co.kr/shop/wproduct.aspx?ISBN={0:s}'
    ptn_isbn = re.compile('ISBN=(\d+X?)')
    ptn_date = re.compile('(\d{4})-(\d{2})-(\d{2})')

    default_value = {'title':'','author':'','isbn':'',
                     'cover_url':'',
                     'publisher':'','publishdate':'',
                     'description':'','subject':''}

    def __init__(self):
        pass

    def search(self,qstr,maxresult=3):
        url = self.search_url.format(urllib.quote_plus(qstr.encode('euc-kr')))
        raw = urllib.urlopen(url).read().decode('euc-kr')
        root = fromstring(raw)

        result = []
        for item in root.xpath('//div[@class="ss_book_box"]')[:maxresult]:
            info = dict()
            # Title & ISBN
            node = item.xpath('.//a[@class="bo3"][1]')[0]
            book_url = node.get('href')
            info['title'] = node.text_content()
            info['isbn'] = book_url.rsplit('ISBN=',1)[1]
            # Author
            node = item.xpath('.//a[contains(@href, "AuthorSearch=")][1]')[0]
            info['author'] = node.text_content()
            # Publisher
            node = item.xpath('.//a[contains(@href, "PublisherSearch=")][1]')[0]
            info['publisher'] = node.text_content()
            # Cover
            info['cover_url'] = item.xpath('.//img[1]/@src')[0].replace('/cover150/', '/cover/')
            if item.xpath('.//a[contains(@href,"wletslookViewer.aspx")]'):
                url = info['cover_url'].replace('/cover/', '/letslook/')
                info['cover_url'] = url.rsplit('_',1)[0]+'_f.jpg'

            result.append(info)
        return result

    def fetch(self,isbn):
        url = self.browse_url.format(isbn)
        raw = urllib.urlopen(url).read().decode('euc-kr')
        root = fromstring(raw)
        info = dict()

        tit_node = root.xpath('//td[@class="pwrap_bgtit"]')[0]
        # Title
        node = tit_node.xpath('.//a[@class="p_topt01"][1]')[0]
        info['title'] = node.text.strip()
        # Author
        node = tit_node.xpath('.//a[@class="np_af" and contains(@href,"AuthorSearch")][1]')[0]
        info['author'] = node.text.strip()
        # Publisher & PublishDate
        node = tit_node.xpath('.//a[@class="np_af" and contains(@href,"PublisherSearch")][1]')[0]
        info['publisher'] = node.text.strip()
        dstr = node.xpath('following-sibling::text()')[0]
        info['publishdate'] = "%s-%s-%s" % self.ptn_date.search(dstr).group(1,2,3)
        # Cover
        info['cover_url'] = root.xpath('//meta[@property="og:image"]/@content')[0]
        urls = root.xpath('//div[@class="p_previewbox"]/a/img/@src')
        if urls:
            info['cover_url'] = urls[0].replace('_fs.', '_f.')
        # ISBN-13
        url = root.xpath('//meta[@property="og:url"]/@content')[0]
        info['isbn'] = url.rsplit('/',1)[1]
        # Short Description
        info['description'] = root.xpath('//meta[@name="Description"]/@content')[0]

        return info

if __name__ == "__main__":
    info = book_scraper().search( u"은하영웅전설 1" )[0]
    print info['title']
    print info['author']
    print info['cover_url']

    info = book_scraper().search( u"[이광수]무정" )[0]
    print info['title']
    print info['author']
    print info['cover_url']

    info = book_scraper().fetch("8932903506")
    print info['title']
    print info['author']
    print info['cover_url']
    print info['isbn']
    print info['description']
    print info['publisher']
    print info['publishdate']
# vim:ts=4:sw=4:et
