###############################
#
# Tools - Data
#
# Won Yong Ha
#
# V.1.0 Ordering data saving tool using CSV file
#
##############################

import csv
import os.path

class Tools_Data():

    directory_name = None

    def __init__(self, directory_name="../Data/" ):
        self.directory_name = directory_name
    
    def OrderDataLoading(self, _order_file_name):
        file_path = self.directory_name + _order_file_name
        orders = []

        if os.path.isfile(file_path):
            new_file = open(file_path, 'r')
            new_file_reader = csv.reader(new_file)
            for each_row in new_file_reader:
                orders.append((int(each_row[0]),
                               [int(x) for x in each_row[1:]]))
            new_file.close()
            print(orders)
        else:
            new_file = open(file_path, 'w', newline='')
            new_file_writer = csv.writer(new_file)
            new_file.close()
        return orders
    
    def OrderDataSaving(self, _order_data, _file_name):
        file_name = self.directory_name + _file_name

        with open(file_name, 'a', newline='') as new_file:
            new_file_writer = csv.writer(new_file)
            for each_order_data in _order_data:
                each_order_data = [each_order_data[0]] + each_order_data[1]
                new_file_writer.writerow(each_order_data)
            
