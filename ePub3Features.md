# ePUB3 #

[idpf](http://www.idpf.org/epub/30/spec/)에서 interactive한 전자책을 목표로 ePUB 3.0을 내놓았다.

기술적으로는 HTML5+CSS3+Javascript를 사용하여 웹프로그래밍이 가능하도록 하였다.

## 새로 지원되는 기능들 ##

  1. 스크립트를 이용한 interactive 지원
  1. 본문과 독립된 그림표시 (`<figure>`)
  1. 주석 (`<aside epub:type="footnote">`)
  1. 일본책 지원(우에서 좌로 보기와 세로 쓰기)
  1. 수학식 (MathML)
  1. 오디오, 비디오 (audio, video 태그와 SMIL 파일)
  1. 머리글, 바닥글 (oeb-page-head, oeb-page-foot)
  1. [fixed layout](http://www.idpf.org/epub/fxl/) 지원

[참고](https://code.google.com/p/epub-samples/wiki/FeatureMatrix)

## 파일구조 ##

ePUB의 구조를 대부분 유지하고 있다.
**content.opf** 안에 정의된 `<package version="3.0">`으로 ePUB2와 구분됨.

가장 크게 바뀐건 [Navigation](http://www.idpf.org/epub/30/spec/epub30-contentdocs.html#sec-xhtml-nav) 부분.
**toc.ncx** 이 **nav.xhtml** 이라는 파일로 대체되었다. 구조도 바뀜.

## 책구조 기술 ##

ePUB3도 이전 버전과 마찬가지로 XHTML을 기반으로 한다.
다만 기존에는 웹프로그래밍과 거의 유사했던데 비해, 이제는 **`<section>`** tag로 전자책 구조에 관련된 정보를 줄 수 있다.

다음은 본문을 section tag로 감싼 예이다.

```
<section epub:type="part">
  <h1>1 부</h1>
  <section epub:type="chapter">
    <h2>1 장</h2>
    ...
  </section>
</section>
```

여기서 핵심은 **`epub:type`** 이라는 parameter로 [Structure Semantic 스펙](http://www.idpf.org/epub/vocab/structure/)에는 책에 관련된 여러 값들을 정의해 놓고 있다.

이 값들은 `<section>`외에도 여러 곳에서 쓰이게 된다.

# 구현 예 #

[샘플참고](https://code.google.com/p/epub-samples/wiki/SamplesListing)

## 주석달기 ##

본문
```
설명이 필요한 글<a epub:type="noteref" href="#n1">1</a>
...
<aside epub:type="footnote"><p>설명글</p></aside>
```

`<aside>`는 평소 화면에서는 표시되어선 안된다.
확인해본 리더 중에 iBooks에서만이 제대로 동작했다.

주석번호를 조그맣게 보이게 하기 위해선 CSS에 다음을 추가한다.
```
@namespace epub "http://www.idpf.org/2007/ops";

a[epub|type='noteref'] { vertical-align: super; }
```

## 일본만화 ##

만화책과 같이 이미 편집된 책을 보기 위해선 fixed layout을 사용한다.

**content.opf** 에 다음을 추가한다.
```
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
  ...
  <meta property="rendition:layout">pre-paginated</meta>
  <meta property="rendition:spread">auto</meta>
  <meta property="rendition:orientation">auto</meta>
  ...
</metadata>
<spine page-progression-direction="rtl">
  <itemref idref="cover-page" properties="page-spread-left"/>
  <itemref idref="page002" properties="rendition:spread-both page-spread-right"/>
  <itemref idref="page003" properties="rendition:spread-both page-spread-left"/>
  <itemref idref="page004" properties="rendition:page-spread-center"/>
  ...
</spine>
```
**rtl** 은 '우에서 좌로 보기'를 뜻한다.

또한 각 페이지가 열리는 방향을 정할 수 있다.(page-spread-right, page-spread-left)

rendition:spread-both를 같이 이용하면 책처럼 보이게 할 수도 있다.

양면에 걸쳐있던 그림인 경우 rendition:page-spread-center 를 지정한다.

XHTML
```
  ...
  <div class="page"><img src="../Image/page004.jpg" alt="page 4"/></div>
  ...
```

CSS
```
img {
    position: absolute;
    margin: 0;
    z-index: 0;
    height: 100%;
}
```