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
import copy as cp
import itertools as itt
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
    def Q_Learning(self, _new_schedules, num_episodes = 1000, discount_factor = 1.0, _alpha = 0.6, epsilon = 0.1, num_actions = 4):
        print("[Path Planning]\t Q-Learning starting")
        
        AGVs_Q_table = {}

        # Get grid map to 2d map
        w_map = self.tools.GetWMap()
        for each_AGVs in self.AGVs:
            pos = self.AGVs[each_AGVs].GetCurrentPos()
            self.tools.UpdateWMap(w_map, 'AGV', pos, AGV_ID = each_AGVs)

        for each_new_schedules in _new_schedules:
            print(each_new_schedules)
            Q_table = col.defaultdict(lambda: np.zeros(num_actions))
            policy  = self.Q_Learning_Epsilon_Greedy_Policy(Q_table, epsilon, num_actions)
            AGVs_Q_table[each_agv] = (policy, Q_table)

        reset_map = cp.deepcopy(w_map)

        for each_episodes in range(num_episodes):
            w_map = cp.deepcopy(reset_map)

            for each_AGVs_Q_table in AGVs_Q_table:
                for t in itt.count():
                    action_probs = policy(str())
                    break
                
        self.print_wmap(w_map)
        
        return [(list(self.AGVs.keys())[0], [(2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12)])]

    def Q_Learning_Epsilon_Greedy_Policy(self, _Q_table, _epsilon, _num_actions):
        def policy_funcion(state):
            action_probs = np.ones(_num_actions, dtype = float) * _epsilon / _num_actions

            best_action = np.argmax(_Q_table[state])
            action_probs[best_action] += (1.0 - _epsilon)
            return action_probs
        return policy_funcion
        
    def print_wmap(self, w_map):
        w = len(w_map)
        h = len(w_map[0])
        print(h)
        for each_h in range(h):
            row = ''
            for each_w in range(w):
                row += str(w_map[each_w][each_h]) + '\t'
            print(row)
        
    
    #--------------------------------------------------
    
    # Update
    def Update(self, _new_schedules):
        new_paths = []
        
        if self.path_planning_type == "Q_Learning":
            new_paths = self.Q_Learning(_new_schedules)
            
        return new_paths
