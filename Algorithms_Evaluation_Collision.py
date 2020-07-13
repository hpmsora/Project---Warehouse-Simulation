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
    def __init__(self, _tools, collision_test_type="EigenvectorCentrality"):
        self.tools = _tools
        self.collision_test_type = collision_test_type

    # Entropy
    def CollisionTest_Entropy(self, _new_path, length_only):
        collision_index = 0

        # Estimator
        if length_only:
            density_matrix = self.tools.Matrixization_Density(_new_path)
            
            return 0

        # Realtor
        elif not length_only:
            pass

        # Error
        else:
            return 0
        return 0

    # Network - Eigenvector Centrality
    def CollisionTest_EigenvectorCentrality(self, _new_path, length_only):
        collision_index = 0

        # Estimator
        if length_only:
            adjacency_matrix = self.tools.Matrixization_Adjacency(_new_path)
            eigvals, eigvecs = la.eig(adjacency_matrix)
            print(adjacency_matrix)
            #print(eigvals)
            return 0

        # Realtor
        elif not length_only:
            pass

        # Error
        else:
            return 0

        return 0
    
    # Update
    def Update(self, _new_path, length_only):
        if self.collision_test_type == "Entropy":
            return self.CollisionTest_Entropy(_new_path, length_only)
        elif self.collision_test_type == "EigenvectorCentrality":
            return self.CollisionTest_EigenvectorCentrality(_new_path, length_only)
        else:
            return 0
