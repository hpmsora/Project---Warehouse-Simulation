###############################
#
# Simulation Canvas
#
# Won Yong Ha
#
#
###############################

import tkinter as tk

class SimulationBoard(tk.Frame):

    num_aisle = 2
    num_rows = 5
    
    background_color = 'grey'
    square_size = 64

    @property
    def canvas_size(self):
        return (self.num_aisle * self.square_size, self.num_rows * self.square_size)
    
    def __init__(self, _parent, num_aisle=2, num_rows=5, square_size=64):
        self.parent = _parent
        self.num_aisle = num_aisle
        self.num_rows = num_rows
        self.square_size = square_size

        canvas_width = self.num_aisle * self.square_size
        canvas_height = self.num_rows * self.square_size

        tk.Frame.__init__(self, _parent)
        
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background=self.background_color)
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
        
