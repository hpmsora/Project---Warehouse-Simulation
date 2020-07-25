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

    time_threshold = None
    result_file_name = None

    # Internal Varialbles
    tools = None
    tools_data = None
    graph_GUI = None
    scheduling_algorithm = None
    new_orders = []

    # Constructor
    def __init__(self,
                 _AGVs,
                 _shelves,
                 _tools,
                 _tools_data,
                 scheduling_type = "Genetic",
                 path_planning_type = "Q_Learning",
                 evaluation_type = "General_n_Balance",
                 time_threshold=10,
                 results_file_name="Result.csv",
                 order_independent = False,
                 graph_GUI = None):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.order_independent = order_independent
        self.time_threshold = time_threshold
        self.results_file_name = results_file_name
        
        self.tools = _tools
        self.tools_data = _tools_data
        self.graph_GUI = graph_GUI

        self.SetSchedulingAlgorithm(scheduling_type, path_planning_type, evaluation_type)

    # Set scheduling algorithm
    def SetSchedulingAlgorithm(self, _scheduling_type, _path_planning_type, _evaluation_type):
        self.scheduling_algorithm = AlgSch.Algorithms_Scheduling(self.AGVs,
                                                                 self.shelves,
                                                                 self.tools,
                                                                 _scheduling_type,
                                                                 _path_planning_type,
                                                                 _evaluation_type,
                                                                 graph_GUI = self.graph_GUI)
  
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
        if len(self.new_orders) >= 40: # total_remaining_time < self.time_threshold:
            
            for each_new_orders in self.new_orders:
                self.ShelfUpdate(each_new_orders)
            (new_paths, eval_values) = self.scheduling_algorithm.Update(self.new_orders, self.order_independent)
            eval_value_total, eval_value_compositions = eval_values
            
            strict_collision = self.tools.CollisionTest_Strict(new_paths)
            print("Collosions: " + str(strict_collision))

            results = [strict_collision, eval_value_total] + list(eval_value_compositions)
            self.tools_data.ResultsSaving([results], self.results_file_name)

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
