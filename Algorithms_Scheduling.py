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
import random as rd
import collections as col

class Algorithms_Scheduling():

    AGVs = None
    shelves = None
    scheduling_type = ""

    # Fixed Variable
    MAX_EPOCH = 100
    CROSSOVER_RATE = 0.80
    
    # Internal Variables
    tools = None
    graph_GUI = None
    path_planning_algorithm = None
    evaluation_algorithm = None

    # Constructor
    def __init__(self,
                 _AGVs,
                 _shelves,
                 _tools,
                 _scheduling_type,
                 _path_planning_type,
                 _evaluation_type,
                 graph_GUI = None):
        self.AGVs = _AGVs
        self.shelves = _shelves
        self.scheduling_type = _scheduling_type

        self.tools = _tools
        self.graph_GUI = graph_GUI
        self.path_planning_algorithm = None
        self.evaluation_algorithm = None
        self.SetPathPlanningAlgorithm(_path_planning_type)
        self.SetEvaluationAlgorithm(_evaluation_type)

        self.tools.SetGraphVariablesType(self.evaluation_algorithm.GetVariablesType())
        self.graph_GUI.BuildGraph()

    # Set path planning algorithm
    def SetPathPlanningAlgorithm(self, _path_planning_type):
        self.path_planning_algorithm = AlgPath.Algorithms_PlathPlanning(self.AGVs,
                                                                        self.shelves,
                                                                        self.tools,
                                                                        _path_planning_type)

    # Set evaluation algorithm
    def SetEvaluationAlgorithm(self, _evaluation_type):
        self.evaluation_algorithm = AlgEval.Algorithms_Evaluation(self.AGVs,
                                                                  self.shelves,
                                                                  self.tools,
                                                                  _evaluation_type)

    #--------------------------------------------------
    
    # Genetic Algorithm
    def GeneticAlgorithm(self,
                         _new_orders,
                         _max_generaion,
                         _crossover_rate,
                         _order_independent):
        print("[Scheduling]\t New orders for scheduling is: " + str(_new_orders))

        self.tools.ResetGraphData()

        new_schedules = []  # [(AGV ID, [(order ID, [order, ...], depot ID), ...]), ...]
        num_AGVs = 0

        # Order independent
        if _order_independent:
            new_orders = []
            for each_orders_num, each_orders in _new_orders:
                for each_each_orders in each_orders:
                    new_orders.append((each_orders_num, [each_each_orders]))
            _new_orders = new_orders

        # Add depot place to new orders
        depot_type_ID = 421  # One depot place for Version 1.0
        for index, each_new_orders in enumerate(_new_orders):
            order_num, orders = each_new_orders
            _new_orders[index] = (order_num, orders, depot_type_ID)

        # Genetic algorithm start
        if True: #self.path_planning_algorithm.Is_Reserve_Full():

            genes = []
            populations = []
            populations_schedules = []
            generation = 0
            max_generation = 200
            population_size = 200
            AGVs_order = []

            AGVs_cuts = []
            for each_AGVs in self.AGVs:
                AGVs_cuts.append(("AGV", [], each_AGVs))
                AGVs_order.append(each_AGVs)
            genes += _new_orders + AGVs_cuts[:-1]

            genes_size = len(genes)

            elite_size = int(20*population_size/100)
            non_elite_size = population_size - elite_size
            half_size = int(50*population_size/100)
            crossover_num = int(genes_size*_crossover_rate)
            non_crossover_num = genes_size - crossover_num

            # Initial population
            for _ in range(population_size):
                populations.append(rd.sample(genes, k=genes_size))

            while True:
                for each_populations in populations:
                    each_new_schedule = self.GeneticAlgorithm_PopulationToNewSchedules(each_populations,
                                                                                       AGVs_order)
                    each_new_path_lengths = self.path_planning_algorithm.Update(each_new_schedule,
                                                                                length_only = True)
                    each_eval_value, each_eval_variables = self.evaluation_algorithm.Update(each_new_path_lengths,
                                                                                            length_only = True)
                    populations_schedules.append((each_eval_value, each_eval_variables, each_populations))

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
                self.tools.Update_GraphData(generation, (each_eval_value, each_eval_variables))
                
                populations = [each_population for _, _, each_population in populations_schedules]
                
                # Path planning process
                new_schedule = self.GeneticAlgorithm_PopulationToNewSchedules(populations[0], AGVs_order)
                new_paths = self.path_planning_algorithm.Update(new_schedule)

                # Evaluation process
                eval_value = self.evaluation_algorithm.Update(new_paths)
                print(str(generation) + ":\t" + str(eval_value))

                if generation >= max_generation:
                    break

                new_populations = []
                
                new_populations.extend(populations[:elite_size])

                for _ in range(non_elite_size):
                    parent_1 = rd.choice(populations[:half_size])
                    parent_2 = rd.choice(populations[:half_size])

                    child = self.GeneticAlgorithm_CrossOperator(parent_1,
                                                                parent_2,
                                                                crossover_num,
                                                                non_crossover_num,
                                                                AGVs_order,
                                                                mutation_prob = 0.1)
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
        eval_values = self.evaluation_algorithm.Update(new_paths)
        
        print("[Scheduling]\t Genetic algorithm scheduling done.\t\t" + str(eval_value))
        
        return (new_paths, eval_values)
            
    # Genetic algorithm - crossover operator
    def GeneticAlgorithm_CrossOperator(self,
                                       _parent_1,
                                       _parent_2,
                                       _crossover_num,
                                       _non_crossover_num,
                                       _AGVs_order,
                                       mutation_prob = 0):
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

    # Genetic algorithm - helper function (schedule to gene format)
    def GeneticAlgorithm_NewScheduleToGenes(self, _new_schedule, _a):
        genes = []
        for each_AGV_ID, each_new_schedule in _new_schedule:
            genes += each_new_schedule + [("AGV", [], each_AGV_ID)]
        return genes[:-1]

    #--------------------------------------------------
            
    # Update
    def Update(self, _new_orders, _order_independent):
        if self.scheduling_type == "Genetic":
            new_paths = self.GeneticAlgorithm(_new_orders,
                                              self.MAX_EPOCH,
                                              self.CROSSOVER_RATE,
                                              _order_independent)
            
        return new_paths
