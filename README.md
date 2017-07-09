# minimum-set-coverage-problem

This repository contains documents and code related to research on the Minimum Set Coverage Problem (MSCP). In MSCP, we are given m tasks and n subsets of these tasks. We would like to select at least k subsets such that the number of tasks in their union is minimized.

## Code

### code/mscp.py

#### Functionality

The purpose of this script is to study constraint matrices of MSCP instances. It has already been used to verify the following properties of the MSCP constraint matrix:

- The matrix is not bi-modular.
- If we remove the lower-bound constraint on the number of subsets to select, the matrix is totally uni-modular.
- The absolute value of any minor of the constraint matrix is bounded by the number of subsets.
- There exists at least one non-trivial problem instance such that given the number of subsets n, for every value v in {-n, -n+1, ..., 0, ..., n}, there exists a minor whose determinant is v.

This script has the following functionality built in:

- generating constraint matrix of a random MSCP instance from a given number of tasks and a given number of subsets.
- generating constraint matrix from a specific number of subsets
- computing all unique minor values of a MSCP constraint matrix.

#### Usage

The python code has been tested with Python 3.6.1 on Windows 7 and Linux (Ubuntu). It requires the numpy package. To install this package on Linux, it may be simplest to follow the `pip install` [instructions](https://www.scipy.org/install.html) for the entire [Scipy](https://www.scipy.org) collection. Installation for Windows seems to be a bit more difficult. As long as the `import numpy` statement works, the script should work as well. The `main()` function offers examples on how to use the script.

## Results

This folders contains [Latex](https://www.latex-project.org/) source files of a document that is a compilation of results and references related to the problem collected so far.