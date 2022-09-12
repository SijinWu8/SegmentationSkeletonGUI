import tkinter as tk
from tkinter import ttk


class ThresholdsWindow:
    def __init__(self, win):
        self.win = win
        self.highLight = ttk.Style()
        self.highLight.configure("H.TLabel", background="#ccc")

        self.lowLight = ttk.Style()
        self.lowLight.configure("L.TLabel")

        self.completed = ttk.Style()
        self.completed.configure("C.TLabel", background="white")

        self.__create_widgets()

    def __create_widgets(self):
        window_width = 600
        window_height = 400

        # get the screen dimension
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.win.title('SegmentationSkeletonGUI')
        self.win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.win.mainloop()