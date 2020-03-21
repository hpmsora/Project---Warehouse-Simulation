###############################
#
# Tools
#
# Won Yong Ha
#
#
###############################

import numpy as np

class Tools():

    canvas = None
    square_size = None
    
    width = 0
    height = 0

    # Internal Variables
    w_map = None
    # -50 : Absolutely no access
    # -10 : Temporary no access
    #  -1 : Open
    #  200: Depot Place
    #  200: 

    # Constructor
    def __init__(self, _canvas, _square_size, _width, _height):
        self.canvas = _canvas
        self.square_size = _square_size

        self.width = _width
        self.height = _height
        self.InitWMap()

    # Building w_map
    def InitWMap(self):
        self.w_map = np.zeros((self.width, self.height))
        for each_w in range(self.width):
            for each_h in range(self.height):
                if each_w == 0 or each_w == self.width - 1 or each_h == 0 or each_h == self.height - 1:
                    self.w_map[each_w][each_h] = -50
        print(self.w_map)
        
    # Get canvas object
    def GetCanvas(self):
        return canvas

    # Get width
    def GetWidth(self):
        return self.width

    # Get height
    def GetHeight(self):
        return self.height

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
