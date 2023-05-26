# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
# Modal root
class TestInfo(tk.Frame):
    def __init__(self, cps, master=None, parent=None):
        super().__init__(master=master)
        self.configure(background='white')
        self.pack() # Pack frame
        # Init variables
        self.cps = cps
        # Create widgets
        self.createWidgets()
        self.master.transient(parent)
        self.grab_set()

    def createWidgets(self):
        # Create content
        self.lblCPS = tk.Label(
            self,
            text=self.cps,
            font=tkfont.Font(
                family='Arial',
                size=20,
                weight='bold',
                slant='roman'
            ),
            foreground='#0b0b13'
        )
        self.btnOK = ttk.Button(self, text='Ок', command=self.master.destroy)
        # Grid
        self.lblCPS.grid(row=0, column=0)
        self.btnOK.grid(row=1, column=0)