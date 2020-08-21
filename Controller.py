###############################
#
# Controller
#
# Won Yong Ha
#
#
###############################

import collections as col

import Algorithms_Scheduling as AlgSch

class Controller():

    AGVs = None
    shelves = None
    order_independent = None

    time_threshold = None
    order_threshold = None
    result_file_name = None

    # Internal Varialbles
    tools = None
    tools_data = None
    graph_GUI = None
    scheduling_algorithm = None
    new_orders = []
    AGV_pos_curr = None
    AGV_pos_pre = None
    
    scheduling_depot_dist_type = ['Random', 'Genetic', 'Min']
    strict_test_type = ['Include Before', 'New Path Only']

    # Constructor
    def __init__(self,
                 _AGVs,
                 _shelves,
                 _tools,
                 _tools_data,
                 scheduling_type = "Genetic",
                 path_planning_type = "Q_Learning",
                 evaluation_type = "General_n_Balance",
                 time_threshold = 10,
                 order_threshold = 10,
                 order_independent = False,
                 graph_GUI = None):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.order_independent = order_independent
        self.time_threshold = time_threshold
        self.order_threshold = order_threshold
        
        self.tools = _tools
        self.tools_data = _tools_data
        self.graph_GUI = graph_GUI

        self.AGV_pos_curr = col.defaultdict(lambda: (0,0))
        self.AGV_pos_pre = col.defaultdict(lambda: (0,0))

        self.scheduling_depot_dist_type = self.scheduling_depot_dist_type[1]
        self.strict_test_type = self.strict_test_type[1]

        self.SetSchedulingAlgorithm(scheduling_type,
                                    path_planning_type,
                                    evaluation_type,
                                    tools_data = self.tools_data,
                                    scheduling_depot_dist_type = self.scheduling_depot_dist_type)

    # Set scheduling algorithm
    def SetSchedulingAlgorithm(self,
                               _scheduling_type,
                               _path_planning_type,
                               _evaluation_type,
                               tools_data = None,
                               scheduling_depot_dist_type = None):
        self.scheduling_algorithm = AlgSch.Algorithms_Scheduling(self.AGVs,
                                                                 self.shelves,
                                                                 self.tools,
                                                                 _scheduling_type,
                                                                 _path_planning_type,
                                                                 _evaluation_type,
                                                                 tools_data = tools_data,
                                                                 graph_GUI = self.graph_GUI,
                                                                 depot_distribution_type = scheduling_depot_dist_type)

    # Set reserve paths
    def SetReservePaths(self, _paths):
        self.scheduling_algorithm.SetReservePaths(_paths)

    # Shelf update
    def ShelfUpdate(self, _new_order):
        new_order_ID = _new_order[0]
        new_order_orders = _new_order[1]
        for each_new_order_orders in new_order_orders:
            self.shelves[each_new_order_orders].AddOrder(new_order_ID)
            
    # Updateing time
    def Update(self, _new_order, _re_run):
        
        total_remaining_time = 0

        if not _re_run:
            # Add orders
            if not len(_new_order[1]) == 0:
                self.new_orders.append(_new_order)

            # Check total remaining time
            for each_AGV_ID, each_AGV_Object in self.AGVs.items():
                total_remaining_time += len(each_AGV_Object.GetSchedule())
            
            # Re-Scheduling
            if len(self.new_orders) >= self.order_threshold: # total_remaining_time < self.time_threshold:
            
                for each_new_orders in self.new_orders:
                    self.ShelfUpdate(each_new_orders)
                (new_paths, eval_values) = self.scheduling_algorithm.Update(self.new_orders, self.order_independent)
                eval_value_total, eval_value_compositions = eval_values
            
                strict_collision, entropy = self.tools.CollisionTest_Strict(new_paths, test_type = self.strict_test_type)
                print("[Result]\tCollosions:\t" + str(strict_collision))
                print("[Result]\tEntropy:\t" + str(entropy))

                results = [strict_collision, entropy, eval_value_total] + list(eval_value_compositions)
                self.tools_data.ResultsSaving([results])

                for each_AGV_ID in new_paths.keys():
                    self.AGVs[each_AGV_ID].AddSchedule(new_paths[each_AGV_ID])

                self.new_orders = []

                # Save on file
                self.tools_data.ResultsPathSaving(self.tools.TotalPathHistory())
        
        # Movement --------------------------------------------------
        # AGV updates
        shelf_occupancy = col.defaultdict(lambda: ())
        self.AGV_pos_curr = col.defaultdict(lambda: (0,0))
        
        for each_AGV_ID, each_AGV_Object in self.AGVs.items():
            each_AGV_pos, each_shelf_occupancy = each_AGV_Object.Move()
            self.AGV_pos_curr[each_AGV_ID] = each_AGV_pos
            shelf_occupancy.update(each_shelf_occupancy)

        # Collision Checking
        collision_AGVs, collision = self.tools.CollisionTest_Strict_Moving(self.AGV_pos_pre,
                                                                           self.AGV_pos_curr)
        for each_AGV_ID in self.AGVs:
            if each_AGV_ID in collision_AGVs:
                self.AGVs[each_AGV_ID].ColorUpdate(collision=True)
            else:
                self.AGVs[each_AGV_ID].ColorUpdate()
        self.AGV_pos_pre = self.AGV_pos_curr

        # Shelves update
        for each_shelf_ID, each_shelf_Object in self.shelves.items():
            each_shelf_Object.update(shelf_occupancy[each_shelf_ID])
