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
        self.tools = _tools

        self.scheduling_type = _scheduling_type
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
        
        while epoch_count < _max_epoch:
            epoch_count += 1
        print("[Scheduling]\t Genetic algorithm scheduling done.")

        #---------------------------
        # Example hard coding
        new_schedules = []
        num_AGVs = 0

        DepotTypeID = 421
        
        for each_AGV in self.AGVs:
            new_schedules.append((each_AGV, []))
            num_AGVs += 1
        
        for index, each_new_order in enumerate(_new_orders):
            order_num, orders = each_new_order
            AGVs_index = index % num_AGVs
            new_schedules[AGVs_index][1].append((order_num, orders, DepotTypeID)) # 3 -> depot ID
        #---------------------------
        
        new_paths = self.path_planning_algorithm.Update(new_schedules)
        return new_paths
            
    # Update
    def Update(self, _new_orders):
        if self.scheduling_type == "Genetic":
            new_paths = self.GeneticAlgorithm(_new_orders, self.MAX_EPOCH)

        for each_AGV, each_new_path in new_paths:
            self.AGVs[each_AGV].AddSchedule(each_new_path)
