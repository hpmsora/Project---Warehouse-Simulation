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

    num_aisles = 2
    num_rows = 5

    grid_width = 0
    grid_height = 0
    
    background_color = 'grey'
    square_size = 64

    depot_area = []
    agv_depot_area = []

    @property
    def canvas_size(self):
        return (self.num_aisles * self.square_size, self.num_rows * self.square_size)

    # Constructor
    def __init__(self, _parent, num_aisles=2, num_rows=5, square_size=64):
        self.parent = _parent
        self.num_aisles = num_aisles
        self.num_rows = num_rows
        self.square_size = square_size
        
    # Grid initialize function
    def GridInit(self):
        self.grid_width += 2
        self.grid_height += 2
        canvas_width = (self.grid_width) * self.square_size
        canvas_height = (self.grid_height) * self.square_size

        tk.Frame.__init__(self, self.parent)
        
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background=self.background_color)
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        for each_index_grid_height in range(0, self.grid_height):
            if each_index_grid_height == 0 or each_index_grid_height == self.grid_height-1:
                for each_index_grid_width in range(0, self.grid_width + 1):
                    tag = self.CellNaming(each_index_grid_width, each_index_grid_height)
                    self.CellBuilding(tag, each_index_grid_width, each_index_grid_height, color='black')
            else:
                tag = self.CellNaming(0, each_index_grid_height)
                self.CellBuilding(tag, 0, each_index_grid_height, color='black')
                tag = self.CellNaming(self.grid_width-1, each_index_grid_width)
                self.CellBuilding(tag, self.grid_width-1,  each_index_grid_height, color='black')
        
    # Basic grid building function
    def GridBuilding(self, warehouse_type='basic'):
        if warehouse_type == 'basic':
            self.grid_width = 3*self.num_aisles
            self.grid_height = self.num_rows+2

            self.GridInit()
            
            list_aisles = range(1, self.grid_width-1)
            list_rows = range(1, self.grid_height-1)
            
            for each_index_rows in list_rows:
                for each_index_aisles in list_aisles:
                    tag = self.CellNaming(each_index_aisles, each_index_rows)
                    if not(each_index_rows == 1 or each_index_rows == self.grid_height-2) and (each_index_aisles % 3 == 1 or each_index_aisles % 3 == 0):
                        self.CellBuilding(tag, each_index_aisles, each_index_rows, color='gray')
                    else:
                        self.CellBuilding(tag, each_index_aisles, each_index_rows, color='white')

    # Cell building function for grid
    def CellBuilding(self, _tag, _posX, _posY, color=''):
        item = self.canvas.create_rectangle(
            _posX*self.square_size, _posY*self.square_size,
            (_posX+1)*self.square_size, (_posY+1)*self.square_size,
            outline="black", fill=color, tag=(_tag))

    # Cell naming function
    def CellNaming(self, posX, posY):
        return str(posX) + ":" + str(posY)

    # Cell color change
    def CellColorChanging(self, posX, posY, color=''):
        pos = self.CellNaming(posX, posY)
        self.canvas.itemconfigure(pos, fill=color)
                        
    # Deposit area building function
    def DepotBuilding(self, depot_type='LeftCorner', custom_depot=[]):
        if depot_type == 'LeftCorner':
            self.depot_area.append((0, self.grid_height-1))
            self.depot_area.append((1, self.grid_height-1))

        for each_depot in self.depot_area:
            self.CellColorChanging(each_depot[0], each_depot[1], color='blue')

    # AGV deposit are building function
    def AGVDepotBuilding(self, depot_type='LeftCorner', custom_depot=[]):
        if depot_type == 'LeftCorner':
            self.agv_depot_area.append((0, self.grid_height-2))

        for each_agv_depot in self.agv_depot_area:
            self.CellColorChanging(each_agv_depot[0], each_agv_depot[1], color='red')
    
