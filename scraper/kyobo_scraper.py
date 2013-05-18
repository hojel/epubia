# -*- encoding: utf-8 -*-
# Cover from Kyobo books

import urllib

class book_scraper:
    def __init__(self):
        pass
    def get_hires_image(self, isbn):
        if len(isbn) != 13:
        	return None
        img_url = "http://image.kyobobook.co.kr/images/book/xlarge/{1:s}/x{0:s}.jpg".format(isbn, isbn[-3:])
        resp = urllib.urlopen(img_url)
        if resp.getcode() == 200:
            return img_url
        return None

if __name__ == "__main__":
    print book_scraper().get_hires_image('9788925856209')      # TEST:OK
    print book_scraper().get_hires_image('9788925856208')      # TEST:FAIL

# vim:ts=4:sw=4:et
