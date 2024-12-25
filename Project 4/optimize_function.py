import numpy as np
from typing import List

class Point:
    max_value = 2 * np.pi
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def calculate_function(self) -> float:
        """
        Calculate the value of the function:
        f(x, y) = |sin(x) + sin(2x) + sin(4x) + cos(y) + cos(2y) + cos(4y)|
        
        Returns:
            float: The computed value of the function.
        """
        result = abs(
            np.sin(self.x) + np.sin(2 * self.x) + np.sin(4 * self.x) +
            np.cos(self.y) + np.cos(2 * self.y) + np.cos(4 * self.y)
        )

        return result
    
    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    

class Algorithm:
    number_of_points = 100
    number_of_iterations = 1000
    mutation_multipliers = [0.999, 1.001]

    def __init__(self):
        self.points = self.generate_points()
        self.best_point: Point = self.get_best_point(self.points)

    def generate_points(self) -> List[Point]:
        points = []
        for _ in range(self.number_of_points):
            x = np.random.uniform(0, Point.max_value)
            y = np.random.uniform(0, Point.max_value)
            point = Point(x, y)
            points.append(point)

        return points
    
    def get_best_point(self, points: List[Point]) -> Point:
        best_point = points[0]
        for point in points:
            point.calculate_function()
            if point.calculate_function() > best_point.calculate_function():
                best_point = point
        
        return best_point

    def cross(self, points: List[Point]) -> List[Point]:
        for i in range(0, Algorithm.number_of_points, 2):
            x_1, y_1, x_2, y_2 = points[i].x, points[i].y, points[i + 1].x, points[i + 1].y
            cross_point_1 = Point(x_1, y_2)
            cross_point_2 = Point(x_2, y_1)
            points += [cross_point_1, cross_point_2]

        return points

    def mutate(self, points: List[Point]) -> List[Point]:
        point_index = np.random.choice(len(points))
        point = points[point_index]
        point_coordinate = np.random.choice(["x", "y"])
        multiplier = np.random.choice(Algorithm.mutation_multipliers)
        if point_coordinate == "x":
            if point.x * multiplier < Point.max_value:
                point.x = point.x * multiplier
        elif point_coordinate == "y":
            if point.y * multiplier < Point.max_value:
                point.y = point.y * multiplier
        
        points[point_index] = point

        return points

    def tournament_selection(self, points: List[Point]) -> List[Point]:
        selected_points = []
        for _ in range(self.number_of_points):
            point_1_index, point_2_index = np.random.choice(len(points), size=2, replace=False)
            point_1, point_2 = points[point_1_index], points[point_2_index]

            if point_1.calculate_function() > point_2.calculate_function():
                selected_points.append(point_1)
            else:
                selected_points.append(point_2)
            
            points.remove(point_1)
            points.remove(point_2)

        return selected_points

    def evolve(self):
        print(f"STARTING EVOLUTION! BEST VALUE: {self.best_point.calculate_function()}")
        for i in range(Algorithm.number_of_iterations):
            current_points = self.points
            crossed_points = self.cross(current_points)
            mutated_points = self.mutate(crossed_points)
            mutated_points = self.mutate(mutated_points)
            mutated_points = self.mutate(mutated_points)
            mutated_points = self.mutate(mutated_points)
            selected_points = self.tournament_selection(mutated_points)
            self.points = selected_points
            best_point = self.get_best_point(selected_points)

            if best_point.calculate_function() > self.best_point.calculate_function():
                print(f"NEW BEST VALUE FOUND: {best_point.calculate_function()} (iteration {i})")
                self.best_point = best_point

        print(f"EVOLUTION FINISHED! BEST POINT: {self.best_point}, VALUE: {self.best_point.calculate_function()}")

if __name__ == "__main__":
    algorithm = Algorithm()
    algorithm.evolve()