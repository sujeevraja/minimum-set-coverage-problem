import time
from typing import List, Optional, Tuple

import mip


class Solver:
    def __init__(self):
        self._num_cols = 0
        self._columns: List[dict] = []
        self._integer_col_indices: List[int] = []
        self._row_indices: List[List[int]] = []
        self._row_coefs: List[List[float]] = []
        self._row_bounds: List[Tuple[Optional[float], Optional[float]]] = []
        self._solution: List[float] = []
        self._model: Optional[mip.Model] = None

    def add_column(self, index: int, lb: Optional[float], ub: Optional[float],
                   obj: float, name: Optional[str] = None):
        self._columns.append({"index": index, "lb": lb, "ub": ub, "obj": obj,
                               "name": name or ""})
        self._num_cols += 1

    def mark_col_as_integer(self, index: int):
        self._integer_col_indices.append(index)

    def add_row(self, indices: List[int], coefs: List[float],
                lb: Optional[float], ub: Optional[float]):
        self._row_indices.append(list(indices))
        self._row_coefs.append(list(coefs))
        self._row_bounds.append((lb, ub))

    def print_constraints(self):
        print("rows")
        for i, (indices, coefs, bounds) in enumerate(
                zip(self._row_indices, self._row_coefs, self._row_bounds)):
            print(f"row {i}")
            for idx, coef in zip(indices, coefs):
                print(f"  ind {idx} coef {coef}")
            print(f"  row lb {bounds[0]} row ub {bounds[1]}")
        print("rows printed")

    def prepare_model(self):
        self._model = mip.Model(sense=mip.MINIMIZE, solver_name=mip.CBC)
        self._model.verbose = 0

        # Create variables sorted by index
        vars_by_index = {}
        for col in sorted(self._columns, key=lambda c: c["index"]):
            lb = col["lb"] if col["lb"] is not None else -mip.INF
            ub = col["ub"] if col["ub"] is not None else mip.INF
            var_type = mip.CONTINUOUS
            name = col["name"] if col["name"] else f"x_{col['index']}"
            v = self._model.add_var(name=name, lb=lb, ub=ub, obj=col["obj"],
                                    var_type=var_type)
            vars_by_index[col["index"]] = v

        # Mark integer variables
        for idx in self._integer_col_indices:
            vars_by_index[idx].var_type = mip.BINARY

        # Add constraints
        for indices, coefs, (lb, ub) in zip(
                self._row_indices, self._row_coefs, self._row_bounds):
            expr = mip.xsum(coefs[j] * vars_by_index[indices[j]]
                            for j in range(len(indices)))
            if lb is not None and ub is not None:
                self._model += lb <= expr <= ub
            elif lb is not None:
                self._model += expr >= lb
            elif ub is not None:
                self._model += expr <= ub

        self._vars_by_index = vars_by_index

    def write_model(self, file_name: str):
        if self._model is not None:
            self._model.write(file_name)

    def solve(self):
        if self._model is None:
            raise RuntimeError("Call prepare_model() before solve()")

        self._model.max_seconds = 300
        start = time.time()
        status = self._model.optimize()
        elapsed_ms = int((time.time() - start) * 1000)

        print(f"Solution time: {elapsed_ms} milliseconds")
        print(f"Number of rows: {self._model.num_rows}")
        print(f"Number of columns: {self._model.num_cols}")

        if status == mip.OptimizationStatus.OPTIMAL:
            print("Status: optimal")
        elif status == mip.OptimizationStatus.INFEASIBLE:
            print("Status: infeasible")
        elif status == mip.OptimizationStatus.NO_SOLUTION_FOUND:
            print("Status: reached limit (no solution found)")
        else:
            print(f"Status: {status}")

        print(f"Number of nodes: {self._model.num_solutions}")
        print(f"Objective value: {self._model.objective_value}")

        self._solution = [self._vars_by_index[i].x for i in range(self._num_cols)]

    def get_solution(self) -> List[float]:
        return self._solution
