# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
import tkinter.messagebox as message
import tkinter.ttk as ttk
import tkinter.font as tkfont
import threading
import rich.console
import modules.settings
import time
import sqlite3
import re

from modules.setupdb import setup
from modules.cpsResult import *
from modules.secondlyRoot import *

# Constants
TRW_COLUMNS = ('Секунды', 'Клики', 'КПС', 'Дата')
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
        size=16,
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
# Init re patterns
class Patterns:
    isNumber = re.compile(r"""^[0-9]+$""")

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
    trwStyle    = "trwStyle.Treeview"
    lblCPS      = "lblCPS.TLabel"
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
    style.configure(
        trwStyle,
        font=Fonts.lblFont,
    )
    style.configure(
        lblCPS,
        font=Fonts.headerFont,
        foreground=Colors.Green,
        background=Colors.White
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

    @staticmethod
    def getMiddleCPS():
        # Connect to data base and get info
        con = sqlite3.connect(Settings['dbPath'])
        cur = con.cursor()
        # Execute
        cur.execute('SELECT cps FROM results')
        # Get response
        response = cur.fetchall()
        # Close
        cur.close()
        con.close()
        response = [_tuple[0] for _tuple in response]
        if sum(response) != 0:
            return round(sum(response)/len(response), 2)
        else:
            return 0
        
    @staticmethod
    def getMaxCPS():
        # Connect to data base and get info
        con = sqlite3.connect(Settings['dbPath'])
        cur = con.cursor()
        # Execute
        cur.execute('SELECT cps FROM results')
        # Get response
        response = cur.fetchall()
        # Close
        cur.close()
        con.close()
        response = [_tuple[0] for _tuple in response]
        if sum(response) != 0:
            return max(response)
        else:
            return 0

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
        # Setup data base
        setup()
        self.master.title(Settings['title']) # Title
        self.master.resizable(*Settings['resizable']) # Can resize root (<x>, <y>)
        self.master.iconbitmap(Settings['iconPath']) # Set icon
        # Set style
        Styles.style.theme_use(Settings['style'])

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
            command=self.recordsInititalization,
            style=Styles.btnRecords
        )
        # Grid
        self.btnReset.grid(row=3, column=0, sticky='w', pady=(0, 20))
        self.btnRecords.grid(row=3, column=1, sticky='w', pady=(0, 20))
        # Create "footer" 
        self.frmFooter = ttk.Frame(self.frmMain, style=Styles.footer)
        self.frmFooter.grid(row=4, column=0, sticky='w', columnspan=2)
        # Create copyright lbl
        self.lblCopyright = ttk.Label(self.frmFooter, text='Eternal Arts | All rights reserved', style=Styles.headerBlack)
        self.lblCopyright.grid(row=0, column=0, padx=(Settings['rootWidth']-Fonts.headerFont.measure('Eternal Arts | All rights received'))//2, pady=(100, 10))
        # Create trw
        self.treeViewInitialization()
        # Stop old timer (if exists)
        self.stopped = True
        self.reset()

    def recordsInititalization(self):
        self.frmMain.destroy()
        # Retitle
        self.master.title(f'{Settings["title"]} рекорды')
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
        # Create header
        self.header = ttk.Label(self.frmMain, text='Ваши результаты', font=Fonts.headerFont, style=Styles.label)
        self.header.grid(row=1, column=0, sticky="w", pady=10, padx=(10, 0))
        # Create tree
        self.treeViewInitialization()
        # Create label middle CPS
        self.lblMiddleCPS = ttk.Label(self.frmMain, text=f'Ваш средний КПС за всё время', font=Fonts.headerFont, style=Styles.label)
        self.lblMiddleCPS.grid(row=4, column=0, sticky="w", pady=10, padx=(10, 0))
        self.middleCPSAllTime = Functions.getMiddleCPS()
        # Create middle CPS
        self.middleCPS = ttk.Label(self.frmMain, text=self.middleCPSAllTime, font=Fonts.headerFont, style=Styles.lblCPS)
        self.middleCPS.grid(row=5, column=0, sticky="w", pady=10, padx=(10, 0))
        # Create label max CPS
        self.lblMaxCPS = ttk.Label(self.frmMain, text=f'Ваш максимальный КПС за всё время', font=Fonts.headerFont, style=Styles.label)
        self.lblMaxCPS.grid(row=6, column=0, sticky="w", pady=10, padx=(10, 0))
        self.maxCPSAllTime = Functions.getMaxCPS()
        # Create middle CPS
        self.maxCPS = ttk.Label(self.frmMain, text=self.maxCPSAllTime, font=Fonts.headerFont, style=Styles.lblCPS)
        self.maxCPS.grid(row=7, column=0, sticky="w", pady=10, padx=(10, 0))
        # Create button reset
        self.btnResetDB = ttk.Button(
            self.frmMain,
            text='Сбросить базу данных',
            style=Styles.btnReset,
            command=self.resetDB
        ) 
        self.btnResetDB.grid(row=8, column=0, sticky='w', padx=(10, 0), pady=(10, 10))
        # Create "footer" 
        self.frmFooter = ttk.Frame(self.frmMain, style=Styles.footer)
        self.frmFooter.grid(row=9, column=0, sticky='w', columnspan=2)
        # Create copyright lbl
        self.lblCopyright = ttk.Label(self.frmFooter, text='Eternal Arts | All rights received', style=Styles.headerBlack)
        self.lblCopyright.grid(row=0, column=0, padx=(Settings['rootWidth']-Fonts.headerFont.measure('Eternal Arts | All rights received'))//2, pady=(100, 10))

    def treeViewReinitialization(self):
        self.frmTrw.destroy() # Destroy old trw
        # Create new
        self.treeViewInitialization()
    
    def treeViewInitialization(self, trwRow=3):
        # Create trw frame
        self.frmTrw = ttk.Frame(self.frmMain, style=Styles.mainFrame)
        self.frmTrw.grid(row=trwRow, column=0, columnspan=2)
        self.trwResults = ttk.Treeview(
            self.frmTrw,
            columns=TRW_COLUMNS,
            displaycolumns=(0, 1, 2, 3),
            show="headings",
            selectmode="none",
            style=Styles.trwStyle
        )
        # Connect and get data from data base
        con = sqlite3.connect(Settings['dbPath'])
        cur = con.cursor()
        # Get it
        cur.execute("SELECT * FROM results")
        for result in cur.fetchall():
            self.trwResults.insert("", "end", None, values=result)
        cur.close()
        con.close()
        for columnName in TRW_COLUMNS:
            self.trwResults.heading(columnName, text=columnName, anchor='w')
            self.trwResults.column(columnName, width=(Settings['rootWidth']-40)//4)
        # Grid
        self.trwResults.grid(row=0, column=0, pady=(0, 17))
        # Add scroll bar
        self.trwScroll = ttk.Scrollbar(self.frmTrw, orient=tk.VERTICAL, command=self.trwResults.yview)
        self.trwScroll.grid(row=0, column=1, sticky="ns")
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure(0, weight=1)


    def timedClickTestReinitialization(self):
        # Destroy main frame
        self.frmMain.destroy()
        # Recreate main frame
        self.timedClickTestInitialization()

    def personalClickTestInitialization(self):
        # Stop old timer (if exists)
        self.stopped = True
        self.reset()
        # Retitle
        self.master.title(f'{Settings["title"]} cвой режим')
        # Destroy olf frame
        self.frmMain.destroy()
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

        # Create frame with settings

        self.frmSettings = ttk.Frame(self.frmMain, style=Styles.mainFrame, width=Settings['rootWidth'])
        self.frmSettings.grid(row=1, column=0, columnspan=2, sticky="w", padx=(10, 0))
        # Texts
        self.lblSettingsTitle = ttk.Label(
            self.frmSettings,
            text='Настройки',
            style=Styles.header
        )
        # Time variable frame
        self.frmTime = ttk.Frame(self.frmSettings)
        # Pack
        self.frmTime.grid(row=1, column=0, sticky='w', padx=(10, 0))
        # Time label
        self.lblPersonalTime = ttk.Label(self.frmTime, text='Время', style=Styles.label)
        # Time variable
        self.entPersonalTime = ttk.Entry(self.frmTime, width=3, textvariable=self.totalTime)
        # Grid
        self.lblSettingsTitle.grid(row=0, column=0, ipady=10, ipadx=10, sticky='w')
        self.lblPersonalTime.grid(row=0, column=0, sticky='w')
        self.entPersonalTime.grid(row=0, column=1, sticky='w')

        # Create frame with description

        self.frmTextContent = ttk.Frame(self.frmMain, style=Styles.mainFrame, width=Settings['rootWidth'])
        self.frmTextContent.grid(row=2, column=0, columnspan=2, sticky='w', padx=(10, 0))
        # Texts
        self.lblClickTest = ttk.Label(
            self.frmTextContent,
            text='Свой режим',
            style=Styles.header
        )
        self.lblTextContent = ttk.Label(
            self.frmTextContent,
            text='Настройте клик тест как хотите!',
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
        self.frmClickPole.grid(row=3, column=0, sticky='w', pady=13, padx=30)
        # Create click info
        self.frmClicksInfo = ttk.Frame(
            self.frmMain,
            height=Settings['rootHeight']/4,
            style=Styles.mainFrame
        )
        
        self.frmClicksInfo.grid(row=3, column=1, sticky='w')
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
            command=self.recordsInititalization,
            style=Styles.btnRecords
        )
        # Grid
        self.btnReset.grid(row=3, column=0, sticky='w', pady=(0, 20))
        self.btnRecords.grid(row=3, column=1, sticky='w', pady=(0, 20))
        # Create "footer" 
        self.frmFooter = ttk.Frame(self.frmMain, style=Styles.footer)
        self.frmFooter.grid(row=5, column=0, sticky='w', columnspan=2)
        # Create copyright lbl
        self.lblCopyright = ttk.Label(self.frmFooter, text='Eternal Arts | All rights reserved', style=Styles.headerBlack)
        self.lblCopyright.grid(row=0, column=0, padx=(Settings['rootWidth']-Fonts.headerFont.measure('Eternal Arts | All rights reserved'))//2, pady=(100, 10))
        # Create trw
        self.treeViewInitialization(trwRow=4)
        self._time['text'] = f'Времени осталось: {self.totalTime.get()}'

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
        self.timeMenu.add_command(label='Свой режим', command=self.personalClickTestInitialization)
        self.mainMenu.add_cascade(label='Время', menu=self.timeMenu)
        # Create records menu
        self.recordsMenu = tk.Menu(
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
        self.recordsMenu.add_command(label='Рекорды', command=self.recordsInititalization)
        self.mainMenu.add_cascade(label='Рекорды', menu=self.recordsMenu)

    def variablesInitilization(self):
        self.totalTime = tk.StringVar(value='1')
        self.varClicks = tk.IntVar(value=0)
        self.stopped = False

    def clickPlus(self, evt):
        self.varClicks.set(self.varClicks.get() + 1)

    def startTime(self, evt):
        if Patterns.isNumber.search(self.totalTime.get()):
            self.stopped = False
            evt.widget.bind('<Button>', self.clickPlus)
            self.lblStart.bind('<Button>', self.clickPlus)
            # Plus 1 click
            self.varClicks.set(1)
            # Create thread for updating total seconds
            self.clickingTimer = threading.Thread(target=self.timer)
            # Run it
            self.clickingTimer.start()
            # Change color
            Styles.style.configure(Styles.clickPole, background=Colors.White)
            Styles.style.configure(Styles.startLbl, background=Colors.White, foreground=Colors.Green)

    def endTime(self):
        self.frmClickPole.unbind('<Button>')
        self.lblStart.unbind('<Button>')
        self.testResult = Result(self.varClicks.get(), float(self.totalTime.get()))
        self.lblCPS['text'] = self.testResult.cps
        TestInfo(self.testResult, master=tk.Toplevel(), parent=self)
        resultValues = {
            "seconds":self.testResult.time,
            "clicks":self.testResult.clicks,
            "cps":self.testResult.cps,
            "date":time.strftime("%d.%m.%Y %H:%M:%S")
        }
        # Create new result in db
        con = sqlite3.connect(Settings['dbPath'])
        cur = con.cursor()
        # Create
        cur.execute(
            "INSERT INTO results VALUES (:seconds, :clicks, :cps, :date)", resultValues)
        con.commit()
        cur.execute("SELECT * FROM results")
        # Close it
        cur.close()
        con.close() 
        self.trwResults.insert("", 'end', None, values=list(resultValues.values()))

    def timer(self):
        timeToEnd = int(self.totalTime.get())
        for i in range(int(self.totalTime.get()) * 10):
            if not self.stopped:
                time.sleep(0.1)
                self._time['text'] = f'Времени осталось: {round(timeToEnd, 2)}'
                timeToEnd -= 0.1
            else:
                self._time['text'] = f'Времени осталось: 0'
                break
        else:
            self._time['text'] = f'Времени осталось: 0'
            self.endTime()

    def reset(self):
        self.stopped = True
        self.varClicks.set(0)
        self.lblCPS['text'] = 0
        self.frmClickPole.bind('<Button>', self.startTime)
        self.lblStart.bind('<Button>', self.startTime)
        # Change color
        Styles.style.configure(Styles.clickPole, background=Colors.Green)
        Styles.style.configure(Styles.startLbl, background=Colors.Green, foreground=Colors.White)

    def resetDB(self):
        if message.askokcancel('Удаление результатов', 'Вы хотите удалить результаты?'):
            # Delete table
            con = sqlite3.connect(Settings['dbPath'])
            cur = con.cursor()
            cur.execute("DROP TABLE results")
            cur.close()
            con.close()
            # Invoke setup metod
            setup()
            # Reinit trw
            self.recordsInititalization()
            # Show message done
            message.showinfo('Удаление результатов', 'База данных сброшена', default=message.OK)


# Launch function
def start():
    app = CPSApplication(master=root)
    root.mainloop()

# Launch programm
if __name__ == '__main__':
    start()