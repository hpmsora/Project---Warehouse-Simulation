###############################
#
# Algorithms - Evaluation
#
# Won Yong Ha
#
# V.1.0
#
###############################

import sys

class Algorithms_Evaluation():

    AGVs = None
    shelves = None
    EvaluationType = ""
    
    # Internal Variables
    tools = None
    variables_type = []

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _EvaluationType):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.tools = _tools

        self.EvaluationType = _EvaluationType

        if self.EvaluationType == "General_n_Balance":
            self.variables_type = ("Total", ("TT", "TTC", "BU"))
        else:
            self.variables_type = ("Total")

    #--------------------------------------------------
    
    # Balance Include
    def General_n_Balance(self, _new_path, length_only = False):
        ITC = {}
        max_ITC = 1
        min_ITC = sys.maxsize
        total_cost = 0
        max_order = 0
        total_order = 0

        for each_AGV_ID in _new_path.keys():
            each_AGV_len_schedule = 0
            each_AGV_num_orders = 0

            if length_only:
                each_path, each_num_order = _new_path[each_AGV_ID]
                each_AGV_len_schedule = each_path
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
        return (value, (max_order/TT, total_order/TTC, BU))

    #--------------------------------------------------

    # Get evaluation variable information
    def GetVariablesType(self):
        return self.variables_type

    # Update
    def Update(self, _new_path, length_only = False):
        #print("[Evaluating]\t Processing ...")
        if self.EvaluationType == "General_n_Balance":
            return self.General_n_Balance(_new_path, length_only = length_only)
