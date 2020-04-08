###############################
#
# Algorithms - Path Planning
#
# Won Yong Ha
#
# V.1.1 - Parallel computing
# V.1.0 - Collision with wall free only.
#
###############################

import numpy as np
import copy as cp
import itertools as itt
import collections as col

import multiprocessing as mp

class Algorithms_PlathPlanning():

    AGVs = None
    shelves = None
    path_planning_type = ""
    
    # Internal Variables
    tools = None
    reserve_paths = {} # Key: (pos(START), pos(END))  Value: (length, [Path])

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _path_planning_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.path_planning_type = _path_planning_type
        
        self.tools = _tools
        self.reserve_paths = {}

    # Determine reserve path is full
    def Is_Reserve_Full(self):
        num_shelves = len(self.shelves)
        num_AGVs = len(self.AGVs)
        if len(self.reserve_paths) >= num_shelves * 2 + num_AGVs:
            return True
        else:
            return False

    #--------------------------------------------------

    # Q-Learning
    def Q_Learning(self,
                   _new_schedules,
                   num_episodes = 1000,
                   discount_factor = 1.0,
                   alpha = 0.6,
                   epsilon = 0.1,
                   num_actions = 4,
                   last_positions = col.defaultdict(lambda: ())):
        #print("[Path Planning]\t Q-Learning starting")

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

        # Q-table initializing
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

        reset_w_map = cp.deepcopy(w_map)

        # Movements
        #-------Multiprocessing-Start
        jobs = []
        manager1 = mp.Manager()
        manager2 = mp.Manager()
        AGVs_paths = manager1.dict()
        new_paths = manager2.dict()
        
        for each_AGVs_ID in AGVs_Order:
            last_position = last_positions[each_AGVs_ID]
            
            p = mp.Process(target=self.Q_Learning_AGV,
                           args=(each_AGVs_ID,
                                 last_position,
                                 AGVs_Q_table,
                                 reset_w_map,
                                 num_episodes,
                                 discount_factor,
                                 alpha,
                                 self.reserve_paths,
                                 AGVs_paths,
                                 new_paths))
            jobs.append(p)
            p.start()
        for each_jobs in jobs:
            each_jobs.join()

        self.reserve_paths.update(new_paths)
        #-------Multiprocessing-End
        
        return AGVs_paths

    # Q-Learning greedy policy
    def Q_Learning_Epsilon_Greedy_Policy(self, _Q_table, _epsilon, _num_actions):
        def policy_funcion(state):
            action_probs = np.ones(_num_actions, dtype = float) * _epsilon / _num_actions

            best_action = self.tools.Arg_Maximum(_Q_table[state])
            action_probs[best_action] += (1.0 - _epsilon)
            return action_probs
        return policy_funcion

    # Q-Learning each job function
    def Q_Learning_AGV(self,
                       _each_AGVs_ID,
                       _each_AGVs_last_position,
                       _AGVs_Q_table,
                       _reset_w_map,
                       _num_episodes,
                       _discount_factor,
                       _alpha,
                       _reserve_paths,
                       _AGVs_paths,
                       _new_paths):
        AGV_path = []
            
        each_last_pos, each_Q_table = _AGVs_Q_table[_each_AGVs_ID]

        # Last position check
        if _each_AGVs_last_position == ():
            starting_state = each_last_pos
        else:
            starting_state = _each_AGVs_last_position
            
        for each_target, each_each_policy, each_each_Q_table in each_Q_table:
            target = []
            target_order, target_ID = each_target
            
            if target_order == "Depot":
                target += self.tools.GetDepotsByID(target_ID)
            else:
                target += self.tools.GetShelvesDepotsPosByID(target_ID)
    
            starting_state_posX, starting_state_posY, *order = starting_state
            starting_state_pos = (starting_state_posX, starting_state_posY)
            target_pos = target[0]

            path_key = (starting_state_pos, target_pos)
            path_key_reverse = (target_pos, starting_state_pos)

            if path_key in _reserve_paths:
                _, path = _reserve_paths[path_key]
            elif path_key_reverse in _reserve_paths:
                _, path = _reserve_paths[path_key_reverse]
                path.reverse()
            else:
                # Episodes
                for each_episodes in range(_num_episodes):
                    w_map = cp.deepcopy(_reset_w_map)
                    state = starting_state

                    for t in itt.count():
                        action_probs = each_each_policy(state)
                        action = np.random.choice(np.arange(len(action_probs)), p = action_probs)
                        
                        next_state, reward, done = self.tools.Step_Action(state, action, w_map, target)
                        
                        next_action = self.tools.Arg_Maximum(each_each_Q_table[next_state])
                        td_target = reward + _discount_factor * each_each_Q_table[next_state][next_action]
                        td_delta = td_target - each_each_Q_table[state][action]
                        each_each_Q_table[state][action] += _alpha * td_delta
                        
                        if done:
                            break
                        state = next_state
                path = self.tools.GetPathByQTable(each_each_Q_table, starting_state, target, each_target)

                _new_paths[path_key] = (len(path), path)

            if not target_order == 'Depot':
                posX, posY, *order = path[-1]
                path[-1] = (posX, posY, each_target)

            starting_state = path[-1]
            AGV_path += path
            
            each_each_Q_table.clear() # Clear memory

        #print("[Path Planning]\t Planning AGV - " + str(_each_AGVs_ID) + " Finished!")

        _AGVs_paths[_each_AGVs_ID] = AGV_path
        
    # Q-Learning length only
    def Q_Learning_Length_Only(self, _new_schedules):
        new_paths_length = col.defaultdict(lambda: (0,0))

        for each_AGV_ID, each_AGV_schedule in _new_schedules:
            each_AGV_path_length = 0
            each_AGV_order_num = 0
            
            last_position = self.AGVs[each_AGV_ID].GetLastScheduledPos()

            for order_ID, shelf_IDs, depot_ID in each_AGV_schedule:
                for each_shelf_IDs in shelf_IDs:
                    each_AGV_order_num += 1

                    # To the shelf
                    each_shelf_pos = self.tools.GetShelvesDepotsPosByID(each_shelf_IDs)[0]
                    path_key = (last_position, each_shelf_pos)
                    reverse_path_key = (each_shelf_pos, last_position)

                    if path_key in self.reserve_paths:
                        each_AGV_path_length += self.reserve_paths[path_key][0]
                    elif reverse_path_key in self.reserve_paths:
                        each_AGV_path_length += self.reserve_paths[reverse_path_key][0]
                    else:
                        last_positions = col.defaultdict(lambda: ())
                        last_positions[each_AGV_ID] = last_position
                        path = self.Q_Learning([(each_AGV_ID, [(order_ID, [each_shelf_IDs], depot_ID)])],
                                               last_positions=last_positions)
                        each_AGV_path_length += self.reserve_paths[path_key][0]

                    last_position = each_shelf_pos

                    # To the depot
                    each_depot_pos = self.tools.GetDepotsByID(depot_ID)[0]
                    path_key = (last_position, each_depot_pos)
                    reverse_path_key = (each_depot_pos, last_position)

                    if path_key in self.reserve_paths:
                        each_AGV_path_length += self.reserve_paths[path_key][0]
                    elif reverse_path_key in self.reserve_paths:
                        each_AGV_path_length += self.reserve_paths[reverse_path_key][0]
                    else:
                        last_positions = col.defaultdict(lambda: ())
                        last_positions[each_AGV_ID] = last_position
                        path = self.Q_Learning([(each_AGV_ID, [(order_ID, [each_shelf_IDs], depot_ID)])],
                                               last_positions=last_positions)
                        each_AGV_path_length += self.reserve_paths[path_key][0]

                    last_position = each_depot_pos
            new_paths_length[each_AGV_ID] = (each_AGV_path_length, each_AGV_order_num)
        return new_paths_length
                    
    #--------------------------------------------------
    
    # Update
    def Update(self, _new_schedules, length_only = False):
        new_paths = []
        
        if self.path_planning_type == "Q_Learning":
            if length_only:
                new_paths = self.Q_Learning_Length_Only(_new_schedules)
            else:
                new_paths = self.Q_Learning(_new_schedules)
        return new_paths
