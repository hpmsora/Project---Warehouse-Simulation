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
    MAX_EPOCH = 1000
    
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
        
    # Genetic Algorithm
    def GeneticAlgorithm(self,_max_epoch):
        
        eval_value = self.evaluation_algorithm.Update()
        epoch_count = 0
        
        while epoch_count < _max_epoch:
            epoch_count += 1
        print("Done")
        new_paths = self.path_planning_algorithm.Update([])
            
    # Update
    def Update(self):
        if self.scheduling_type == "Genetic":
            self.GeneticAlgorithm(self.MAX_EPOCH)
