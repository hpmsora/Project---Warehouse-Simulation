###############################
#
# Algorithms - Evaluation
#
# Won Yong Ha
#
# V.1.0
#
###############################

class Algorithms_Evaluation():

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

    #--------------------------------------------------
    
    # Balance Include
    def General_n_Balance(self):
        ITC = {}
        max_ITC = 1
        min_ITC = 0
        total_cost = 0
        max_order = 0
        total_order = 0

        for each_AGV in self.AGVs.values():
            key = each_AGV.GetID()
            print(key)
            each_AGV_num_orders = len(each_AGV.GetOrder())
            cost = len(each_AGV.GetSchedule()) + each_AGV_num_orders
            ITC[key] = cost
            
            if each_AGV_num_orders > max_order:
                max_order = each_AGV_num_orders
            total_order += each_AGV_num_orders
        
        for each_key in ITC.keys():
            value = ITC[each_key]

            if value > max_ITC:
                max_ITC = value
            elif value < min_ITC:
                min_ITC = value
            total_cost += value

        TT = max_ITC
        TTC = total_cost
        BU = min_ITC / max_ITC

        return max_order/TT + total_order/TTC + BU

    #--------------------------------------------------

    # Update
    def Update(self):
        if self.EvaluationType == "General_n_Balance":
            return self.General_n_Balance()
