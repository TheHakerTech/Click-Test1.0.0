# -*- coding: utf-8 -*-
from __future__ import annotations
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import time

from modules.cpsResult import *
# Modal root
class TestInfo(tk.Frame):
    def __init__(self, testResult: Result, master=None, parent=None):
        super().__init__(master=master)
        self.configure(background='white')
        self.pack() # Pack frame
        # Init variables
        self.testResult = testResult
        # Create widgets
        self.createWidgets()
        # Start animation
        self.lblCPSAnimation()
        self.master.transient(parent)
        self.grab_set()

    def createWidgets(self):
        # Create content
        self.lblCPS = tk.Label(
            self,
            text='0',
            font=tkfont.Font(
                family='Arial',
                size=20,
                weight='bold',
                slant='roman'
            ),
            foreground='#0ed145',
            background='white'
        )
        self.lblMiddleCPS = tk.Label(
            self,
            text='Твой средний КПС',
            font=tkfont.Font(
                family='Arial',
                size=14,
                weight='normal',
                slant='roman'
            ),
            foreground='#0b0b13',
            background='white'
        )
        self.btnOK = ttk.Button(self, text='Ок', command=self.master.destroy)
        # Grid
        self.lblCPS.grid(row=0, column=0)
        self.lblMiddleCPS.grid(row=1, column=0)
        self.btnOK.grid(row=2, column=0)
        # Set focus
        self.btnOK.focus()


    def lblCPSAnimation(self):
        for i in range(1, self.testResult.cps+1):
           time.sleep(0.1)
           self.lblCPS['text'] = str(float(i))