###############################
#
# Algorithms - Scheduling
#
# Won Yong Ha
#
# V.1.0
#
###############################

import Algorithms_PathPlanning as AlgPath
import Algorithms_Evaluation as AlgEval

import numpy as np
import random as rd

class Algorithms_Scheduling():

    AGVs = None
    shelves = None
    scheduling_type = ""

    # Fixed Variable
    MAX_EPOCH = 1
    
    # Internal Variables
    tools = None
    path_planning_algorithm = None
    evaluation_algorithm = None

    # Constructor
    def __init__(self, _AGVs, _shelves, _tools, _scheduling_type, _path_planning_type, _evaluation_type):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.scheduling_type = _scheduling_type

        self.tools = _tools
        self.path_planning_algorithm = None
        self.evaluation_algorithm = None
        self.SetPathPlanningAlgorithm(_path_planning_type)
        self.SetEvaluationAlgorithm(_evaluation_type)

    # Set path planning algorithm
    def SetPathPlanningAlgorithm(self, _path_planning_type):
        self.path_planning_algorithm = AlgPath.Algorithms_PlathPlanning(self.AGVs, self.shelves, self.tools, _path_planning_type)

    # Set evaluation algorithm
    def SetEvaluationAlgorithm(self, _evaluation_type):
        self.evaluation_algorithm = AlgEval.Algorithms_Evaluation(self.AGVs, self.shelves, self.tools, _evaluation_type)

    #--------------------------------------------------
    
    # Genetic Algorithm
    def GeneticAlgorithm(self, _new_orders, _max_epoch):
        
        #eval_value = self.evaluation_algorithm.Update()
        epoch_count = 0

        print("[Scheduling]\t New orders for scheduling is: " + str(_new_orders))

        
        new_schedules = []  # [(AGV ID, [(order ID, [order, ...], depot ID), ...]), ...]
        num_AGVs = 0

        # Add depot place to new orders
        depot_type_ID = 421  # One depot place for Version 1.0
        for index, each_new_orders in enumerate(_new_orders):
            order_num, orders = each_new_orders
            _new_orders[index] = (order_num, orders, depot_type_ID)
            
        # Initial random scheduling 
        for each_AGV in self.AGVs:
            new_schedules.append((each_AGV, []))
            num_AGVs += 1
        for index, each_new_order in enumerate(_new_orders):
            AGVs_index = index % num_AGVs
            new_schedules[AGVs_index][1].append(each_new_order)

        print(new_schedules)
        new_paths = self.path_planning_algorithm.Update(new_schedules)

        # Evaluation process
        eval_value = self.evaluation_algorithm.Update(new_paths)

        print(_new_orders)
        # Genetic algorithm start
        if True: #self.path_planning_algorithm.Is_Reserve_Full():

            genes = []
            populations = []
            populations_schedules = []
            generation = 0
            population_size = 10
            AGVs_order = []

            AGVs_cuts = []
            for each_AGVs in self.AGVs:
                AGVs_cuts.append(("AGV", [], 0))
                AGVs_order.append(each_AGVs)
            genes += _new_orders + AGVs_cuts[:-1]

            genes_size = len(genes)

            # Initial population
            for _ in range(population_size):
                populations.append(rd.sample(genes, k=genes_size))

            for each_populations in populations:
                each_new_schedule = self.GeneticAlgorithm_PopulationToNewSchedules(each_populations, AGVs_order)
                each_new_path = self.path_planning_algorithm.Update(each_new_schedule)
                each_eval_value, TT, TTC, BU = self.evaluation_algorithm.Update(each_new_path)
                populations_schedules.append((each_eval_value, each_new_schedule))
            populations_schedules = sorted(populations_schedules, reverse=True)
            print(populations_schedules)
            
            while epoch_count < _max_epoch:
                
            
                epoch_count += 1
        print("[Scheduling]\t Genetic algorithm scheduling done.")

        print(eval_value)
        
        return new_paths
    def GeneticAlgorithm_PopulationToNewSchedules(self, _population, _AGVs_order):
        new_schedules = []
        AGVs_order_count = 0
        each_AGV_schedule = (_AGVs_order[AGVs_order_count], [])
        for each_population in _population:
            p_ID, p_object, *p_depot = each_population
            if p_ID == "AGV":
                new_schedules.append(each_AGV_schedule)
                AGVs_order_count += 1
                each_AGV_schedule = (_AGVs_order[AGVs_order_count], [])
            else:
                each_AGV_schedule[1].append(each_population)
        new_schedules.append(each_AGV_schedule)
        return new_schedules
                
                
            
    #--------------------------------------------------
            
    # Update
    def Update(self, _new_orders):
        if self.scheduling_type == "Genetic":
            new_paths = self.GeneticAlgorithm(_new_orders, self.MAX_EPOCH)
            
        return new_paths
