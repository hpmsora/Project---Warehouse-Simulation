###############################
#
# Algorithms - Evaluation
#
# Won Yong Ha
#
#
###############################

class AlgorithmsEvaluation():

    AGVs = None
    shelves = None
    EvaluationType = ""
    
    # Internal Variables
    tools = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _EvaluationType):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.EvaluationType = _EvaluationType

    # Balance Include
    def General_n_Balance(self):
        pass
