import numpy as np
from typing import List

class Salesman:
    iterations = 100000
    min_distance = 10
    max_distance = 100
    number_of_cities = 100

    def __init__(self):
        self.distances = None
        self.best_assignment = None
        self.best_distance = None
        self.default_distance = None
        self.init_actions()

    def init_actions(self) -> None:
        self.distances = self.create_distance_matrix()
        self.best_assignment = self.create_default_assignment()
        self.best_distance = self.calculate_distance(self.best_assignment)
        self.default_distance = self.best_distance

    def create_distance_matrix(self) -> List:
        distance_matrix = np.random.randint(Salesman.min_distance, Salesman.max_distance, size=(Salesman.number_of_cities, Salesman.number_of_cities))
        np.fill_diagonal(distance_matrix, 0)
        distance_matrix = np.minimum(distance_matrix, distance_matrix.T)
        return distance_matrix

    def create_default_assignment(self) -> List:
        init_assignment = np.arange(0, Salesman.number_of_cities)
        np.random.shuffle(init_assignment)
        return init_assignment
    
    def calculate_distance(self, assignment) -> int:
        distance = 0
        for i in range(Salesman.number_of_cities):
            start_city = assignment[i]
            if i < Salesman.number_of_cities - 1 :
                end_city = assignment[i + 1]
            else:
                end_city = assignment[0]
            distance += self.distances[start_city, end_city]
        return distance

    def mutate(self, assignment) -> List:
        idx1, idx2 = np.random.choice(len(assignment), size=2, replace=False)
        assignment[idx1], assignment[idx2] = assignment[idx2], assignment[idx1]
        
        return assignment

    def evolve(self) -> None:
        print(f"START DISTANCE: {self.default_distance})")
        for i in range(Salesman.iterations):
            active_assignment = self.best_assignment
            mutated_assignment = self.mutate(active_assignment)
            mutated_distance = self.calculate_distance(mutated_assignment)
            if mutated_distance < self.best_distance:
                self.best_assignment = mutated_assignment
                self.best_distance = mutated_distance
                print(f"IMPROVED DISTANCE: {self.best_distance} (iteration {i})")
        percentage_improvement = 100 - (self.best_distance * 100 / self.default_distance)
        print(f"IMPROVED DISTANCE FROM: {self.default_distance} TO {self.best_distance} ({percentage_improvement:.2f} %)")


if __name__ == "__main__":
    salesman = Salesman()
    salesman.evolve()

