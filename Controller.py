###############################
#
# Controller
#
# Won Yong Ha
#
#
###############################

class Controller():

    #

    # Constructor
    def __init__(self, _AGVs):
        self.AGVs = _AGVs

    # Set Schedule
    def SetAGVScheule(self, _AGV):
        route = []
        for i in range(2, 15):
            route.append((2,i))
        _AGV.SetSchedule(route)

    # Updateing time
    def Update(self):
        total_remaining_time = 0
        for each_AGV in self.AGVs:
            AGV = self.AGVs[each_AGV]
            total_remaining_time += len(AGV.GetSchedule())
            AGV.Move()
        if total_remaining_time <= 2:
            self.SetAGVScheule(self.AGVs[0])
