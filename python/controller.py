from typing import Optional

from problem_instance import ProblemInstance
from solver import Solver
from utility import folder_exists


class Controller:
    def __init__(self):
        self._problem_instance: Optional[ProblemInstance] = None
        self._solver: Optional[Solver] = None
        self._instance_name: str = ""

    def generate_instance(self, num_tasks: int, num_subsets: int,
                          num_subsets_to_select: int):
        self._problem_instance = ProblemInstance(num_tasks, num_subsets,
                                                 num_subsets_to_select)
        self._instance_name = self._problem_instance.get_name()

    def get_instance_name(self) -> str:
        return self._instance_name

    def get_problem_instance(self) -> Optional[ProblemInstance]:
        return self._problem_instance

    def get_solver(self) -> Optional[Solver]:
        return self._solver

    def write_problem_data(self):
        if self._problem_instance is None:
            return
        folder_name = "data"
        if folder_exists(folder_name):
            file_name = f"data/{self._instance_name}.txt"
            self._problem_instance.write_to_file(file_name)
        else:
            print(f"WARN: could not find folder {folder_name}. "
                  f"problem data not written.")

    def add_problem_data_to_solver(self):
        self._solver = Solver()
        pi = self._problem_instance
        num_tasks = pi.num_tasks
        num_subsets = pi.num_subsets

        # Add task variables (obj=1.0, binary, indices 0..num_tasks-1)
        for i in range(num_tasks):
            self._solver.add_column(i, 0.0, 1.0, 1.0, f"task_{i}")

        # Add subset variables (obj=0.0, binary, indices num_tasks..num_tasks+num_subsets-1)
        for i in range(num_subsets):
            self._solver.add_column(num_tasks + i, 0.0, 1.0, 0.0, f"subset_{i}")

        # Mark all as integer
        for i in range(num_tasks + num_subsets):
            self._solver.mark_col_as_integer(i)

        # VUB constraints: subset_i - task_j <= 0 for each task j in subset i
        for i, subset in enumerate(pi.subsets):
            for task_index in subset:
                self._solver.add_row(
                    [num_tasks + i, task_index],
                    [1.0, -1.0],
                    lb=None, ub=0.0
                )

        # Cardinality constraint: sum(subset_i) >= k
        subset_indices = list(range(num_tasks, num_tasks + num_subsets))
        self._solver.add_row(
            subset_indices,
            [1.0] * num_subsets,
            lb=float(pi.num_subsets_to_select), ub=None
        )
