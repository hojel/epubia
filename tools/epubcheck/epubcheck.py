# -*- coding: utf-8 -*-
# epubcheck GUI
import wx
import os
import threading
import subprocess

__program__ = 'epubcheck'

#--------------------------------------------------
class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        panel = wx.Panel(self, wx.ID_ANY)

        # top button bar
        tlb1 = wx.StaticText(panel, label="File")
        self.filebox = wx.TextCtrl(panel)
        btn1 = wx.Button(panel, wx.ID_ANY, "Select")
        self.Bind(wx.EVT_BUTTON, self.OnSelectFile, btn1)

        btn2 = wx.Button(panel, wx.ID_ANY, "Check")
        self.Bind(wx.EVT_BUTTON, self.OnCheck, btn2)

        btnszer = wx.BoxSizer(wx.HORIZONTAL)
        btnszer.Add(tlb1, 0, wx.GROW|wx.CENTER|wx.LEFT, 5)
        btnszer.Add(self.filebox, 1, wx.GROW|wx.CENTER|wx.LEFT, 5)
        btnszer.Add(btn1, 0, wx.GROW|wx.CENTER|wx.LEFT, 5)
        btnszer.Add(btn2, 0, wx.GROW|wx.CENTER|wx.RIGHT, 5)

        # log
        self.log = wx.TextCtrl(panel, size=(600,300),
                        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btnszer, 0, wx.GROW|wx.CENTER|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(self.log, 1, wx.GROW|wx.ALL, 5)

        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.Show(True)

    def OnSelectFile(self, evt):
        dlg = wx.FileDialog(self, "Choose file", ".", "", "*.epub", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            fname  = dlg.GetFilename()
            self.epubpath = os.path.join(dirname, fname)
            self.filebox.SetValue( self.epubpath )
        dlg.Destroy()

    def OnText(self, text):
        self.log.AppendText(text)

    def OnCheck(self, evt):
        # create thread
        thread = threading.Thread(target=self.RunCheck, args=(self.filebox.GetValue(),))
        thread.setDaemon(True)
        thread.start()

    def RunCheck(self, file):
        # ext call
        cmd = ['java', '-jar', 'epubcheck-1.0.5.jar', file.encode('euc-kr')]
        info = None
        if os.name == 'nt':
            info = subprocess.STARTUPINFO()
            info.dwFlags = 1
            info.wShowWindow = 0
        proc = subprocess.Popen(cmd, startupinfo=info,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            wx.CallAfter(self.OnText, line)

#--------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, __program__)
    app.MainLoop()
# vim:ts=4:sw=4:et
