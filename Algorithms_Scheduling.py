###############################
#
# Algorithms - Scheduling
#
# Won Yong Ha
#
#
###############################

import Algorithms_Evaluation as AlgEval

class Algorithms_Scheduling():

    AGVs = None
    shelves = None
    scheduling_type = ""
    
    # Internal Variables
    tools = None
    evaluation_algorithm = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _scheduling_type, _evaluation_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.scheduling_type = _scheduling_type
        self.SetEvaluationAlgorithm(_evaluation_type)

    # Set evaluation algorithm
    def SetEvaluationAlgorithm(self, _evaluation_type):
        self.evaluation_algorithm = AlgEval.Algorithms_Evaluation(self.AGVs, self.shelves, self.tools, _evaluation_type)
        
    # Genetic Algorithm
    def GeneticAlgorithm(self,_MaxEpoch):
        pass

    # Update
    def Update(self):
        if self.scheduling_type == "Genetic":
            eval_value = self.evaluation_algorithm.Update()
            print(eval_value)
