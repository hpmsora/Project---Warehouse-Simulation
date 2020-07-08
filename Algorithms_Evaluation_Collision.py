###############################
#
# Algorithms - Evaluation (Collision)
#
# Won Yong Ha
#
# V.1.0 Entropy method
#
###############################

class Algorithms_Evaluation_Collision():

    collision_test_type = None

    # Internal Variables
    tools = None
    
    # Contructor
    def __init__(self, _tools, collision_test_type="entropy"):
        self.tools = _tools
        self.collision_test_type = collision_test_type

    # Entropy
    def CollisionTest_Entropy(self, new_path, length_only):
        collision_index = 0

        # Estimator
        if length_only:
            density_matrix = self.tools.Matrixization(new_path)
            
            return 0
        # Realtor
        elif not length_only:
            pass
        else:
            return 0
        return 0
    
    # Update
    def Update(self, _new_path, length_only):
        if self.collision_test_type == "entropy":
            return self.CollisionTest_Entropy(_new_path, length_only)
        else:
            return 0
