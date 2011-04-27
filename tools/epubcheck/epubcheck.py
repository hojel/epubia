# -*- coding: utf-8 -*-
# epubcheck GUI
import wx
import os
import threading
import subprocess

__program__ = 'epubcheck'

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        self.obj.SetInsertionPointEnd()
        # create thread
        thread = threading.Thread(target=self.RunCheckMulti, args=(filenames,))
        thread.setDaemon(True)
        thread.start()

    def RunCheckMulti(self, filenames):
        for filename in filenames:
            self.RunCheck(filename)

    def RunCheck(self, filename):
        # ext call
        cmd = ['java', '-jar', 'epubcheck-1.0.5.jar', filename.encode('euc-kr')]
        info = None
        if os.name == 'nt':
            info = subprocess.STARTUPINFO()
            info.dwFlags = 1
            info.wShowWindow = 0
        proc = subprocess.Popen(cmd, startupinfo=info,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            wx.CallAfter(self.OnText, line)

    def OnText(self, text):
        self.obj.AppendText(text)

#--------------------------------------------------
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        panel = wx.Panel(self, wx.ID_ANY)

        # top button bar
        tlb1 = wx.StaticText(panel, label="Drop ePub file below")
        self.log = wx.TextCtrl(panel, size=(600,300),
                        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        # set Drop zone
        self.log.SetDropTarget( FileDropTarget(self.log) )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tlb1, 0, wx.GROW|wx.CENTER|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(self.log, 1, wx.GROW|wx.ALL, 5)

        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.Show(True)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, __program__)
    app.MainLoop()
# vim:ts=4:sw=4:et
