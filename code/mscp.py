"""
This script is used to perform random generation and testing of instances of the
Minimum Set Coverage Problem (MSCP).

Throughout this script, tasks are indexed from 0, i.e. if there are x tasks, the
tasks are numbered {0, 1, ..., x-1}.
"""

import itertools
import logging
import math
import numpy as np
import random
import sys


class ScriptException(Exception):
    """Custom exception class for this script."""
    def __init__(self, value): self.value = value
    def __repr__(self): return repr(self.value)


def get_constraint_rows(num_tasks, num_subsets, subsets):
    """This function generates the constraint matrix as a list of lists based on the given number of
    tasks, and the subsets. Given the subsets, the constraint matrix columns are set up in the
    following order:

        z_0 z_1 ... z_n x_0 x_1 ... x_n.

    Here, z_i are subset variables and x_j are task variables.
    The constraints are z_i <= x_j, (sum of z_i) >= k.
    The matrix is set up to write the constraints as Ax <= b."""
    num_columns = num_subsets + num_tasks
    rows = list()
    for i, subset in enumerate(subsets):
        for task_index in subset:
            row = [0] * num_columns
            row[i] = 1
            row[num_subsets + task_index] = -1
            rows.append(row)
    last_row = [-1] * num_subsets
    last_row.extend([0] * num_tasks)
    rows.append(last_row)
    return rows


class ProblemInstance(object):
    """Class used to build and store random MSCP instances."""
    def __init__(self):
        self.num_tasks, self.num_subsets, self.num_subsets_to_select = None, None, None
        self.subsets, self.num_columns, self.constraint_rows = None, None, None

    @classmethod
    def from_parameters(cls, num_tasks, num_subsets, num_subsets_to_select):
        """Constructor that randomly generates an instance with the given parameters."""
        pi = cls()
        pi.num_tasks = num_tasks
        pi.num_subsets = num_subsets
        pi.num_subsets_to_select = num_subsets_to_select
        pi.subsets = pi._get_randomly_generated_subsets(num_tasks, num_subsets)
        pi.num_columns = num_subsets + num_tasks
        pi.constraint_rows = get_constraint_rows(num_tasks, num_subsets, pi.subsets)
        return pi

    @classmethod
    def from_subsets(cls, subsets):
        """Constructor that builds a constraint matrix based on the given subsets."""
        pi = cls()
        pi.subsets = subsets
        pi.num_subsets = len(pi.subsets)
        pi.num_tasks = max([max(ss) for ss in subsets]) + 1
        pi.num_columns = pi.num_subsets + pi.num_tasks
        pi.constraint_rows = get_constraint_rows(pi.num_tasks, pi.num_subsets, subsets)
        return pi

    def __repr__(self):
        return 'ProblemInstance({}, {}, {})'.format(self.num_tasks, self.num_subsets,
            self.num_subsets_to_select)

    @staticmethod
    def _get_randomly_generated_subsets(num_tasks, num_subsets):
        tasks = list(range(num_tasks))
        subsets = list()
        for _ in range(num_subsets):
            subset_len = random.randint(1, num_tasks)
            subsets.append(sorted(random.sample(tasks, subset_len)))
        return subsets

    def log_data(self):
        logging.info('#tasks: {}, #subsets: {}, #select: {}'.format(self.num_tasks,
            self.num_subsets, self.num_subsets_to_select))
        logging.info('subsets')
        for ss in self.subsets:
            logging.info(ss)

    def log_rows(self):
        logging.info('rows of constraint matrix.')
        for row in self.constraint_rows:
            logging.info(row)


class ModularityChecker(object):
    def __init__(self, num_subsets, constraint_rows):
        self.matrix = np.asarray(constraint_rows)

        self.num_rows = len(constraint_rows)
        if self.num_rows == 0:
            raise ScriptException("No rows in matrix.")

        self.num_cols = len(constraint_rows[0])
        if self.num_cols == 0:
            raise ScriptException("No columns in matrix.")

        self.col_indices = list(range(self.num_cols))

        # We only want to check minors that include the last row.
        # The reason behind this is that if a minor is built without any elment from the last row,
        # we know for sure that this minor's value is one of {-1, 0, 1}. Further details on why
        # this is true is available in the report.
        self.row_indices = list(range(self.num_rows - 1))

        self.minor_vals = set([])
        self.max_minor_size = min(self.num_rows, self.num_cols)
        self._max_num_minor_vals = (2 * num_subsets + 1)  # reason: abs(any minor val)<=num-subsets

    def compute_minor_values(self):
        for i in range(2, self.max_minor_size+1):
            all_minor_vals_computed = self._compute_minor_values_at_rank(i)
            if all_minor_vals_computed:
                break

        minor_val_list = list(self.minor_vals)
        minor_val_list.sort()
        logging.info("Minor values: {}".format(minor_val_list))

    def _compute_minor_values_at_rank(self, rank):
        col_choices = itertools.combinations(self.col_indices, rank)
        row_choices = itertools.combinations(self.row_indices, rank - 1)

        for col_tup in col_choices:
            cols = self.matrix[:, list(col_tup)]
            for row_tup in row_choices:
                row_tup += (self.num_rows - 1,)
                reduced_matrix = np.asarray([cols[i] for i in list(row_tup)])
                det = int(round(np.linalg.det(reduced_matrix), 0))
                if det not in self.minor_vals:
                    logging.info('new minor value: {}'.format(det))
                    logging.info('row indices of minor: {}'.format(row_tup))
                    logging.info('col indices of minor: {}'.format(col_tup))
                    logging.info('minor:\n{}'.format(reduced_matrix))
                    self.minor_vals.add(det)
                    if len(self.minor_vals) >= self._max_num_minor_vals:
                        return True

        return False


def main():
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # uncomment the following line to log to console
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    # uncomment the following line to log to a file
    # logging.basicConfig(filename='instances.txt', format='%(message)s', level=logging.INFO)

    # uncomment the following line to disable the logger
    # logger.disabled=True

    try:
        # Alternative 1: generate a random instance and check modularity.
        # pi = ProblemInstance.from_parameters(5, 4, 3)

        # Alternative 2: give a specific list of subsets and check modularity for it.
        # Note: the following MSCP instance is a good example with 5 tasks and 4 subsets.
        # The minimum and maximum minor values are -4 and 4. For every integer z in [-4, 4], there
        # exists a minor of the constraint matrix of this instance whose determinant equals z.
        subsets = [
            [0, 1, 2,],
            [2, 3, 4,],
            [2, 4],
            [0, 1, 3, 4],]
        pi = ProblemInstance.from_subsets(subsets)

        # Alternative 3: compute all minor values for a given problem instance
        pi.log_data()
        pi.log_rows()
        mc = ModularityChecker(pi.num_subsets, pi.constraint_rows)
        mc.compute_minor_values()

    except ScriptException as se:
        logging.error('Script exception: {}'.format(se.args[0]))
        logging.info('Press <RETURN> to exit.')
        sys.stdin.read(1)


if __name__ == '__main__':
    main()
