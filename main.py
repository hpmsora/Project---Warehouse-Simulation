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
WAREHOUSE_TYPE = 'basic_island_wide' # Default warehouse type is basic
ORDER_TYPE = 'basic'     # Default order type is basic stochastic

NUM_AISLE = 12           # Default 6 aisle (Goal: 12)
NUM_ROWS  = 24           # Default 12 rows each aisle (Goal: 24)
SQUARE_SIZE = 20         # Default 20 per each square

DEPOT_TYPE = ['Equal_Above']
DEPOT_NUM = [4]

EVALUATION_TYPES = ['General_n_Balance',
                    'General_n_Balance_n_Collision',
                    'General_n_Balance_n_Collision_Eff']

ORDER_PER_BATCH = 1     # Default average number of batch per order is 10
NUM_ORDER = 30          # Default number of order at once is 100

NUM_AGVs = 10             # Default 5 AGVs (Goal:30)

MOVEMENT_SPEED = 80    # 80

# Fixed Variable
PADDING_SIZE = 10

# Display simulation
def Display_SimulationBoard(run_type = None):
    root = tk.Tk()
    root.title("Warehouse Simulation")
    
    Board = sgui.SimulationBoard(root,
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
    Board.SetController(evaluation_type = EVALUATION_TYPES[2],
                        order_threshold = 10,
                        order_independent = True,
                        graph_GUI_show = True,
                        padx = PADDING_SIZE,
                        pady = PADDING_SIZE)
    Board.SetOrder(order_type='basic',
                   order_per_batch=ORDER_PER_BATCH,
                   num_order=NUM_ORDER)
    Board.SetFinal()

    if run_type == "rerun":
        Board.SetReRun()
    
    Board.pack(side = 'top',
               fill = 'both',
               expand = True,
               padx = PADDING_SIZE,
               pady = PADDING_SIZE)

    Board.Update()
    
    root.mainloop()

# Main method
def main():
    run_type = None
    if not len(sys.argv) == 1:
        run_type, *conditions = sys.argv[1:]
    
    Display_SimulationBoard(run_type = run_type)

# Trigger
if __name__ == "__main__":
    main()
