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
import numpy as np
import cupy as cp
import Algorithms_Evaluation_Collision as AlgEvalColl

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
        elif self.evaluation_type == "General_n_Balance_n_Collision_Eff":
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
            
            t_m = cp.reshape(cp.dot(S_matrix, cp.array([[[1],[0],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            x_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[1],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            y_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[0],[1],[0]]]*n_order_points)),
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

    # Balance and collision with effective distance include
    def General_n_Balance_n_Collision_Eff(self,
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
            S_matrix = cp.array(np.array(S_matrix).astype(float))

            ITC_matrix = cp.reshape(cp.dot(T_matrix, cp.array([[1],[1]])), (population_size, n_AGV))
            O_matrix = cp.reshape(cp.dot(T_matrix, cp.array([[0],[1]])), (population_size, n_AGV))
            TC_matrix = cp.reshape(cp.dot(ITC_matrix, cp.ones((n_AGV, 1))), (population_size))
            TO_matrix = cp.reshape(cp.dot(O_matrix, cp.ones((n_AGV, 1))), (population_size))

            max_ITC_matrix = cp.amax(ITC_matrix, axis=1)
            min_ITC_matrix = cp.amin(ITC_matrix, axis=1)
            max_order_matrix = cp.amax(O_matrix, axis=1)
            
            _, n_order_points, _  = S_matrix.shape
            
            t_m = cp.reshape(cp.dot(S_matrix, cp.array([[[1],[0],[0],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            x_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[1],[0],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            y_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[0],[1],[0],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            l_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[0],[0],[1],[0]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            o_m = cp.reshape(cp.dot(S_matrix, cp.array([[[0],[0],[0],[0],[1]]]*n_order_points)),
                             (population_size, n_order_points, n_order_points))
            t_m_l = cp.reshape(cp.dot(S_matrix, cp.array([[[1],[0],[0],[0],[0]]])),
                               (population_size, n_order_points))

            t_m_diff = t_m - cp.transpose(t_m, (0, 2, 1))
            x_m_diff = x_m - cp.transpose(x_m, (0, 2, 1))
            y_m_diff = y_m - cp.transpose(y_m, (0, 2, 1))

            m_xy_diff = cp.absolute(x_m_diff) + cp.absolute(y_m_diff)

            m_diff = cp.absolute(t_m_diff) + m_xy_diff
            
            m_diff_l = m_diff - l_m * 2
            
            m_diff_l_sign = (cp.logical_xor(cp.sign(m_diff_l) + 1, True))

            m_diff_l_eff = cp.multiply(m_diff, m_diff_l_sign)

            m_diff_l_sign = cp.sign(m_diff_l_eff)

            m_diff_l_H = cp.multiply(cp.multiply(cp.reciprocal(m_diff_l_eff + m_diff_l_sign - 1), m_diff_l_sign),
                                     cp.log10(m_diff_l_eff + cp.absolute(m_diff_l_sign - 1)))
            
            d_m = cp.reciprocal(cp.sum(m_diff_l_H,
                                       (1,2)))

            # Occupancy test
            """
            t_m_o = t_m + o_m - 1
            m_diff_o = cp.absolute(t_m_o - cp.transpose(t_m_o, (0, 2, 1))) - o_m - 1
            m_occupancy = (cp.logical_xor(cp.sign(m_diff_o) + 1, True))
            
            m_idn = cp.identity(n_order_points)
            OT = cp.prod(cp.logical_or(m_xy_diff,
                                       cp.logical_not(m_occupancy - m_idn)),
                         (1,2))
            """
            
            G1 = max_order_matrix/max_ITC_matrix
            G2 = TO_matrix/TC_matrix
            BU = min_ITC_matrix/max_ITC_matrix
            CI = cp.multiply(d_m, BU) # d_m * 0.1
            
            E_matrix = G1 + G2 + BU + CI
            
            cp.cuda.Stream.null.synchronize()

            return (list(E_matrix), (list(max_ITC_matrix), list(TC_matrix), list(BU), list(CI)))

        # Non-Paralleization
        else:
            print("[Scheduling] Must be use GPU to calculate")
            
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
            CI = 0
            
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
        if self.evaluation_type == "General_n_Balance_n_Collision_Eff":
            return self.General_n_Balance_n_Collision_Eff(_new_path,
                                                      length_only = length_only,
                                                      GPU_accelerating = GPU_accelerating,
                                                      GPU_accelerating_data = GPU_accelerating_data,
                                                      matrix_data = matrix_data)
