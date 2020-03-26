###############################
#
# Algorithms - Scheduling
#
# Won Yong Ha
#
# V.1.0
#
###############################

import Algorithms_PathPlanning as AlgPath
import Algorithms_Evaluation as AlgEval

class Algorithms_Scheduling():

    AGVs = None
    shelves = None
    scheduling_type = ""

    # Fixed Variable
    MAX_EPOCH = 1
    
    # Internal Variables
    tools = None
    path_planning_algorithm = None
    evaluation_algorithm = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _scheduling_type, _path_planning_type, _evaluation_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.scheduling_type = _scheduling_type

        self.tools = _tools
        self.path_planning_algorithm = None
        self.evaluation_algorithm = None
        self.SetPathPlanningAlgorithm(_path_planning_type)
        self.SetEvaluationAlgorithm(_evaluation_type)

    # Set path planning algorithm
    def SetPathPlanningAlgorithm(self, _path_planning_type):
        self.path_planning_algorithm = AlgPath.Algorithms_PlathPlanning(self.AGVs, self.shelves, self.tools, _path_planning_type)

    # Set evaluation algorithm
    def SetEvaluationAlgorithm(self, _evaluation_type):
        self.evaluation_algorithm = AlgEval.Algorithms_Evaluation(self.AGVs, self.shelves, self.tools, _evaluation_type)

    #--------------------------------------------------
    
    # Genetic Algorithm
    def GeneticAlgorithm(self, _new_orders, _max_epoch):
        
        #eval_value = self.evaluation_algorithm.Update()
        epoch_count = 0

        print("[Scheduling]\t New orders for scheduling is: " + str(_new_orders))

        
        new_schedules = []  # [(AGV ID, [(order ID, [order, ...], depot ID), ...]), ...]
        num_AGVs = 0

        # Add depot place to new orders
        depot_type_ID = 421  # One depot place for Version 1.0
        for index, each_new_orders in enumerate(_new_orders):
            order_num, orders = each_new_orders
            _new_orders[index] = (order_num, orders, depot_type_ID)
            
        # Initial random scheduling 
        for each_AGV in self.AGVs:
            new_schedules.append((each_AGV, []))
            num_AGVs += 1
        for index, each_new_order in enumerate(_new_orders):
            AGVs_index = index % num_AGVs
            new_schedules[AGVs_index][1].append(each_new_order)

        new_paths = self.path_planning_algorithm.Update(new_schedules)

        # Evaluation Process
        eval_value = self.evaluation_algorithm.Update(new_paths)

        is_full_reserved_path = self.path_planning_algorithm.Is_Reserve_Full()
        if is_full_reserved_path:
            while epoch_count < _max_epoch:
                
            
                epoch_count += 1
        print("[Scheduling]\t Genetic algorithm scheduling done.")

        print(eval_value)
        
        return new_paths
            
    # Update
    def Update(self, _new_orders):
        if self.scheduling_type == "Genetic":
            new_paths = self.GeneticAlgorithm(_new_orders, self.MAX_EPOCH)
            
        return new_paths
