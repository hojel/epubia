# -*- coding: utf-8 -*-
# File Table in Main Window
import wx
import wx.grid as gridlib

class MyDataTable(gridlib.PyGridTableBase):
    def __init__(self):
        gridlib.PyGridTableBase.__init__(self)

        self.colLabels = [u"선택", u"파일이름", u"제목", u"저자", "ISBN"]

        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
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
# vim:ts=4:sw=4:et
