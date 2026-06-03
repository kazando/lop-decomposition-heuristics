# experiments folder

This folder contains the following three Python scripts. Each script reads benchmark instances from `../data/` and writes experiment results in CSV format to `../results/`.

- `run_constructive.py`
- `run_local_search.py`
- `run_maxsize.py`

## Requirements

- Python 3 installed
- Current working directory is the `experiments` folder
- `../src/`, `../data/`, and `../results/` exist
- `../data/<benchmark>/` contains instance files matching `N-*`

## Usage

### 1. `run_constructive.py`

Runs constructive heuristics (`Becker`, `Borda`, `mincut`, `level`, `rBorda`) 
for the given benchmark instances and saves the results to `../results/constructive/`.

```bash
python run_constructive.py <benchmark> <MAXSIZE>
```

- `<benchmark>`: dataset name (`../data/<benchmark>/`)
- `<MAXSIZE>`: maximum size used by `level`, `mincut`, and `rborda`

Output files:

- `../results/constructive/<benchmark>-level_<MAXSIZE>.csv`
- `../results/constructive/<benchmark>-mincut_<MAXSIZE>.csv`
- `../results/constructive/<benchmark>-rborda_<MAXSIZE>.csv`
- `../results/constructive/<benchmark>-becker_<MAXSIZE>.csv`
- `../results/constructive/<benchmark>-borda_<MAXSIZE>.csv`

Each CSV row has the following format:

```
<instance>,<time>,<objective>
```

### 2. `run_local_search.py`

Runs local search starting with initial solution obtained by  (`rBorda`, `Becker`, `Borda`) for all instances and saves the results to `../results/ls/`.

```bash
python run_local_search.py <benchmark> <MAXSIZE>
```

- `<benchmark>`: dataset name (`../data/<benchmark>/`)
- `<MAXSIZE>`: maximum size used by `rBorda`

Output files:

- `../results/ls/<benchmark>-rborda_<MAXSIZE>.csv`
- `../results/ls/<benchmark>-becker.csv`
- `../results/ls/<benchmark>-borda.csv`

### 3. `run_maxsize.py`

Performs sensitivity analysis on `MAXSIZE` for `level`, `mincut`, and `rBorda` heuristics.

```bash
python run_maxsize.py <benchmark>
```

- `<benchmark>`: dataset name (`../data/<benchmark>/`)

The current implementation tests the following `MAXSIZE` values:

```python
[1, 10, 20, 30, 40, 50, 60]
```

Output files:

- `../results/maxsize/<benchmark>-level_<MAXSIZE>.csv`
- `../results/maxsize/<benchmark>-mincut_<MAXSIZE>.csv`
- `../results/maxsize/<benchmark>-rborda_<MAXSIZE>.csv`

## Notes

- `run_constructive.py` and `run_local_search.py` require a `MAXSIZE` argument.
- `run_maxsize.py` does not take `MAXSIZE` directly; it runs multiple values defined inside the script.
- Create the output directories in advance if they do not exist.
- Each CSV file records the runtime and objective value.

## Example

```bash
cd experiments
python run_constructive.py mybench 30
python run_local_search.py mybench 30
python run_maxsize.py mybench
```
