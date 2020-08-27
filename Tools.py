
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
import math

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
    ABS_NO_ACC = -100
    TEMP_NO_ACC = -10
    OPEN = 0
    TARGET = 400
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

    AGV_moving_without_shelf = None
    AGV_moving_with_shelf = None
    AGV_collision = None

    shelf_nothing = None
    shelf_waiting = None
    shelf_moving = None

    # Constructor
    def __init__(self,
                 _parent,
                 _canvas,
                 _square_size,
                 _width,
                 _height,
                 order_limit_threshold = 15,
                 reschedule_time_threshold = 50,
                 AGV_moving_without_shelf = "yellow",
                 AGV_moving_with_shelf = "green",
                 AGV_collision = "red",
                 shelf_nothing = "gray",
                 shelf_waiting = "green",
                 shelf_moving = "white"):
        self.parent = _parent
        self.canvas = _canvas
        self.square_size = _square_size

        self.width = _width
        self.height = _height
        self.InitWMap()

        self.AGVs = None

        self.order_limit_threshold = order_limit_threshold
        self.reschedule_time_threshold = reschedule_time_threshold

        self.AGV_moving_without_shelf = AGV_moving_without_shelf
        self.AGV_moving_with_shelf = AGV_moving_with_shelf
        self.AGV_collision = AGV_collision

        self.shelf_nothing = shelf_nothing
        self.shelf_waiting = shelf_waiting
        self.shelf_moving = shelf_moving

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

    # Get depots
    def GetDepots(self):
        return self.depots
    
    # Set depots
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

    # Get AGV moving without shelf color
    def GetAGVMovingWithoutShelf_Color(self):
        return self.AGV_moving_without_shelf

    # Get AGV moving with shelf color
    def GetAGVMovingWithShelf_Color(self):
        return self.AGV_moving_with_shelf

    # Get AGV collision color
    def GetAGVCollision_Color(self):
        return self.AGV_collision

    # Get shelf waiting color
    def GetShelfNothing_Color(self):
        return self.shelf_nothing

    # Get shelf waiting color
    def GetShelfWaiting_Color(self):
        return self.shelf_waiting

    # Get shelf moving color
    def GetShelfMoving_Color(self):
        return self.shelf_moving

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

    # Auto argument editting
    def AutoArgments(self, _argv):
        new_argv = []
        f_m, cmd, sch_list, eval_list, c_num, n_num, status = _argv
        c_num = int(c_num)
        n_num = int(n_num)

        if c_num >= n_num and status == 'r':
            if len(sch_list) == 0 or len(eval_list) == 0:
                new_argv = _argv
                return (True, new_argv)
            else:
                sch_list = eval(sch_list)
                eval_list = eval(eval_list)
                sch_o = sch_list.pop()
                eval_o = eval_list.pop()
                new_argv = [f_m, cmd, str(sch_list), str(eval_list), str(1), str(n_num), 's']
                return (False, new_argv)
        elif status == 's':
            new_argv = [f_m, cmd, str(sch_list), str(eval_list), str(c_num), str(n_num), 'r']
            return (False, new_argv)
        elif c_num < n_num and status == 'r':
            c_num = str(c_num + 1)
            new_argv = [f_m, cmd, str(sch_list), str(eval_list), str(c_num), str(n_num), 's']
            return (False, new_argv)
        else:
            return (True, [])
        

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
        elif not comment == "":
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

    # Action movement
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
    def GetPathByQTable(self, _q_table, _start_point, _end_point, _order, max_count = 300):
        path = [_start_point]

        action = np.argmax(_q_table[_start_point])
        state = self.Next_Action(_start_point, action)

        count = 0
        is_path = True
        
        while not state in _end_point:
            path.append(state)
            action = np.argmax(_q_table[state])
            state = self.Next_Action(state, action)

            count += 1

            if count > 300:
                is_path = False
                break
            
        path.append(state)

        return (is_path, path)

    #--------------------------------------------------
    # Collision test
    
    # Strict collision test
    def CollisionTest_Strict(self, _AGVs_paths, test_type = 'Include Before'):
        paths = []
        paths_length = []
        AGVs_IDs = list(self.AGVs.keys())
        collision = 0
        entropy = 0

        if test_type == 'Include Before':
            for each_AGVs_ID in AGVs_IDs:
                each_AGVs_path = self.AGVs[each_AGVs_ID].GetSchedule()
                each_AGVs_path += _AGVs_paths[each_AGVs_ID]
                paths_length.append(len(each_AGVs_path))
                paths.append(each_AGVs_path)
                
        if test_type == 'New Path Only':
            remained_AGVs_path = {}
            remained_AGVs_path_length = []
            for each_AGVs_ID in AGVs_IDs:
                remained_each_AGVs_path = self.AGVs[each_AGVs_ID].GetSchedule()
                remained_AGVs_path[each_AGVs_ID] = remained_each_AGVs_path
                remained_AGVs_path_length.append(len(remained_each_AGVs_path))

            remained_AGVs_path_length_min = min(remained_AGVs_path_length)

            if remained_AGVs_path_length_min <= 0:
                return collision
            
            for each_AGVs_ID in AGVs_IDs:
                each_AGVs_path = remained_AGVs_path[each_AGVs_ID][remained_AGVs_path_length_min:]
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
                each_posX, each_posY, *each_order = each_pos
                each_posX_before, each_posY_before, *each_order_before = each_pos_before

                each_pos = (each_posX, each_posY)
                each_pos_before = (each_posX_before, each_posY_before)
                
                for each_other_pos, each_other_pos_before in zip(each_paths_time[index+1:], each_paths_time_before[index+1:]):
                    each_other_posX, each_other_posY, *each_other_order = each_other_pos
                    each_other_posX_before, each_other_posY_before, *each_other_order_before = each_other_pos_before

                    each_other_pos = (each_other_posX, each_other_posY)
                    each_other_pos_before = (each_other_posX_before, each_other_posY_before)

                    p = abs(each_posX - each_other_posX) + abs(each_posY - each_other_posY)
                    if p == 0 or p == 1:
                        entropy += math.log10(2)/2
                    else:
                        entropy += 1/p * math.log10(p)
                    
                    # Heading same position collision
                    if each_pos == each_other_pos:
                        collision += 1

                    # Turning following position collosion
                    if each_pos_before == each_other_pos and \
                       not (each_pos == each_other_pos_before) and \
                       not (each_other_pos == each_other_pos_before):
                        if not self.Tuple_Subtraction(each_other_pos, each_other_pos_before) == self.Tuple_Subtraction(each_pos, each_pos_before):
                            collision += 1

                    # Corssover collision
                    if (each_pos == each_other_pos_before and \
                        each_other_pos == each_pos_before) and \
                        not (each_pos == each_pos_before and each_other_pos == each_other_pos_before):
                        collision += 1

            each_paths_time_before = each_paths_time

        return (collision, entropy)
    
    # Strict collision test - Moving
    def CollisionTest_Strict_Moving(self, _AGV_pos_pre, _AGV_pos_curr):

        collision_AGVs = set()
        collision = 0
        
        for each_AGV_pre_ID, each_AGV_pre_pos in _AGV_pos_pre.items():
            each_AGV_curr_pos = _AGV_pos_curr[each_AGV_pre_ID]
            
            for each_other_AGV_curr_ID, each_other_AGV_curr_pos in _AGV_pos_curr.items():
                each_other_AGV_pre_pos = _AGV_pos_pre[each_other_AGV_curr_ID]

                # Heading same position collision
                if not each_other_AGV_curr_ID == each_AGV_pre_ID:
                    if each_AGV_curr_pos == each_other_AGV_curr_pos:
                        collision_AGVs.add(each_AGV_pre_ID)
                        collision_AGVs.add(each_other_AGV_curr_ID)
                        collision += 1

                # Turning following position collision
                if each_AGV_pre_pos == each_other_AGV_curr_pos and \
                   not (each_AGV_curr_pos == each_other_AGV_pre_pos) and \
                   not (each_other_AGV_curr_pos == each_other_AGV_pre_pos):
                    if not self.Tuple_Subtraction(each_other_AGV_curr_pos, each_other_AGV_pre_pos) == self.Tuple_Subtraction(each_AGV_curr_pos, each_AGV_pre_pos):
                        collision_AGVs.add(each_AGV_pre_ID)
                        collision_AGVs.add(each_other_AGV_curr_ID)
                        collision += 1

                # Crossover collision
                if each_AGV_curr_pos == each_other_AGV_pre_pos and \
                   each_other_AGV_curr_pos == each_AGV_pre_pos and \
                   not (each_AGV_curr_pos == each_AGV_pre_pos and each_other_AGV_curr_pos == each_other_AGV_pre_pos):
                    collision_AGVs.add(each_AGV_pre_ID)
                    collision_AGVs.add(each_other_AGV_curr_ID)
                    collision += 1
        return (collision_AGVs, collision)
    
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

    # AGVs path returning with matrix
    def TotalPathHistory(self):
        AGVs_path_history = []
        AGVs_path_history_t = []
        
        for each_AGVs in self.AGVs:
            each_AGVs_path = []
            for each_pos in self.AGVs[each_AGVs].GetScheduleHistory():
                each_AGVs_path.append(each_pos)
            AGVs_path_history_t.append(each_AGVs_path)

        for each_AGVs_path in zip(*AGVs_path_history_t):
            AGVs_path_history.append(each_AGVs_path)
            
        return AGVs_path_history

    # AGVs path finished
    def IsFinished(self):
        total_path = 0
        for each_AGVs in self.AGVs:
            total_path += self.AGVs[each_AGVs].GetRemainedScheduleLength()

        return total_path <= len(self.AGVs)

    # AGVs each path density
    def Density_AGV(self, _AGVs_pos, min_l = 5):
        total_score = 0
        each_distance = 0
        num_AGV = 0
        
        for each_AGV_ID, each_AGV_pos in _AGVs_pos.items():
            each_AGV_posX, each_AGV_posY, *order = each_AGV_pos
            for each_other_AGV_ID, each_other_AGV_pos in _AGVs_pos.items():
                each_other_AGV_posX, each_other_AGV_posY, *order = each_other_AGV_pos
                if not each_AGV_ID == each_other_AGV_ID:
                    each_distance = abs(each_AGV_posX - each_other_AGV_posX) + abs(each_AGV_posY - each_other_AGV_posY) + 1
                    if each_distance <= min_l:
                        total_score += 1/each_distance
            num_AGV += 1
        
        return total_score/num_AGV
