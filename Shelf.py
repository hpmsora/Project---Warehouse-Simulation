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
        self.on_AGV = None
        self.orders = []
        self.tools = _tools
    
    # Add order
    def AddOrder(self, _add_order):
        self.orders.append(_add_order)

    # Set shelf status
    def UpdateStatus(self, _status):
        self.status = _status

    # Update on AGV status
    def UpdateAGVStatus(self, _each_shelf_occupancy):
        if not _each_shelf_occupancy == ():
            AGV_ID, is_on_AGV = _each_shelf_occupancy
            if is_on_AGV:
                self.on_AGV = AGV_ID
            else:
                self.on_AGV = None

    # Coloring the shelf
    def UpdateColoring(self):
        if self.status == "nothing":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfNothing_Color())
        elif self.status == "waiting":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfWaiting_Color())
        elif self.status == "moving":
            self.tools.ChangeColorObject(self.ID, color=self.tools.GetShelfMoving_Color())

    # Update
    def update(self, _each_shelf_occupancy):
        self.UpdateAGVStatus(_each_shelf_occupancy)
        
        if self.on_AGV == None and not len(self.orders) == 0:
            self.UpdateStatus("waiting")
        elif not self.on_AGV == None:
            self.UpdateStatus("moving")
        else:
            self.UpdateStatus("nothing")
        self.UpdateColoring()
