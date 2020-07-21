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

class Algorithms_Evaluation_Collision():

    collision_test_type = None

    # Internal Variables
    tools = None
    
    # Contructor
    def __init__(self, _tools, collision_test_type="EntropyDistance"):
        self.tools = _tools
        self.collision_test_type = collision_test_type

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
            (pos_x, pos_y, time_t) = self.tools.Matrixization_Separation(_new_path)

            pos_x = np.array(pos_x)
            pos_y = np.array(pos_y)
            time_t = np.array(time_t)

            pos_x_diff = np.substract(pos_x, pos_x.transpose())
            pos_y_diff = np.substract(pos_y, pos_y.transpose())
            time_t_diff = np.substract(time_t, time_t.transpose())
            
            collision_index = np.trace(np.multiply(pos_x_diff, pos_x_diff.transpose())
                                       + np.multiply(pos_y_diff, pos_y_diff.transpose())
                                       + np.multiply(time_z_diff, time_z_diff.transpose()))

            print(collision_index)

            collision_index = 0
            
            return collision_index
        
        # Realtor
        elif not _length_only:
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
