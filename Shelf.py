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

    # Internal Varialbe
    status = None
    On_AGV = None
    orders = None
    tools = None
    
    # Constructor
    def __init__(self, _ID, _pos, _tools):
        self.ID = _ID
        self.current_pos = _pos

        self.status = "nothing"
        self.On_AGV = None
        self.orders = []
        self.tools = _tools
    
    # Add order
    def AddOrder(self, _add_order):
        self.orders.append(_add_order)

    # Set shelf status
    def UpdateStatus(self, _status):
        self.status = _status

    # Coloring the shelf
    def Coloring(self):
        if self.status == "nothing":
            self.tools.ChangeColorObject(self.ID, color="gray")
        elif self.status == "waiting":
            self.tools.ChangeColorObject(self.ID, color="green")
        elif self.status == "moving":
            self.tools.ChangeColorObject(self.ID, color="gold")

    # Update
    def update(self):
        if self.On_AGV == None and not len(self.orders) == 0:
            self.UpdateStatus("waiting")
        elif not self.On_AGV == None:
            self.UpdateStatus("moving")
        else:
            self.UpdateStatus("nothing")
        self.Coloring()
