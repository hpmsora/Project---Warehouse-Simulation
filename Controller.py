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
    shelves = None
    canvas = None
    square_size = 0

    # Constructor
    def __init__(self, _AGVs, _shelves, _canvas, _square_size):
        self.AGVs = _AGVs
        self.shelves = _shelves
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

    # Shelf update
    def ShelfUpdate(self, _new_order):
        for each_new_order in _new_order:
            self.canvas.itemconfigure(each_new_order, fill='green')

    # Updateing time
    def Update(self, _new_order):
        total_remaining_time = 0
        print(_new_order)

        # Shelves update
        self.ShelfUpdate(_new_order)
        
        for each_AGV in self.AGVs:
            AGV = self.AGVs[each_AGV]
            total_remaining_time += len(AGV.GetSchedule())
            pos = self.PosToCoord(AGV.Move())
            self.canvas.coords(each_AGV, pos)
            
        if total_remaining_time <= 2:
            self.SetAGVScheule(self.AGVs)
