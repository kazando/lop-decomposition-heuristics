#
# This script runs the proposed methods with different MAXSIZE values on the given benchmark instances and records the time taken and objective value for each instance in separate CSV files. The MAXSIZE parameter is used for the level, mincut, and rBorda heuristics.
# Usage: python run_maxsize.py <benchmark_name>
# Example: python run_maxsize.py xLOLIB
# The results are saved in the ../results/maxsize/ directory with filenames in the format <benchmark_name>-<method_name>_<maxsize>.csv for each method and MAXSIZE combination.
#
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results" / "maxsize"
import glob
import time

from function import read_matrix, calc_fitness
import level_graph as level
import mincut as mincut
import recursive_borda as rborda

def heuristics(benchmark,instance,MAXSIZE):
    methods = [
        ('level', level.level),
        ('mincut', mincut.mincut_method),
        ('rborda', rborda.rBorda),
    ]

    for name, _ in methods:
        with open(RESULTS_DIR.joinpath(benchmark+'-'+name+'_'+str(MAXSIZE)+'.csv'), 'w') as r:
            pass

    for name, func in methods:
        output_path = RESULTS_DIR.joinpath(benchmark+'-'+name+'_'+str(MAXSIZE)+'.csv')
        for i in instance:
            start = time.time()
            B = read_matrix(i)
            sigma = func(B, MAXSIZE)
            end = time.time()
            time_taken = end - start
            obj = calc_fitness(B, sigma)
            print(i)
            base = i.stem.split('/')[0]
            with open(output_path, 'a') as f:
                print(base, time_taken, obj, file=f, sep=",")

if __name__ == '__main__':
    benchmark = sys.argv[1]
    instances = list(sorted(DATA_DIR.joinpath(benchmark).glob('N-*')))
    #print(instances)
    if not instances:
        print('##### benchmark error. #####')
        exit()

    #for MAXSIZE in [2,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]:
    for MAXSIZE in [1,10,20,30,40,50,60]:
        heuristics(benchmark,instances,MAXSIZE)
