import tkinter as tk
from tkinter import ttk, Text

class TestFrame(ttk.Frame):

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
        Test_button = ttk.Button(
            self,
            text='Test',
            command=self.process
        )
        Test_button.grid(column=1, row=0, sticky='W', **options)

        self.text = Text(self, height=8, width= 50)
        self.text.grid(column=1, row=1, sticky='W', **options)

    def process(self):
        self.text.insert('1.0', 'Runing test.py ...')