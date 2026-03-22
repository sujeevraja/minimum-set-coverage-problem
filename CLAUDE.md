# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

Research on the **Minimum Set Coverage Problem (MSCP)**: given m tasks and n subsets of those tasks, select at least k subsets such that the number of tasks in their union is minimized. The repo has three folders: `python/` for all code, `lean/` for formal proofs, and `notes/` for LaTeX research notes.

## MIP Formulation

Variables: binary `task_i` (task covered) and binary `subset_j` (subset selected).
Constraints: `subset_j - task_i <= 0` for each task i in subset j; `sum(subset_j) >= k`.
Objective: minimize `sum(task_i)`.
Column ordering in the solver: `task_0 ... task_{m-1} subset_0 ... subset_{n-1}`.

---

## `python/`

**Tooling:** [uv](https://docs.astral.sh/uv/) for package management, [ruff](https://docs.astral.sh/ruff/) for linting/formatting. Config in `python/pyproject.toml`.

```bash
cd python
uv sync                  # install dependencies (mip, numpy) + dev deps (ruff)
uv run ruff check .      # lint
uv run ruff format .     # format
```

### Running the MIP solver (`main.py`)

```bash
cd python
uv run python main.py
```

Generates a random MSCP instance, writes instance data and an MPS file to `python/data/`, solves with CBC, and prints solution stats. Instance parameters are set at the top of `main.py`.

### Running the constraint matrix analyzer (`mscp.py`)

```bash
cd python
uv run python mscp.py
```

Analyzes minor values of the MSCP constraint matrix. Configure which mode runs by editing `main()` — three alternatives are commented in the file.

### Module architecture

- `utility.py` — `MSCPException`, `get_current_timestamp()`, `folder_exists()`, `eps`
- `problem_instance.py` — `ProblemInstance`: randomly generates an MSCP instance (tasks, subsets, k); writes to `data/<name>.txt`
- `solver.py` — `Solver`: builds a `python-mip` CBC model column/row by column/row; writes MPS files; runs branch-and-bound and prints stats
- `controller.py` — `Controller`: orchestrates the workflow — generates `ProblemInstance`, writes it to disk, populates `Solver` with variables and constraints
- `main.py` — sets instance parameters and calls `Controller` methods in sequence
- `mscp.py` — standalone constraint matrix analysis (independent of the above modules)

### Clean data output

```bash
rm python/data/*.txt python/data/*.mps  # remove generated instance files
```

---

## `lean/`

Lean 4 project for formal proofs about MSCP.

**Build** (requires Lean 4 + Lake installed):
```bash
cd lean
lake build
```

- `lakefile.toml` — Lake project config
- `Mscp.lean` — top-level import
- `Mscp/Basic.lean` — proof files go here

---

## `notes/`

LaTeX research notes compiled with BibTeX.

- `report.tex` — main document
- `references.bib` — bibliography (cite from `report.tex` using `\cite{...}`)

**Compile:**
```bash
cd notes
pdflatex report.tex && bibtex report && pdflatex report.tex && pdflatex report.tex
```
