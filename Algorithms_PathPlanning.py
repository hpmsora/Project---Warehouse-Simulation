###############################
#
# Algorithms - Path Planning
#
# Won Yong Ha
#
# V.1.0
#
###############################

import numpy as np
import collections as col

class Algorithms_PlathPlanning():

    AGVs = None
    shelves = None
    path_planning_type = ""
    
    # Internal Variables
    tools = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _path_planning_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.path_planning_type = _path_planning_type

    #--------------------------------------------------

    # Q Learning
    def Q_Learning(self, _new_schedulings, num_episodes = 1000, discount_factor = 1.0, _alpha = 0.6, epsilon = 0.1):
        print("Q-Learning")

        
        
        for each_episodes in range(num_episodes):
            pass
        
        Q_table = col.defaultdict(lambda: np.zeros(4))
        
        
        return []
    
    #--------------------------------------------------
    
    # Update
    def Update(self, _new_schedulings):
        new_paths = []
        
        if self.path_planning_type == "Q_Learning":
            new_paths = self.Q_Learning(_new_schedulings)
            
        return new_paths