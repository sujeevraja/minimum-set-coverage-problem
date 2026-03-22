import random
from typing import List

from utility import MSCPException, get_current_timestamp


class ProblemInstance:
    def __init__(self, num_tasks: int, num_subsets: int, num_subsets_to_select: int):
        if num_tasks <= 0 or num_subsets <= 0 or num_subsets_to_select <= 0:
            raise MSCPException("invalid data provided")

        self.num_tasks = num_tasks
        self.num_subsets = num_subsets
        self.num_subsets_to_select = num_subsets_to_select
        self._timestamp = get_current_timestamp()
        self.subsets: List[List[int]] = self._generate_subsets()

    def _generate_subsets(self) -> List[List[int]]:
        task_indices = list(range(self.num_tasks))
        subsets = []
        for _ in range(self.num_subsets):
            random.shuffle(task_indices)
            cut = random.randint(0, self.num_tasks - 1)
            subset = sorted(task_indices[:cut + 1])
            subsets.append(subset)
        return subsets

    def get_name(self) -> str:
        return (
            f"instance_{self.num_tasks}_tasks_"
            f"{self.num_subsets}_subsets_"
            f"{self.num_subsets_to_select}_to_select_"
            f"{self._timestamp}"
        )

    def write_to_file(self, file_name: str):
        with open(file_name, "w") as f:
            f.write(f"Number of tasks (m): {self.num_tasks}\n")
            f.write(f"Number of subsets (n): {self.num_subsets}\n")
            f.write(f"Number of subsets to select (k): {self.num_subsets_to_select}\n")
            f.write("Subsets:\n")
            for subset in self.subsets:
                f.write(" ".join(str(i) for i in subset) + "\n")

    def print_subsets(self):
        print("subsets:")
        for subset in self.subsets:
            print(" " + " ".join(str(i) for i in subset))
