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
import os

class Tools_Data():

    data_order_directory_name = None
    data_path_directory_name = None
    results_directory_name = None

    def __init__(self,
                 data_order_directory_name="../Values_OrderData/",
                 data_path_directory_name="../Values_PathData/",
                 results_directory_name="../Values_Results/"):
        self.data_order_directory_name = data_order_directory_name
        self.data_path_directory_name = data_path_directory_name
        self.results_directory_name = results_directory_name

    # Loading the order data if exist
    def OrderDataLoading(self, _order_file_name):
        file_name = self.data_order_directory_name + _order_file_name
        orders = []

        if not os.path.exists(self.data_order_directory_name):
            os.makedirs(self.data_order_directory_name)

        if os.path.isfile(file_name):
            new_file = open(file_name, 'r')
            new_file_reader = csv.reader(new_file)
            for each_row in new_file_reader:
                orders.append((int(each_row[0]),
                               [int(x) for x in each_row[1:]]))
            new_file.close()
        else:
            new_file = open(file_name, 'w', newline='')
            new_file_writer = csv.writer(new_file)
            new_file.close()
        return orders

    # Overwrite the order data upon file name
    def OrderDataSaving(self, _order_data, _order_file_name):
        file_name = self.data_order_directory_name + _order_file_name

        with open(file_name, 'a', newline='') as new_file:
            new_file_writer = csv.writer(new_file)
            for each_order_data in _order_data:
                each_order_data = [each_order_data[0]] + each_order_data[1]
                new_file_writer.writerow(each_order_data)

    def PathDataSaving(self, _path_data, _path_file_name):

        with open(file_name, 'a', newline='') as new_file:
            new_file_writer = csv.writer(new_file)

    # Write the result
    def ResultsSaving(self, _results, _results_file_name):
        file_name = self.results_directory_name + _results_file_name

        if not os.path.exists(self.results_directory_name):
            os.makedirs(self.results_directory_name)

        if not os.path.isfile(file_name):
            new_file = open(file_name, 'w', newline='')
            new_file_writer = csv.writer(new_file)
            new_file.close()

        with open(file_name, 'a', newline='') as new_file:
            new_file_writer = csv.writer(new_file)
            for each_results in _results:
                new_file_writer.writerow(each_results)
