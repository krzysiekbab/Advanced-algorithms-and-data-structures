import numpy as np
from typing import List, Dict

class Processor():
    multiplier = 1

    def __init__(self, id, task_list, execution_times):
        self.id = id
        self.task_list = task_list
        self.execution_times = execution_times
        self.multiplier = Processor.multiplier
        Processor.multiplier += 0.25

    def calculate_tasks_execution_time(self) -> int:
        time = 0

        for task in self.task_list:
            time += self.execution_times[task]
        
        return time * self.multiplier
    
    def __repr__(self):
        return f"Processor(id={self.id}, multiplier={self.multiplier}, tasks={self.task_list}, execution_time={self.calculate_tasks_execution_time()}"


class Multiprocessor():
    iterations = 100000

    def __init__(self, number_of_processors, execution_times):
        self.number_of_processors = number_of_processors
        self.execution_times = execution_times
        self.number_of_tasks = len(self.execution_times)

        self.default_assignment: List[int] = None
        self.best_assignment : List[int]= None
        self.processors: Dict[int, Processor] = None
        self.slowest_processor: Processor = None

        self.init_actions()

    def init_actions(self) -> None:
        self.default_assignment = self.assign_tasks()
        self.best_assignment = self.default_assignment
        tasks_per_processor = self.divide_tasks_between_processors(self.default_assignment)
        self.processors = self.create_processors(tasks_per_processor)
        self.slowest_processor = self.pick_slowest_processor(self.processors)

    def assign_tasks(self) -> List:
        return np.random.randint(0, self.number_of_processors, size=self.number_of_tasks)
    
    def create_processors(self, tasks_per_processor) -> Dict[int, Processor]:
        Processor.multiplier = 1

        return {i: Processor(i, tasks_per_processor[i], self.execution_times) for i in range(self.number_of_processors)}
    
    def divide_tasks_between_processors(self, task_list) -> Dict[int, List]:
        processor_ids = np.unique(task_list)
        tasks_per_processor = {id: np.where( task_list == id)[0].tolist() for id in processor_ids}

        return tasks_per_processor


    def pick_slowest_processor(self, processors) -> Processor:
        execution_times = []

        for i in range(len(processors)):
            execution_times.append(processors[i].calculate_tasks_execution_time())
        
        index_of_processor_with_longest_execution_time = execution_times.index(max(execution_times))

        return processors[index_of_processor_with_longest_execution_time]


    def mutate(self, active_assignment) -> List[int]:
        random_index = np.random.randint(0, self.number_of_tasks)
        processor_to_mutate = active_assignment[random_index]
        mutated_processor = np.random.randint(0, self.number_of_processors)

        if processor_to_mutate != mutated_processor:
            active_assignment[random_index] = mutated_processor
        
            return active_assignment
        else:
            return self.mutate(active_assignment)

    
    def evolve(self) -> None:
        for i in range(Multiprocessor.iterations):
            active_assignment = self.best_assignment
            mutated_assignment = self.mutate(active_assignment)

            new_tasks_per_processor = self.divide_tasks_between_processors(mutated_assignment)
            new_processors = self.create_processors(new_tasks_per_processor)
            new_slowest_processor = self.pick_slowest_processor(new_processors)
            new_slowest_execution_time = new_slowest_processor.calculate_tasks_execution_time()
            old_slowest_execution_time = self.slowest_processor.calculate_tasks_execution_time()

            if (new_slowest_execution_time < old_slowest_execution_time):
                self.best_assignment = mutated_assignment
                self.processors = new_processors
                self.slowest_processor = new_slowest_processor
                print(f"IMPROVED EXECUTION TIME TO: {new_slowest_execution_time} (mutation {i})")

    def show_processors(self) -> None:
        for i in range(len(self.processors)):
            print(self.processors[i])


if __name__ == "__main__":
    number_of_items = 100
    number_of_processors = 4
    task_weights = {i: np.random.randint(10, 91) for i in range(0, number_of_items)}

    multiprocessor = Multiprocessor(number_of_processors, task_weights)
    multiprocessor.show_processors()
    multiprocessor.evolve()
    multiprocessor.show_processors()
