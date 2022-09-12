import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import os
import re
import tifffile
import numpy as np

import matplotlib.pyplot as plt

class ThresholdsWindow:
    def __init__(self, win, selectFolderFrame):
        self.win = win
        self.selectFolderFrame = selectFolderFrame
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

        rawDataPath = self.selectFolderFrame.getRawDataPath()

        raw_list = os.listdir(rawDataPath)
        sort_tmp = [int(re.sub("[^0-9]", "", s)) for s in raw_list]
        raw_list = [x for _, x in sorted(zip(sort_tmp, raw_list))]

        n_timepoints = len(raw_list)

        # Get shape information:
        dummy = 0
        try:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        except:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        (nZ, nX, nY) = dummy.shape

        raw = np.zeros((n_timepoints, nZ, nX, nY))

        for time_index in range(n_timepoints):
            raw_name = os.path.join(rawDataPath, raw_list[time_index])

            raw_ = 0
            try:
                raw_ = tifffile.imread(raw_name)
            except:
                raw_ = tifffile.imread(raw_name)

            raw[time_index] = raw_

        img = ImageTk.PhotoImage(master=self.win, image=Image.fromarray(raw[0, 4]*256))

        canvas = Canvas(self.win, width=400, height=400)
        canvas.pack()
        canvas.create_image(20, 20, anchor="nw", image=img)

        self.win.mainloop()