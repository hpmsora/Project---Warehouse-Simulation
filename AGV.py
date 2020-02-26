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
    schedule = []
    AGV_UI = None

    
    # Constructor
    def __init__(self, _ID, _pos, _AGV_UI):
        self.ID = _ID
        self.current_pos = _pos
        self.AGV_UI = _AGV_UI

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
        return self.current_pos
