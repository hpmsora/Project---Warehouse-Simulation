###############################
#
# Algorithms - Path Planning
#
# Won Yong Ha
#
# V.1.0
# Collision with wall free only.
#
###############################

import numpy as np
import copy as cp
import itertools as itt
import collections as col

import plotting as plt

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
    def Q_Learning(self, _new_schedules, num_episodes = 1000, discount_factor = 1.0, alpha = 0.6, epsilon = 0.1, num_actions = 4):
        print("[Path Planning]\t Q-Learning starting")

        AGVs_paths = []
        
        AGVs_Q_table = {}
        AGVs_Order = []

        # Get grid map to 2d map
        w_map = self.tools.GetWMap()

        self.tools.UpdateWMapShelves(w_map)

        #------- For future multi-agents path planning
        #for each_AGVs in self.AGVs:
        #    pos = self.AGVs[each_AGVs].GetCurrentPos()
        #    self.tools.UpdateWMap(w_map, 'AGV', pos, AGV_ID = each_AGVs)
        #-------

        for each_AGV_ID, each_new_schedules in _new_schedules:
            each_AGV = self.AGVs[each_AGV_ID]
            Q_tables = []
            
            for each_each_new_schedules_ID, each_each_new_schedules, _each_each_depot in each_new_schedules:
                for each_each_each_new_schedules in each_each_new_schedules:

                    # Heading to target
                    Q_table = col.defaultdict(lambda: np.zeros(num_actions))
                    policy  = self.Q_Learning_Epsilon_Greedy_Policy(Q_table, epsilon, num_actions)
                    Q_tables.append(((each_each_new_schedules_ID, each_each_each_new_schedules), policy, Q_table))
                    
                    # Heading to depot
                    Q_table = col.defaultdict(lambda: np.zeros(num_actions))
                    policy  = self.Q_Learning_Epsilon_Greedy_Policy(Q_table, epsilon, num_actions)
                    Q_tables.append((('Depot', _each_each_depot), policy, Q_table))
            
            AGVs_Q_table[each_AGV_ID] = (each_AGV.GetLastScheduledPos(), Q_tables)
            AGVs_Order.append(each_AGV_ID)

        reset_map = cp.deepcopy(w_map)
        
        # Movements
        for each_AGVs_ID in AGVs_Order:
            AGV_path = []
            
            each_last_pos, each_Q_table = AGVs_Q_table[each_AGVs_ID]
            starting_state = each_last_pos
            
            for each_target, each_each_policy, each_each_Q_table in each_Q_table:
                target = []
                target_order, target_ID = each_target
                
                if target_order == "Depot":
                    target += self.tools.GetDepotsByID(target_ID)
                else:
                    target += self.tools.GetShelvesDepotsPosByID(target_ID)

                stats = plt.EpisodeStats(
                    episode_lengths = np.zeros(num_episodes),
                    episode_rewards = np.zeros(num_episodes))
                
                # Episodes
                for each_episodes in range(num_episodes):
                    w_map = cp.deepcopy(reset_map)
                    state = starting_state
                    
                    for t in itt.count():
                        action_probs = each_each_policy(state)
                        action = np.random.choice(np.arange(len(action_probs)), p =action_probs)

                        next_state, reward, done = self.tools.Step_Action(state, action, w_map, target)

                        stats.episode_rewards[each_episodes] += reward
                        stats.episode_lengths[each_episodes] = t

                        next_action = np.argmax(each_each_Q_table[next_state])
                        td_target = reward + discount_factor * each_each_Q_table[next_state][next_action]
                        td_delta = td_target - each_each_Q_table[state][action]
                        each_each_Q_table[state][action] += alpha * td_delta

                        if done:
                            break
                        state = next_state
                path = self.tools.GetPathByQTable(each_each_Q_table, starting_state, target)
                state = path[-1]
                AGV_path += path
            AGVs_paths.append((each_AGVs_ID, AGV_path))
        return AGVs_paths

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
