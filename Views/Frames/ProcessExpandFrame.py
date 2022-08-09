import tkinter as tk
from tkinter import ttk, Text

from Views.Frames.MainTextFrame import MainTextFrame


class ProcessExpandFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        # convert button
        processExpand_button = ttk.Button(
            self,
            text='Process_Expand',
            command=self.process
        )
        processExpand_button.grid(column=1, row=0, sticky='W', **options)

        # self.text = Text(self, height=8)
        # self.text.grid(column=1, row=1, sticky='W', **options)

        self.textFrame = MainTextFrame(self)
        self.textFrame.grid(column=0, row=2, sticky='W', **options)

    def process(self):
        self.textFrame.insert('Runing processExpand.py ...')