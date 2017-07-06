"""
This script is used to perform random generation and testing of instances of the
Minimum Set Coverage Problem (MSCP).
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


class Config(object):
    """Class that holds global data."""
    EPS = 1e-6


def get_constraint_rows(num_tasks, num_subsets, subsets):
    """This function generates the constraint matrix as a list of lists
    based on the given number of tasks, and the subsets.
    Given the subsets, the constraint matrix columns are set up as:
    z_0 z_1 ... z_n x_0 x_1 ... x_n
    where z_i are subset variables and x_i are task variables.
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
    def __init__(self, constraint_rows, check_every_minor):
        self.matrix = np.asarray(constraint_rows)
        self.check_every_minor = check_every_minor
        self.bimodular = True

        self.num_rows = len(constraint_rows)
        if self.num_rows == 0:
            raise ScriptException("No rows in matrix.")

        self.num_cols = len(constraint_rows[0])
        if self.num_cols == 0:
            raise ScriptException("No columns in matrix.")

        self.col_indices = list(range(self.num_cols))

        # we only want to check minors that include the last row
        self.row_indices = list(range(self.num_rows - 1))

        self.max_minor_size = min(self.num_rows, self.num_cols)
        self.minor_vals = set([])

    def all_minors_valid(self, minor_size):
        logging.info("checking minors of size {}".format(minor_size))
        is_valid = True
        for col_tup in itertools.combinations(self.col_indices, minor_size):
            cols = self.matrix[:, list(col_tup)]
            for row_tup in itertools.combinations(self.row_indices, minor_size - 1):
                row_tup += (self.num_rows - 1,)
                reduced_matrix = np.asarray([cols[i] for i in list(row_tup)])
                det = int(round(np.linalg.det(reduced_matrix), 0))
                self.minor_vals.add(det)
                if abs(det) > 2:
                    logging.info('row indices of invalid minor: {}'.format(row_tup))
                    logging.info('column indices of invalid minor: {}'.format(col_tup))
                    logging.info('determinant: {}'.format(det))
                    logging.info('minor')
                    logging.info(reduced_matrix)
                    if not self.check_every_minor:
                        return False
                    else:
                        is_valid = False

        return is_valid

    def check(self):
        for i in range(2, self.max_minor_size+1):
            if not self.all_minors_valid(i):
                self.bimodular = False
                if not self.check_every_minor:
                    break

    def log_results(self):
        logging.info("Matrix is bi-modular: {}".format(self.bimodular))
        minor_val_list = list(self.minor_vals)
        minor_val_list.sort()
        logging.info("Minor values: {}".format(minor_val_list))


def check_modularity(problem_instance, check_every_minor):
    problem_instance.log_data()
    problem_instance.log_rows()
    bc = ModularityChecker(problem_instance.constraint_rows, check_every_minor)
    bc.check()
    bc.log_results()


def bimodularity_check_batch_run():
    instance_num = 0

    # The number of subsets to select doesn't really matter for this script as we are only
    # interested in constraint coefficients. So, we will leave this fixed.
    num_subsets_to_select = 2

    for num_tasks in range(5, 16):
        for num_subsets in range(5, 20):
            for _ in range(10):
                logging.info('instance number: {}'.format(instance_num))
                pi = ProblemInstance(num_tasks, num_subsets, num_subsets_to_select)
                check_modularity(pi)
                logging.info('----------------------------------------------------')
                print('completed instance number {} with m={}, n={}, k={}'.format(
                    instance_num, num_tasks, num_subsets, num_subsets_to_select))
                instance_num += 1

    print('testing completed.')


def main():
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # uncomment the following line to log to console
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    # uncomment the following line to log to a file
    # logging.basicConfig(filename='instances.txt', format='%(message)s', level=logging.INFO)

    # uncomment the following line to disable the logger
    # logger.disabled=True

    try:
        # alternative 1: generate a random instance and check bimodularity.
        # pi = ProblemInstance.from_parameters(5, 4, 3)

        # alternative 2: give a specific list of subsets and check bimodularity for it.
        subsets = [
            [0, 1, 2,],
            [2, 3, 4,],
            [2, 4],
            [0, 1, 3, 4],]
        pi = ProblemInstance.from_subsets(subsets)

        check_every_minor = False
        check_modularity(pi, check_every_minor)

    except ScriptException as se:
        logging.error('Script exception: {}'.format(se.args[0]))
        logging.info('Press <RETURN> to exit.')
        sys.stdin.read(1)


if __name__ == '__main__':
    main()
