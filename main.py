# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import threading
import rich.console
import modules.settings
import time

from modules.cpsResult import *
from modules.secondlyRoot import *

# Constants
ENT_WIDTH = 0
BTN_WIDTH = 0
# Root (need firstly!)
root = tk.Tk()
# Console object
console = rich.console.Console()
# Init fonts
class Fonts:
    menuFont = tkfont.Font(
        family='Times New Roman Greek',
        size='13',
        weight='normal',
        slant='roman'
    )
    lblFont = tkfont.Font(
        family='Arial',
        size='13',
        weight='normal',
        slant='roman'
    )
    headerFont = tkfont.Font(
        family='Arial',
        size=20,
        weight='bold',
        slant='roman'
    )
    littleFont = tkfont.Font(
        family='Arial',
        size=10,
        weight='normal',
        slant='roman'
    )
    btnFont = tkfont.Font(
        family='Arial',
        size=16,
        weight='normal',
        slant='roman'
    )
# Init colors
class Colors:
    # Colors
    EerieBlack = '#1e1e1e'
    EerieBlackDark = '#111111'
    White = 'white'
    Green = '#0ed145'
    Black = '#0b0b13'
    Blue = '#5db9e1'
    Red = '#ec1c24'
# Init styles
class Styles:
    # Init style for all appication
    style = ttk.Style(root) # Style
    # Styles names
    mainFrame   = "mainFrame.TFrame"
    label       = "label.TLabel"
    header      = "header.TLabel"
    labelBlack  = "labelBlack.TLabel"
    headerBlack = "headerBlack.TLabel"
    clickPole   = "clickPole.TFrame"
    startLbl    = "startLbl.TLabel"
    footer      = "footer.TFrame"
    footerLbl   = "foolerLbl.TLabel"
    underMenu   = "underMenu.TFrame"
    littleText  = "littleText.TLabel"
    btnReset    = "btnReset.TButton"
    btnRecords  = "btnRecords.TButton"
    # Configure styles
    style.configure(
        mainFrame,
        background=Colors.White
    )
    style.configure(
        label,
        font=Fonts.lblFont,
        foreground=Colors.Black,
        background=Colors.White
    )
    style.configure(
        header,
        font=Fonts.headerFont,
        foreground=Colors.Black,
        background=Colors.White
    )
    style.configure(
        labelBlack,
        font=Fonts.lblFont,
        foreground=Colors.White,
        background=Colors.EerieBlack
    )
    style.configure(
        headerBlack,
        font=Fonts.headerFont,
        foreground=Colors.White,
        background=Colors.EerieBlack
    )
    style.configure(
        clickPole,
        foreground=Colors.White,
        background=Colors.Green,
        border=tk.RAISED,
        borderwidth=10
    )
    style.configure(
        startLbl,
        font=Fonts.headerFont,
        foreground=Colors.White,
        background=Colors.Green
    )
    style.configure(
        footer,
        foreground=Colors.White,
        background=Colors.EerieBlack
    )
    style.configure(
        underMenu,
        background=Colors.EerieBlack,
        foreground=Colors.White
    )
    style.configure(
        littleText,
        font=Fonts.littleFont,
        background=Colors.White,
        foreground=Colors.Black
    )
    style.configure(
        btnReset,
        font=Fonts.btnFont,
        background=Colors.Red,
        foreground=Colors.White,
        highlightcolor=Colors.Red,
        highlightthickness=0,
        borderwidth=0
    )
    style.configure(
        btnRecords,
        font=Fonts.btnFont,
        background=Colors.Blue,
        foreground=Colors.White,
        highlightcolor=Colors.Blue,
        highlightthickness=0,
        borderwidth=0
    )


# Init settings
"""Settings = {
    'resizable':(False, False), # Can resize root (<x>, <y>)
    'rootWidth':730,
    'rootHeight':500,
    'iconPath':'images/icon.ico',
    'title':'CPS Test (click test)', # Title
    'times':['1', '2', '5', '10', '15', '30', '60', '100', '1000'],
    'poleWidth':30
}"""
Settings = modules.settings.loadSettings()
# Global funcitions
class Functions:
    @staticmethod
    def debug(string: str):
        console.print(f'[blue]DEBUG[/]: {string}')
    
    @staticmethod
    def openTimeMenu(evt):
        menu = ttk.Frame(evt.widget)
        lbl = ttk.Label(menu, text='test')
        lbl.pack()
        menu.place(x=evt.x, y=evt.y)

# Application class
class CPSApplication(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.settingsInitialization() # Init settings
        self.pack() # Pack in root
        self.variablesInitilization() # Create variables for widgets
        self.menuInititalization() # Create menu
        self.timedClickTestInitialization() # Create widgets

    def settingsInitialization(self):
        self.master.title(Settings['title']) # Title
        self.master.resizable(*Settings['resizable']) # Can resize root (<x>, <y>)
        self.master.iconbitmap(Settings['iconPath'])

    def timedClickTestInitialization(self):
        # Retitle
        self.master.title(f'{Settings["title"]} {self.totalTime.get()+" секунд" if self.totalTime.get() != "1" else self.totalTime.get()+" секунда"}')
        # Main frame
        self.frmMain = ttk.Frame(self, style=Styles.mainFrame)
        self.frmMain.pack()
        # Create under menu frame
        self.frmUnderMenu = ttk.Frame(
            self.frmMain,
            width=Settings['rootWidth']+3,
            height=70,
            style=Styles.underMenu
        )
        self.frmUnderMenu.grid(row=0, column=0, sticky='w', columnspan=2)
        # Create frame with description
        self.frmTextContent = ttk.Frame(self.frmMain, style=Styles.mainFrame, width=Settings['rootWidth'])
        self.frmTextContent.grid(row=1, column=0, columnspan=2)
        # Texts
        self.lblClickTest = ttk.Label(
            self.frmTextContent,
            text='Клик тест '+(f'{self.totalTime.get()} секунд' if self.totalTime.get() != '1' else f'{self.totalTime.get()} секунда'),
            style=Styles.header
        )
        self.lblTextContent = ttk.Label(
            self.frmTextContent,
            text='Сколько кликов вы сможете сделать за '+(f'{self.totalTime.get()} секунд' if self.totalTime.get() != '1' else f'{self.totalTime.get()} секунду')+'? Нажмите на кнопку "Старт" и кликайте!',
            style=Styles.label
        )
        # Grid
        self.lblClickTest.grid(row=0, column=0, ipady=10, ipadx=10, sticky='w')
        self.lblTextContent.grid(row=1, column=0, ipady=10, ipadx=10, sticky='w')
        # Click pole
        self.frmClickPole = ttk.Frame(
            self.frmMain,
            width=Settings['rootWidth'],
            height=Settings['rootHeight']/4,
            style=Styles.clickPole
        )
        self.frmClickPole.bind('<Button>', self.startTime)
        self.frmClickPole.grid(row=2, column=0, sticky='w', pady=13, padx=30)
        # Create click info
        self.frmClicksInfo = ttk.Frame(
            self.frmMain,
            height=Settings['rootHeight']/4,
            style=Styles.mainFrame
        )
        
        self.frmClicksInfo.grid(row=2, column=1, sticky='w')
        # Create var clicks
        self.lblClicksCount = ttk.Label(
            self.frmClicksInfo,
            textvariable=self.varClicks,
            style=Styles.header
        )
        # Create cps var
        self.lblCPS = ttk.Label(
            self.frmClicksInfo,
            text='0',
            style=Styles.header
        )
        # Create label
        self.lblStart = ttk.Label(self.frmClickPole, text='Старт!', style=Styles.startLbl)
        self.lblStart.bind('<Button>', self.startTime)
        self.lblStart.pack(padx=170, pady=70)
        # Under titles
        self.lblClicks = ttk.Label(self.frmClicksInfo, text='Кликов сделано', style=Styles.littleText)
        self.lblCPSText = ttk.Label(self.frmClicksInfo, text='КПС', style=Styles.littleText)

        self._time = ttk.Label(self.frmClicksInfo, text=f'Времени осталось: {self.totalTime.get()}', style=Styles.littleText)
        # Grid
        self.lblClicksCount.grid(row=0, column=0, sticky='nw', padx=(10, 90))
        self.lblCPS.grid(row=0, column=1, sticky='ne', padx=(50, 30))

        self.lblClicks.grid(row=1, column=0, sticky='nw', pady=(10, 0), padx=(0, 50))
        self.lblCPSText.grid(row=1, column=1, sticky='nw', pady=(10, 0), padx=(40, 0))
        self._time.grid(row=2, column=0, columnspan=2, pady=(0, 50))
        # Create buttons
        self.btnReset = ttk.Button(
            self.frmClicksInfo,
            width=8,
            text='Сброс',
            command=self.reset,
            style=Styles.btnReset
        )
        self.btnRecords = ttk.Button(
            self.frmClicksInfo,
            width=7,
            text='Рекорды',
            style=Styles.btnRecords
        )
        # Grid
        self.btnReset.grid(row=3, column=0, sticky='w', pady=(0, 20))
        self.btnRecords.grid(row=3, column=1, sticky='w', pady=(0, 20))
        # Create "footer" 
        self.frmFooter = ttk.Frame(self.frmMain, style=Styles.footer)
        self.frmFooter.grid(row=3, column=0, sticky='w', columnspan=2)
        # Create copyright lbl
        self.lblCopyright = ttk.Label(self.frmFooter, text='Eternal Arts | All rights received', style=Styles.headerBlack)
        self.lblCopyright.grid(row=0, column=0, padx=(Settings['rootWidth']-Fonts.headerFont.measure('Eternal Arts | All rights received'))//2, pady=(100, 10))

    def timedClickTestReinitialization(self):
        # Destroy main frame
        self.frmMain.destroy()
        # Recreate main frame
        self.timedClickTestInitialization()

    def menuInititalization(self):
        # Create main menu and bind it to master
        self.mainMenu = tk.Menu(
            self,
            background=Colors.EerieBlack,
            foreground=Colors.White,
            activebackground=Colors.White,
            activeforeground=Colors.EerieBlack,
            borderwidth=0,
            font=Fonts.lblFont,
            selectcolor=Colors.White,
            relief=tk.FLAT
        )
        self.master['menu'] = self.mainMenu
        # Create and add under menu
        self.timeMenu = tk.Menu(
            self.mainMenu,
            background=Colors.EerieBlack,
            foreground=Colors.White,
            activebackground=Colors.White,
            activeforeground=Colors.EerieBlack,
            font=Fonts.menuFont,
            relief=tk.FLAT,
            borderwidth=0,
            selectcolor=Colors.White,
            tearoff=False
        )
        # Add options to ander menu
        for strTime in Settings['times']:
            self.timeMenu.add_radiobutton(
                label=f'{strTime} секунд' if strTime != '1' else f'{strTime} секунда',
                variable=self.totalTime,
                value=strTime,
                command=self.timedClickTestReinitialization
            )
        self.mainMenu.add_cascade(label='Время', menu=self.timeMenu)

    def variablesInitilization(self):
        self.totalTime = tk.StringVar(value='1')
        self.varClicks = tk.IntVar(value=0)

    def clickPlus(self, evt):
        self.varClicks.set(self.varClicks.get() + 1)

    def startTime(self, evt):
        evt.widget.bind('<Button>', self.clickPlus)
        self.lblStart.bind('<Button>', self.clickPlus)
        self.timer = threading.Timer(int(self.totalTime.get()), self.endTime)
        self.timer.start()

    def endTime(self):
        self.frmClickPole.unbind('<Button>')
        self.lblStart.unbind('<Button>')
        self.testResult = Result(self.varClicks.get(), int(self.totalTime.get()))
        self.lblCPS['text'] = self.testResult.cps
        TestInfo(self.testResult.cps, master=tk.Toplevel(), parent=self)

    def reset(self):
        self.varClicks.set(0)
        self.lblCPS['text'] = 0
        self.frmClickPole.bind('<Button>', self.startTime)
        self.lblStart.bind('<Button>', self.startTime)

# Launch function
def start():
    app = CPSApplication(master=root)
    root.mainloop()

# Launch programm
if __name__ == '__main__':
    start()