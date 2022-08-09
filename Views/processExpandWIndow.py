import tkinter as tk
from tkinter import ttk

from Views.Frames.ProcessExpandFrame import ProcessExpandFrame
from Views.Frames.StepFrame import StepFrame


class ProcessExpandWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "ProcessExpand"

        stepFrame = StepFrame(self.win, self.view_manager, self.current_view)
        stepFrame.place(x = 30, y = 50)

        processExpandFrame = ProcessExpandFrame(self.win)
        processExpandFrame.place(x=200, y=50)