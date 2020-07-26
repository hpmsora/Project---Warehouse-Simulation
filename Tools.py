###############################
#
# Tools
#
# Won Yong Ha
#
#
# V.1.2 Add matrix calculation
# V.1.1 Add Q-learning map
# V.1.0 General tools
#
###############################

import numpy as np
import random as rnd
import copy as cp
import collections as col
import bisect as bit

import sys

class Tools():

    parent = None
    canvas = None
    square_size = None
    
    width = 0
    height = 0

    # Internal Variables
    w_map = None
    # -55 : AGV starting place
    # -50 : Absolutely no access
    # -10 : Temporary no access
    #   0 : Open
    #  150: Target
    #  200: Depot Place
    ABS_NO_ACC = -50
    TEMP_NO_ACC = -10
    OPEN = 0
    TARGET = 200
    DEPOT_PLACE = 200

    AGVs = None
    shelves_depots = {}
    depots = {}

    order_limit_threshold = None
    reschedule_time_threshold = None

    # Graph GUI internal variables
    graph_data = None
    graph_variables_type = None
    graph_variables_type_list = None

    # Constructor
    def __init__(self,
                 _parent,
                 _canvas,
                 _square_size,
                 _width,
                 _height,
                 order_limit_threshold = 15,
                 reschedule_time_threshold = 50):
        self.parent = _parent
        self.canvas = _canvas
        self.square_size = _square_size

        self.width = _width
        self.height = _height
        self.InitWMap()

        self.AGVs = None

        self.order_limit_threshold = order_limit_threshold
        self.reschedule_time_threshold = reschedule_time_threshold

        self.graph_data = {}
        self.graph_variables_type = ()
        self.graph_variables_type_list = []
        
    # Building w_map
    def InitWMap(self):
        self.w_map = [[0 for i in range(self.height)] for j in range(self.width)]
        for each_w in range(self.width):
            for each_h in range(self.height):
                if each_w == 0 or each_w == self.width - 1 or each_h == 0 or each_h == self.height - 1:
                    self.w_map[each_w][each_h] = self.ABS_NO_ACC

    # Get parent object
    def GetParent(self):
        return self.parent
    
    # Get order limit threshold
    def GetOrderLimitThreshold(self):
        return self.order_limit_threshold

    # Get reschedule time threshold
    def GetRescheduleTimeThreshold(self):
        return self.reschedule_time_threshold

    # Get canvas object
    def GetCanvas(self):
        return self.canvas

    # Set AGVs
    def SetAGVs(self, _AGVs):
        self.AGVs = _AGVs

    # Get shelves positions by ID
    def GetShelvesDepotsByID(self, _shelf_ID):
        return self.shelves_depots[_shelf_ID]

    # Get shelves positions tuple by ID
    def GetShelvesDepotsPosByID(self, _shelf_ID):
        return [self.CellNameToPos(self.GetShelvesDepotsByID(_shelf_ID))]
        
    # Set shelves positions
    def SetShelvesDepots(self, _shelf_pos, _shelf_ID):
        self.shelves_depots[_shelf_ID] = _shelf_pos

    # Get depots positions by ID
    def GetDepotsByID(self, _depot_ID):
        return self.depots[_depot_ID]

    def SetDepots(self, _depot_pos, _depot_ID):
        self.depots[_depot_ID] = _depot_pos

    # Get width
    def GetWidth(self):
        return self.width

    # Get height
    def GetHeight(self):
        return self.height

    # Get w_map
    def GetWMap(self):
        return cp.deepcopy(self.w_map)

    # Get graph variables type
    def GetGraphVariablesType(self):
        return self.graph_variables_type

    # Set graph variables type
    def SetGraphVariablesType(self, _graph_variables_type):
        self.graph_variables_type = _graph_variables_type
        data_total, data_variables = self.graph_variables_type
        self.graph_variables_type_list = [data_total] + list(data_variables)
        for each_values in self.graph_variables_type_list:
            self.graph_data[each_values] = [[0],[0]]

    # Get graph data
    def GetGraphData(self):
        return self.graph_data

    # Update absolute w_map
    def UpdateAbsWMap(self, _type, _pos):
        if _type == 'Depot':
            self.w_map[_pos[0]][_pos[1]] = self.DEPOT_PLACE
        elif _type == 'AGVDepot':
            self.w_map[_pos[0]][_pos[1]] = self.OPEN

    # Update w_map
    def UpdateWMap(self, _w_map, _type, _pos, AGV_ID = None):
        if _type == 'AGV':
            _w_map[_pos[0]][_pos[1]] = (self.TEMP_NO_ACC, AGV_ID)

    # Update w_map with shelves depot positions
    def UpdateWMapShelves(self, _w_map):
        for each_pos_shelves_depot in self.shelves_depots.values():
            pos = self.CellNameToPos(each_pos_shelves_depot)
            _w_map[pos[0]][pos[1]] = self.ABS_NO_ACC

    # Moving object to desire position
    def MoveObject(self, _object_ID, _pos):
        pos = self.PosToCoord(_pos)
        self.canvas.coords(_object_ID, pos)

    # Changing object filling color to desire color
    def ChangeColorObject(self, _object_ID, color="Black"):
        self.canvas.itemconfigure(_object_ID, fill=color)
    
    # Pos to coordinate
    def PosToCoord(self, _pos):
        return (_pos[0]*self.square_size, _pos[1]*self.square_size,
                (_pos[0]+1)*self.square_size, (_pos[1]+1)*self.square_size)

    # Cell naming function
    def CellNaming(self, _posX, _posY):
        return str(_posX) + ":" + str(_posY)


    # Cell name to pos tuple function
    def CellNameToPos(self, _name):
        pos = _name.split(':')
        return (int(pos[0]), int(pos[1]))

    #--------------------------------------------------
    # Console Printing Tools

    # Evaluation data printing function
    def PrintEvaluationData(self, _eval_data, _level, decimals=4, order_num="", comment=""):
        total_value, component_values = _eval_data

        print_str = "( "

        for each_value in component_values:
            print_str += str(round(each_value, 4)) + "\t"

        print_str += ")"

        if not order_num == "":
            print("[" + _level  + "]\t" + str(order_num) + "\tT: " \
                  + str(round(total_value, decimals)) + "\t" + print_str)
        elif comment == "":
            print("[" + _level  + "]\t" + comment + "\tT: " \
                  + str(round(total_value, decimals)) + "\t" + print_str)
        else:
            print("[" + _level  + "]\tT: " \
                  + str(round(total_value, decimals)) + "\t" + print_str)

    #--------------------------------------------------
    # Algorithms Tools

    # Get next state by action
    def Next_Action(self, _pos, _action):
        posX, posY, *order = _pos

        if _action == 0:   # Up
            posY += 1
        elif _action == 1: # Down
            posY -= 1
        elif _action == 2: # Right
            posX += 1
        elif _action == 3: # Left
            posX -= 1
            
        return (posX, posY)

    # Action Movement
    def Step_Action(self, _pos, _action, _w_map, _target):
        reward = -1
        done = False

        next_pos = self.Next_Action(_pos, _action)
        posX, posY, *order = next_pos

        if next_pos in _target:
            reward = self.TARGET
            done = True
            
        elif _w_map[posX][posY] == self.ABS_NO_ACC:
            reward = self.ABS_NO_ACC
            done = True
            
        return next_pos, reward, done

    # Get path by q-table
    def GetPathByQTable(self, _q_table, _start_point, _end_point, _order):
        path = []

        action = np.argmax(_q_table[_start_point])
        state = self.Next_Action(_start_point, action)
        
        while not state in _end_point:
            path.append(state)
            action = np.argmax(_q_table[state])
            state = self.Next_Action(state, action)
            
        path.append(state)

        return path

    #--------------------------------------------------
    # Collision test

    # Strict collision test
    def CollisionTest_Strict(self, _AGVs_paths):
        paths = []
        paths_length = []
        AGVs_IDs = list(self.AGVs.keys())
        collision = 0
        
        for each_AGVs_ID in AGVs_IDs:
            each_AGVs_path = self.AGVs[each_AGVs_ID].GetSchedule()
            each_AGVs_path += _AGVs_paths[each_AGVs_ID]
            paths_length.append(len(each_AGVs_path))
            paths.append(each_AGVs_path)

        paths_length_min = min(paths_length)
        if paths_length_min <=0:
            return collision
        
        for index, (each_paths, each_paths_length) in enumerate(zip(paths, paths_length)):
            #each_paths += [each_paths[-1]] * (paths_length_max - each_paths_length)
            paths[index] = each_paths[:paths_length_min]

        paths_time = list(zip(*paths))
        each_paths_time_before = paths_time[0]

        for each_paths_time in paths_time[1:]:
            for index, (each_pos, each_pos_before) in enumerate(zip(each_paths_time, each_paths_time_before)):
                for each_other_pos, each_other_pos_before in zip(each_paths_time[index+1:], each_paths_time_before[index+1:]):

                    # Heading same position collision
                    if each_pos == each_other_pos:
                        collision += 1

                    # Turning following position collosion
                    if each_pos_before == each_other_pos and \
                       not (each_pos == each_other_pos_before) and \
                       not (each_other_pos, each_other_pos_before):
                        if not self.Tuple_Subtraction(each_other_pos, each_other_pos_before) == self.Tuple_Subtraction(each_pos, each_pos_before):
                            collision += 1

                    # Corssover collision
                    if (each_pos == each_other_pos_before and \
                        each_other_pos == each_pos_before) and \
                        not (each_pos == each_pos_before and each_other_pos == each_other_pos_before):
                        collision += 1

            each_paths_time_before = each_paths_time

        return collision

    
    #--------------------------------------------------
    # Graph Tools
    
    # Update each iteration
    def Update_GraphData(self, _index, _data):
        data_total, data_variables = _data
        data_list = [data_total] + list(data_variables)
        for index, each_graph_variables_type in enumerate(self.graph_variables_type_list):
            self.graph_data[each_graph_variables_type][0] += [_index]
            self.graph_data[each_graph_variables_type][1] += [data_list[index]]

    # Reset graph data
    def ResetGraphData(self):
        for each_values in self.graph_variables_type_list:
            self.graph_data[each_values] = [[0],[0]]


    #--------------------------------------------------
    # Math Tools

    # Find arg maximum
    def Arg_Maximum(self, _state_actions):
        max_index_list = []
        max_value = _state_actions[0]
        for index, value in enumerate(_state_actions):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return rnd.choice(max_index_list)

    # Tuple subtraction
    def Tuple_Subtraction(self, _pos_1, _pos_2):
        return tuple(map(lambda i, j: i - j, _pos_1, _pos_2))

    # Time coordinate data ordering (Not using)
    def Matrixization_TimeOrder(self, _new_path):
        path_list = []

        for each_AGV in _new_path:
            (_, _, coords) = _new_path[each_AGV]
            path_list += coords

        path_list = sorted(path_list, key=lambda x: x[-1])
        print(path_list)

    # Time coordinate data seperation
    def Matrixization_Separation(self, _new_path):
        path_list_x = []
        path_list_y = []
        path_list_t = []

        m_size = 0
        min_t = float('inf')
        max_t = 0

        for each_AGV in _new_path:
            (_, _, coords) = _new_path[each_AGV]
            for each_coords in coords:
                (time_t, pos_x, pos_y) = each_coords
                path_list_x.append(pos_x)
                path_list_y.append(pos_y)
                path_list_t.append(time_t)
                m_size += 1

                if max_t < time_t:
                    max_t = time_t

                if min_t > time_t:
                    min_t = time_t

        path_list_x = [path_list_x]*m_size
        path_list_y = [path_list_y]*m_size
        path_list_t = [path_list_t]*m_size

        return (path_list_t, path_list_x, path_list_y, min_t, max_t, m_size)

    # Time coordinate data to occupancy matrix
    def Matrixization_Density(self, _new_path):
        path_list = []
        
        for each_AGV in _new_path:
            (_, _, coords) = _new_path[each_AGV]
            path_list += coords

        path_list = np.array(path_list)

        t_min = sys.maxsize
        t_max = 0
        x_min = sys.maxsize
        x_max = 0
        y_min = sys.maxsize
        y_max = 0
        
        for (t, x, y) in path_list:
            if t_max < t:
                t_max = t
            if t_min > t:
                t_min = t
            if x_max < x:
                x_max = x
            if x_min > x:
                x_min = x
            if y_max < y:
                y_max = y
            if y_min > y:
                y_min = y

        density_matrix = np.zeros((t_max - t_min + 1,
                                   x_max - x_min + 1,
                                   y_max - y_min + 1))

        for (t, x, y) in path_list:
            density_matrix[t - t_min, x - x_min, y - y_min] = 1

        #print(list(density_matrix))

        return []

    # Time coordinate data to adjacency matrix
    def Matrixization_Adjacency(self, _new_path, threshold = 0):
        adjacency_matrix = []
        
        adjacency_dict = col.defaultdict(list)
        for each_AGV in _new_path:
            (_, _, each_orders) = _new_path[each_AGV]
            for each_index, each_order in enumerate(each_orders[:-1]):
                (current_order_time_step, _, _) = each_order
                next_order = each_orders[each_index+1]
                (next_order_time_step, _, _) = next_order
                adjacency_dict[each_order] += [(next_order, next_order_time_step - current_order_time_step)]
                adjacency_dict[next_order] += []
        
        # Assigned order
        adjacency_matrix_order = {}
        adjacency_matrix_size = 0
        for each_index, each_adjancency_dict in enumerate(adjacency_dict):
            adjacency_matrix_size += 1
            adjacency_matrix_order[each_adjancency_dict] = each_index

        adjacency_matrix = np.zeros((adjacency_matrix_size, adjacency_matrix_size))
        
        for each_adjancency_dict in adjacency_dict:
            m_i = adjacency_matrix_order[each_adjancency_dict]

            for (each_connection, each_length) in adjacency_dict[each_adjancency_dict]:
                m_j = adjacency_matrix_order[each_connection]
                adjacency_matrix[m_i, m_j] = each_length

        return adjacency_matrix
