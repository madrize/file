# textctrl version
# text editor

import wx
import os
import re
"""
to do
------
- exceptions
- about menu ++
- review the code, fix errors
"""
class cMenu(wx.Menu):
    """ Context Menu """
    def __init__(self,parent):
        
        wx.Menu.__init__(self)
        
        self.parent = parent
        
        itemMin = wx.MenuItem(self,wx.NewId(),"Minimize")
        self.AppendItem(itemMin)
        self.Bind(wx.EVT_MENU, self.onMin, itemMin)
        
        itemClose = wx.MenuItem(self,wx.NewId(),"Close")
        self.AppendItem(itemClose)
        self.Bind(wx.EVT_MENU, self.onClose, itemClose )
        
    def onMin(self,e):
        self.parent.Iconize()
    
    def onClose(self,e):
        self.parent.Close()
        

class wxTextEditor(wx.Frame):
    
    def __init__(self,parent):
        
        wx.Frame.__init__(self,parent,title="wx Text Editor",size=(700,570))
        
        # control
        self.cont = wx.Notebook(self)
        """
        p = wx.TextCtrl(self.cont,style=wx.TE_MULTILINE)
        self.cont.AddPage(p,"Page")
        """
        self.statusbar = self.CreateStatusBar()
        # create the toolbar
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        
        # add tools and bind the events
        newicon = wx.ArtProvider.GetBitmap(wx.ART_NEW,wx.ART_TOOLBAR,(12,12))
        newTool = self.toolbar.AddSimpleTool(wx.ID_ANY, newicon, "New", "Opens a new tab")
        self.Bind(wx.EVT_MENU, self.newPage, newTool)
        
        clicon = wx.ArtProvider.GetBitmap(wx.ART_QUIT,wx.ART_TOOLBAR,(12,12))
        clTool = self.toolbar.AddSimpleTool(wx.ID_ANY, clicon, "Close", "Closes the current page")
        self.Bind(wx.EVT_MENU, self.closePage, clTool)
        
        saveicon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,wx.ART_TOOLBAR,(12,12))
        saveTool = self.toolbar.AddSimpleTool(wx.ID_ANY, saveicon, "Save", "Saves the currently open file")
        self.Bind(wx.EVT_MENU,self.OnSave,saveTool)
        
        openicon= wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,wx.ART_TOOLBAR,(16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY,openicon,"Open","Opens a new file")
        self.Bind(wx.EVT_MENU,self.OnOpen,openTool)

        self.toolbar.AddSeparator()

        undoicon= wx.ArtProvider.GetBitmap(wx.ART_UNDO,wx.ART_TOOLBAR,(16,16))
        undoTool = self.toolbar.AddSimpleTool(wx.ID_ANY,undoicon,"Undo","Undoes the last operation")
        self.Bind(wx.EVT_MENU,self.OnUndo,undoTool)
        
        redoicon= wx.ArtProvider.GetBitmap(wx.ART_REDO,wx.ART_TOOLBAR,(16,16))
        redoTool = self.toolbar.AddSimpleTool(wx.ID_ANY,redoicon,"Redo","Redoes the last undo")
        self.Bind(wx.EVT_MENU,self.OnRedo,redoTool)
        
        copyicon = wx.ArtProvider.GetBitmap(wx.ART_COPY,wx.ART_TOOLBAR,(16,16))
        copyTool = self.toolbar.AddSimpleTool(wx.ID_ANY,copyicon,"Copy","Copy the selected text")
        self.Bind(wx.EVT_MENU,self.OnCopy,copyTool)
        
        pasteicon = wx.ArtProvider.GetBitmap(wx.ART_PASTE,wx.ART_TOOLBAR,(16,16))
        pasteTool = self.toolbar.AddSimpleTool(wx.ID_ANY, pasteicon,"Paste","Paste")
        self.Bind(wx.EVT_MENU,self.OnPaste, pasteTool)
        
        cuticon = wx.ArtProvider.GetBitmap(wx.ART_CUT,wx.ART_TOOLBAR,(16,16))
        cutTool = self.toolbar.AddSimpleTool(wx.ID_ANY, cuticon,"Cut","Cut")
        self.Bind(wx.EVT_MENU,self.OnCut, cutTool)
        
        # activate !
        self.toolbar.Realize()
        
        # create menu's
        filemenu = wx.Menu()
        editmenu = wx.Menu()
        viewmenu = wx.Menu()
        aboutmenu = wx.Menu()
        
        # new Id's
        selectId = wx.NewId()
        saveasId = wx.NewId()
        
        # add items to file menu
        menuNew=filemenu.Append(wx.ID_NEW,"New\tCtrl+N","New page")
        menuOpen=filemenu.Append(wx.ID_OPEN,"Open","Opens a new file")
        self.menuSave=filemenu.Append(wx.ID_SAVE,"Save\tCtrl+S","Saves the file")
        self.menuSave.Enable(False)
        self.menuSaveAs = filemenu.Append(saveasId,"Save As\tCtrl+Alt+S","Saves the file under a different name")
        self.menuSaveAs.Enable(False)
        filemenu.AppendSeparator()
        # construct recent files
        self.menuRecentFiles = wx.Menu()
        filemenu.AppendMenu(wx.ID_ANY,"Recent Files",self.menuRecentFiles)
        rf = open("recent_files.txt","r")
        self.recent_files = list(rf)
        rf.seek(0)
        rfall = [self.menuRecentFiles.Append(wx.ID_ANY,x) for x in rf]
        rf.close()
        filemenu.AppendSeparator()
        # filemenu complete
        menuClose=filemenu.Append(wx.NewId(),"Close","Close the program")
        
        # add items to edit menu
        menusearch = editmenu.Append(wx.ID_ANY,"Search\tCtrl+F","Search the page")
        menuUndo = editmenu.Append(wx.ID_UNDO,"Undo\tCtrl+Z","Undoes the last action")
        menuRedo = editmenu.Append(wx.ID_REDO,"Redo\tCtrl+Y","Redo")
        menuCut = editmenu.Append(wx.ID_CUT,"Cut\tCtrl+X","Cut")
        menuCopy = editmenu.Append(wx.ID_COPY,"Copy\tCtrl+C","Copy")
        menuPaste = editmenu.Append(wx.ID_PASTE,"Paste\tCtrl+V","Paste")
        editmenu.AppendSeparator()
        tabtospace = editmenu.Append(wx.ID_ANY,"Convert tabs to space","Converts tabs to spaces")

        # add items to about menu
        menuAbout = aboutmenu.Append(wx.ID_ANY,"About","About the application")
        
        # add to view menu
        self.showtb = viewmenu.Append(wx.ID_ANY,"Show Toolbar","Show Toolbar ?",kind=wx.ITEM_CHECK)
        viewmenu.Check(self.showtb.GetId(),True)
        self.showsb = viewmenu.Append(wx.ID_ANY,"Show Status Bar","Show Status Bar ?",kind=wx.ITEM_CHECK)
        viewmenu.Check(self.showsb.GetId(),True)
        
        # create menubar and add menu's
        menubar = wx.MenuBar()
        menubar.Append(filemenu,"File")
        menubar.Append(editmenu,"Edit")
        menubar.Append(viewmenu,"View")
        menubar.Append(aboutmenu,"About")
        self.SetMenuBar(menubar)
        
        # bind the events
        for x in range(0,len(rfall)):
            self.Bind(wx.EVT_MENU, self.OnRF, rfall[x])
        self.Bind(wx.EVT_MENU, self.OnSave, self.menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnClose, menuClose)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.tab2space, tabtospace)
        self.Bind(wx.EVT_MENU, self.selectAll, id=selectId)
        self.Bind(wx.EVT_MENU, self.newPage, menuNew)
        self.Bind(wx.EVT_MENU, self.search, menusearch)
        self.Bind(wx.EVT_MENU, self.toggleToolbar, self.showtb)
        self.Bind(wx.EVT_MENU, self.toggleStatusbar, self.showsb)
        self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
        self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
        self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)
        self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
        # context menu
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        
        # accel table
        accel = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('A'), selectId),
                                     (wx.ACCEL_CTRL|wx.ACCEL_ALT, ord('S'), saveasId)])
        self.SetAcceleratorTable(accel)
        
        self.dirname = ''
        p = wx.TextCtrl(self.cont,style=wx.TE_MULTILINE)
        self.cont.AddPage(p,"Page")
    
    def OnOpen(self,event):
        dbox = wx.FileDialog(self,"Choose a file to open",self.dirname,"","*.*",wx.OPEN)
        if dbox.ShowModal() == wx.ID_OK:
            self.filename = dbox.GetFilename()
            self.dirname  = dbox.GetDirectory()
            ofile = open(os.path.join(self.dirname, self.filename),"r")
            cp = self.cont.GetCurrentPage()
            if cp is None:
                p = wx.TextCtrl(self.cont,style=wx.TE_MULTILINE)
                self.cont.AddPage(p,"Page")
                p.SetValue(ofile.read())
            else:
                cp.SetValue(ofile.read())
            ofile.close()
        dbox.Destroy()
        # add to recent files
        self.recent_files.append(os.path.join(self.dirname, self.filename))
        # enable save and save as
        self.menuSaveAs.Enable(True)
        self.menuSave.Enable(True)

    def OnClose(self,event):
        # update the recent files.txt
        recfiles = open("recent_files.txt","w")
        for item in self.recent_files[-10:]:
            recfiles.write(item)
        recfiles.close()
        # dialog
        exitmsg = "Are you sure you want to exit ?"
        ebox = wx.MessageDialog(self,exitmsg,"Exit ?",style=wx.OK|wx.CANCEL)
        result = ebox.ShowModal()
        ebox.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        elif result == wx.CANCEL:
            pass

    def OnSaveAs(self,event):
        dbox = wx.FileDialog(self,"Choose a directory...",self.dirname,self.filename,"*.*",wx.SAVE)
        if dbox.ShowModal() == wx.ID_OK:
            self.dirname = dbox.GetDirectory()
            self.filename = dbox.GetFilename()
            content = self.cont.GetCurrentPage().GetValue()
            ofile = open(os.path.join(self.dirname, self.filename),"w")
            ofile.write(content)
            ofile.close()
        dbox.Destroy()

    def OnSave(self,event):
        dbox = wx.FileDialog(self,"Choose a directory",self.dirname,"","*.*",wx.SAVE|wx.OVERWRITE_PROMPT)
        if dbox.ShowModal() == wx.ID_OK:
            self.dirname = dbox.GetDirectory()
            self.filename = dbox.GetFilename()
            content = self.cont.GetCurrentPage().GetValue()
            ofile = open(os.path.join(self.dirname, self.filename),"w")
            ofile.write(content)
            ofile.close()
        dbox.Destroy()
    
    # converts tab to space
    def tab2space(self,event):
        txt = self.cont.GetCurrentPage().GetValue()
        new = txt.replace("\t","    ")
        self.cont.GetCurrentPage().SetValue(new)

    # activates ctrl+A
    def selectAll(self,event):
        self.cont.GetCurrentPage().SetSelection(-1,-1)

    def newPage(self,event):
        p = wx.TextCtrl(self.cont,style=wx.TE_MULTILINE)
        self.cont.AddPage(p,"Page")

    def OnUndo(self,event):
        self.cont.GetCurrentPage().Undo()

    def OnRedo(self,event):
        self.cont.GetCurrentPage().Redo()
    
    def OnPaste(self,event):
        self.cont.GetCurrentPage().Paste()
    
    def OnCopy(self,event):
        self.cont.GetCurrentPage().Copy()
    
    def OnCut(self,event):
        self.cont.GetCurrentPage().Cut()
    
    def closePage(self,event):
        self.cont.GetCurrentPage().Destroy()
    
    def search(self,event):
        page = self.cont.GetCurrentPage()
        mbox = wx.TextEntryDialog(self,"Enter the text","Search","")
        if mbox.ShowModal() == wx.ID_OK:
            word = mbox.GetValue()
        lst = [(w.start(),w.end()) for w in list(re.finditer(word,page.GetValue()))]
        for (f1,f2) in lst:
            page.SetSelection(f1,f2)
        mbox.Destroy()
    
    def toggleToolbar(self,event):
        if self.showtb.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()
    
    def toggleStatusbar(self,event):
        if self.showsb.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()
    
    def onRightDown(self,e):
        self.PopupMenu(cMenu(self))
    
    def OnRF(self,e):
        cnt = self.cont.GetCurrentPage()
        cf = open(self.menuRecentFiles.GetLabelText(e.GetId()),"r")
        cnt.SetValue(cf.read())
        cf.close()
    
    def OnAbout(self,e):
        desc = "This a simple Text Editor application written in Python using wxPython GUI."
        licence = "This application is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as \
                    published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version."
        info = wx.AboutDialogInfo()
        # info.SetIcon(wx.Icon('image.png', wx.BITMAP_TYPE_PNG))
        info.SetName('MadText')
        info.SetVersion('1.0')
        info.SetDescription(desc)
        info.SetCopyright('(C) 2012 Ugur Yoruk')
        info.SetWebSite('http://www.google.com')
        info.SetLicence(licence)
        info.AddDeveloper('Ugur Yoruk')
        info.AddDocWriter('Ugur Yoruk')
        info.AddArtist('Ugur Yoruk')
        info.AddTranslator('Ugur Yoruk')
        wx.AboutBox(info)



## Run the program
app = wx.App(False)
te = wxTextEditor(None)
te.Show()
app.MainLoop()
