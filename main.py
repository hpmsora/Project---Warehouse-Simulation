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
NUM_AISLE = 8   # Default 2 Aisle
NUM_ROWS  = 8   # Defualt 5 Rows each aisle
SQUARE_SIZE = 64 # Defualt 64 per each square

# Display simulation
def Display_SimulationBoard():
    root = tk.Tk()
    root.title("Warehouse Simulation")
    print(root.title)
    
    Board = sgui.SimulationBoard(root, num_aisle=NUM_AISLE, square_size=SQUARE_SIZE)
    Board.pack(side='top', fill='both', expand='true', padx=4, pady=4)
    
    root.mainloop()

def main():
    Display_SimulationBoard()

if __name__ == "__main__":
    main()
