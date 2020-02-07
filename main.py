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
NUM_AISLE = 20   # Default 2 Aisle
NUM_ROWS  = 40   # Defualt 5 Rows each aisle
SQUARE_SIZE = 20 # Defualt 64 per each square

# Display simulation
def Display_SimulationBoard():
    root = tk.Tk()
    root.title("Warehouse Simulation")
    print(root.title)
    
    Board = sgui.SimulationBoard(root, num_aisles=NUM_AISLE, num_rows=NUM_ROWS, square_size=SQUARE_SIZE)
    Board.GridBuilding()
    
    Board.pack(side='top', fill='both', expand='true', padx=4, pady=4)
    
    root.mainloop()

def main():
    Display_SimulationBoard()

if __name__ == "__main__":
    main()
