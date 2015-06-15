# ePUB 변환 #

  * [epub-tools](http://code.google.com/p/epub-tools/)
> > Java로된 Adobe EPUBGen 엔진을 사용하고 있으며,
> > frontend engine에는 XSLT 기술을 사용.
  * [python-epub-builder](https://code.google.com/p/python-epub-builder/)
> > [Genshi](http://genshi.edgewall.org/) template library 기반으로 한 text to epub 변환기.
> > 간단한 text만을 대상으로 하여 markup을 넣기가 어렵고, Genshi 자체가 덩치가 있어보여 수정을 포기.
  * [rst2epub](http://bitbucket.org/wierob/rst2epub/)
> > reStructured Text를 ePUB으로 변환.
> > 프로젝트를 완료하고 발견. 괜히 고생했다는 생각이 나게 만든다.
  * [Universal Document Converter(Pandoc)](http://johnmacfarlane.net/pandoc/)
> > Markdown, ePub, PDF 를 포함한 다양한 포맷을 변환.
  * [EPUB Sharp](http://epubsharp.sourceforge.net/)
> > .NET/C# 기반

# Markup 언어 #
여러 텍스트용 markup이 존재하고
주로 program document를 간단하게 작성하는 용으로 사용된다.

  * [reStructured Text](http://docutils.sourceforge.net/rst.html)(RST)
> > Python Docutils에서 사용하는 포맷
  * [Markdown](http://www.freewisdom.org/projects/python-markdown/)
> > Calibre에서 지원한다
  * [html2text](http://www.aaronsw.com/2002/html2text/)
> > HTML(이것도 Markup의 일종이다)을 Markdown text로 변환
  * [Textile](http://www.textism.com/tools/textile/)
> > HTML에 대한 controllability가 좋으나, 그만큼 readability는 떨어짐
  * [Google Wiki](http://code.google.com/p/support/wiki/WikiSyntax)
> > 여기 문서 작성하는 포맷

# PDF 변환 #
PDF 생성엔진으로 [ReportLab Toolkit](http://www.reportlab.com/software/opensource/rl-toolkit/)을 대부분 사용하고 있고, 그위에 frontend engine을 올려 변환기들이 나와 있음.

  * [xhtml2pdf](http://www.xhtml2pdf.com) (aka pisa)
> > XHTML을 PDF로 변환
  * [rst2pdf](http://code.google.com/p/rst2pdf)
> > reStructured Text를 PDF로 변환
  * [PDFMiner](http://www.unixuser.org/~euske/python/pdfminer/)
> > CJK지원하는 PDF parser. 아직 버그가 많다.

# RSS 언어 #
RSS 처리는 [Universal Feed Parser](http://feedparser.org)가 진리.

HTML 처리는 [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)이 진리.

  * [rss2epub](http://cafe.naver.com/ebook/82965)
> > [이북카페](http://ebookcafe.kr) 욱님이 만든 python script.
> > Matt's epub.py 라는 간단한 생성기를 사용

# 그외 #

  * [Calibre](http://calibre-ebook.com)
> > ePUB 툴의 대명사. Python 기반.
  * [LRFtool](http://code.google.com/p/lrf-epub-tools/)
> > Sony Reader용 포맷인 LRF를 ePUB으로 변환하는 툴이지만
> > 그외에도 여러 포맷을 지원
  * [epubcheck](http://code.google.com/p/epubcheck)
> > ePUB 파일을 검사하는 툴. Java 기반.
  * [XSLT를 사용한 ePUB](http://www.stylusstudio.com/xsllist/200901/post90300.html)
> > XSLT를 공부해야하나...