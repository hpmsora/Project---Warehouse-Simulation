###############################
#
# Tools
#
# Won Yong Ha
#
#
###############################

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
    #  -1 : Open
    #  200: Depot Place
    #  200: Target

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
                    self.w_map[each_w][each_h] = -50
        
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
            self.w_map[_pos[0]][_pos[1]] = 200
        elif _type == 'AGVDepot':
            self.w_map[_pos[0]][_pos[1]] = 0

    # Update w_map
    def UpdateWMap(self, _w_map, _type, _pos, AGV_ID = None):
        if _type == 'AGV':
            _w_map[_pos[0]][_pos[1]] = (-10, AGV_ID)

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
