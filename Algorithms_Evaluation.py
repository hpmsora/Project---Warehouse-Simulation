###############################
#
# Algorithms - Evaluation
#
# Won Yong Ha
#
# V.1.3 Parallization
# V.1.2 Collision evaluation edited
# V.1.1 Collision evaluation added
# V.1.0 General evaluation
#
###############################

import sys
import cupy as cp
import Algorithms_Evaluation_Collision as AlgEvalColl

import time as t ###########

class Algorithms_Evaluation():

    AGVs = None
    shelves = None
    evaluation_type = None
    
    # Internal Variables
    tools = None
    variables_type = None
    eval_collision = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _evaluation_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.evaluation_type = _evaluation_type

        if self.evaluation_type == "General_n_Balance":
            self.variables_type = ("Total", ("TT", "TTC", "BU"))
        elif self.evaluation_type == "General_n_Balance_n_Collision":
            self.variables_type = ("Total", ("TT", "TTC", "BU", "CI"))
            self.eval_collision = AlgEvalColl.Algorithms_Evaluation_Collision(self.tools)
        else:
            self.variables_type = ("Total", ("Total"))

    #--------------------------------------------------
    
    # Balance include
    def General_n_Balance(self, _new_path, length_only = True):
        ITC = {}
        max_ITC = 1
        min_ITC = sys.maxsize
        total_cost = 0
        max_order = 0
        total_order = 0
        
        for each_AGV_ID in _new_path.keys():
            each_AGV_len_schedule = 0
            each_AGV_num_orders = 0
            each_AGV_len_schedule, each_num_order, _ = _new_path[each_AGV_ID]

            if length_only:
                each_AGV_len_schedule, each_num_order, _ = _new_path[each_AGV_ID]
                each_AGV_num_orders = each_num_order
            else:
                each_path = _new_path[each_AGV_ID]
                for each_pos_path in each_path:
                    if len(each_pos_path) == 3:
                        each_AGV_num_orders += 1
                    each_AGV_len_schedule += 1
                    
            cost = each_AGV_len_schedule + each_AGV_num_orders
            ITC[each_AGV_ID] = cost
            
            if each_AGV_num_orders > max_order:
                max_order = each_AGV_num_orders
            total_order += each_AGV_num_orders
        
        for each_key, each_value in ITC.items():

            if each_value > max_ITC:
                max_ITC = each_value
            if each_value < min_ITC:
                min_ITC = each_value
            total_cost += each_value

        TT = max_ITC
        TTC = total_cost
        BU = min_ITC / max_ITC

        value = max_order/TT + total_order/TTC + BU
        return (value, (TT, TTC, BU))

    # Balance and collision include
    def General_n_Balance_n_Collision(self,
                                      _new_path,
                                      length_only = True,
                                      GPU_accelerating = False,
                                      GPU_accelerating_data = None,
                                      matrix_data = None):
        ITC = {}
        max_ITC = 1
        min_ITC = sys.maxsize
        total_cost = 0
        max_order = 0
        total_order = 0

        standard_index = self.tools.GetWidth()**2 + self.tools.GetHeight()**2

        # Parallelization
        if GPU_accelerating and length_only:
            n_AGV, population_size = GPU_accelerating_data

            T_matrix, S_matrix = matrix_data

            T_matrix = cp.array(T_matrix)
            S_matrix = cp.array(S_matrix)

            ITC_matrix = cp.reshape(cp.dot(T_matrix, cp.array([[1],[1]])), (population_size, n_AGV))
            O_matrix = cp.reshape(cp.dot(T_matrix, cp.array([[0],[1]])), (population_size, n_AGV))
            TC_matrix = cp.reshape(cp.dot(ITC_matrix, cp.ones((n_AGV, 1))), (population_size))
            TO_matrix = cp.reshape(cp.dot(O_matrix, cp.ones((n_AGV, 1))), (population_size))

            max_ITC_matrix = cp.amax(ITC_matrix, axis=1)
            min_ITC_matrix = cp.amin(ITC_matrix, axis=1)
            max_order_matrix = cp.amax(O_matrix, axis=1)

            _, n_order_points, _  = S_matrix.shape
            
            t_m = cp.reshape(cp.dot(S_matrix, cp.array([[[1],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            x_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[1],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            y_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[0],[1]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            
            d_m = cp.sum(cp.sqrt(cp.square(t_m - cp.transpose(t_m, (0, 2, 1)))
                                 + cp.square(x_m - cp.transpose(x_m, (0, 2, 1)))
                                 + cp.square(y_m - cp.transpose(y_m, (0, 2, 1)))),
                         (1,2))

            d_m_max = cp.multiply(cp.sqrt(cp.add(cp.square(cp.subtract(cp.amax(t_m, (1, 2)),
                                                                       cp.amin(t_m, (1, 2)))),
                                                 standard_index)),
                                  (n_order_points**2))
            
            G1 = max_order_matrix/max_ITC_matrix
            G2 = TO_matrix/TC_matrix
            BU = min_ITC_matrix/max_ITC_matrix
            CI = cp.multiply(d_m/d_m_max, BU)
            
            E_matrix = G1 + G2 + BU + CI
            
            cp.cuda.Stream.null.synchronize()

            return (list(E_matrix), (list(max_ITC_matrix), list(TC_matrix), list(BU), list(CI)))

        # Non-Paralleization
        else:
            for each_AGV_ID in _new_path.keys():
                each_AGV_len_schedule = 0
                each_AGV_num_orders = 0

                if length_only:
                    each_AGV_len_schedule, each_num_order, each_order_list = _new_path[each_AGV_ID]
                    each_AGV_num_orders = each_num_order
                else:
                    each_path = _new_path[each_AGV_ID]
                    for each_pos_path in each_path:
                        if len(each_pos_path) == 3:
                            each_AGV_num_orders += 1
                        each_AGV_len_schedule += 1
                    
                cost = each_AGV_len_schedule + each_AGV_num_orders
                ITC[each_AGV_ID] = cost
                
                if each_AGV_num_orders > max_order:
                    max_order = each_AGV_num_orders
                total_order += each_AGV_num_orders
        
            for _, each_value in ITC.items():
                
                if each_value > max_ITC:
                    max_ITC = each_value
                if each_value < min_ITC:
                    min_ITC = each_value
                total_cost += each_value

            TT = max_ITC
            TTC = total_cost
            BU = min_ITC / max_ITC
            CI = self.eval_collision.Update(_new_path, length_only) * BU
            
            G1 = max_order/TT
            G2 = total_order/TTC
            
            value = G1 + G2 + BU + CI
            return (value, (TT, TTC, BU, CI))

    #--------------------------------------------------

    # Get evaluation variable information
    def GetVariablesType(self):
        return self.variables_type

    # Update
    def Update(self, _new_path, length_only = False, GPU_accelerating = False, GPU_accelerating_data = None, matrix_data = None):
        #print("[Evaluating]\t Processing ...")
        if self.evaluation_type == "General_n_Balance":
            return self.General_n_Balance(_new_path, length_only = length_only)
        if self.evaluation_type == "General_n_Balance_n_Collision":
            return self.General_n_Balance_n_Collision(_new_path,
                                                      length_only = length_only,
                                                      GPU_accelerating = GPU_accelerating,
                                                      GPU_accelerating_data = GPU_accelerating_data,
                                                      matrix_data = matrix_data)
