import tkinter as tk
from tkinter import ttk

from Views.Frames.StepFrame import StepFrame
from Views.Frames.TestFrame import TestFrame


class TestWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "Test"

        processFrame = StepFrame(self.win, self.view_manager, self.current_view)
        processFrame.place(x = 30, y = 50)

        testFrame = TestFrame(self.win)
        testFrame.place(x=200, y=50)