# -*- coding: utf-8 -*-
# Main Window
import wx
from wx.lib.wordwrap import wordwrap
import wx.grid as gridlib
import os

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
        self.tmpldir = "template"
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
        self.grid.SetDropTarget( FileDropTarget(self) );

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
                self.loadFile(fname)
        dlg.Destroy()

    def loadFile(self, fname):
        import txtformat
        from ftxt2markdown import extract_meta
        newrow = self.grid.table.GetNumberRows()
        self.scrap.append({'file':fname,'dir':self.dirname})
        # add new row
        self.grid.table.SetValue( newrow, 0, True )
        self.grid.table.SetValue( newrow, 1, fname )
        # try to fetch directive inside
        text = txtformat.load( os.path.join(self.dirname,fname) )
        info = extract_meta(text)
        if 'title' in info:
            self.grid.table.SetValue( newrow, 2, info['title'] )
        if 'author' in info:
            self.grid.table.SetValue( newrow, 3, info['author'] )
        if 'isbn' in info:
            self.grid.table.SetValue( newrow, 4, info['isbn'] )
        if 'cover_url' in info:
            self.grid.table.SetValue( newrow, 5, info['cover_url'] )
        self.scrap[newrow]['info'] = info

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
        maxcnt = cnt
        dlg = wx.ProgressDialog(u"Book Scrapping",
                                u"책정보 가져오기",
                                maximum = maxcnt,
                                parent = self,
                                style = wx.PD_CAN_ABORT
                                      | wx.PD_AUTO_HIDE
                                      | wx.PD_APP_MODAL
                                )
        # scrapping
        cnt = 0
        keepGoing = True
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                fname  = self.grid.table.GetValue(row, 1)
                fname = os.path.splitext(os.path.split(fname)[1])[0]
                title  = self.grid.table.GetValue(row, 2)
                isbn   = self.grid.table.GetValue(row, 4)
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
                    srch = fname
                    rslt = self.scraper.search( srch.encode('utf-8') )
                    if rslt:
                        info = rslt[0]
                if info is None:
                    info = self.scraper.default_value
                # copy result
                if self.scrap[row]['info'] is None:
                    self.scrap[row]['info'] = dict()
                for key,val in info.items():
                    if not self.config['PreserveUserMeta'] or not key in self.scrap[row]['info']:
                        self.scrap[row]['info'][key] = val
                # display
                self.grid.table.SetValue(row, 2, self.scrap[row]['info']['title'])
                self.grid.table.SetValue(row, 3, self.scrap[row]['info']['author'])
                self.grid.table.SetValue(row, 4, self.scrap[row]['info']['isbn'])
                self.grid.table.SetValue(row, 5, self.scrap[row]['info']['cover_url'])
                cnt += 1
        if keepGoing:
            dlg.Update(cnt, u"완료")
        else:
            dlg.Update(maxcnt, u"취소")

    def runConvert(self, evt):
        import txtformat
        from ftxt2markdown import insert_meta
        # get total count to do
        cnt = 0
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                cnt += 1
        if cnt == 0:
            return
        maxcnt = cnt
        dlg = wx.ProgressDialog(u"Book Conversion",
                                u"ePub 변환",
                                maximum = maxcnt,
                                parent = self,
                                style = wx.PD_CAN_ABORT
                                      | wx.PD_APP_MODAL
                                )
        # scrapping
        cnt = 0
        keepGoing = True
        for row in range(self.grid.table.GetNumberRows()):
            if self.grid.table.GetValue(row, 0):        # selected
                # load
                txtfile = os.path.join( self.scrap[row]['dir'], self.scrap[row]['file'] )
                text = txtformat.load(txtfile)
                if self.config['ReformatText']:
                    correct_word_break = self.config['CorrectWordBreak']
                    if not correct_word_break:
                        correct_word_break = None
                    text = txtformat.clean(text, correct_word_break=correct_word_break)
                info = self.scrap[row]['info']
                info['title']  = self.grid.table.GetValue(row, 2)
                if not info['title']: del info['title']
                info['author'] = self.grid.table.GetValue(row, 3)
                if not info['author']: del info['author']
                info['isbn']   = self.grid.table.GetValue(row, 4)
                if not info['isbn']: del info['isbn']
                info['cover_url'] = self.grid.table.GetValue(row, 5)
                if not info['cover_url']: del info['cover_url']
                info['language'] = 'Korean'
                atxt = insert_meta(text, info)

                dlgtit = u'<미지정>'
                if 'title' in info:
                    dlgtit = info['title']
                (keepGoing, skip) = dlg.Update(cnt, u"%s 변환중" % dlgtit)
                if not keepGoing: break

                # output
                if self.config['UseTitleInOutputName']:
                    filebase = info['title']
                else:
                    filebase = os.path.splitext( os.path.basename(txtfile) )[0]
                if self.config['UseDestDir']:
                    out_nex = os.path.join(self.config['DestDir'], filebase)
                else:
                    out_nex = os.path.join(os.path.dirname(txtfile), filebase)
                # generate
                if self.config['OutputEPub']:
                    from markdown2epub import markdown2epub
                    epubfile = out_nex+'.epub'
                    markdown2epub(atxt, epubfile,
                                target_css = self.targetcss,
                                template_dir = self.tmpldir,
                                src_dir = os.path.dirname(txtfile),
                                fontfile=self.config['FontFile'],
                                tocLevel=self.config['MaxBrowseLevel'],
                                skipTo1st = self.config['SkipToFirstChapter'] )
                    print u"%s is generated" % epubfile
                if self.config['OutputMarkdown']:
                    open(out_nex+'.txt', 'w').write( atxt.encode('utf-8-sig') )
                if self.config['OutputPDF']:
                    from markdown2pdf import markdown2pdf
                    pdffile = out_nex+'.pdf'
                    markdown2pdf(atxt, pdffile,
                                cssfile='xhtml2pdf.css',
                                fontfile=self.config['FontFile'],
                                src_dir = os.path.dirname(txtfile),
                                skipTo1st = self.config['SkipToFirstChapter'] )
                    print u"%s is generated" % pdffile
                cnt += 1
        if keepGoing:
            dlg.Update(cnt, u"변환완료: %d개" % cnt)
        else:
            dlg.Update(maxcnt, u"변환취소: %d개" % cnt)

    def OnOption(self, evt):
        dlg = MyOption(self.panel, u"설정", self.config)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            dlg.UpdateConfig(self.config)
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
            u"읽어오기, 책정보가져오기, 변환 순서로 누르면 ePub파일이 만들어 집니다.\n"
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
            import scraper.naver_scraper
            self.scraper = scraper.naver_scraper.book_scraper()
            self.scraper.key = self.config['NaverAPIKey']
        else:
            import scraper.daum_scraper
            self.scraper = scraper.daum_scraper.book_scraper()
            self.scraper.key = self.config['DaumAPIKey']

#--------------------------------------------------
class MyDataTable(gridlib.PyGridTableBase):
    def __init__(self):
        gridlib.PyGridTableBase.__init__(self)

        self.colLabels = [u"선택", u"파일이름", u"제목", u"저자", "ISBN", u"이미지"]

        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_STRING,
                          ]

        # array of heterogeneous array
        self.data = []

    # required methods
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.colLabels)
    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
            try:
                return self.data[row][col]
            except IndexError:
                return ''

    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
                newline = 0
            except IndexError:
                # add new
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)
                newline = 1
            # notify grid
            msg = gridlib.GridTableMessage(self,
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,
                        newline       # how many
                        )
            self.GetView().ProcessTableMessage(msg)
        innerSetValue(row, col, value)

    # optional methods
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False
    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

    # my own methods
    def DeleteRow(self, row):
        self.data.pop(row)
        msg = gridlib.GridTableMessage(self,
                    gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED,
                    row, 1)
        self.GetView().ProcessTableMessage(msg)

class MyGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, wx.ID_ANY)
        self.table = MyDataTable()
        self.SetTable(self.table, True)

        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(False)

        self.SetColSize(0, 5)       # selection
        self.SetColSize(1, 200)     # file
        self.SetColSize(2, 200)     # title
        self.SetColSize(3, 100)     # author
        self.SetColSize(4, 100)     # isbn
        self.SetColSize(5, 100)     # cover_url

        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnCellClick)
        gridlib.EVT_GRID_LABEL_LEFT_CLICK(self, self.OnLabelClick)

    def OnCellClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def OnLabelClick(self, evt):
        c = evt.GetCol()
        if c == 0:      # select
            num_row = self.table.GetNumberRows()
            cnt = 0
            for i in range(num_row):
                if self.table.data[i][c]:
                    cnt += 1
            if cnt == num_row:
                forceval = False
            else:
                forceval = True
            for i in range(num_row):
                self.table.data[i][c] = forceval
            # refresh
            if num_row:
                self.table.SetValue(0, c, forceval)
        else:
            # sort in column
            pass    # not yet

#--------------------------------------------------
class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        for fname in filenames:
            self.obj.loadFile(fname)

#--------------------------------------------------
class MyOption(wx.Dialog):
    """ Option Dialog """
    def __init__(self, parent, title, config):
        wx.Dialog.__init__(self, parent, title=title)

        sizer = wx.BoxSizer( wx.VERTICAL )
        mvs = wx.BoxSizer( wx.VERTICAL )

        # Target CSS
        box1_title = wx.StaticBox(self, wx.ID_ANY, u"출력장치")
        box1  = wx.StaticBoxSizer(box1_title, wx.VERTICAL)
        grid11 = wx.FlexGridSizer(0, 2, 0, 0)
        grid12 = wx.FlexGridSizer(0, 2, 0, 0)

        tgtlabel = wx.StaticText(self, wx.ID_ANY, u"장치설정")
        targetList = []
        import glob
        for css in glob.glob("target/*.css"):
            targetList.append( os.path.splitext(os.path.basename(css))[0] )
        if not config['TargetCSS'] in targetList:
            config['TargetCSS'] = targetList[0]

        cb1 = wx.Choice(self, choices=targetList)
        cb1.SetStringSelection(config['TargetCSS'])
        grid11.Add( tgtlabel, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        grid11.Add( cb1, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        self.css_cb = cb1;

        tgtlabel = wx.StaticText(self, wx.ID_ANY, u"글꼴")
        targetList = []
        import glob
        for font in glob.glob("fonts/*.[ot]tf"):
            targetList.append( os.path.basename(font) )
        if not config['FontFile'] in targetList:
            config['FontFile'] = targetList[0]

        cb1 = wx.Choice(self, choices=targetList)
        cb1.SetStringSelection(config['FontFile'])
        grid12.Add( tgtlabel, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        grid12.Add( cb1, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        self.font_cb = cb1;

        box1.Add( grid11, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        box1.Add( grid12, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        mvs.Add( box1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        # Scraper Selection
        box2_title = wx.StaticBox(self, wx.ID_ANY, "Scraper / Key")
        box2  = wx.StaticBoxSizer(box2_title, wx.VERTICAL)
        grid2 = wx.FlexGridSizer(0, 2, 0, 0)

        self.scrap_ctrls = []
        radio1 = wx.RadioButton( self, wx.ID_ANY, "Daum", style=wx.RB_GROUP )
        radio2 = wx.RadioButton( self, wx.ID_ANY, "Naver" )
        text1  = wx.TextCtrl( self, wx.ID_ANY, config['DaumAPIKey'] )
        text2  = wx.TextCtrl( self, wx.ID_ANY, config['NaverAPIKey'] )
        self.scrap_ctrls.append( (radio1, text1) )
        self.scrap_ctrls.append( (radio2, text2) )

        for radio, text in self.scrap_ctrls:
            if radio.GetLabel() == config['Scraper']:
                radio.SetValue(True)
            else:
                radio.SetValue(False)

        for radio, text in self.scrap_ctrls:
            grid2.Add( radio, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            grid2.Add( text, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        box2.Add( grid2, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        mvs.Add( box2, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        sizer.Add(mvs, 0, wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 5)

        # Extra Control
        box3_title = wx.StaticBox(self, wx.ID_ANY, u"기타")
        box3  = wx.StaticBoxSizer(box3_title, wx.VERTICAL)
        grid31 = wx.FlexGridSizer(0, 2, 0, 0)

        label1 =  wx.StaticText(self, wx.ID_ANY, u"단어분리 교정")
        self.wordbreak_cb = wx.Choice(self, choices=['Disabled', 'Pattern', 'Naver Autospacing'])
        self.wordbreak_cb.SetStringSelection(({'':'Disabled', 'pattern':'Pattern', 'naver_autospacing':'Naver Autospacing'})[config['CorrectWordBreak']])
        grid31.Add( label1, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        grid31.Add( self.wordbreak_cb, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );

        box3.Add( grid31, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        sizer.Add(box3, 0, wx.ALIGN_CENTER, 5)

        # Output Format
        outfmt_list = [ 'ePub', 'Markdown Text', 'PDF' ]
        self.outfmt_lb = wx.CheckListBox(self, wx.ID_ANY, choices=outfmt_list, name=u"출력")
        setval = []
        if config['OutputEPub']:
            setval.append( 0 )
        if config['OutputMarkdown']:
            setval.append( 1 )
        if config['OutputPDF']:
            setval.append( 2 )
        self.outfmt_lb.SetChecked( setval )

        sizer.Add(self.outfmt_lb, 0, wx.ALIGN_CENTER, 5)

        # Ok & Cancel Button
        btnsizer = wx.StdDialogButtonSizer()
        # Ok button
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton( btn )
        # Cancel button
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton( btn )
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALL, 5)

        self.SetSizer( sizer )
        sizer.Fit( self )

        # default selection
        for radio, text in self.scrap_ctrls:
            self.Bind( wx.EVT_RADIOBUTTON, self.OnScraperSelect, radio )

    def OnScraperSelect(self, evt):
        radio_selected = evt.GetEventObject()
        for radio, text in self.scrap_ctrls:
            if radio == radio_selected:
                text.Enable(True)
            else:
                text.Enable(False)

    def UpdateConfig(self, config):
        #
        config['TargetCSS'] = self.css_cb.GetStringSelection()
        config['FontFile'] = self.font_cb.GetStringSelection()
        #
        for radio, text in self.scrap_ctrls:
            srvname = radio.GetLabel()
            config['%sAPIKey' % srvname] = text.GetLabel()
            if radio.GetValue():
                config['Scraper'] = srvname
        #
        sel = self.wordbreak_cb.GetCurrentSelection()
        config['CorrectWordBreak'] = (['', 'pattern', 'naver_autospacing'])[sel]
        #
        config['OutputEPub'] = False
        config['OutputPDF'] = False
        config['OutputMarkdown'] = False
        for str in self.outfmt_lb.GetCheckedStrings():
            if str.lower() == 'epub':
                config['OutputEPub'] = True
            elif str.lower().startswith('markdown'):
                config['OutputMarkdown'] = True
            elif str.lower() == 'pdf':
                config['OutputPDF'] = True
            else:
                print >> sys.stderr, "ERROR: Internal error on output format"

#--------------------------------------------------
def gui(config):
    app = wx.App(False)
    frame = MyFrame(None, __program__, config)
    app.MainLoop()
# vim:ts=4:sw=4:et
