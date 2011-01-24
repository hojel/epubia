설명
==========
Plain text 파일을 ePub 또는 PDF 로 출력

홈페이지: http://code.google.com/p/epubia

입력
==========
Plain text 파일을 알아서 포맷팅한다.

Markdown 표현을 지원하여 텍스트를 포맷팅하거나 그림을 넣을 수도 있다.
또한 Meta 확장을 지원하여 텍스트 파일에 저자, 표지등의 책에 대한 정보를 삽입가능하다.

참고: http://code.google.com/p/epubia/wiki/HangulText

책정보
==========
Daum 과 Naver OpenAPI를 이용하여 책정보를 자동으로 넣어준다.
Naver 경우에는 개발키를 발급받아야함.

출력
==========
3가지를 지원

   - ePub
   - PDF
   - Markdown Text

설치
================

1. Python 2.7 설치

2. wxPython for Python 2.7 설치

3. 필요 패키지 설치

  > easy_install pil
  > easy_install chardet
  > easy_install markdown 
  > easy_install cheetah
  > easy_install reportlab
  > easy_install html5lib
  > easy_install pisa

4. 만약 C version Name Mapper가 없다는 경고가 날 경우:
   - Base 패키지 다운로드 (http://www.lfd.uci.edu/~gohlke/pythonlibs/#base)
   - 7-zip 프로그램으로 exe를 읽어서 _namemapper.pyd 을 추출
   - _namemapper.pyd 를 site-package\cheetah-*.egg\Cheetah 에 복사