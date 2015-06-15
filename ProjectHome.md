한글 TEXT 파일을 ePub, PDF 로 변환하는 툴입니다.

문서내에 markup 문자를 사용하면 보다 좋은 결과를 얻을 수 있습니다.

또한 네이버/다음의 OpenAPI를 사용하여 책정보 및 표지를 가져와서 ePub에 같이 넣어줍니다.

Python을 기반으로 제작되었으며 wxPython과 Markdown, Cheetah 라이브러리를 사용하고 있습니다.
PDF 출력을 위해서 xhtml2pdf 가 사용되었고, 그래픽 파일 호환을 위해 PIL 이 사용되었습니다.



**꼭 기억할 것**

출력장치를 단지 선택하는 것만으로는 한글이 나오지 않음

꼭 target/ 디렉토리 밑에 있는 CSS 파일에 지정된 한글폰트가 이북리더에 있는지 확인



**공지**

[Calibre](http://calibre-ebook.com)가 플러그인을 지원함에 따라 '[한글 책정보](https://github.com/hojel/calibre-aladin-metadata-plugin)'와 '[입력 자동정렬](https://github.com/hojel/calibre-hangul-reformatter-plugin)' 기능을 때서 플러그인으로 만들었습니다.

처음부터 calibre를 대체할 목적도 아니였고 이젠 calibre에서 모두 가능해진 만큼 기능추가가 있지는 않을 것 같습니다.

다만 calibre가 epub3 지원을 할 계획이 없다고 한 만큼 epubia를 epub3 전용으로 해서 floating footnote 지원하도록 변경할까 생각만 있습니다.

[만화용 epub3 변환기](https://github.com/hojel/cbz2epub3)는 만들어봤으니 필요하신 분은 참고하세요.