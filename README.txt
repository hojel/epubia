설명
==========
Plain text 파일을 ePub 또는 PDF 로 출력

홈페이지: http://code.google.com/p/epubia

입력
==========
Plain text 파일을 넣어주면 인코딩 및 포맷을 알아서 포맷팅한다.

또한 Markdown 표현을 지원하여 텍스트를 포맷팅하거나 그림을 넣을 수도 있다.

그러나 Markdown과 다음이 다르다.

- '-' 로 새로운 줄이 시작하더라도 numbered list 취급되지 않는다.
- '*' 만 있는 줄은 문단과 문단 사이에 빈 문단을 삽입한다.
- '* * *'은 문단과 문단 사이에 분리그림을 넣는다.
- '\t'(탭)으로 시작하는 절은 preformatted text로 취급한다.

참고: http://code.google.com/p/epubia/wiki/HangulText

자세한 사용예는 input/example 을 참고할 것.

책정보
==========
Markdown의 Meta 확장을 지원하여 텍스트 파일에 저자, 표지등의 책에 대한 정보를 삽입가능하다.

Title: <책제목>
Subtitle: <책 소제목>
Author: <저자>
Translator: <옮긴이>
Publisher: <출판사>
cover_url: <책표지 파일의 이름 또는 주소>
ISBN: <분류코드>

자세한 사용예는 input/example 을 참고할 것.

Daum 과 Naver OpenAPI를 이용하여 책정보를 자동으로 넣어준다.
Naver 경우에는 개발키를 발급받아야함.

GUI에서 넣어준 사용자 정보로 검색을 한다.
만약 사용자가 정보를 주지 않을 경우 파일이름으로 검색한다.

출력
==========
3가지를 지원

   - ePub
   - PDF
   - Markdown Text

target/ 아래에는 출력기기 설정파일이 있다.
이 파일은 css 포맷으로 되어 있으며 주로 폰트파일 설정이 들어있다.
만약 새로운 폰트 파일을 사용하고 싶다면 비슷한 파일을 복사한 후 수정한다.

tgtxchg 프로그램을 사용하여 epubia로 만들어진 epub 파일의 출력기기를 변경할 수 있다.

Customize
==========
template/ 아래 있는 파일들을 수정하여 출력 ePUB의 형태를 customize 가능하다.

template/generic.css 를 수정하여 변경가능한 사항들
- 줄간격:   p{ line-indent } 변경. 기본값(1.4)
- 들여쓰기:  p{ text-indent } 변경. 기본값(1.2)
- 문단간격: p{ margin-top } 변경.
- 페이지 여백: body{margin-* } 변경.
- 장(챕터) 글꼴: h1
- 절(섹션) 글꼴: h2

자세한 것은 아래를 참고.
https://code.google.com/p/epubia/wiki/ePubTemplate

알려진 문제
==========
- ePUB 스펙에는 xhtml 파일의 크기가 제한되어 있다.
  구현된 epubgen은 html을 쪼개는 기능이 없어서 사용자가 문단을 따로 나누어야 한다.

알아두면 유용한 사항들
======================
- 만약 문단 시작을 잘 모를 때는 제목없는 # 을 넣는다. 
  제목이 없으면 문단은 나뉘더라도 목차에는 보이지 않는다.

- 챕터가 나눠줘 있지 않다면 너무 큰 xhtml 파일이 만들어져서 속도저하나 에러가 나타날 수 있다. (버그)
  되도록 챕터를 나눠주고, 만약 챕터를 모른다면 제목없이 '#' 을 넣어서 강제로 분할한다.

- 시(poem)나 게임소설의 status 등은 tab(preformatted text)이 유용하다.

- 편지등은 '>'을 이용한 indent가 유용하다.

- 만약 검색이 마음에 들지 않는다면 ISBN 번호만을 넣고 검색하면 된다.

- 출력기기용 설정을 변경하는 것 이외에도 generic.css 를 변경했을 때도 tgtxchg 를 사용하여 기존 epub의 수정이 가능하다.

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
   - http://www.lfd.uci.edu/~gohlke/pythonlibs/
   - Precompile된 Cheetah, PIL 을 설치