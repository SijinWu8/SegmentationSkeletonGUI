# from tkinter import ttk
from Views.Frames.PreprocessFrame import PreprocessFrame
from Views.Frames.StepFrame import StepFrame


class PreprocessWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "Preprocess"

        processFrame = StepFrame(self.win, self.view_manager, self.current_view)
        processFrame.place(x = 30, y = 50)

        preprocessFrame = PreprocessFrame(self.win)
        preprocessFrame.place(x=200, y=50)