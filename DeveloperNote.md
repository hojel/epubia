# 컴파일 방법 #

## 필요한 도구들 ##

  * [Python 2.6](http://www.activestate.com/activepython/downloads)
  * [wxPython](http://www.wxpython.org) GUI widget
  * [Cheetah](http://www.cheetahtemplate.org) template library
  * [Python Image Library](http://www.pythonware.com/products/pil/)
  * py2exe
  * [SVN](http://tortoisesvn.tigris.org) version control system

## 컴파일과정 ##

  1. Python 2.x를 설치한다. 개발에는 ActivePython 2.6을 사용하였다.
  1. wxPython 을 설치한다. 코드수정을 생각한다면 wxPython demo 설치를 추천한다.
  1. Cheetah와 py2exe를 설치한다.
```
    easy_install Cheetah
    easy_install py2exe
```
  1. SVN 을 설치한다.
  1. 개발디렉토리에 SVN을 사용하여 코드를 복사한다.
  1. compile.bat을 실행하면 dist/ 밑에 실행파일이 생성된다.

# 프로그램 파일구조 #
크게 GUI 와 Converter Engine으로 구정되어 있음.

## GUI ##
gui/ 디렉토리에 소스코드 위치.

  * gui.py : 전체 GUI framework
  * txt\_table.py : 파일테이블

## Converter Engine (ptxt2epub) ##
ptxt2epub/ 디렉토리에 소스코드 위치

  * txt\_cleaner.py  : 주어진 text를 포맷된 text로 변환
  * txt\_parser.py   : 포맷된 text에서 부터 object 생성
  * book\_scraper\_daum.py : (Daum OpenAPI 사용)
  * book\_scraper\_naver.py : (Naver OpenAPI 사용)
  * epub\_gen.py   : object와 template에서 ePUB 파일을 생성

Scraper는 OpenAPI를 사용하기 때문에 사용자가 키를 받아서 넣어줘야 한다.

ptxt2epub.py 는 command-line 유틸리티로 디버깅용으로만 사용된 파일이다.