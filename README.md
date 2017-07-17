# minimum-set-coverage-problem

This repository contains documents and code related to research on the Minimum Set Coverage Problem (MSCP). In MSCP, we are given m tasks and n subsets of these tasks. We would like to select at least k subsets such that the number of tasks in their union is minimized.

## Code

### code/mscp.py

#### Functionality

The purpose of this script is to study constraint matrices of MSCP instances. It has already been used to verify the following properties of the MSCP constraint matrix:

- The matrix is not bi-modular in general.
- If we remove the lower-bound constraint on the number of subsets to select, the matrix is totally uni-modular.
- The absolute value of any minor of the constraint matrix is bounded by the number of subsets.
- There exists at least one non-trivial problem instance such that given the number of subsets n, for every value v in {-n, -n+1, ..., 0, ..., n}, there exists a minor whose determinant is v.

This script has the following functionality built in:

- generating constraint matrix of a random MSCP instance from a given number of tasks and a given number of subsets.
- generating constraint matrix from a specific number of subsets
- computing all unique minor values of a MSCP constraint matrix.

#### Usage

The python code has been tested with Python 3.6.1 on Windows 7 and Linux (Ubuntu). It requires the [numpy](http://www.numpy.org/) package. Running `pip istall numpy` seems to suffice on Windows 7 (native, not Cygwin) and Linux (Ubuntu). The `main()` function offers examples on how to use the script.

### code/cpp

#### Functionality

This folder contains cpp files that can be used to generate random MSCP instances and solve them using open source MIP solvers. It has been tested with gcc 6.3.0 on Cygwin and Ubuntu 16.04.

#### Dependencies

- [Cbc](https://projects.coin-or.org/Cbc), an open source MIP solver that is part of the [COIN-OR](https://www.coin-or.org) package.
- [Boost](http://www.boost.org) C++ libraries.

#### Usage

- Build Cbc from source using the instructions in the "Quick Start Guide for Unix-like Environments" section on the [Cbc page](https://projects.coin-or.org/Cbc) in a folder like `~/coin/Cbc-x.x.x`.
- Download and extract boost source files to a folder, say `~/boost_x_xx_x`.
- Open the terminal, `cd` to the `code/cpp` folder of this repository and open the Makefile in this folder.
- Change the values of `CBCDIR` and `BOOSTDIR` to point to the Cbc and Boost folders respectively.
- Close the Makefile and run `make`. This will generate the executable `main.out`.
- Running `main.out` will:
    - generate a random MSCP instance and writes a file with details about this instance in the data folder.
    - write a MPS file named `model.mps`.
    - solve the model with Cbc and prints the problem and solution to the console.
- `make clean` does the usual (cleans up the exe, object and dependency files).
- `make deepclean` removes _all_ txt files from the data folder as well.

## Results

This folder contains [Latex](https://www.latex-project.org/) source files of a document that is a compilation of results and references related to the problem collected so far.