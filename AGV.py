###############################
#
# AGV
#
# Won Yong Ha
#
#
###############################

class AGV:

    ID = None
    current_pos = None
    canvas = None

    # Internal Variables
    schedule = []
    #
    # [(_, _)...]    Xpos, Ypos
    # [(_, _, _)...] Xpos, Ypos, orderID
    #
    order = []
    tools = None

    # Constructor
    def __init__(self, _ID, _pos, _tools):
        self.ID = _ID
        self.current_pos = _pos
        self.tools = _tools

    # Get ID
    def GetID(self):
        return self.ID

    # Get current position
    def GetCurrentPos(self):
        return self.current_pos

    # Get schedule
    def GetSchedule(self):
        return self.schedule
    
    # Set schedule
    def SetSchedule(self, _new_schedule):
        self.schedule = _new_schedule

    # Add schedule
    def AddSchedule(self, _add_schedule):
        for each_add_schedule in _add_schedule:
            self.schedule.append(each_add_schedule)
            if len(each_add_schedule) == 3:
                self.order.append(each_add_schedule[-1])
        print(self.schedule)
        print(self.order)

    # Get Order
    def GetOrder(self):
        return self.order
    
    # AGV move
    def Move(self):
        if not self.schedule == []:
            posX, posY, *order = self.schedule.pop(0)
            
            self.current_pos = (posX, posY)
            if order:
                for each_order in order:
                    self.order.remove(each_order)
            self.tools.MoveObject(self.ID, self.current_pos)
