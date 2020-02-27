###############################
#
# Tools
#
# Won Yong Ha
#
#
###############################

class Tools():

    canvas = None
    square_size = None

    # Constructor
    def __init__(self, _canvas, _square_size):
        self.canvas = _canvas
        self.square_size = _square_size

    # Getting canvas object
    def GetCanvas(self):
        return canvas

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
