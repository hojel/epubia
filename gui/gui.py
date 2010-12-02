# -*- coding: utf-8 -*-
# Main Window
import wx
from wx.lib.wordwrap import wordwrap
import os

from file_table import MyGrid
from optiondlg import MyOption

import sys
__program__ = sys.modules['__main__'].__program__
__version__ = sys.modules['__main__'].__version__

#--------------------------------------------------
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title, config):
        wx.Frame.__init__(self, parent, title=title)
        panel = wx.Panel(self, wx.ID_ANY)

        # default option
        self.config = config
        self.dirname = os.curdir
        self.scrap = []     # scrap result
        self.tmpldir = "ptxt2epub/template"
        self.targetcss = "target/%s.css" % self.config['TargetCSS']

        # init
        self.SetScraper()

        # top button bar
        btn1 = wx.Button(panel, wx.ID_ANY, u"읽어오기")    # Import
        btn2 = wx.Button(panel, wx.ID_ANY, u"제거")        # Remove
        btn3 = wx.Button(panel, wx.ID_ANY, u"책정보읽기")  # Scrap
        btn4 = wx.Button(panel, wx.ID_ANY, u"변환")        # Convert
        btn5 = wx.Button(panel, wx.ID_ANY, u"설정")        # Option
        btn6 = wx.Button(panel, wx.ID_ANY, u"정보")        # About
        btn7 = wx.Button(panel, wx.ID_ANY, u"나가기")      # Exit
        self.Bind(wx.EVT_BUTTON, self.runImport, btn1)
        self.Bind(wx.EVT_BUTTON, self.runRemove, btn2)
        self.Bind(wx.EVT_BUTTON, self.runScrap, btn3)
        self.Bind(wx.EVT_BUTTON, self.runConvert, btn4)
        self.Bind(wx.EVT_BUTTON, self.OnOption, btn5)
        self.Bind(wx.EVT_BUTTON, self.OnAbout, btn6)
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn7)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        btnszer1 = wx.BoxSizer(wx.HORIZONTAL)
        for btn in [btn1, btn2, btn3, btn4, btn5, btn6, btn7]:
            btnszer1.Add(btn, 1, wx.LEFT|wx.RIGHT, 2)

        # second bar
        #selbtn1 = wx.Button(panel, wx.ID_ANY, u"전체선택")
        #selbtn2 = wx.Button(panel, wx.ID_ANY, u"전체취소")
        #self.Bind(wx.EVT_BUTTON, self.SelectAll, selbtn1)
        #self.Bind(wx.EVT_BUTTON, self.SelectNone, selbtn2)

        # target directory
        ddchk = wx.CheckBox(panel, wx.ID_ANY, u"출력위치")
        ddchk.SetValue( self.config['UseDestDir'] )
        dtb1 = wx.TextCtrl(panel, value=self.config['DestDir'])
        ddbtn = wx.Button(panel, wx.ID_ANY, u"선택")
        self.Bind(wx.EVT_CHECKBOX, self.OnUseDestDir, ddchk)
        self.Bind(wx.EVT_BUTTON, self.OnDestDirSelect, ddbtn)

        ddszer = wx.BoxSizer(wx.HORIZONTAL)
        ddszer.Add(ddchk, 0, wx.CENTER|wx.LEFT, 5)
        ddszer.Add(dtb1, 1, wx.GROW|wx.LEFT|wx.RIGHT, 2)
        ddszer.Add(ddbtn, 0, wx.LEFT|wx.RIGHT, 2)

        btnszer2 = wx.BoxSizer(wx.HORIZONTAL)
        #btnszer2.Add(selbtn1, 0, wx.LEFT, 1)
        #btnszer2.Add(selbtn2, 0, wx.LEFT, 1)
        #btnszer2.Add( (20,10) )
        btnszer2.Add(ddszer, 0, wx.RIGHT, 1)

        # file table
        self.grid = MyGrid(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btnszer1, 0, wx.GROW|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(btnszer2, 0, wx.GROW|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(self.grid, 1, wx.GROW|wx.ALL, 5)

        self.panel = panel
        self.dirbox = dtb1

        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.Show(True)

        (h,w) = self.GetSize()
        self.SetSize( (h,w+300) )

    def SelectAll(self, evt):
        for row in range(self.grid.table.GetNumberRows()):
            self.grid.table.SetValue(row, 0, True)

    def SelectNone(self, evt):
        for row in range(self.grid.table.GetNumberRows()):
            self.grid.table.SetValue(row, 0, False)

    def runImport(self, evt):
        # multi-file open dialogue
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose files", self.dirname, "", "*.txt", wx.FD_OPEN|wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetDirectory()
            for fname in dlg.GetFilenames():
                newrow = self.grid.table.GetNumberRows()
                # add new row
                self.grid.table.SetValue( newrow, 0, True )
                self.grid.table.SetValue( newrow, 1, fname )
                self.scrap.append({'file':fname,'dir':self.dirname})
        dlg.Destroy()

    def runRemove(self, evt):
        cntl = range(self.grid.table.GetNumberRows())
        cntl.reverse()
        for row in cntl:
            if self.grid.table.GetValue(row, 0):
                self.scrap.pop(row)
                self.grid.table.DeleteRow(row)

    def runScrap(self, evt):
        # get total count to do
        cnt = 0
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                cnt += 1
        if cnt == 0:
            return
        dlg = wx.ProgressDialog(u"Book Scrapping",
                                u"책정보 가져오기",
                                maximum = cnt,
                                parent = self,
                                style = wx.PD_CAN_ABORT
                                      | wx.PD_AUTO_HIDE
                                      | wx.PD_APP_MODAL
                                )
        # scrapping
        cnt = 0
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                fname = self.grid.table.GetValue(row, 1)
                title = self.grid.table.GetValue(row, 2)
                isbn  = self.grid.table.GetValue(row, 4)
                # scrapping main
                info = None
                if isbn:
                    (keepGoing, skip) = dlg.Update(cnt, u"%s 검색중" % isbn)
                    if not keepGoing: break
                    info = self.scraper.fetch(isbn)
                elif title:
                    (keepGoing, skip) = dlg.Update(cnt, u"%s 검색중" % title)
                    if not keepGoing: break
                    rslt = self.scraper.search( title.encode('utf-8') )
                    if rslt:
                        info = rslt[0]
                else:
                    (keepGoing, skip) = dlg.Update(cnt, u"%s 검색중" % fname)
                    if not keepGoing: break
                    srch = os.path.splitext(fname)[0]
                    rslt = self.scraper.search( srch.encode('utf-8') )
                    if rslt:
                        info = rslt[0]
                if info:
                    self.grid.table.SetValue(row, 2, info['title'])
                    self.grid.table.SetValue(row, 3, info['author'])
                    self.grid.table.SetValue(row, 4, info['isbn'])
                else:
                    info = {'title':os.path.splitext(fname)[0],
                            'author':'','isbn':'',
                            'image':'',
                            'publisher':'','description':'','subject':''}
                self.scrap[row]['info'] = info
                cnt += 1
        dlg.Update(cnt, u"완료")

    def runConvert(self, evt):
        from ptxt2epub.txt_cleaner import txt_cleaner
        from ptxt2epub.txt_parser import txt_parser
        from ptxt2epub.book_writer import html_writer
        from ptxt2epub.epub_gen import epub_gen
        # get total count to do
        cnt = 0
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                cnt += 1
        if cnt == 0:
            return
        dlg = wx.ProgressDialog(u"Book Conversion",
                                u"ePUB 변환",
                                maximum = cnt,
                                parent = self,
                                style = wx.PD_CAN_ABORT
                                      | wx.PD_APP_MODAL
                                )
        # scrapping
        cnt = 0
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                # parse
                txtfile = os.path.join( self.scrap[row]['dir'], self.scrap[row]['file'] )
                txt  = txt_cleaner().load( txtfile, start=1 )
                book = txt_parser().parse(txt)
                info = self.scrap[row]['info']
                book.title = self.grid.table.GetValue(row, 2)
                book.author = self.grid.table.GetValue(row, 3)
                book.isbn = self.grid.table.GetValue(row, 4)
                book.publisher = info['publisher']
                book.description = info['description']
                book.subject = [ info['subject'] ]

                (keepGoing, skip) = dlg.Update(cnt, u"%s 변환중" % book.title)
                if not keepGoing:
                    break

                # generate
                if self.config['UseTitleInOutputFile']:
                    filebase = book.title
                else:
                    filebase = os.path.splitext( os.path.basename(txtfile) )[0]
                if self.config['UseDestDir']:
                    epubfile = os.path.join(self.config['DestDir'], filebase+'.epub')
                else:
                    epubfile = os.path.join(os.path.dirname(txtfile), filebase+'.epub')
                htm = html_writer(book).per_chapter()
                epub_gen(book, htm, info['image'], self.tmpldir, self.targetcss, epubfile)
                print u"%s is generated" % epubfile
                cnt += 1
        dlg.Update(cnt, u"변환완료: %d개" % cnt)

    def OnOption(self, evt):
        tempcfg = self.config
        dlg = MyOption(self.panel, u"설정", tempcfg)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            self.config = tempcfg
            self.SetScraper()
            self.targetcss = "target/%s.css" % self.config['TargetCSS']
        dlg.Destroy()

    def OnAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = __program__
        info.Version = __version__
        info.Copyright = "(c) 2010, follows MIT License Policy"
        info.Description = wordwrap(
            u"한글 텍스트를 ePub으로 변환\n\n"
            u"읽어오기, 책정보가져오기, 변환 순서로 누르면 ePUB파일이 만들어 집니다.\n"
            u"출력장치를 추가하려면 target/에 있는 css파일을 복사 편집하세요.\n",
            350, wx.ClientDC(self))
        info.WebSite = ("http://code.google.com/p/epubia", "Project Home")
        info.Developers = [ "hojelei@gmail.com" ]

        #info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)

    def OnClose(self, evt):
        self.Close(True)

    def OnExit(self, evt):
        self.Destroy()

    def OnUseDestDir(self, evt):
        self.config['UseDestDir'] = evt.IsChecked()

    def OnDestDirSelect(self, evt):
        dlg = wx.DirDialog(self, u"디렉토리 선택:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.config['DestDir'] = dlg.GetPath()
            self.dirbox.SetValue( self.config['DestDir'] )
        dlg.Destroy()

    def SetScraper(self):
        if self.config['Scraper'] == 'Naver':
            import ptxt2epub.book_scraper_naver
            self.scraper = ptxt2epub.book_scraper_naver.book_scraper()
            self.scraper.key = self.config['NaverAPIKey']
        else:
            import ptxt2epub.book_scraper_daum
            self.scraper = ptxt2epub.book_scraper_daum.book_scraper()
            self.scraper.key = self.config['DaumAPIKey']

#--------------------------------------------------
def gui(config):
    app = wx.App(False)
    frame = MyFrame(None, __program__, config)
    app.MainLoop()
# vim:ts=4:sw=4:et
