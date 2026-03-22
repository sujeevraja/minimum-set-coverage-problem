# minimum-set-coverage-problem

This repository contains code, formal proofs, and research notes related to the Minimum Set Coverage Problem (MSCP). In MSCP, we are given m tasks and n subsets of these tasks. We would like to select at least k subsets such that the number of tasks in their union is minimized.

## Repository Structure

| Folder | Contents |
|--------|----------|
| `python/` | Python implementation: MIP solver and constraint matrix analysis |
| `lean/` | Lean 4 formal proofs about MSCP |
| `notes/` | LaTeX research notes and bibliography |

---

## `python/`

### Setup

Requires Python 3.9+ and [uv](https://docs.astral.sh/uv/).

```bash
cd python
uv sync       # installs mip, numpy, and ruff
```

### MIP Solver (`main.py`)

Generates a random MSCP instance, solves it with the [CBC](https://github.com/coin-or/Cbc) MIP solver (via [python-mip](https://www.python-mip.com/)), and prints the solution. Instance parameters (number of tasks, subsets, and subsets to select) are set at the top of `main.py`.

```bash
cd python
uv run python main.py
```

This will:
- Generate a random MSCP instance and write details to `python/data/<instance_name>.txt`
- Write a MPS file to `python/data/<instance_name>.mps`
- Solve the model with CBC and print status and objective value to the console

To clean generated files:

```bash
rm python/data/*.txt python/data/*.mps
```

### Constraint Matrix Analyzer (`mscp.py`)

Studies properties of the MSCP constraint matrix. Has been used to verify:

- The matrix is not bi-modular in general.
- Removing the lower-bound constraint on the number of subsets to select makes the matrix totally uni-modular.
- The absolute value of any minor is bounded by the number of subsets.
- There exists at least one instance where, given n subsets, every integer value in {-n, ..., 0, ..., n} is achieved as a minor determinant.

The script supports:
- Generating the constraint matrix for a random instance
- Generating the constraint matrix from a specific set of subsets
- Computing all unique minor values of the constraint matrix

Edit the `main()` function in `mscp.py` to choose between the three modes (alternatives are commented in the file), then run:

```bash
cd python
uv run python mscp.py
```

### Linting and Formatting

```bash
cd python
uv run ruff check .     # lint
uv run ruff format .    # format
```

---

## `lean/`

Lean 4 project for formal proofs about MSCP properties. Requires [Lean 4 and Lake](https://leanprover.github.io/lean4/doc/setup.html).

```bash
cd lean
lake build
```

---

## `notes/`

LaTeX source for research notes. Compile with:

```bash
cd notes
pdflatex report.tex && bibtex report && pdflatex report.tex && pdflatex report.tex
```

Add references to `notes/references.bib` and cite them in `report.tex` with `\cite{key}`.
