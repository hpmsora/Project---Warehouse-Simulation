###############################
#
# Simulation Canvas
#
# Won Yong Ha
#
#
###############################

import tkinter as tk

import Controller as ctr
import Order as od
import AGV as AGV
import Shelf as shf

import Tools as t

class SimulationBoard(tk.Frame):

    # Custom Variables
    num_aisles = 2
    num_rows = 5

    grid_width = 0
    grid_height = 0

    grid_active_width = 0
    grid_active_height = 0
    
    background_color = 'grey'
    square_size = 64

    # Internal Variables
    depot_area = []
    agv_depot_area = []
    shelves = {}
    AGVs = {}
    controller = None
    order_generator = None
    order_list = []
    new_order = None
    tools = None

    @property
    def canvas_size(self):
        return (self.num_aisles * self.square_size, self.num_rows * self.square_size)

    # Constructor
    def __init__(self, _parent, num_aisles=2, num_rows=5, square_size=64):
        self.parent = _parent
        self.num_aisles = num_aisles
        self.num_rows = num_rows
        self.square_size = square_size
        
    # Grid initialize with border cells function
    def GridInit(self):
        self.grid_width += 2
        self.grid_height += 2

        self.grid_active_width = self.grid_width
        self.grid_active_height = self.grid_height
        
        canvas_width = (self.grid_width) * self.square_size
        canvas_height = (self.grid_height) * self.square_size

        tk.Frame.__init__(self, self.parent)
        
        self.canvas = tk.Canvas(self,
                                width=canvas_width,
                                height=canvas_height,
                                background=self.background_color)
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)
        self.tools = t.Tools(self.canvas, self.square_size, self.grid_active_width, self.grid_active_height)

        # Borders
        for each_index_grid_height in range(0, self.grid_height):
            if each_index_grid_height == 0 or each_index_grid_height == self.grid_height-1:
                for each_index_grid_width in range(0, self.grid_width + 1):
                    tag = (self.tools.CellNaming(each_index_grid_width, each_index_grid_height), "border")
                    self.CellBuilding(tag,
                                      each_index_grid_width,
                                      each_index_grid_height,
                                      color='black')
            else:
                tag = (self.tools.CellNaming(0, each_index_grid_height), "border")
                self.CellBuilding(tag,
                                  0,
                                  each_index_grid_height,
                                  color='black')
                tag = (self.tools.CellNaming(self.grid_width-1, each_index_grid_width), "border")
                self.CellBuilding(tag,
                                  self.grid_width-1,
                                  each_index_grid_height,
                                  color='black')
        
    # Basic grid building with shelves function
    def GridBuilding(self, warehouse_type='basic'):
        if warehouse_type == 'basic':
            self.grid_width = 3*self.num_aisles
            self.grid_height = self.num_rows+2

            self.GridInit()
            
            list_aisles = range(1, self.grid_width-1)
            list_rows = range(1, self.grid_height-1)
            
            for each_index_rows in list_rows:
                for each_index_aisles in list_aisles:
                    if not(each_index_rows == 1 or each_index_rows == self.grid_height-2) and (each_index_aisles % 3 == 1 or each_index_aisles % 3 == 0):
                        shelf_position_name = self.tools.CellNaming(each_index_aisles, each_index_rows)
                        tag = (shelf_position_name, "shelf")
                        shelf_ID = self.CellBuilding(tag,
                                                     each_index_aisles,
                                                     each_index_rows,
                                                     color='gray')
                        self.shelves[shelf_ID] = shf.Shelf(shelf_ID,
                                                           (each_index_aisles, each_index_rows),
                                                           self.tools)
                        self.tools.SetShelvesDepots(shelf_position_name, shelf_ID)
                    else:
                        tag = (self.tools.CellNaming(each_index_aisles, each_index_rows), "road")
                        self.CellBuilding(tag,
                                          each_index_aisles,
                                          each_index_rows,
                                          color='white')

    # Cell building function for grid
    def CellBuilding(self, _tag, _posX, _posY, color=''):
        return self.canvas.create_rectangle(
            _posX*self.square_size, _posY*self.square_size,
            (_posX+1)*self.square_size, (_posY+1)*self.square_size,
            outline="black", fill=color, tag=_tag)
                        
    # Deposit area building function
    def DepotBuilding(self, depot_type='BottomCenter2', custom_depot=[]):
        if depot_type == 'LeftCorner':
            depot_ID = 1
            depot_pos = [(2, self.grid_active_height-2)]
            self.depot_area += depot_pos
            self.tools.SetDepots(depot_pos, depot_ID)
        if depot_type == 'BottomCenter':
            depot_ID = 2
            depot_pos = [(int(self.grid_width/2), self.grid_active_height-2)]
            self.depot_area += depot_pos
            self.tools.SetDepots(depot_pos, depot_ID)
        if depot_type == 'BottomCenter2':
            depot_ID = 3
            depot_pos = [(int(self.grid_width/2), self.grid_active_height-2),
                         (int(self.grid_width/2-1), self.grid_active_height-2)]
            self.depot_area += depot_pos
            self.tools.SetDepots(depot_pos, depot_ID)

        for each_depot in self.depot_area:
            name = self.tools.CellNaming(each_depot[0], each_depot[1])
            self.tools.ChangeColorObject(name, color='blue')
            self.tools.UpdateAbsWMap('Depot', each_depot)

    # AGV deposit are building function
    def AGVDepotBuilding(self, depot_type='TopCenter', custom_depot=[]):
        if depot_type == 'LeftCorner':
            self.agv_depot_area.append((0, self.grid_active_height-2))
        if depot_type == 'TopCenter':
            self.agv_depot_area.append((int(self.grid_width/2), 1))

        for each_agv_depot in self.agv_depot_area:
            name = self.tools.CellNaming(each_agv_depot[0], each_agv_depot[1])
            self.tools.ChangeColorObject(name, color='red')
            self.tools.UpdateAbsWMap('AGVDepot', each_agv_depot)

    # AGV building function
    def AGVBuilding(self, _tag, _posX, _posY, color=''):
        return self.canvas.create_oval(
            _posX*self.square_size, _posY*self.square_size,
            (_posX+1)*self.square_size, (_posY+1)*self.square_size,
            outline="black", fill=color, tag=_tag)


    # AGV building function
    def AddAGV(self, num=1):
        num_AGVs = len(self.AGVs)
        pos = self.agv_depot_area[0]
        init_posX, init_posY = pos
        for each_newAGV in range(0, num):
            newAGV_ID = self.AGVBuilding("AGV", init_posX,
                                         init_posY,
                                         color='yellow')
            self.AGVs[newAGV_ID] = AGV.AGV(newAGV_ID, pos, self.tools)
        return len(self.AGVs)

    # Set controller function
    def SetController(self, controller_type='Default'):
        self.controller = ctr.Controller(self.AGVs, self.shelves, self.tools)

    # Set order generator function
    def SetOrder(self, order_type='basic', order_per_batch=1, num_order=100):
        self.order_generator = od.Order(self.shelves,
                                        order_type=order_type,
                                        order_per_batch=order_per_batch,
                                        num_order=num_order,
                                        order_gap = 30)

    # Add order to list of order function
    def AddOrder(self, _order):
        self.order_list += self.order_generator.OrderGenerator()

    # Update
    def Update(self):
        if len(self.order_list) <= len(self.AGVs)*3:
            self.AddOrder(self.order_generator)

        self.new_order = self.order_list.pop(0)
        
        self.controller.Update(self.new_order)
        self.canvas.after(200, self.Update)
        
