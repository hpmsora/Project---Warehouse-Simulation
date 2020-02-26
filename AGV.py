###############################
#
# AGV Objects
#
# Won Yong Ha
#
#
###############################

class AGV:

    ID = None
    current_pos = (0,0)
    schedule = []

    
    # Constructor
    def __init__(self, _ID):
        self.ID = _ID

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
        self.schedule += _add_schedule

    def Move(self):
        if not self.schedule == []:
            self.current_pos = self.schedule.pop(0)
