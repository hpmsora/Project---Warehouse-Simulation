###############################
#
# Algorithms - Evaluation (Collision)
#
# Won Yong Ha
#
# V.1.1 Eigenvector centrality method
# V.1.0 Entropy method
#
###############################

import scipy.linalg as la
import numpy as np
import math

class Algorithms_Evaluation_Collision():

    collision_test_type = None

    # Internal Variables
    tools = None
    standard_index = None
    
    # Contructor
    def __init__(self, _tools, collision_test_type="EntropyDistance"):
        self.tools = _tools
        self.collision_test_type = collision_test_type

        if self.collision_test_type == "EntropyDistance":
            self.standard_index = self.tools.GetWidth()**2 + self.tools.GetHeight()**2

    # Entropy - Matrix
    def CollisionTest_EntropyMatrix(self, _new_path, _length_only):
        collision_index = 0

        # Estimator
        if _length_only:
            density_matrix = self.tools.Matrixization_Density(_new_path)
            
            return collision_index

        # Realtor
        elif not _length_only:
            return collision_index

        # Error
        else:
            return 0
        return collision_index

    # Entropy - Distance
    def CollisionTest_EntropyDistance(self, _new_path, _length_only):
        collision_index = 0

        # Estimator
        if _length_only:
            (time_t, pos_x, pos_y, min_t, max_t, m_size) = self.tools.Matrixization_Separation(_new_path)

            time_t = np.array(time_t)
            pos_x = np.array(pos_x)
            pos_y = np.array(pos_y)

            time_t_diff = np.subtract(time_t, time_t.transpose())
            pos_x_diff = np.subtract(pos_x, pos_x.transpose())
            pos_y_diff = np.subtract(pos_y, pos_y.transpose())
            
            distance_matrix = np.multiply(time_t_diff, time_t_diff) \
                            + np.multiply(pos_y_diff, pos_y_diff) \
                            + np.multiply(pos_x_diff, pos_x_diff)

            distance_matrix = np.dot(np.sqrt(distance_matrix), np.ones((m_size, 1)))

            collision_index_sum = distance_matrix.sum()

            collision_index_max = (m_size**2)*math.sqrt((max_t-min_t)**2 + self.standard_index)

            collision_index = collision_index_sum / collision_index_max

            return collision_index
        
        # Realtor
        elif not _length_only:

            #print(_new_path)
            
            return collision_index

        # Error
        else:
            return 0

        return collision_index
    
    # Network - Eigenvector Centrality
    def CollisionTest_EigenvectorCentrality(self, _new_path, _length_only):
        collision_index = 0

        # Estimator
        if _length_only:
            adjacency_matrix = self.tools.Matrixization_Adjacency(_new_path)
            eigvals, eigvecs = la.eig(adjacency_matrix)
            print(adjacency_matrix)
            #print(eigvals)
            return 0

        # Realtor
        elif not _length_only:
            pass

        # Error
        else:
            return 0

        return collision_index
    
    # Update
    def Update(self, _new_path, length_only):
        if self.collision_test_type == "EntropyMatrix":
            return self.CollisionTest_Entropy(_new_path, length_only)
        elif self.collision_test_type == "EntropyDistance":
            return self.CollisionTest_EntropyDistance(_new_path, length_only)
        elif self.collision_test_type == "EigenvectorCentrality":
            return self.CollisionTest_EigenvectorCentrality(_new_path, length_only)
        else:
            return 0
