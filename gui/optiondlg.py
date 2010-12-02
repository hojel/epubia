# -*- coding: utf-8 -*-
# Option Dialog
import wx
import os

#--------------------------------------------------
class MyOption(wx.Dialog):
    """ Option Dialog """
    def __init__(self, parent, title, config):
        wx.Dialog.__init__(self, parent, title=title)

        self.config = config
        sizer = wx.BoxSizer( wx.VERTICAL )
        mvs = wx.BoxSizer( wx.VERTICAL )

        # Target CSS
        box1_title = wx.StaticBox(self, wx.ID_ANY, u"CSS 선택")
        box1  = wx.StaticBoxSizer(box1_title, wx.VERTICAL)
        grid1 = wx.FlexGridSizer(0, 2, 0, 0)

        tgtlabel = wx.StaticText(self, wx.ID_ANY, u"출력장치")
        targetList = []
        import glob
        for css in glob.glob("target/*.css"):
            targetList.append( os.path.splitext(os.path.basename(css))[0] )
        if not self.config['TargetCSS'] in targetList:
            self.config['TargetCSS'] = targetList[0]

        cb1 = wx.Choice(self, choices=targetList)
        cb1.SetStringSelection(self.config['TargetCSS'])
        self.Bind(wx.EVT_CHOICE, self.OnTargetSelect, cb1)
        grid1.Add( tgtlabel, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );
        grid1.Add( cb1, 0, wx.ALIGN_CENTRE|wx.LEFT, 5 );

        box1.Add( grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        mvs.Add( box1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        # Scraper Selection
        box2_title = wx.StaticBox(self, wx.ID_ANY, "Scraper / Key")
        box2  = wx.StaticBoxSizer(box2_title, wx.VERTICAL)
        grid2 = wx.FlexGridSizer(0, 2, 0, 0)

        self.scrap_ctrls = []
        radio1 = wx.RadioButton( self, wx.ID_ANY, "Daum", style=wx.RB_GROUP )
        radio2 = wx.RadioButton( self, wx.ID_ANY, "Naver" )
        text1  = wx.TextCtrl( self, wx.ID_ANY, self.config['DaumAPIKey'] )
        text2  = wx.TextCtrl( self, wx.ID_ANY, self.config['NaverAPIKey'] )
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

    def OnTargetSelect(self, evt):
        self.config['TargetCSS'] = evt.GetString()

    def OnScraperSelect(self, evt):
        radio_selected = evt.GetEventObject()
        for radio, text in self.scrap_ctrls:
            if radio == radio_selected:
                text.Enable(True)
                srvname = radio.GetLabel()
                self.config['Scraper'] = srvname
                self.config['%sAPIKey' % srvname] = text.GetLabel()
            else:
                text.Enable(False)
# vim:ts=4:sw=4:et
