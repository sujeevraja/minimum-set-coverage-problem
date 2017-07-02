# minimum-set-coverage-problem
Contains documents and code related to research on the Minimum Set Coverage Problem (MSCP).

## Code

### check_bimodularity.py

This is a hacky python script to do a brute-force search to identify a constraint matrix of the minimum set coverage problem that is not bimodular. The python code has been used with Python 3.6.1 and requires numpy. It may be simplest to follow the `pip install` [instructions](https://www.scipy.org/install.html) on Linux for the entire [Scipy](https://www.scipy.org) collection.


In the minimum set coverage problem, we are given m tasks and n subsets of these tasks.
We would like to select at least k subsets such that the number of tasks in their union is
minimized.

Bimodular matrices are matrices in which every k-minor has a value in [-2, 2]. A k minor of
of a matrix is the intersection of any k rows and k columns.

The goal is as follows:

- We know that if a constraint matrix is bimodular, the problem can be solved in strongly polynomial time.
- If we can't come up with a matrix that is not bimodular, a theoretical proof may needed to prove bimodularity. Then, no more work is needed on this problem as it can be solved quickly.
- If we can come up with one, then the problem merits further research.
- Current conclusion: the problem is n-modular where n is the number of subsets and does not depend on m or k at all. This bound of n is tight and has been verified computationally with this script.