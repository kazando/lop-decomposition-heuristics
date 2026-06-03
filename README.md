# Decomposition-Based Constructive Heuristics for the Linear Ordering Problem

This repository contains the Python implementation used in the paper

> Decomposition-Based Constructive Heuristics for the Linear Ordering Problem

The repository implements several constructive heuristics for the Linear Ordering Problem (LOP), including a recursive Borda method based on recursive decomposition.


## Implemented Methods

### Classical constructive heuristics and their Variants

* Becker's algorithm
* Borda rule
* Static variant of Becker's algorithm
* Sequential variant of Borda rule

### Decomposition-based constructive heuristics proposed in this paper

* Level graph method
* Minimum cut method
* Recursive Borda method

### Improvement method

* Insertion-based local search (best-improvement)

## Directory Structure

```text
src/
    source codes of algorithms

cpp/
    C++ extension for the Hao--Orlin minimum cut algorithm
    used by the minimum cut heuristic

experiments/
    scripts used for the computational experiments reported in the paper

scripts/
    scripts for solving a single instance

data/
    benchmark instances

results/
    computational results
```

See cpp/README.md for build instructions and dependencies.

## Gurobi License

Some components of this repository use Gurobi to solve subproblems exactly.

In the recursive decomposition heuristics implemented in this repository, subproblems of size at most `MAXSIZE` are solved by an exact mixed-integer programming formulation. Consequently, the practical upper bound on `MAXSIZE` may depend on the available Gurobi license.

To reproduce the computational experiments reported in the paper, a full Gurobi license (e.g., an academic license) is strongly recommended. Users running Gurobi under a size-limited free license may encounter restrictions on the size of subproblems that can be solved exactly. As a result, some experiments, particularly those involving larger values of `MAXSIZE`, may not be reproducible without an appropriate license.

Information on obtaining academic licenses can be found on the Gurobi website:

https://www.gurobi.com/academia/

## Running a Single Instance

### `run_constructive_one.py`

- Executes a constructive heuristic method for the linear ordering problem.
- Reads an instance matrix from a file.
- Uses one of several available methods to generate a solution ordering.
- Computes and prints the objective value and runtime.
- Supported methods:
  - `becker` (Becker's algorithm)
  - `becker_static` (a static variant of Becker's algorithm)
  - `borda` (Borda rule)
  - `borda_sequential` (a sequential variant of Borda rule)
  - `mincut` (the mincut method)
  - `level` (the level graph method)
  - `rborda` (the recursive Borda method)

### Usage 
```bash
python scripts/run_constructive_one.py --instance path/to/instance.txt --method becker
python scripts/run_constructive_one.py --instance path/to/instance.txt --method rborda --maxsize 40
```

## `run_ls_one.py`

- Runs a local search procedure for the linear ordering problem.
- Uses a constructive heuristic method to build an initial solution.
- Applies the `neighbour_insert` local search improvement step.
- Computes and prints the objective value and runtime.
- Supports the same initial solution methods as `run_constructive_one.py`.

### Usage

Run either script from this folder and specify the instance file and method:

```bash
python scripts/run_ls_one.py --instance path/to/instance.txt --method borda
python scripts/run_ls_one.py --instance path/to/instance.txt --method level --maxsize 40
```

## Reproducing the Experiments

### Sensitivity Analysis of MAXSIZE

```bash
python experiments/run_maxsize.py xLOLIB_150
```
### Comparison of Constructive Heuristics

```bash
python experiments/run_constructive.py xLOLIB_150 40
python experiments/run_constructive.py xLOLIB_250 40
```

### Comparison after Local Search

```bash
python experiments/run_local_search.py xLOLIB_150 40
python experiments/run_local_search.py xLOLIB_750 40
python experiments/run_local_search.py xLOLIB_1000 40
```

See experiments/README.md for the detail.

## Benchmark Instances

The repository contains benchmark instances derived from xLOLIB https://github.com/sgpceurj/EJOR2015 and related test sets used in the paper. 
See data/README.md for the detail. 

## License

This repository is provided for research and educational purposes.
