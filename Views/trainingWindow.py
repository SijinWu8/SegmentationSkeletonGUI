import tkinter as tk
from tkinter import ttk

from Views.Frames.StepFrame import StepFrame
from Views.Frames.TrainingFrame import TrainingFrame


class TrainingWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "Training"

        processFrame = StepFrame(self.win, self.view_manager, self.current_view)
        processFrame.place(x = 30, y = 50)

        trainingFrame = TrainingFrame(self.win)
        trainingFrame.place(x=200, y=50)