###############################
#
# Order
#
# Won Yong Ha
#
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
    
    shelves = None
    
    # Constructor
    def __init__(self, _shelves, order_type="basic", order_per_batch=1, num_order = 100):
        self.shelves = _shelves
        self.order_type = order_type
        self.order_per_batch = order_per_batch
        self.num_order = num_order

    # Get number of order at once
    def GetNumOrder(self):
        return self.num_order
        
    # Order generator
    def OrderGenerator(self):
        all_shelves = list(self.shelves.keys())
        num_shelves = len(all_shelves)
        order = []

        if self.order_type == "basic":
            for _ in range(0, self.num_order):
                batch_size = math.ceil(abs(gauss(self.order_per_batch, self.order_per_batch/2)))
                order.append(choices(all_shelves, k=batch_size))
        return order
                
