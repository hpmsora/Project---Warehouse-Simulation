###############################
#
# Simulation Canvas
#
# Won Yong Ha
#
# V.2.2 - Depot central even added
# V.2.1 - Collision detector
# V.2.0 - Basic simulation
# V.1.2 - Added multi AGVs
# V.1.1 - Added wide
# V.1.0 - General building
#
###############################

import tkinter as tk
import sys
import os

import Controller as ctr
import Order as od
import AGV as AGV
import Shelf as shf

import Tools as t
import Tools_Data as t_d
import SimulationGUI_GraphGUI as ggui

class SimulationBoard(tk.Frame):

    # Custom Variables
    warehouse_type = None
    depot_type = None
    
    num_aisles = None
    num_rows = None

    grid_width = 0
    grid_height = 0

    grid_active_width = 0
    grid_active_height = 0
    
    background_color = 'grey'
    square_size = None

    movement_speed = 50

    # Internal Variables
    parent = None
    canvas = None
    depot_area = []
    AGV_depot_area = []
    shelves = {}
    AGVs = {}
    controller = None
    order_generator = None
    order_list = []
    new_order = None

    graph_GUI = None
    tools = None
    tools_data = None
    re_run = None

    AGV_moving_without_shelf = None
    AGV_moving_with_shelf = None
    AGV_collision = None

    shelf_nothing = None
    shelf_waiting = None
    shelf_moving = None

    #@property
    #def canvas_size(self):
    #    return (self.num_aisles * self.square_size, self.num_rows * self.square_size)

    # Constructor
    def __init__(self,
                 _parent,
                 num_aisles=2,
                 num_rows=5,
                 square_size=64,
                 movement_speed=200):
        self.parent = _parent
        self.num_aisles = num_aisles
        self.num_rows = num_rows
        self.square_size = square_size
        self.movement_speed = movement_speed

        self.canvas  = None
        self.tools = None
        self.tools_data = None
        self.re_run = False
        self.graph_GUI = None

        self.AGV_moving_without_shelf = "yellow"
        self.AGV_moving_with_shelf = "green"
        self.AGV_collision = "red"

        self.shelf_nothing = "gray"
        self.shelf_waiting = "green"
        self.shelf_moving = "white"
        
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
        self.tools = t.Tools(self.parent,
                             self.canvas,
                             self.square_size,
                             self.grid_active_width,
                             self.grid_active_height,
                             reschedule_time_threshold = 50,
                             AGV_moving_without_shelf = self.AGV_moving_without_shelf,
                             AGV_moving_with_shelf = self.AGV_moving_with_shelf,
                             AGV_collision = self.AGV_collision,
                             shelf_nothing = self.shelf_nothing,
                             shelf_waiting = self.shelf_waiting,
                             shelf_moving = self.shelf_moving)
        
        self.tools_data = t_d.Tools_Data()

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
        self.warehouse_type = warehouse_type
        
        if self.warehouse_type == 'basic':
            self.grid_width = 3*self.num_aisles
            self.grid_height = self.num_rows+2

            self.GridInit()
            
            list_aisles = range(1, self.grid_width-1)
            list_rows = range(1, self.grid_height-1)
            
            for each_index_rows in list_rows:
                for each_index_aisles in list_aisles:
                    if not(each_index_rows == 1 or each_index_rows == self.grid_height-2) \
                       and (each_index_aisles % 3 == 1 or each_index_aisles % 3 == 0):
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
                        
        elif self.warehouse_type == 'basic_island_wide':
            print("[Map]\t\tBasic island wide map")
            road_width = 2
            island_height = 3
            upper_road_height = 3
            lower_road_height = 4
            
            self.grid_width = (road_width + 2)*self.num_aisles
            self.grid_height = self.num_rows+2

            self.GridInit()
            
            list_aisles = range(1, self.grid_width-1)                     # remove border index
            list_rows = range(1, self.grid_height-1)                      # remove border index
            list_upper_road = range(1, upper_road_height + 1)
            list_lower_road = range(self.grid_height -1 - lower_road_height, self.grid_height - 1)
            
            for each_index_rows in list_rows:
                for each_index_aisles in list_aisles:
                    if not (each_index_rows in list_upper_road or each_index_rows in list_lower_road) and \
                       (each_index_aisles % (road_width + 2) == 1 or each_index_aisles % (road_width + 2) == 0) and \
                       not (each_index_rows % (island_height + 1) == island_height):
                        shelf_position_name = self.tools.CellNaming(each_index_aisles, each_index_rows)
                        tag = (shelf_position_name, "shelf")
                        shelf_ID = self.CellBuilding(tag,
                                                     each_index_aisles,
                                                     each_index_rows,
                                                     color=self.tools.GetShelfNothing_Color())
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
    def DepotBuilding(self, depot_type=['BottomCenter2'], custom_depot=[], above=1, depth = 1):
        self.depot_type = depot_type
        for each_depot_type in self.depot_type:
            if each_depot_type == 'LeftCorner':
                depot_ID = 1
                depot_pos = [(2, self.grid_active_height - 2)]
                self.depot_area += depot_pos
                self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomCenter':
                depot_ID = 2
                depot_pos = [(int(self.grid_width/2), self.grid_active_height - 2)]
                self.depot_area += depot_pos
                self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomCenter2':
                depot_ID = 3
                depot_pos = [(int(self.grid_width/2), self.grid_active_height - 2),
                             (int(self.grid_width/2-1), self.grid_active_height-2)]
                self.depot_area += depot_pos
                self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomCenter1_Above':
                depot_ID = 421
                for each_depth in range(depth):
                    depot_pos = [(int(self.grid_width/2), self.grid_active_height - 2 - above - each_depth)]
                    self.depot_area += depot_pos
                    self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomCenter4_Above':
                depot_ID = 421
                for each_depth in range(depth):
                    depot_pos = [(int(self.grid_width/2+1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/2), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/2-1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/2-2), self.grid_active_height - 2 - above - each_depth)]
                    self.depot_area += depot_pos
                    self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomLeftQ4_Above':
                depot_ID = 422
                for each_depth in range(depth):
                    depot_pos = [(int(self.grid_width/4+1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/4), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/4-1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width/4-2), self.grid_active_height - 2 - above - each_depth)]
                    self.depot_area += depot_pos
                    self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'BottomRightQ4_Above':
                depot_ID = 423
                for each_depth in range(depth):
                    depot_pos = [(int(self.grid_width*3/4+1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width*3/4), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width*3/4-1), self.grid_active_height - 2 - above - each_depth),
                                 (int(self.grid_width*3/4-2), self.grid_active_height - 2 - above - each_depth)]
                    self.depot_area += depot_pos
                    self.tools.SetDepots(depot_pos, depot_ID)
            elif each_depot_type == 'Equal_Above':
                n_depot = custom_depot[0]
                for each_depot_ID in range(n_depot):
                    depot_pos = []
                    for each_depth in range(depth):
                        depot_pos += [(int(self.grid_width * (2 * each_depot_ID + 1) / (n_depot * 2)), self.grid_active_height - 2 - above - each_depth)]
                    self.depot_area += depot_pos
                    self.tools.SetDepots(depot_pos, each_depot_ID + 400)
                
                
        for each_depot in self.depot_area:
            name = self.tools.CellNaming(each_depot[0], each_depot[1])
            self.tools.ChangeColorObject(name, color='blue')
            self.tools.UpdateAbsWMap('Depot', each_depot)

    # AGV deposit are building function
    def AGVDepotBuilding(self, AGV_depot_type=['Equal'], custom_depot=[], AGV_size=5, above=1):
        for each_AGV_depot_type in AGV_depot_type:
            if each_AGV_depot_type == 'LeftCorner':
                self.AGV_depot_area.append((0, self.grid_active_height - 2 - above))
            if each_AGV_depot_type == 'TopCenter':
                self.AGV_depot_area.append((int(self.grid_width/2), 1 + above))
            if each_AGV_depot_type == 'Equal':
                for each_AGV in range(AGV_size):
                    self.AGV_depot_area.append((int(self.grid_width * (2 * each_AGV + 1) / (AGV_size * 2)), 1 + above))

        for each_AGV_depot in self.AGV_depot_area:
            name = self.tools.CellNaming(each_AGV_depot[0], each_AGV_depot[1])
            self.tools.ChangeColorObject(name, color='white')
            self.tools.UpdateAbsWMap('AGVDepot', each_AGV_depot)

    # AGV building function
    def AGVBuilding(self, _tag, _posX, _posY, color=''):
        return self.canvas.create_oval(
            _posX*self.square_size, _posY*self.square_size,
            (_posX+1)*self.square_size, (_posY+1)*self.square_size,
            outline="black", fill=color, tag=_tag)


    # AGV building function
    def AddAGV(self, num=5):
        num_AGVs = len(self.AGVs)
        for index, each_newAGV in enumerate(range(num)):

            if index >= len(self.AGV_depot_area):
                break;
            
            pos = self.AGV_depot_area[index]
            init_posX, init_posY = pos
            newAGV_ID = self.AGVBuilding("AGV",
                                         init_posX,
                                         init_posY,
                                         color = self.tools.GetAGVMovingWithoutShelf_Color())
            self.AGVs[newAGV_ID] = AGV.AGV(newAGV_ID, pos, self.tools)
        return len(self.AGVs)

    # Set controller and tools function
    def SetController(self,
                      controller_type='Default',
                      scheduling_type = 'Genetic',
                      evaluation_type = 'General_n_Balance',
                      order_threshold = 10,
                      order_independent = False,
                      graph_GUI_show = False,
                      padx = 0,
                      pady = 0,
                      max_scheduling = None):
        if graph_GUI_show:
            self.SetGraphGUI(padx = padx, pady = pady)

        self.controller = ctr.Controller(self.AGVs,
                                         self.shelves,
                                         self.tools,
                                         self.tools_data,
                                         scheduling_type = scheduling_type,
                                         evaluation_type = evaluation_type,
                                         time_threshold = self.tools.GetRescheduleTimeThreshold(),
                                         order_threshold = order_threshold,
                                         order_independent = order_independent,
                                         graph_GUI = self.graph_GUI,
                                         max_scheduling = max_scheduling)
        self.tools.SetAGVs(self.AGVs)

    # Set order generator function
    def SetOrder(self, order_type='basic', order_per_batch=1, num_order=100):
        self.order_generator = od.Order(self.shelves,
                                        self.tools_data,
                                        order_type = order_type,
                                        order_per_batch = order_per_batch,
                                        num_order = num_order,
                                        order_gap = 5)

    # Add order to list of order function
    def AddOrder(self, _order):
        self.order_list += self.order_generator.OrderGenerator()

    # Build a graph
    def SetGraphGUI(self, padx = 0, pady = 0):
        self.graph_GUI = ggui.SimulationGUI_GraphGUI(self.tools,
                                                     padx = padx,
                                                     pady = pady)

    # Set final
    def SetFinal(self, run_type = None, file_name = None):

        # File name creating
        w_t = "[" + self.warehouse_type + "-" + str(self.num_aisles) + "_" + str(self.num_rows) + "]"
        sim_name = w_t

        self.tools_data.SetStandardFileName(sim_name)

        # Order loading
        self.order_list += self.order_generator.SavedOrder()

        # Path loading
        saved_paths = self.tools_data.PathDataLoading()
        self.controller.SetReservePaths(saved_paths)

        # File name check
        if not file_name == None:
            if run_type == "rerun":
                done = self.tools_data.ResultFile_Existance(file_name, 'r')
            else:
                done = self.tools_data.ResultFile_Existance(file_name, 's')

            if done:
                self.AutoRun()
            self.controller.SetSavingFileName(file_name)
            

    # Rerun
    def SetReRun(self, file_name = None):
        print("[Running]\tRe-Running")
        
        self.re_run = True

        paths = self.tools_data.ResultsPathLoading(results_path_file_name=file_name)
        for index, each_AGVs_ID in enumerate(self.AGVs):
            self.AGVs[each_AGVs_ID].SetSchedule(paths[index])

    # Auto running system
    def AutoRun(self):
        all_done, new_argv = self.tools.AutoArgments(sys.argv)
        print(sys.argv)
        print("[Running]\tAlready finished")

        if all_done:
            sys.exit()
        else:
            python = sys.executable
            os.execl(python, python, *new_argv)

    # Update
    def Update(self):

        if not self.re_run:
            if len(self.order_list) <= self.tools.GetOrderLimitThreshold():
                self.AddOrder(self.order_generator)

            self.new_order = self.order_list.pop(0)
        
        done = self.controller.Update(self.new_order, self.re_run)

        if done:
            self.AutoRun()
                    
        self.canvas.after(self.movement_speed, self.Update)
        
