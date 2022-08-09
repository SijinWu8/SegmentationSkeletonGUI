import tkinter as tk
from tkinter import ttk

class ExitWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "Exit"

        exit_button = ttk.Button(
            self.win,
            text='Exit',
            command=self.quit
        )

        exit_button.pack(
            ipadx=5,
            ipady=5,
            expand=True
        )

    def quit(self):
        exit()


