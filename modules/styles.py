# -*- coding: utf-8 -*-
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkfont
# Set root in main.py
root: tk.Tk = None
# Init fonts
def init():
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