###############################
#
# Order
#
# Won Yong Ha
#
# V.1.1 Saving
# V.1.0 Random ordering
#
###############################

from random import random
from random import gauss
from random import choices
import math

class Order():
    
    order_type = None # Defualt basic stochastic
    order_per_batch = None
    num_order = None
    order_gap = 1
    
    order_file_name = None # Must include extension (.csv)
    
    shelves = None

    tools_data = None

    # Internal Variables
    order_ID_count = None
    
    # Constructor
    def __init__(self,
                 _shelves,
                 _tools_data,
                 order_type="basic",
                 order_per_batch=1,
                 num_order = 100,
                 order_gap = 1):
        self.shelves = _shelves
        self.order_type = order_type
        self.order_per_batch = order_per_batch
        self.num_order = num_order
        self.order_gap = order_gap

        self.tools_data = _tools_data
        
        self.order_ID_count = 0

    # Get number of order at once
    def GetNumOrder(self):
        return self.num_order

    # Get saved order
    def SavedOrder(self):
        saved_order = self.tools_data.OrderDataLoading()
        self.order_ID_count = len(saved_order)
        
        return saved_order
    
    # Order generator
    def OrderGenerator(self):
        all_shelves = list(self.shelves.keys())
        num_shelves = len(all_shelves)
        order = []

        if self.order_type == "basic":
            for count in range(self.num_order):
                if count % self.order_gap == 0 or count == 0:
                    batch_size = math.ceil(abs(gauss(self.order_per_batch, self.order_per_batch/2)))
                    order.append((self.order_ID_count, choices(all_shelves, k=batch_size)))
                else:
                    order.append((self.order_ID_count, []))
                self.order_ID_count += 1

        self.tools_data.OrderDataSaving(order, self.order_file_name)
        
        return order
                
