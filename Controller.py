###############################
#
# Controller
#
# Won Yong Ha
#
#
###############################

class Controller():

    AGVs = None
    canvas = None
    square_size = 0

    # Constructor
    def __init__(self, _AGVs, _canvas, _square_size):
        self.AGVs = _AGVs
        self.canvas = _canvas
        self.square_size = _square_size

    # Set Schedule
    def SetAGVScheule(self, _AGVs):
        route = []
        for i in range(2, 15):
            route.append((2,i))

        for each_AGV in _AGVs:
            _AGVs[each_AGV].SetSchedule(route)

    # Pos to coordinate
    def PosToCoord(self, pos):
        return (pos[0]*self.square_size, pos[1]*self.square_size,
                (pos[0]+1)*self.square_size, (pos[1]+1)*self.square_size)

    # Updateing time
    def Update(self, _new_order):
        total_remaining_time = 0
        print(_new_order)
        for each_AGV in self.AGVs:
            AGV = self.AGVs[each_AGV]
            total_remaining_time += len(AGV.GetSchedule())
            pos = self.PosToCoord(AGV.Move())
            self.canvas.coords(each_AGV, pos)
            
        if total_remaining_time <= 2:
            self.SetAGVScheule(self.AGVs)
