# ePUB 파일구조 #

ePUB은 기본적으로 xml과 그림 파일들을 zip으로 묶어놓은 것이다.
따라서 확장자를 zip으로 변경하여 풀면 내부구조를 볼 수 있다.

## 고정 파일들 ##
ePUB에는 mimetype 과 META-INF/container.xml 파일이 항상 존재해야 한다.

  * mimetype : 파일의 형식을 알림 (_zip파일에 비압축으로 저장되어 있어야함_)
  * container.xml : 책정보파일(OPF)을 가르킴

## 책정보 (OPF 파일) ##
책제목, 저자, 출판사 등의 책에 대한 정보와
ePUB 파일에 포함된 파일들에 대한 정보가지고 있는 파일.
ePUB의 핵심이라 하겠다.
_epubia_ 는 content.opf 라는 파일을 생성한다.

책정보, 포함된 파일정보, 책이 보여지는 순서, 이 세가지 정보를 포함하고 있다.

#### 책정보(Metadata) ####
다음 정보들이 정의되어 있음.

  * 저자 `<dc:creator opf:role="aut">`
  * 책제목 `<dc:title>`
  * 출판사 `<dc:publisher>`
  * 출판일시 `<dc:date>`
  * ISBN `<dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1/" opf:scheme="ISBN">`
  * 설명 `<dc:description>`
  * 주제 `<dc:subject>`

#### 파일정보(manifest) ####
ePUB 파일에 포함된 모든 파일들과 타입을 정한다.
본문, CSS, 이미지 파일은 물론 목차파일(NCX)도 포함된다.

```
<item id="c01" href="text/chapter1.xhtml" media-type="application/xhtml+xml"/>
```

#### 책순서(spine) ####
책이 읽혀질 순서. manifest에 정의된 파일들의 id들이 적힌다.

```
<itemref idref="c01"/>
```

## 바로가기 정보 (NCX 파일) ##
리더에서 목차(Contents) 버튼을 누르면 보여지는 정보가 되겠다.
_epubia_ 는 toc.ncx 라는 파일을 생성한다.

`<nav>`, `<navMap>`, `<navPoint>`의 순서로 적히며, `<navLabel>`에 이름, `<content>`에 건더뛸 주소를 적는다.

```
<navPoint id="navPoint-1" playOrder="1">
  <navLabel>
    <text>창세기</text>
  </navLabel>
  <content src="text/chapter1.xhtml"/>
</navPoint>
```

## 책(OEBPS/OPS 파일) ##
책의 내용은 xhtml이라는 html의 간략화(?)된 파일로 저장되어 있어야 한다.
모든 파일의 위치는 OPF에 포함되어 있지만, 통상적으로 OEBPS나 OPS라는
폴더 밑에 나두게 된다.

CSS(stylesheet)은 책의 모양과 글꼴을 결정하게 되는데
각 xhtml파일에 연결되어 있어야 한다.
하나 이상의 CSS를 가질 수 있으며, _epubia_ 는
  * 문단 모양을 결정하는 generic.css
  * 출력장치별 글꼴을 결정하는 target.css
를 출력파일에 포함시킨다.

## 표지 ##
표지그림이 있다면 coverpage.xhtml를 포함시킨다.
(루트에 있는 이유는 그래야 Nook Color에서 미리보기를 만들기 때문이다.)

책제목과 저자명으로 titlepage.xhtml 을 만들고 책의 가장 앞에 놓는다.

목차(Table of Contents)는 굳이 생성하지 않는데 이는 NCX 파일이 있기 때문이다.

# Template 설명 #
epubia 은 ptxt2epub/template 란 디렉토리와 target/ 디렉토리에 있는 파일들을
사용하여 ePUB 파일을 만든다.

## 전반적인 ePUB 맞춤(customization) ##
ptxt2epub/template에는 다음 파일들이 존재하며 각각은 다음 역활을 한다.
  * chapter.xhtml : 책내용
  * content.opf   : 책정보
  * toc.ncx       : 바로가기
  * titlepage.xhtml : 속표지
  * coverpage.xhtml : 겉표지
  * generic.css   : 문단 모양 stylesheet
페이지 모양을 바꾸고 싶다면 generic.css을 수정하면 된다.

## 출력장치에 맞춘 변경 ##
target/ 디렉토리 밑에는 여러 이름의 css 파일이 있으며,
이중 하나를 골라 target.css 라는 이름으로 ePUB 파일에 복사된다.