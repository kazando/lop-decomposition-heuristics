# 
# This script runs local search heuristics (rBorda, Becker, and Borda) on the given benchmark instances and records the time taken and objective value for each instance in separate CSV files. The MAXSIZE parameter is used for the rBorda heuristic. 
# Usage: python run_local_search.py <benchmark_name> <maxsize>
# Example: python run_local_search.py xLOLIB 40
# The results are saved in the ../results/ls/ directory with filenames in the format <benchmark_name>-<method_name>_<maxsize>.csv for rBorda and <benchmark_name>-<method_name>.csv for Becker and Borda.
# The script reads the instances from the ../data/<benchmark_name>/ directory, where each instance is expected to be a file containing a matrix. The local search heuristic is applied to each instance, and the results are recorded in the corresponding CSV files. Each line in the CSV files contains the instance name (without path and extension), time taken for the local search, and the objective value of the solution found, separated by commas.
# Note: Ensure that the required libraries (networkx, numpy, hao_orlin_cpp, and gurobipy) are installed and properly configured in your Python environment before running this script. Also, make sure that the instance files are correctly formatted and located in the specified directory.
# 
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results" / "ls"
import glob
import time

from local_search import neighbour_insert
from function import read_matrix, calc_fitness
#from mincut import mincut_method
#from level_graph import level
from recursive_borda import rBorda
from baselines import becker, borda

methods = [
    ('rborda', rBorda, True),
    ('becker', becker, False),
    ('borda', borda, False),
]

if __name__ == '__main__':
    benchmark = sys.argv[1]
    MAXSIZE = int(sys.argv[2])
    instances = list(sorted(DATA_DIR.joinpath(benchmark).glob('N-*')))
    #print(instances)
    if not instances:
        print('##### benchmark error. #####')
        exit()

    for name, _, use_maxsize in methods:
        suffix = '_'+str(MAXSIZE) if use_maxsize else ''
        with open(RESULTS_DIR.joinpath(benchmark+'-'+name+suffix+'.csv'), 'w') as r:
            pass

    for name, func, use_maxsize in methods:
        output_path = RESULTS_DIR.joinpath(benchmark+'-'+name + ('_'+str(MAXSIZE) if use_maxsize else '') + '.csv')
        for i in instances:
            start = time.time()
            B = read_matrix(i)
            sigma = func(B, MAXSIZE) if use_maxsize else func(B)
            sigma = neighbour_insert(B, sigma)
            end = time.time()
            time_taken = end - start
            obj = calc_fitness(B, sigma)
            print(i)
            base = i.stem.split('/')[0]
            with open(output_path, 'a') as f:
                print(base, time_taken, obj, file=f, sep=",")
