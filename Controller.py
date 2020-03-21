###############################
#
# Controller
#
# Won Yong Ha
#
#
###############################

import Algorithms_Scheduling as AlgSch

class Controller():

    AGVs = None
    shelves = None

    # Internal Varialbles
    tools = None
    scheduling_algorithm = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, scheduling_type = "Genetic", path_planning_type = "Q_Learning", evaluation_type = "General_n_Balance"):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.SetSchedulingAlgorithm(scheduling_type, path_planning_type, evaluation_type)
        
    # Set schedule
    def SetAGVScheule(self, _AGVs):
        route = []
        for i in range(2, 15):
            route.append((2,i))

        count = 2
        for each_AGV in _AGVs:
            _AGVs[each_AGV].SetSchedule(route)
            _AGVs[each_AGV].AddSchedule([(3,2,1)])
            count += 1

    # Set scheduling algorithm
    def SetSchedulingAlgorithm(self, _scheduling_type, _path_planning_type, _evaluation_type):
        self.scheduling_algorithm = AlgSch.Algorithms_Scheduling(self.AGVs, self.shelves, self.tools, _scheduling_type, _path_planning_type, _evaluation_type)
    
    # Shelf update
    def ShelfUpdate(self, _new_order):
        new_order_ID = _new_order[0]
        new_order_orders = _new_order[1]
        for each_new_order_orders in new_order_orders:
            self.shelves[each_new_order_orders].AddOrder(new_order_ID)
            
    # Updateing time
    def Update(self, _new_order):
        total_remaining_time = 0
        print(_new_order)

        # Add orders
        self.ShelfUpdate(_new_order)
        
        # AGV updates
        for each_AGV_ID, each_AGV_Object in self.AGVs.items():
            total_remaining_time += len(each_AGV_Object.GetSchedule())
            each_AGV_Object.Move()

        # Shelves update
        for each_shelf_ID, each_shelf_Object in self.shelves.items():
            each_shelf_Object.update()

        # Re-Scheduling
        if total_remaining_time == 0:
            self.SetAGVScheule(self.AGVs)
            self.scheduling_algorithm.Update()
            
