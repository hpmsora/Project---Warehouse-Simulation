###############################
#
# AGV
#
# Won Yong Ha
#
#
###############################

import copy as cp

class AGV:

    ID = None
    current_pos = None
    canvas = None

    # Internal Variables
    status = None # {'Moving', 'MovingWithShelf'}
    schedule = []
    schedule_history = []
    #
    # [(_, _)...]    Xpos, Ypos
    # [(_, _, (_, _))...] -> (Xpos, Ypos, (orderID, shelf_ID)) ...
    #
    order = []
    tools = None
    
    # Constructor
    def __init__(self, _ID, _pos, _tools):
        self.ID = _ID
        self.current_pos = _pos
        self.tools = _tools
        self.previous_schedule = self.current_pos

        self.status = 'Moving'
        self.schedule = []
        self.schedule_history = []
        self.order = []

        self.AddSchedule([_pos])

    # Get ID
    def GetID(self):
        return self.ID

    # Get current position
    def GetCurrentPos(self):
        return self.current_pos

    # Get last scheduled position
    def GetLastScheduledPos(self):
        return self.schedule[-1]

    # Get remained schedule length
    def GetRemainedScheduleLength(self):
        return len(self.schedule)

    # Get schedule
    def GetSchedule(self):
        return cp.deepcopy(self.schedule)
    
    # Set schedule
    def SetSchedule(self, _new_schedule):
        self.schedule = _new_schedule

    # Add schedule
    def AddSchedule(self, _add_schedule):
        for each_add_schedule in _add_schedule:
            self.schedule.append(each_add_schedule)
            self.schedule_history.append(each_add_schedule)
            if len(each_add_schedule) == 3:
                self.order.append(each_add_schedule[-1])

    # Get Order
    def GetOrder(self):
        return self.order

    # Get schedule history
    def GetScheduleHistory(self):
        return cp.deepcopy(self.schedule_history)

    # Color update
    def ColorUpdate(self, collision=False):
        if collision:
            self.tools.ChangeColorObject(self.ID, self.tools.GetAGVCollision_Color())
        else:
            if self.status == 'Moving':
                self.tools.ChangeColorObject(self.ID, self.tools.GetAGVMovingWithoutShelf_Color())
            elif self.status == 'MovingWithShelf':
                self.tools.ChangeColorObject(self.ID, self.tools.GetAGVMovingWithShelf_Color())
            else:
                print("Error")
                self.tools.ChangeColorObject(self.ID, self.tools.GetAGVMovingWithoutShelf_Color())
    
    # AGV move
    def Move(self):
        shelf_occupancy = {}
        
        if not self.schedule == []:
            current_schedule = self.schedule.pop(0)
            
            posX, posY, *order = current_schedule

            if not order == []:
                target_order_ID, target_order, target_ID = order[0]
                if target_order == 'Depot':
                    self.status = 'MovingWithShelf'
                elif target_order == 'Shelf-Picking':
                    self.status = 'MovingWithShelf'
                    self.tools.ChangeColorObject(self.ID, self.tools.GetAGVMovingWithShelf_Color())
                    shelf_occupancy[target_ID] = (self.ID, True, target_order_ID)
                elif target_order == 'Shelf-Returning':
                    self.status = 'Moving'
                    self.tools.ChangeColorObject(self.ID, self.tools.GetAGVMovingWithoutShelf_Color())
                    shelf_occupancy[target_ID] = (self.ID, False, target_order_ID)

            if len(self.schedule) == 0:
                self.schedule.append(current_schedule)
            
            self.current_pos = (posX, posY)

            if order:
                for each_order in order:
                    if each_order in self.order:
                        self.order.remove(each_order)

            self.tools.MoveObject(self.ID, self.current_pos)

        return (self.current_pos, shelf_occupancy)
