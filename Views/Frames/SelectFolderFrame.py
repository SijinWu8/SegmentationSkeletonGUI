import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
import os


class SelectFolderFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.rawDataPath = ""

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        path = tk.StringVar()
        self.path_entry = ttk.Entry(self, textvariable=path, width=30)
        self.path_entry.grid(column=1, row=0, **options)
        self.path_entry.focus()

        # convert button
        open_button = ttk.Button(
            self,
            text='Select folder',
            command=self.select_folder
        )
        open_button.grid(column=2, row=0, sticky='W', **options)

    def select_folder(self):
        path = askdirectory(title='Select Folder')
        self.rawDataPath = path
        self.set_text(path)

        return


    def set_text(self,path):
        self.path_entry.delete(0, 0)
        self.path_entry.insert(0, path)
        return

    def getRawDataPath(self):
        return self.rawDataPath