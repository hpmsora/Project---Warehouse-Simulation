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
    order_independent = None

    # Internal Varialbles
    tools = None
    scheduling_algorithm = None
    new_orders = []

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, scheduling_type = "Genetic", path_planning_type = "Q_Learning", evaluation_type = "General_n_Balance", order_independent = False):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.order_independent = order_independent
        self.tools = _tools

        self.SetSchedulingAlgorithm(scheduling_type, path_planning_type, evaluation_type)

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

        # Add orders
        if not len(_new_order[1]) == 0:
            self.new_orders.append(_new_order)

        # Check total remaining time
        for each_AGV_ID, each_AGV_Object in self.AGVs.items():
            total_remaining_time += len(each_AGV_Object.GetSchedule())
            
        # Re-Scheduling
        if total_remaining_time < 10:
            for each_new_orders in self.new_orders:
                self.ShelfUpdate(each_new_orders)
            new_paths = self.scheduling_algorithm.Update(self.new_orders, self.order_independent)

            for each_AGV_ID in new_paths.keys():
                self.AGVs[each_AGV_ID].AddSchedule(new_paths[each_AGV_ID])

            self.new_orders = []
        
        # Movement --------------------------------------------------
        # AGV updates
        for each_AGV_ID, each_AGV_Object in self.AGVs.items():
            each_AGV_Object.Move()

        # Shelves update
        for each_shelf_ID, each_shelf_Object in self.shelves.items():
            each_shelf_Object.update()
