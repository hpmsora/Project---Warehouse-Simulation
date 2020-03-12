###############################
#
# Algorithms - Scheduling
#
# Won Yong Ha
#
#
###############################

class AlgorithmsScheduling():

    AGVs = None
    shelves = None
    SchedulingType = ""
    
    # Internal Variables
    tools = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _SchedulingType):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.SchedulingType = _SchedulingType
    
    # Genetic Algorithm
    def GeneticAlgorithm(_MaxEpoch):
        pass
        
