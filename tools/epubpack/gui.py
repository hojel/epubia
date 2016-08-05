# -*- coding: utf-8 -*-
# epubcheck GUI
import wx
import os

__program__ = 'epubpack'

class FileDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        self.obj.SetInsertionPointEnd()
        # main body
        for filename in filenames:
            if os.path.exists(filename) and os.path.isfile(filename) and filename.endswith(".epub"):
            	import zipfile
            	epubdir = os.path.splitext(filename)[0]
            	zipf = zipfile.ZipFile(filename, 'r')
            	zipf.extractall(epubdir)
                self.obj.AppendText(u"Extracted to %s\n" %epubdir)
            elif os.path.exists(filename) and os.path.isdir(filename) and os.path.exists( os.path.join(filename, "mimetype") ):
                from epubpack import epubpack
                epubfile = filename+".epub"
                epubpack(filename, epubfile)
                self.obj.AppendText(u"INFO: Archived to %s\n" %epubfile)
            else:
                self.obj.AppendText("FAIL: Wrong file or directory\n")

#--------------------------------------------------
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        panel = wx.Panel(self, wx.ID_ANY)

        # top button bar
        tlb1 = wx.StaticText(panel, label="Drop directory below")
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
