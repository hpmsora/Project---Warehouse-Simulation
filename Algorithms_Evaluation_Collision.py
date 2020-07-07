###############################
#
# Algorithms - Evaluation (Collision)
#
# Won Yong Ha
#
# V.1.0
#
###############################

class Algorithms_Evaluation_Collision():

    collision_test_type = None

    # Internal Variables
    
    # Contructor
    def __init__(self, collision_test_type="entropy"):
        self.collision_test_type = collision_test_type

    # Entropy
    def CollisionTest_Entropy(self, new_path):
        print(new_path)
        return 0
    
    # Update
    def Update(self, _new_path):
        if self.collision_test_type == "entropy":
            return self.CollisionTest_Entropy(_new_path)
        else:
            return 0
