###############################
#
# Tools
#
# Won Yong Ha
#
#
###############################

import numpy as np
import copy as cp

class Tools():

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
    TARGET = 150
    DEPOT_PLACE = 200
    
    shelves_depots = {}
    depots = {}

    # Constructor
    def __init__(self, _canvas, _square_size, _width, _height):
        self.canvas = _canvas
        self.square_size = _square_size

        self.width = _width
        self.height = _height
        self.InitWMap()

    # Building w_map
    def InitWMap(self):
        self.w_map = [[0 for i in range(self.height)] for j in range(self.width)]
        for each_w in range(self.width):
            for each_h in range(self.height):
                if each_w == 0 or each_w == self.width - 1 or each_h == 0 or each_h == self.height - 1:
                    self.w_map[each_w][each_h] = self.ABS_NO_ACC

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
        
    # Get canvas object
    def GetCanvas(self):
        return canvas

    # Get width
    def GetWidth(self):
        return self.width

    # Get height
    def GetHeight(self):
        return self.height

    # Get w_map
    def GetWMap(self):
        return cp.deepcopy(self.w_map)

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
    # Algorithms Tools

    # Get next state by action
    def Next_Action(self, _pos, _action):
        posX, posY = _pos

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
        posX, posY = _pos
        
        if _w_map[posX][posY] == self.ABS_NO_ACC:
            reward = self.ABS_NO_ACC
            done = True
        elif next_pos in _target:
            reward = self.TARGET
            done = True

        return next_pos, reward, done

    # Get path by q-table
    def GetPathByQTable(self, _q_table, _start_point, _end_point):
        path = []

        state = _start_point

        while not state in _end_point:
            action = np.argmax(_q_table[state])
            state = self.Next_Action(state, action)
            path.append(state)
            print("A")
            
        path.append(state)

        return path
