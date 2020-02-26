###############################
#
# Shelf
#
# Won Yong Ha
#
#
###############################

class Shelf():

    ID = None
    current_pos = None

    orders = []
    
    # Constructor
    def __init__(self, _ID, _pos):
        self.ID = _ID
        self.current_pos = _pos

    # Set order
    def SetOrder(self, _new_order):
        orders = _new_order

    # Add order
    def AddOder(self, _add_order):
        self.orders += _add_order

    
