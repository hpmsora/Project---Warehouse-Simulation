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
WAREHOUSE_TYPE = 'Basic' # Defualt warehouse type is basic
NUM_AISLE = 10           # Default 2 aisle
NUM_ROWS  = 10           # Defualt 5 rows each aisle
SQUARE_SIZE = 20         # Defualt 64 per each square

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
    
    Board.pack(side='top', fill='both', expand='true', padx=PADDING_SIZE, pady=PADDING_SIZE)
    
    root.mainloop()

def main():
    Display_SimulationBoard()

if __name__ == "__main__":
    main()
