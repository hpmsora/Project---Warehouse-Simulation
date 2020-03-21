###############################
#
# Main
#
# Won Yong Ha
#
#
###############################

import SimulationGUI as sgui
import tkinter as tk

# Global Variables
WAREHOUSE_TYPE = 'basic' # Default warehouse type is basic
ORDER_TYPE = 'basic'     # Default order type is basic stochastic

NUM_AISLE = 10           # Default 2 aisle
NUM_ROWS  = 10           # Default 5 rows each aisle
SQUARE_SIZE = 20         # Default 64 per each square

ORDER_PER_BATCH = 1     # Default average number of batch per order is 10
NUM_ORDER = 30          # Default number of order at once is 100

NUM_AGVs = 1             # Default 20 AGVs

# Fixed Variable
PADDING_SIZE = 10

# Display simulation
def Display_SimulationBoard():
    root = tk.Tk()
    root.title("Warehouse Simulation")
    print(root.title)
    
    Board = sgui.SimulationBoard(root, num_aisles=NUM_AISLE, num_rows=NUM_ROWS, square_size=SQUARE_SIZE)
    Board.GridBuilding(warehouse_type = 'basic')
    Board.DepotBuilding()
    Board.AGVDepotBuilding()

    Board.AddAGV(NUM_AGVs)
    Board.SetController()
    Board.SetOrder(order_type='basic', order_per_batch=ORDER_PER_BATCH, num_order=NUM_ORDER)
    
    Board.pack(side='top', fill='both', expand='true', padx=PADDING_SIZE, pady=PADDING_SIZE)
    Board.Update()
    
    root.mainloop()

def main():
    Display_SimulationBoard()

if __name__ == "__main__":
    main()
