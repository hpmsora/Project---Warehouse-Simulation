###############################
#
# Main
#
# Won Yong Ha
#
# V.2.0 - Collision test
# V.1.0 - Genetic Algorithm
#
###############################

import sys
import SimulationGUI as sgui
import tkinter as tk

# Global Variables
WAREHOUSE_TYPE = 'basic_island_wide'   # Default warehouse type is basic
ORDER_TYPE = 'basic'                   # Default order type is basic stochastic

NUM_AISLE = 12                         # Default 6 aisle (Goal: 12)
NUM_ROWS  = 24                         # Default 12 rows each aisle (Goal: 24)
SQUARE_SIZE = 20                       # Default 20 per each square

DEPOT_TYPE = ['Equal_Above']
DEPOT_NUM = [4]

SCHEDULING_TYPES_LIST = ['Random',
                         'Genetic']
SCHEDULING_TYPES = 1

EVALUATION_TYPES_LIST = ['General_n_Balance',
                         'General_n_Balance_n_Collision',
                         'General_n_Balance_n_Collision_Eff']
EVALUATION_TYPES = 2

ORDER_PER_BATCH = 1                    # Default average number of batch per order is 10
NUM_ORDER = 30                         # Default number of order at once is 100

NUM_AGVs = 10                          # Default 5 AGVs (Goal: 30)
ORDER_THRESHHOLD = 40                 # Default 80 orders per one time rescheduling (Goal: 200)

MOVEMENT_SPEED = 50                    # Default: 80; Simulation: 50 (Lower is faster)

# Fixed Variable
PADDING_SIZE = 10

# Display simulation
def Display_SimulationBoard(_root, run_type = None, max_scheduling = None, file_name = None):
    Board = sgui.SimulationBoard(_root,
                                 num_aisles=NUM_AISLE,
                                 num_rows=NUM_ROWS,
                                 square_size=SQUARE_SIZE,
                                 movement_speed=MOVEMENT_SPEED)
    Board.GridBuilding(warehouse_type = WAREHOUSE_TYPE)
    Board.DepotBuilding(depot_type = DEPOT_TYPE,
                        custom_depot = DEPOT_NUM,
                        above=0,
                        depth=1)
    Board.AGVDepotBuilding(AGV_size = NUM_AGVs)

    Board.AddAGV(num = NUM_AGVs)
    Board.SetController(scheduling_type = SCHEDULING_TYPES_LIST[SCHEDULING_TYPES],
                        evaluation_type = EVALUATION_TYPES_LIST[EVALUATION_TYPES],
                        order_threshold = ORDER_THRESHHOLD,
                        order_independent = True,
                        graph_GUI_show = False,
                        padx = PADDING_SIZE,
                        pady = PADDING_SIZE,
                        max_scheduling = max_scheduling)
    Board.SetOrder(order_type='basic',
                   order_per_batch=ORDER_PER_BATCH,
                   num_order=NUM_ORDER)
    Board.SetFinal(file_name = file_name)

    if run_type == "rerun":
        Board.SetReRun(file_name = file_name)
    
    Board.pack(side = 'top',
               fill = 'both',
               expand = True,
               padx = PADDING_SIZE,
               pady = PADDING_SIZE)

    Board.Update()
    
    _root.mainloop()

# Auto run
def Auto_Run(_root, _conditions, max_scheduling = 1):
    re_run, file_name = Auto_FileNaming(_conditions)
    Display_SimulationBoard(_root,
                            run_type = re_run,
                            max_scheduling = max_scheduling,
                            file_name = file_name)

# Auto file naming
def Auto_FileNaming(_args):
    sch_list, eval_list, c_exp, n_exp, status = _args
    sch_o = eval(sch_list).pop()
    eval_o = eval(eval_list).pop()

    file_name = "(" + str(SCHEDULING_TYPES_LIST[sch_o])  + ")_" + \
        "(" + str(EVALUATION_TYPES_LIST[eval_o])  + ")_" + \
        str(c_exp) + "-"+str(n_exp)

    if status == 's':
        re_run = None
    elif status == 'r':
        re_run = "rerun"
    else:
        re_run = None
    
    return (re_run, file_name)
    
# Main method
def main():
    run_type = None

    root = tk.Tk()
    root.title("Automated Warehouse Simulation")
    
    if not len(sys.argv) == 1:
        run_type, *conditions = sys.argv[1:]

    if run_type == "auto":
        Auto_Run(root, conditions);

    else:
        Display_SimulationBoard(root, run_type = run_type)

# Trigger
if __name__ == "__main__":
    main()
