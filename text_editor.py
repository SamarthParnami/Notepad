# -*- coding: utf-8 -*-
"""Text Editor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lGeeP2D6O246WtiJgGE2Gpl14HZ6ya7i
"""



from configparser import ConfigParser
config=ConfigParser()
config['window']={
    'title':'Notepad'
}

with open('literal.ini','w') as file:
  config.write(file)
  if(file):
    file.close()

from tkinter import *
from tkinter.filedialog import *
from configparser import ConfigParser
import re
labels=ConfigParser()
labels.read("literal.ini")

class Notepad:
  def __init__(self):
    self.changed=False
    self.file=None
    self.font="Consolas"
    self.main=Tk()
    self.elements()
    self.windowTitle()
    self.pack()
    if( not self.changed):
      self.textWindow.bind("<KeyPress>",self.textChanged)
    self.main.mainloop()

  def elements(self):
    self.setupMenuBar()
    self.scrollbarSetup()
    self.textWindowSetup()    
    self.scrollbarConfig()
    


from tkinter import *
import re
from configparser import ConfigParser
pref=ConfigParser()
gui=ConfigParser()
string=ConfigParser()

pref.read('pref.ini')
gui.read('gui.ini')
string.read('string.ini')


class Notepad:
  def __init__(self):
    self.file=None
    self.changed=False
    self.font=gui["main"]["font"]

    self.main=Tk()
    self.setupMenuBar()
    self.textWidget()
    self.setupTitleBar()
    self.addEvents()
    self.main.mainloop()

 
  #extracting file name from filepath
  def getFileName(self):
    filename=re.search("[^\\\\|////]*\.[\w]*$",self.file).group()
    print(filename)
    return filename
  #seting up title name of the window
  def setupTitleBar(self):
    self.textWindow.bind("<KeyPress>",self.changeSaveStatus)
    titleText=pref["file"]["changedIndicator"] if self.changed else ""
    print(titleText)
    titleText+=pref["file"]["defaultName"] if not self.file else self.getFileName()
    print(titleText)
    titleText+=" "+ gui["main"]["titleSuffix"]
    print(titleText)
    self.main.title(titleText)
    self.setWindowIcon()

  #adding icon to title bar 
  def setWindowIcon(self):
    icon=PhotoImage(file=gui["icon"]["name"])
    self.main.iconphoto(False,icon)

  def scrollBarWidget(self):
    self.scrollBarX=Scrollbar(self.main,orient=HORIZONTAL)
    self.scrollBarY=Scrollbar(self.main)
    self.scrollBarX.config(command=self.textWindow.xview)
    self.scrollBarY.config(command=self.textWindow.yview)
    if not self.textWindow.see("end"):
      self.scrollBarY.pack(side=RIGHT,fill=Y)

    if not self.textWindow.see("1.end"):
      self.scrollBarX.pack(side=BOTTOM,fill=X)

      
  def textWidget(self):
    
    self.textWindow=Text(self.main)   
    self.scrollBarWidget()
    #defining text window with  basic configurations like font, wrap, scroll functions
    font=gui["main"]["font"]
    print(font)
    self.textWindow.config(font=font,undo=True,wrap=NONE,yscrollcommand=self.scrollBarY.set,xscrollcommand=self.scrollBarX.set)
    self.textWindow.pack(expand=True,fill=BOTH)

    self.textWindow.bind("<KeyPress>",self.changeSaveStatus)
  def changeSaveStatus(self,event):
    print(event)
    if (event.char.isprintable() and len(event.keysym)==1) or (event.keysym=="Return"):
      self.changed=True
      self.setupTitleBar()
      self.textWindow.unbind("<KeyPress>")


  def setupMenuBar(self):

    #adding menubar to window
    
    self.menuBar=Menu(self.main,tearoff=2)
    self.main.config(menu=self.menuBar)

    #First Menu Item
    self.menuItem1=Menu(self.menuBar)
    self.menuBar.add_cascade(label="File",menu=self.menuItem1)
    self.menuItem1.add_command(label = 'New',accelerator="Ctrl+N", command = self.startFresh)
    self.menuItem1.add_command(label = 'New Window',accelerator="Ctrl+Shift+N", command = self.newWindow)
    self.menuItem1.add_command(label = 'Open',accelerator="Ctrl+O",command = self.openFile)
    self.menuItem1.add_command(label = 'Save',accelerator="Ctrl+S",command = self.saveFile)
    self.menuItem1.add_command(label = 'Save As',accelerator="Ctrl+Shift+S",command = self.saveFileAs)
    self.menuItem1.add_separator()
    self.menuItem1.add_command(label = 'Exit',command = self.exitNotepad)

    #Second Menu Item
    self.menuItem2=Menu(self.menuBar)
    self.menuBar.add_cascade(label="Edit",menu=self.menuItem2)
    self.menuItem2.add_command(label = 'Undo',accelerator="Ctrl+Z",command = self.undo)
    self.menuItem2.add_separator()
    self.menuItem2.add_command(label = 'Cut',accelerator="Ctrl+X", command = self.cut)
    self.menuItem2.add_command(label = 'Copy',accelerator="Ctrl+C", command = self.copy)    
    self.menuItem2.add_command(label = 'Paste',accelerator="Ctrl+V",command = self.paste)
    self.menuItem2.add_command(label = 'Delete',accelerator="Del",command = self.delete)
    self.menuItem2.add_separator()
    self.menuItem2.add_command(label = 'Find',command = self.find)
    self.menuItem2.add_command(label = 'Replace',command = self.replace)
    self.menuItem2.add_command(label = 'Goto',command = self.goto)

    #Third Menu Item
    self.menuItem3=Menu(self.menuBar)
    self.menuBar.add_cascade(label="Format",menu=self.menuItem3)
    self.menuItem3.add_command(label = 'Font', command = self.fontSelector)
    self.menuItem3.add_command(label = 'Zoom', command = self.zoom)
    

  
  # function call new button in file menu
  def startFresh(self):
    print('New')
    if self.changed:
      self.newFilePrompt()

  def newFilePrompt(self):
    option=""
    pop=Toplevel()
    pop.wm_title(gui["popup"]["title"])
    pop.resizable(FALSE,FALSE)
    label=Label(pop)
    if( not self.file):
      label.config(text=string["popup"]["question"]+" "+pref["file"]["defaultName"]+"?")
    else:
      label.config(text=string["popup"]["question"]+" "+f"{self.file}"+"?")
    label.pack()
    savebutton=Button(pop,text=string["popup"]["saveoption"],command=lambda:self.saveAndClear(pop))
    noSavebutton=Button(pop,text=string["popup"]["nosaveoption"],command=lambda :self.onlyClear(pop))
    cancelButton=Button(pop,text=string["popup"]["removePopup"],command=lambda:pop.destroy())
    
    savebutton.pack()
    noSavebutton.pack()
    cancelButton.pack()


  def saveAndClear(self,widget):
    self.saveFile()
    widget.destroy()
    self.textWindow.delete("1.0","end")
    self.file=None
    self.changed=False
    self.setupTitleBar()
  def onlyClear(self,widget):
    widget.destroy()
    self.textWindow.delete("1.0","end")
    self.file=None
    self.changed=False
    self.setupTitleBar()
  





  def newWindow(self):
    print('New Window')
    Notepad()




  def openFile(self):
    print('open')
    filepath=askopenfilename(filetypes=[("Text Document","*.txt"),("All Files","*.*")])
    print(filepath)
    if(filepath):
      self.file=filepath
      self.changed=False
      print(self.file)
      
      file=open(filepath,'r')
      text=file.read()
      file.close()
      self.textWindow.delete("1.0","end")
      self.textWindow.insert("1.0",text)
      self.textWindow.edit_modified(False)
      self.setupTitleBar()


  


  def saveFile(self,name=None):
    print('save') 
    if not self.file:
      self.saveFileAs(name)
    if(self.file):
      file=open(self.file,"w")
      text=self.textWindow.get("1.0","end")
      print(text)
      file.write(text)
      file.close()
      self.changed=False
      self.setupTitleBar()

  def saveFileAs(self,name=None):
    print('saveAs',name)
    file=asksaveasfilename(filetypes=[("Text Document","*.txt"),("All Files","*.*")],
                           defaultextension=[("Text Document","*.txt"),("All Files","*.*")],
                           initialfile=name if name else (self.getFileName() if self.file else pref["file"]["defaultName"]))
    if(file):
      self.file=file
      self.saveFile()



  def saveAndClose(self,pop):
    pop.destroy()
    self.saveFile(pref["file"]["defaultName"])
  def savePrompt(self, destroy=True):
    pop=Toplevel()
    pop.wm_title(gui["popup"]["title"])
    pop.resizable(FALSE,FALSE)
    label=Label(pop)
    if( not self.file):
      label.config(text=string["popup"]["question"]+" "+pref["file"]["defaultName"]+"?")
    else:
      label.config(text=string["popup"]["question"]+" "+f"{self.file}"+"?")
    label.pack()
    savebutton=Button(pop,text="Save",command=lambda:self.saveAndClose(pop))
    noSavebutton=Button(pop,text="Don't Save",command=lambda :(
        self.main.destroy() if destroy 
                        else 
                          pop.destroy()) )
    cancelButton=Button(pop,text="Cancel",command=lambda:pop.destroy())
    savebutton.pack()
    noSavebutton.pack()
    cancelButton.pack()
 
  def exitNotepad(self):
    if(self.changed):
      self.savePrompt()
    else:
      self.main.destroy()
    print("Exit")

  def undo(self):
    print('Undo')
    self.textWindow.edit_undo()
  
  def cut(self):
    print("cut")
    self.textWindow.focus_get().event_generate("<<Cut>>")

  def copy(self):
    print("copy")
    self.textWindow.focus_get().event_generate("<<Copy>>")

  def paste(self):
    print("paste")
    self.textWindow.focus_get().event_generate("<<Paste>>")
  
  def delete(self):
    print("delete")
    self.textWindow.focus_get().event_generate("<Delete>")
    # print(position)
  
  def find(self):
    print("find")
  
  def replace(self):
    print("replace")

  def goto(self):
    print("goto")

  def fontSelector(self):
    print("font")

  def zoom(self):
    print("zoom")

  def addEvents(self):
    self.main.bind("<Control-n>",lambda event: self.startFresh())
    self.main.bind("<Control-Shift-N>",lambda event: self.newWindow())
    self.textWindow.bind("<Control-o>",lambda event: self.openFile())
    self.textWindow.bind("<Control-s>",lambda event: self.saveFile())
    self.textWindow.bind("<Control-Shift-S>",lambda event: self.saveFileAs())
notepad=Notepad()