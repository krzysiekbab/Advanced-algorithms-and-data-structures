import numpy as np
from typing import List, Tuple

class Backpack():
    iterations = 1000
    weight_limit = 2500

    def __init__(self, default_shuffle, backpack_items):
        self.backpack_items = backpack_items
        self.number_of_items = len(backpack_items)
        self.best_shuffle = default_shuffle
        self.best_weight = self.compute_backup_weight(default_shuffle)
    
    def compute_backup_weight(self, shuffle) -> int:
        weight = 0
        for key, value in self.backpack_items.items():
            weight += shuffle[key] * value
        
        return weight
    
    def mutate(self, shuffle) -> List[int]:
        random_index = np.random.randint(0, self.number_of_items)
        if shuffle[random_index] == 0:
            shuffle[random_index] = 1
        elif shuffle[random_index] == 1:
            shuffle[random_index] = 0

        return shuffle
    
    def check_if_mutated_shuffle_is_better(self, mutated_shuffle) -> Tuple[bool, int]:
        mutated_shuffle_weight = self.compute_backup_weight(mutated_shuffle)
        is_better = False

        if self.best_weight > Backpack.weight_limit and mutated_shuffle_weight < self.best_weight:
            is_better = True
        elif self.best_weight < Backpack.weight_limit and mutated_shuffle_weight <= Backpack.weight_limit and mutated_shuffle_weight > self.best_weight:
            is_better = True
        
        return is_better, mutated_shuffle_weight


    def evelove(self) -> None:
        print(f"START WEIGTH: {self.best_weight}")
        for i in range(Backpack.iterations):
            active_shuffle = self.best_shuffle
            mutated_shuffle = self.mutate(active_shuffle)
            is_better, mutated_shuffle_weight = self.check_if_mutated_shuffle_is_better(mutated_shuffle)
            
            if(is_better):
                self.best_shuffle = mutated_shuffle
                self.best_weight = mutated_shuffle_weight
                print(f"NEW BEST WEIGHT: {self.best_weight} (iteration {i})")
                if self.best_weight == Backpack.weight_limit:
                    print(f"OPTIMAL SOLUTION HAS BEEN REACHED IN {i} ITERATIONS.")
                    break 
        print(f"OPTIMAL WEIGTH: {self.best_weight}")

if __name__ == "__main__":
    items = {0: 51, 1: 10, 2: 91, 3: 48, 4: 89, 5: 14, 6: 35, 7: 39, 8: 18, 9: 36, 10: 97, 11: 59, 12: 56, 13: 27, 14: 78, 15: 35, 16: 10, 17: 27, 18: 38, 19: 57, 20: 82, 21: 14, 22: 17, 23: 65, 24: 55, 25: 100, 26: 52, 27: 58, 28: 96, 29: 30, 30: 86, 31: 99, 32: 14, 33: 20, 34: 15, 35: 38, 36: 64, 37: 48, 38: 50, 39: 71, 40: 19, 41: 89, 42: 51, 43: 17, 44: 75, 45: 87, 46: 72, 47: 39, 48: 83, 49: 43, 50: 56, 51: 56, 52: 26, 53: 81, 54: 14, 55: 23, 56: 50, 57: 36, 58: 73, 59: 41, 60: 86, 61: 97, 62: 25, 63: 42, 64: 85, 65: 92, 66: 73, 67: 90, 68: 87, 69: 36, 70: 42, 71: 100, 72: 99, 73: 39, 74: 58, 75: 99, 76: 39, 77: 10, 78: 12, 79: 41, 80: 99, 81: 65, 82: 78, 83: 42, 84: 33, 85: 98, 86: 53, 87: 35, 88: 93, 89: 30, 90: 46, 91: 85, 92: 30, 93: 13, 94: 31, 95: 25, 96: 49, 97: 30, 98: 49, 99: 78}
    random_shuffle = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0
    , 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0
    , 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1]

    backpack = Backpack(random_shuffle, items)
    backpack.evelove()








