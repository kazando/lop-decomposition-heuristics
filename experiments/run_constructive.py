# 
# This script runs the proposed methods with the given MAXSIZE on the given benchmark instances and records the time taken and objective value for each instance in separate CSV files. The MAXSIZE parameter is used for the level, mincut, and rBorda heuristics.
# Usage: python run_constructive.py <benchmark_name> <maxsize>
# Example: python run_constructive.py xLOLIB_150 40
# The results are saved in the ../results/constructive/ directory with filenames in the format <benchmark_name>-<method_name>_<maxsize>.csv for each method and MAXSIZE combination.
#
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results" / "constructive"
import glob
import time

from function import read_matrix, calc_fitness
from mincut import mincut_method
from level_graph import level
from recursive_borda import rBorda
from baselines import becker, borda


methods = [
    ('level', level, True),
    ('mincut', mincut_method, True),
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
            end = time.time()
            time_taken = end - start
            obj = calc_fitness(B, sigma)
            print(i)
            base = i.stem.split('/')[0]
            with open(output_path, 'a') as f:
                print(base, time_taken, obj, file=f, sep=",")
