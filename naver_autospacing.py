maxline = 10000         # from web-page
qurl = 'http://s.lab.naver.com/autospacing/?'
qvalues = { "query": "",
            "result_type": "paragraph"
          }
qheaders = {"Referer": qurl,
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
           }

import urllib, urllib2
import re

def _naver_autospacing(txt):
    qvalues['query'] = txt.encode('utf-8').replace('\n','\r\n')
    data = urllib.urlencode(qvalues)
    req = urllib2.Request(qurl, data, qheaders)
    r = urllib2.urlopen(req)
    doc = r.read().decode('utf-8')
    markup = re.compile('<div class="wrap_spacing2" style="clear:both;">(.*?)</div>', re.S).search(doc).group(1)
    markup = re.compile('<br>').sub('\n',markup)
    txt = re.compile('<[^<>]*>').sub('',markup)
    return txt.strip()
    
def naver_autospacing(txt):
    # warning if #line > maxline
    return _naver_autospacing(txt)

#################################################3
# main
if __name__ == "__main__":
    import sys
    txt = open(sys.argv[1], 'r').read()[3:].decode('utf-8')
    txt2 = naver_autospacing(txt)
    open(sys.argv[2], 'w').write(txt2.encode('utf-8'))
# vim:sts=4:et
