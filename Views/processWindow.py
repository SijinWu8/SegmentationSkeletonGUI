import tkinter as tk
from tkinter import ttk

from Views.Frames.ProcessFrame import ProcessFrame
from Views.Frames.StepFrame import StepFrame


class ProcessWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "Process"

        stepFrame = StepFrame(self.win, self.view_manager, self.current_view)
        stepFrame.place(x = 30, y = 50)

