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
import copy as cp
import cupy as cpy
import random as rd
import collections as col
import operator as op

import time as t

class Algorithms_Scheduling():

    AGVs = None
    shelves = None
    scheduling_type = ""

    # Fixed Variable
    MAX_EPOCH = 100
    CROSSOVER_RATE = 0.60
    
    # Internal Variables
    tools = None
    graph_GUI = None
    max_generation = None
    population_size = None
    path_planning_algorithm = None
    evaluation_algorithm = None
    
    GPU_accelerating = None
    n_AGV = None

    depot_distribution_type = None

    # Constructor
    def __init__(self,
                 _AGVs,
                 _shelves,
                 _tools,
                 _scheduling_type,
                 _path_planning_type,
                 _evaluation_type,
                 tools_data = None,
                 graph_GUI = None,
                 depot_distribution_type = "Default"): # Defualt: Randomly preassidned
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.scheduling_type = _scheduling_type

        self.tools = _tools
        self.tools_data = tools_data
        self.graph_GUI = graph_GUI
        self.depot_distribution_type = depot_distribution_type

        
        self.max_generation = 10000
        self.population_size = 100
        self.path_planning_algorithm = None
        self.evaluation_algorithm = None
        self.SetPathPlanningAlgorithm(_path_planning_type, tools_data = self.tools_data)
        self.SetEvaluationAlgorithm(_evaluation_type)

        self.tools.SetGraphVariablesType(self.evaluation_algorithm.GetVariablesType())
        if not self.graph_GUI == None:
            self.graph_GUI.BuildGraph()

    # Set path planning algorithm
    def SetPathPlanningAlgorithm(self, _path_planning_type, tools_data = None):
        self.path_planning_algorithm = AlgPath.Algorithms_PlathPlanning(self.AGVs,
                                                                        self.shelves,
                                                                        self.tools,
                                                                        _path_planning_type,
                                                                        tools_data = tools_data)

    # Set evaluation algorithm
    def SetEvaluationAlgorithm(self, _evaluation_type):
        self.evaluation_algorithm = AlgEval.Algorithms_Evaluation(self.AGVs,
                                                                  self.shelves,
                                                                  self.tools,
                                                                  _evaluation_type)
        if _evaluation_type == "General_n_Balance_n_Collision":
            self.GPU_accelerating = True
            self.n_AGV = len(self.AGVs)
        if _evaluation_type == "General_n_Balance_n_Collision_Eff":
            self.GPU_accelerating = True
            self.n_AGV = len(self.AGVs)

    # Set reserve paths
    def SetReservePaths(self, _paths):
        self.path_planning_algorithm.SetReservePaths(_paths)

    # Order independent check
    def OrderIndependenctAndDepotDistribution(self, _new_orders, _order_independent):
        # Add defualt depot place to new orders
        if self.depot_distribution_type == 'Genetic':
            for index, each_new_orders in enumerate(_new_orders):
                order_num, orders = each_new_orders
                _new_orders[index] = (order_num, orders, None)
        elif self.depot_distribution_type == 'Min':
            depots_key_list = list(self.tools.GetDepots().keys())
            depots_list = self.tools.GetDepots()
            
            for index, each_new_orders in enumerate(_new_orders):
                order_num, orders = each_new_orders
                depots_distance_list = []
                for each_depots_key in depots_key_list:
                    each_depots_distance = 0
                    for each_orders in orders:
                        each_orders_posX, each_orders_posY = self.tools.GetShelvesDepotsPosByID(each_orders)[0]
                        for each_depots_posX, each_depots_posY in depots_list[each_depots_key]:
                            each_depots_distance += abs(each_orders_posX - each_depots_posX) + abs(each_orders_posY - each_depots_posY)
                    depots_distance_list.append((each_depots_distance/len(depots_list[each_depots_key]), each_depots_key))
                depots_place = min(depots_distance_list, key=op.itemgetter(0))
                _new_orders[index] = (order_num, orders, depots_place[1])
        else:
            depots_key_list = list(self.tools.GetDepots().keys())
            for index, each_new_orders in enumerate(_new_orders):
                order_num, orders = each_new_orders
                _new_orders[index] = (order_num, orders, rd.choice(depots_key_list))
        
        # Order independent
        if _order_independent:
            new_orders = []
            for each_orders_num, each_orders, each_depot_ID in _new_orders:
                for each_each_orders in each_orders:
                    new_orders.append((each_orders_num, [each_each_orders], each_depot_ID))
            _new_orders = new_orders

        return _new_orders

    #--------------------------------------------------
    
    # Genetic Algorithm
    def GeneticAlgorithm(self,
                         _new_orders,
                         _order_independent,
                         _max_generaion,
                         _crossover_rate,
                         GPU_accelerating = False,
                         GPU_accelerating_data = None):
        print("[Scheduling]\tGenetic algorithm")
        print("[Scheduling]\tNew orders for scheduling is: " + str(_new_orders))

        if not self.graph_GUI == None:
            self.tools.ResetGraphData()

        _new_orders = self.OrderIndependenctAndDepotDistribution(_new_orders, _order_independent)

        new_schedules = []  # [(AGV ID, [(order ID, [order, ...], depot ID), ...]), ...]
        eval_value = (0, (0)) # Initial eval data
        num_AGVs = 0
        
        # Genetic algorithm start
        if True: #self.path_planning_algorithm.Is_Reserve_Full():

            genes = []
            populations = []
            populations_schedules = []
            generation = 0
            
            AGVs_order = []
            AGVs_cuts = []

            if self.depot_distribution_type == 'Genetic':
                for each_AGVs in self.AGVs:
                    for each_depot_ID in self.tools.GetDepots():
                        AGVs_cuts.append(("AGV", [], None))
                        AGVs_order.append((each_AGVs, each_depot_ID))
            else:
                for each_AGVs in self.AGVs:
                    AGVs_cuts.append(("AGV", [], None))
                    AGVs_order.append((each_AGVs, None))
            genes += _new_orders + AGVs_cuts[:-1]

            genes_size = len(genes)

            elite_size = int(20*self.population_size/100)
            non_elite_size = self.population_size - elite_size
            half_size = int(50*self.population_size/100)
            crossover_num = int(genes_size*_crossover_rate)
            non_crossover_num = genes_size - crossover_num
            mutation_prob = 0.1
            mutation_num = 1

            # Initial population
            for _ in range(self.population_size):
                populations.append(rd.sample(genes, k=genes_size))

            while True:

                populations_schedules = []
                T_matrix_list = []
                S_matrix_list = []

                for each_populations in populations:
                    each_new_schedule = self.GeneticAlgorithm_PopulationToNewSchedules(each_populations,
                                                                                       AGVs_order)
                    each_new_path_lengths, T_matrix, S_matrix = self.path_planning_algorithm.Update(each_new_schedule,
                                                                                                    length_only = True,
                                                                                                    count = generation,
                                                                                                    GPU_accelerating = GPU_accelerating)
                    
                    if GPU_accelerating:
                        T_matrix_list.append(T_matrix)
                        S_matrix_list.append(S_matrix)
                        
                    else:
                        each_eval_value, each_eval_variables = self.evaluation_algorithm.Update(each_new_path_lengths,
                                                                                            length_only = True)
                        populations_schedules.append((each_eval_value, each_eval_variables, each_populations))
                        
                if GPU_accelerating:
                    eval_value_matrix, eval_variables_matrix = self.evaluation_algorithm.Update([],
                                                                                                length_only = True,
                                                                                                GPU_accelerating = GPU_accelerating,
                                                                                                GPU_accelerating_data = GPU_accelerating_data,
                                                                                                matrix_data = (T_matrix_list, S_matrix_list))
                    for index, each_populations in enumerate(populations):
                        eval_variables = []
                        for each_eval_variables_matrix in eval_variables_matrix:
                            eval_variables.append(each_eval_variables_matrix[index])
                        populations_schedules.append((eval_value_matrix[index], eval_variables, each_populations))
                
                #try:(TT, TTC, BU)
                populations_schedules.sort(key=lambda each_populations: each_populations[0], reverse=True)
                #except TypeError:
                #    print("[Error]\t TypeError for sorting")
                #    for each_value, _ in populations_schedules:
                #        if not type(each_value) == type(0.1):
                #            print(each_value)
                #    print()

                # Update graph data
                each_eval_value, each_eval_variables, _ = populations_schedules[0]
                if type(each_eval_value) == type(cpy.array([])):
                    each_eval_value = float(cpy.asnumpy(each_eval_value))
                    each_eval_variables_list = []
                    for each_each_eval_variables in  each_eval_variables:
                        each_eval_variables_list.append(float(cpy.asnumpy(each_each_eval_variables)))
                    each_eval_variables = each_eval_variables_list

                if not self.graph_GUI == None:
                    self.tools.Update_GraphData(generation, (each_eval_value, each_eval_variables))

                populations = [each_population for _, _, each_population in populations_schedules]
                
                # Path planning process
                new_schedule = self.GeneticAlgorithm_PopulationToNewSchedules(populations[0], AGVs_order)
                new_paths, _, _ = self.path_planning_algorithm.Update(new_schedule, length_only=True)

                # Evaluation process
                #eval_value= self.evaluation_algorithm.Update(new_paths, length_only=True)
                eval_value = (each_eval_value, each_eval_variables)

                # Console print
                if generation % 500 == 0:
                    self.tools.PrintEvaluationData(eval_value, "Scheduling", order_num=generation)

                if generation >= self.max_generation:
                    break

                new_populations = []
                
                new_populations.extend(populations[:elite_size])

                if generation >= 5000:
                    mutataion_prob = 0.3
                    mutation_num = 1
                elif generation >= 1000:
                    mutataion_prob = 0.15
                    mutation_num = 1

                for _ in range(non_elite_size):
                    parent_1 = rd.choice(populations[:half_size])
                    parent_2 = rd.choice(populations[:half_size])

                    child = self.GeneticAlgorithm_CrossOperator(parent_1,
                                                                parent_2,
                                                                crossover_num,
                                                                non_crossover_num,
                                                                AGVs_order,
                                                                mutation_prob = mutation_prob,
                                                                mutation_num = mutation_num)
                    new_populations.append(child)

                populations = new_populations
            
                generation += 1

            new_schedules = self.GeneticAlgorithm_PopulationToNewSchedules(populations[0], AGVs_order)
        else:
            # Initial random scheduling 
            for each_AGV in self.AGVs:
                new_schedules.append((each_AGV, []))
                num_AGVs += 1
            for index, each_new_order in enumerate(_new_orders):
                AGVs_index = index % num_AGVs
                new_schedules[AGVs_index][1].append(each_new_order)

        # Path planning process
        new_paths = self.path_planning_algorithm.Update(new_schedules)

        # Evaluation process
        real_eval_value = eval_value
        
        print("[Scheduling]\tGenetic algorithm scheduling done.")
        self.tools.PrintEvaluationData(real_eval_value, "Scheduling", comment="Final")
        
        return (new_paths, real_eval_value)
            
    # Genetic algorithm - crossover operator
    def GeneticAlgorithm_CrossOperator(self,
                                       _parent_1,
                                       _parent_2,
                                       _crossover_num,
                                       _non_crossover_num,
                                       _AGVs_order,
                                       mutation_prob = 0,
                                       mutation_num = 5):
        child = []

        _parent_2 = cp.deepcopy(_parent_2)
        reserve_index = rd.choice(range(_crossover_num))
        reserve_genes = _parent_1[reserve_index:reserve_index+_non_crossover_num]

        child += reserve_genes

        for each_reserve_genes in reserve_genes:
            try:
                _parent_2.remove(each_reserve_genes)
            except ValueError:
                pass
        child += _parent_2
        
        if rd.random() <= mutation_prob:
            for _ in range(mutation_num):
                mutation_gene_1, mutation_gene_2 = rd.choices(child, k=2)
                mutation_gene_1_index = child.index(mutation_gene_1)
                mutation_gene_2_index = child.index(mutation_gene_2)
                
                child[mutation_gene_1_index] = mutation_gene_2
                child[mutation_gene_2_index] = mutation_gene_1
                
        return child

    # Genetic algorithm - helper function (population to schedule format)
    def GeneticAlgorithm_PopulationToNewSchedules(self, _population, _AGVs_order):
        new_schedules = []
        AGVs_order_count = 0
        each_AGV_ID, each_depot_ID = _AGVs_order[AGVs_order_count]
        
        each_AGV_schedule = (each_AGV_ID, [])

        # Depot distribution type
        if self.depot_distribution_type == 'Genetic':
            for each_population in _population:
                p_ID, p_object, *p_depot = each_population
                if p_ID == "AGV":
                    each_next_AGV_ID, each_next_depot_ID =  _AGVs_order[AGVs_order_count + 1]
                    if each_AGV_ID == each_next_AGV_ID:
                        AGVs_order_count += 1
                        each_AGV_ID = each_next_AGV_ID
                        each_depot_ID = each_next_depot_ID
                    else:
                        new_schedules.append(each_AGV_schedule)
                        AGVs_order_count += 1
                        each_AGV_ID = each_next_AGV_ID
                        each_depot_ID = each_next_depot_ID
                        each_AGV_schedule = (each_AGV_ID, [])
                else:
                    order_ID, shelf_IDs, _ = each_population
                    each_AGV_schedule[1].append((order_ID, shelf_IDs, each_depot_ID))
            new_schedules.append(each_AGV_schedule)
        else:
            for each_population in _population:
                p_ID, p_object, *p_depot = each_population
                if p_ID == "AGV":
                        new_schedules.append(each_AGV_schedule)
                        AGVs_order_count += 1
                        each_AGV_ID, _ = _AGVs_order[AGVs_order_count]
                        each_AGV_schedule = (each_AGV_ID, [])
                else:
                    each_AGV_schedule[1].append(each_population)
            new_schedules.append(each_AGV_schedule)

        return new_schedules
    
    # Random assigned algorithm
    def RandomAlgorithm(self,
                        _new_orders,
                        _order_independent,
                        is_shuffle = False):
        print("[Scheduling]\tRandom algorithm")
        print("[Scheduling]\tNew orders for scheduling is: " + str(_new_orders))

        if not self.graph_GUI == None:
            self.tools.ResetGraphData()

        _new_orders = self.OrderIndependenctAndDepotDistribution(_new_orders, _order_independent)

        new_schedules = []  # [(AGV ID, [(order ID, [order, ...], depot ID), ...]), ...]
        eval_value = (0, [0]) # Initial eval data
        AGVs_list = list(self.AGVs.keys())
        num_AGVs = len(AGVs_list)

        # Initialize the schedule
        for each_AGVs_ID in AGVs_list:
            new_schedules.append((each_AGVs_ID, []))

        # random shuffle
        if is_shuffle:
            rd.shuffle(_new_orders)

        # Assigning by order
        AGV_order = 0
        for each_orders in _new_orders:
            if AGV_order == num_AGVs:
                AGV_order = 0
                
            AGV_ID, AGV_path = new_schedules[AGV_order]
            AGV_path.append(each_orders)
            new_schedules[AGV_order] = (AGV_ID, AGV_path)

            AGV_order += 1

        # Path planning process
        new_paths = self.path_planning_algorithm.Update(new_schedules)

        # Evaluation process
        real_eval_value = eval_value
        
        print("[Scheduling]\tRandom algorithm scheduling done.")
        
        return (new_paths, real_eval_value)

    #--------------------------------------------------
            
    # Update
    def Update(self, _new_orders, _order_independent):
        if self.scheduling_type == "Genetic":
            new_paths = self.GeneticAlgorithm(_new_orders,
                                              _order_independent,
                                              self.MAX_EPOCH,
                                              self.CROSSOVER_RATE,
                                              GPU_accelerating = self.GPU_accelerating,
                                              GPU_accelerating_data = (self.n_AGV, self.population_size))
        elif self.scheduling_type == "Random":
            new_paths = self.RandomAlgorithm(_new_orders,
                                             _order_independent,
                                             is_shuffle = True)

        return new_paths
